%%%% The stylesheet for MTF-ARNOLD music notation font
%%%%
%%%% In order for this to work, this file's directory needs to 
%%%% be placed in LilyPond's path
%%%%
%%%% NOTE: If a change in the staff-size is needed, include
%%%% this file after it, like:
%%%%
%%%% #(set-global-staff-size 17)
%%%% \include "mtf-arnold.ily"
%%%%
%%%% Copyright (C) 2014-2016 Abraham Lee (tisimst.lilypond@gmail.com)

\version "2.19.12"

\paper {
  #(define fonts
    (set-global-fonts
    #:music "mtf-arnold"
    #:brace "mtf-arnold"
    #:factor (/ staff-height pt 20)
  ))
}

%%%%
%%%% THE FOLLOWING WAS CONTRIBUTED BY URS LISKA TO MATCH UNIVERSAL EDITION STYLE
%%%%
\layout {

  \context {
    \Voice
    \override Beam.beam-thickness = 0.52
    \override Slur.thickness = 1.75
    \override Slur.line-thickness = 0.6
    \override Tie.thickness = 1.6
    \override Tie.line-thickness = 0.6
  }

  \context {
    \Lyrics
    \override LyricText.font-size = 0.3
    % REMOVE THE FOLLOWING WHEN A SUITABLE TEXT FONT IS FOUND WITH THIS PROPERTY
    \override LyricText.stencil =
    #(lambda (grob)
       (ly:stencil-scale (lyric-text::print grob) 0.9 1))
  }
  

  \context {
    \Score
    \override DynamicText.font-size = 1.15
    \override Stem.thickness = 1.15
    \override Hairpin.thickness = 1.4
    \override Hairpin.height = 0.45
    \override InstrumentName.font-size = 1.5
    \override MetronomeMark.font-size = 1.5
    % REMOVE THE FOLLOWING WHEN A SUITABLE TEXT FONT IS FOUND WITH THIS PROPERTY
    \override MetronomeMark.stencil =
    #(lambda (grob)
       (ly:stencil-scale (ly:text-interface::print grob) 0.78 1))
  }
}

#(append! default-script-alist
   (list
    `("arnoldWeakbeat"
       . ((script-stencil . (feta . ("weakbeat" . "weakbeat")))
          ; any other properties
          (toward-stem-shift-in-column . 0.0)
          (padding . 1)
          (avoid-slur . around)
          (direction . ,UP)))
    `("arnoldStrongbeat"
       . ((script-stencil . (feta . ("strongbeat" . "strongbeat")))
          ; any other properties
          (toward-stem-shift-in-column . 0.0)
          (padding . 1)
          (avoid-slur . around)
          (direction . ,UP)))
    `("arnoldVaraccent"
       . ((toward-stem-shift-in-column . 0.0)
          (script-stencil . (feta . ("varaccent" . "varaccent")))
          ; any other properties
          (padding . 0.20)
          (side-relative-direction . ,DOWN)
          (avoid-slur . around)))
    ))

%%%% create postfix commands to use the articulations
arnoldWeakbeat = #(make-articulation "arnoldWeakbeat")
arnoldStrongbeat = #(make-articulation "arnoldStrongbeat")
arnoldVaraccent = #(make-articulation "arnoldVaraccent")

altAccent =
#(define-void-function (parser location)()
   (set! dashLarger arnoldVaraccent))

defAccent =
#(define-void-function (parser location)()
   (set! dashLarger accent))

hauptstimme = \markup { \halign #1 \musicglyph #"scripts.hauptstimme" }
nebenstimme = \markup { \halign #1 \musicglyph #"scripts.nebenstimme" }
endstimme = \markup { \halign #-1.5 \musicglyph #"scripts.endstimme" }
