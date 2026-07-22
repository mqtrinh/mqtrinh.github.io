#!/usr/bin/env python3

"""

Input:
* MBOX, an mbox file containing a Gmail inbox export
* TARGET_ADDRESSES, a set of email addresses

Output:
* an Obsidian vault at VAULT_ROOT (absolute path ABS_ROOT)
* a subfolder containing the messages from MBOX in which at least one of the TARGET_ADDRESSES appears
* a further subfolder containing the file attachments from those messages

To avoid collisions, messages are named using UTC datetime (yy-mm-dd-HHMM) and subject; file attachments are renamed by prefixing the UTC datetime.

Written with help from ChatGPT 5.3 Instant.

Minh-Tam Trinh
July 22, 2026

"""

from __future__ import annotations

import mailbox
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.header import decode_header, make_header
from email.utils import getaddresses, parsedate_to_datetime
from pathlib import Path
from typing import Optional

import re

from bs4 import BeautifulSoup

from markdownify import markdownify

import unicodedata

########################
# Configuration
########################

MBOX = "mbox_name" ### REPLACE mbox_name
MBOX_PATH = Path(f"{MBOX}.mbox")

TARGET_ADDRESSES = {
	"name1@domain1".lower(),
	"name2@domain2".lower(), ### REPLACE name1, domain1, name2, domain2, ...
}

# https://forum.obsidian.md/t/how-to-link-a-local-file-in-obsidian/5815
ABS_ROOT = "file:///home/user_name/vaults/vault_name" ### REPLACE /user_name/...
VAULT_ROOT = Path("vault_name") ### REPLACE vault_name
FILES = "files"

SUBJECT_MAX_LEN = 36

_SUBJECT_PREFIX = re.compile(r"^(?:(?:re|fw|fwd)\s*:\s*)", re.IGNORECASE)
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

########################
# data model
########################

@dataclass
class Attachment:
	raw_name: str
	cid: str
	content_type: str
	payload: bytes
	name: str

@dataclass
class EmailMessage:
	index: int
	message_id: str
	raw_subject: str
	date: Optional[datetime]
	sender: tuple[str, str]
	to: list[tuple[str, str]]
	cc: list[tuple[str, str]]
	bcc: list[tuple[str, str]]
	in_reply_to: str
	references: list[str]
	gmail_labels: list[str]
	raw_message: object

	body_text: Optional[str] = None
	body_html: Optional[str] = None
	body_kind: str = ""
	attachments: list[Attachment] = field(default_factory=list)
	
	subject: str = ""
	root: Optional["EmailMessage"] = None
	parent: Optional["EmailMessage"] = None
	children: list["EmailMessage"] = field(default_factory=list)
    
	def __repr__(self):
		return (f"<EmailMessage #{self.index} {self.message_id!r}>")

########################
# filtering and parsing
########################

def raw_involves_target(msg: EmailMessage) -> bool:
	participants = set()
	for header in ("From", "To", "Cc", "Bcc"):
		for _, address in parse_address_list(msg.get(header)):
			participants.add(address)
	return not TARGET_ADDRESSES.isdisjoint(participants)
	
def decode_header_value(value: Optional[str]) -> str:
	# decode RFC2047 MIME headers into ordinary Unicode
	if not value: return ""
	try:
		return str(make_header(decode_header(value)))
	except Exception:
		return value

def parse_address_list(value: Optional[str]) -> list[tuple[str, str]]:
	# return [(display_name, email_address), ...]
	if not value: return []
	addresses = []
	for name, addr in getaddresses([value]):
		addresses.append(
			(
				decode_header_value(name).strip(),
				addr.lower().strip(),
			)
		)
	return addresses

def parse_date(value: Optional[str]) -> Optional[datetime]:
	if not value: return None
	try:
		return parsedate_to_datetime(value)
	except Exception:
		return None

def parse_email(index: int, msg) -> EmailMessage:
	sender_list = parse_address_list(msg.get("From"))
	sender = sender_list[0] if sender_list else ("", "")
	refs = msg.get("References", "").split()
	labels = []

	if msg.get("X-Gmail-Labels"):
		labels = [
			label.strip()
			for label in msg["X-Gmail-Labels"].split(",")
			if label.strip()
		]

	return EmailMessage(
		index=index,
		message_id=msg.get("Message-ID", "").strip(),
		raw_subject=decode_header_value(msg.get("Subject")),
		date=parse_date(msg.get("Date")),
		sender=sender,
		to=parse_address_list(msg.get("To")),
		cc=parse_address_list(msg.get("Cc")),
		bcc=parse_address_list(msg.get("Bcc")),
		in_reply_to=msg.get("In-Reply-To", "").strip(),
		references=refs,
		gmail_labels=labels,
		raw_message=msg,
	)

########################
# extracting metadata
########################

