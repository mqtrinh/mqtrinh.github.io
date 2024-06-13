/*
 ADOBE CONFIDENTIAL
 ___________________

 Copyright 2011 Adobe Systems Incorporated
 All Rights Reserved.

 NOTICE:  All information contained herein is, and remains
 the property of Adobe Systems Incorporated and its suppliers,
 if any.  The intellectual and technical concepts contained
 herein are proprietary to Adobe Systems Incorporated and its
 suppliers and may be covered by U.S. and Foreign Patents,
 patents in process, and are protected by trade secret or copyright law.
 Dissemination of this information or reproduction of this material
 is strictly forbidden unless prior written permission is obtained
 from Adobe Systems Incorporated.
*/
(function(a){function b(a){var b=a.css("background-image");a.css("background-image","");var c=a.css("background-image");b!=c&&a.css("background-image",b);return c.replace(/^\s*url\(\"?/,"").replace(/['"]?\)$/,"")}if(!Muse.Browser.Features.checkCSSFeature("background-size")){var c=function(c){var d=a(c),g=b(d),f=document.createElement("img"),i=document.createElement("div"),m=this,l=!1,o=!1,q=!0,p={};a(i).css({overflow:"hidden",position:"absolute",top:"0px",left:"0px",width:c.clientWidth+"px",height:c.clientHeight+
"px",marginBottom:"-"+c.clientHeight+"px",marginRight:"-"+c.clientWidth+"px",zIndex:"-1"}).addClass("museBgSizePolyfill");f.src=g;f.alt="";f.style.position="absolute";i.appendChild(f);c.children.length>0?c.insertBefore(i,c.children[0]):c.appendChild(i);if(c===document.body)d=a("html"),c=d.get(0),g=b(d),f.src=g,d.css("background-attachment")=="fixed"?(i.style.position="fixed",q=!1):i.style.position="absolute";else if(d.is("#page"))d.css("marginLeft").toLowerCase()=="auto"&&(o=!0),i.style.top=d.offset().top+
parseInt(d.css("borderTopWidth"))+"px",i.style.bottom=parseInt(d.parent().css("paddingBottom"))+parseInt(d.css("borderBottomWidth"))+"px",i.style.left=d.offset().left+parseInt(d.css("borderLeftWidth"))+"px",i.style.right=d.offset().left+parseInt(d.css("borderRightWidth"))+"px",i.style.zIndex=0;else if(d.css("position")=="static")c.style.position="relative";this.reloadImage=function(){var a=b(d),g=d.css("background-color");if(a!=f.src)f.src=a;c.style.backgroundImage="none";c.style.backgroundColor=
"transparent";i.style.backgroundColor=g;a=(d.css("background-position-x")+" "+d.css("background-position-y")).replace(/^\s+/,"").replace(/\s+$/,"").split(/\s+/);a.length==1&&a[0].indexOf("center")>=0&&a.push("center");if(d.data("hasBackgroundPositionScrollEffect")!=!0)for(var g=0,m=a.length;g<m;g++)switch(a[g]){case "center":case "50%":g==0?(f.style.right="",f.style.left="50%",f.style.marginLeft="-"+Math.ceil(f.offsetWidth/2)+"px"):(f.style.bottom="",f.style.top="50%",f.style.marginTop="-"+Math.ceil(f.offsetHeight/
2)+"px");break;case "left":f.style.right="";f.style.left="0px";f.style.marginLeft="0px";break;case "right":f.style.left="";f.style.right="0px";f.style.marginLeft="0px";break;case "top":f.style.bottom="";f.style.top="0px";f.style.marginTop="0px";break;case "bottom":f.style.top="";f.style.bottom="0px";f.style.marginTop="0px";break;default:g==0?(f.style.left=a[g],f.style.marginLeft="-"+Math.ceil(f.offsetWidth/2)+"px"):(f.style.top=a[g],f.style.marginTop="-"+Math.ceil(f.offsetHeight/2)+"px")}};this.resizeImage=
function(a){var b=c.getBoundingClientRect(),g=c.scrollWidth-(Muse.Browser.Bugs.ScrollWidthHeightIncludesBorder?b.right-b.left-d.innerWidth():0),b=c.scrollHeight-(Muse.Browser.Bugs.ScrollWidthHeightIncludesBorder?b.bottom-b.top-d.innerHeight():0),g=!q?c.clientWidth:Math.max(g,c.clientWidth),b=!q?c.clientHeight:Math.max(b,c.clientHeight);!p[f.src]&&f.clientWidth&&(p[f.src]={width:f.clientWidth,height:f.clientHeight});var m=g/(p[f.src]?p[f.src].width:1),l=b/(p[f.src]?p[f.src].height:1);i.style.height=
b+"px";i.style.marginBottom="-"+b+"px";i.style.width=g+"px";i.style.marginRight="-"+g+"px";m<l==a?(f.style.height=b+1+"px",f.style.width="auto"):(f.style.width=g+1+"px",f.style.height="auto")};this.update=function(){if(l){c.style.backgroundImage="";d.css("background-color","");var a=d.css("background-image").toLowerCase(),b=(c.currentStyle||window.getComputedStyle(c,null))["background-size"];b&&b.toLowerCase();if(a!="none"&&(b=="cover"||b=="contain")){if(m.reloadImage(),i.style.display="block",i.style.width=
"0px",i.style.height="0px",m.resizeImage(b=="cover"),o)i.style.left=d.offset().left+parseInt(d.css("borderLeftWidth"))+"px",i.style.right=d.offset().left+parseInt(d.css("borderRightWidth"))+"px"}else i.style.display="none"}};if(f.complete||g=="none")l=!0;else a(f).one("load",function(){l=!0;m.update()});this.update()},d=[];a(".museBGSize").each(function(){var b=new c(this);this!==document.body?d.push(b):(a(window).resize(function(){setTimeout(function(){b.update()},10)}),a(window).load(function(){setTimeout(function(){b.update()},
10)}))});var f=d.length;f>0&&setInterval(function(){for(var a=0;a<f;a++)d[a].update()},Math.max(120,16*f))}})(jQuery);