def display_date(dt: datetime) -> str:
	return dt.strftime("%y-%m-%d-%H%M")
	
def display_date_utc(dt: datetime) -> str:
	# https://www.pythonmorsels.com/converting-to-utc-time/
	return display_date(dt.astimezone(timezone.utc))

def _handle_part(msg: EmailMessage, part) -> None:
	content_type = part.get_content_type()
	disposition = part.get_content_disposition()
	payload = part.get_payload(decode=True) or b""
	charset = part.get_content_charset() or "utf-8"
	filename = part.get_filename()

	try:
		text = payload.decode(charset, errors="replace")
	except LookupError:
		text = payload.decode("utf-8", errors="replace")

	if filename is not None or disposition == "attachment":
		cid = part.get("Content-ID")
		if cid is not None: cid = cid.strip("<>")
		msg.attachments.append(
			Attachment(
				raw_name=filename,
				cid=cid,
                		content_type=content_type,
                		payload=payload,
                		name=f"{display_date_utc(msg.date)} {filename}"
			)
		)
	else:
		if content_type == "text/plain":
			if msg.body_text is None:
				msg.body_text = text
				msg.body_kind = "plain"
			return

		if content_type == "text/html":
			if msg.body_html is None:
				msg.body_html = text
				if msg.body_kind == "":
					msg.body_kind = "html"
			return
        
def extract_metadata(msg: EmailMessage) -> None:
	"""
	Populate
	* body_text
	* body_html
	* attachments
	by walking the MIME tree.

	The EmailMessage is modified in place.
	"""

	raw = msg.raw_message
	if not raw.is_multipart():
		_handle_part(msg, raw)
		return
	for part in raw.walk():
		if part.is_multipart():
			continue
		_handle_part(msg, part)

########################
# building thread graph
########################

def build_message_lookup(messages: list[EmailMessage]) -> dict[str, EmailMessage]:
	lookup = {}
	for msg in messages:
		if msg.message_id:
			lookup[msg.message_id] = msg
	return lookup

def build_thread_graph(
	messages: list[EmailMessage],
	message_by_id: dict[str, EmailMessage],
) -> None:
	for msg in messages:
		# skip root messages
		if not msg.in_reply_to: continue

		parent = message_by_id.get(msg.in_reply_to)

		# parent wasn't retained
		if parent is None: continue
		
		msg.parent = parent
		parent.children.append(msg)

def sanitize_subject(subject: str) -> str:
	# remove repeated 'Re:', 'Fw:', and 'Fwd:' prefixes
	subject = subject.strip()
	while True:
		new_subject = _SUBJECT_PREFIX.sub("", subject)
		if new_subject == subject: break
		subject = new_subject.strip()
	
	"""
	Convert subject into a canonical folder name. The result:
	* contains only ASCII lowercase letters, digits, and dashes;
	* replaces whitespace with dashes;
	* converts apostrophes within words to dashes;
	* removes punctuation unsuitable for filenames;
	* collapses repeated dashes;
	* is truncated to at most max_length characters.
	"""

	# convert accented letters to ASCII equivalents
	subject = unicodedata.normalize("NFKD", subject)
	subject = subject.encode("ascii", "ignore").decode("ascii")

	# lowercase
	subject = subject.lower()

	# apostrophes between letters become dashes
	subject = re.sub(r"(?<=[a-z])['’](?=[a-z])", "-", subject)

	# remove all remaining quotation marks
	subject = re.sub(r"""['"`‘’“”«»]""", "", subject)

	# remove selected punctuation
	subject = re.sub(r"[/:?]", "", subject)

	# replace whitespace with dashes
	subject = re.sub(r"\s+", "-", subject)

	# remove everything except letters, digits, and dashes
	subject = re.sub(r"[^a-z0-9-]", "", subject)

	# collapse repeated dashes
	subject = re.sub(r"-{2,}", "-", subject)

	# remove leading/trailing dashes
	subject = subject.strip("-")

	# truncate
	if len(subject) > SUBJECT_MAX_LEN:
		cutoff = subject.rfind("-", 0, SUBJECT_MAX_LEN)
		if cutoff != -1:
			subject = subject[:cutoff]
		else:
			subject = subject[:SUBJECT_MAX_LEN]
	subject = subject.rstrip("-")

	# avoid empty names
	if not subject: subject = "untitled"

	return subject
	
########################
# writing Markdown
########################
	
def filename(msg: EmailMessage) -> str:
	if msg is not None:
		return f"{display_date_utc(msg.date)} {msg.subject}"
	return "none"

def yaml_frontmatter(msg: EmailMessage) -> str:
	temp = "---"
	#temp += f"\nindex: {msg.index}"
	temp += f"\nroot: '[[{filename(msg.root)}]]'"
	temp += f"\nparent: '[[{filename(msg.parent)}]]'"
	temp += "\nchildren: "
	for child in msg.children:
		temp += f"\n- '[[{filename(child)}]]'"
		
	temp += f"\nyear: {msg.date.strftime('%Y')}"
	temp += f"\ndate: {msg.date.strftime('%A, %B %d')}"
	temp += f"\ntime: {msg.date.strftime('%H:%M %z')}"	
	
	temp += f"\nfrom: {msg.sender[1]}"
	temp += f"\nsubject: {msg.subject}"
	#temp += f"\nto: {format_address_list(msg.to)}"
	#temp += f"\ncc: {format_address_list(msg.cc)}"
	#temp += f"\nbcc: {format_address_list(msg.bcc)}"
	temp += "\nattachments: "
	for file in msg.attachments:
		temp += f"\n- '[[{FILES}/{file.name}]]'"
	temp += "\n---"
	return temp

def write_attachments(msg: EmailMessage):
	for file in msg.attachments:
		path = (
			VAULT_ROOT
			/ MBOX
			/ FILES
			/ f"{file.name}"
		)
		path.parent.mkdir(
			parents=True,
			exist_ok=True,
		)
		payload = file.payload
		with open(path, "wb") as f:
			f.write(payload)

def normalize_plaintext(text: str) -> str:
	text = text.replace("\r\n", "\n")
	text = text.replace("\r", "\n")
	return text.rstrip()

def build_cid_lookup(file_lst) -> dict[str, str]:
	lookup = {}
	for file in file_lst:
		if file.cid:
			lookup[file.cid] = file.name
	return lookup
	
def rewrite_inline_images(soup, file_lst) -> None:
	file_by_cid = build_cid_lookup(file_lst)
	for img in soup.find_all("img"):
		src = img.get("src")
		if src is not None and src.startswith("cid:"):
			cid = src[4:]
			if cid in file_by_cid:
				img["src"] = (f"<{ABS_ROOT}/{MBOX}/{FILES}/{file_by_cid[cid]}>")

def rewrite_gmail_quote_headers(soup):
	for a in soup.find_all("a"):
		text = a.get_text(strip=True)
		href = a.get("href", "")
		if (
			_EMAIL_RE.fullmatch(text)
			and (
				href.startswith("mailto:")
				or href.startswith("javascript:")
			)
		): a.replace_with(f"<{text}>")

def html_to_markdown(html, file_lst) -> str:
	soup = BeautifulSoup(html, "html.parser")
	rewrite_inline_images(soup, file_lst)
	rewrite_gmail_quote_headers(soup)
	return markdownify(
		str(soup),
		strip=['h1']
	).rstrip()

def body_as_markdown(msg: EmailMessage) -> str:
	# chooses html over plain where available
	if msg.body_html is not None:
		return html_to_markdown(msg.body_html, msg.attachments)
	elif msg.body_text is not None:
		return normalize_plaintext(msg.body_text)
	else:
		return ""

def write_markdown(msg: EmailMessage):
	path = (
		VAULT_ROOT
		/ MBOX
		/ f"{filename(msg)}.md"
	)
	path.parent.mkdir(
		parents=True,
		exist_ok=True,
	)
	with path.open("w", encoding="utf-8") as f:
		f.write(yaml_frontmatter(msg))
		f.write("\n")
		f.write(body_as_markdown(msg))

########################
# main
########################

def load_messages(path: Path) -> list[EmailMessage]:
	archive = mailbox.mbox(path)
	kept = []
	total = 0
	for index, raw in enumerate(archive, start=1):
		total = index
		if not raw_involves_target(raw): continue
		try:
			msg = parse_email(index, raw)
		except Exception as exc:
			print(f"Skipping malformed message #{total}: {exc}")
			continue
		kept.append(msg)
	print(f"read {total:,} messages")
	print(f"retained {len(kept):,} messages")
	return kept

if __name__ == "__main__":
	messages = load_messages(MBOX_PATH)
	
	for msg in messages:
		extract_metadata(msg)
		
	message_by_id = build_message_lookup(messages)
	
	build_thread_graph(
		messages,
		message_by_id,
	)
	
	for msg in messages:
		msg.children.sort(
			key=lambda child: (
				child.date is None,
				child.date,
				child.index,
			)
		)

		root = None
		if msg.references:
			num_refs = len(msg.references)
			flag = False
			i = 0
			while flag == False and i < num_refs:
				ref_id = msg.references[i]
				ref = message_by_id.get(ref_id)
				if ref is not None:
					root = ref
					flag = True
				else:
					i += 1
		else:
			root = msg
		
		msg.root = root
		if root is not None:
			msg.subject = sanitize_subject(root.raw_subject)
		else:
			msg.subject = ""
	
	for msg in messages:
		print(f"writing message #{msg.index}")
		write_attachments(msg)
		write_markdown(msg)
