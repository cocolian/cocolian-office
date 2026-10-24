# Mac Word reference profile

The production renderer pipeline sets `COCOLIAN_WORD_MAC_METRICS=1` and installs
one private, hash-pinned Office font pack in the editor and PDF conversion images.
The engine's default Windows Word behavior remains available when the variable
is absent. This profile uses actual GB2312 font files for FangSong_GB2312 and
KaiTi_GB2312. Its explicit missing-Fangzheng substitutions reproduce the font
families observed in the Mac Word reference PDFs; they do not substitute those
two GB2312 fonts. Font binaries remain outside Git.

The ten-document, 90-page government corpus also identifies missing Wenxing,
CESI Song, and FZ ShuSong families that Mac Word resolves to Microsoft YaHei.
These aliases are confined to this profile. The private font manifest additionally
pins the four Arial faces and Wingdings 2 from the installed Mac Word resources.
Native GB2312 families remain intact. The corpus is not visually accepted yet;
the individual renderer repairs are tested separately from full corpus acceptance.

The shared profile pins 41 private font files, with native Aptos/Segoe UI faces,
Helvetica, Menlo, Wingdings and Apple Color Emoji fallback. No binaries or sample
documents belong in Git. All three deployed renderers use this same profile.
The pipeline additionally enables `COCOLIAN_WORD_MAC_AUTOFIT=1` and
`COCOLIAN_WORD_MAC_GRID_BOTTOM=1`; the source repository contains generated
regressions for their supported layouts and boundary conditions.
The renderer also enables `COCOLIAN_WORD_MAC_FLEX_SCRIPT_GAPS=1` and
`COCOLIAN_WORD_MAC_LINE_BUDGET=1`, covered by generated Word-reference regressions.

`COCOLIAN_WORD_MAC_CLASSIC_METRICS=1` uses measured Mac Word line metrics for
SimSun, SimHei, FangSong and KaiTi, and measured leading for YaHei/DengXian.
The engine pipeline runs 32 bundled-font regressions and 26 native-font
regressions before packaging. The private 15-document/229-page corpus includes
page geometry and visual comparisons; page-count agreement is not full visual
acceptance, and remaining differences stay in local reports.

The renderer preserves explicit OOXML `wordWrap` values on paragraphs and styles.
The Mac profile permits character-level ASCII wrapping when the value is false.
Decimal and percentage tokens retain their closing CJK punctuation fit allowance.
Generated regressions verify namespaced DOCX export and save/reload inheritance;
private sample documents and fonts remain outside Git.

The Mac profile now preserves explicit row-level cell spacing and renders
uniform positive spacing on flat, top-level, non-floating tables without merged
rows. Generated cases cover zero spacing, merged-row fallback, disabled-profile
behavior and namespaced DOCX save/reload. This does not add table-level default
spacing support or establish full visual corpus acceptance.

The Mac profile keeps an ASCII HTTP(S) path tail together after a hyphen when
the complete tail fits the next line. Explicit `wordWrap=false` still uses
character-level wrapping, including underscores in identifiers. The generated
`testWordMacUrlBreakUnits` covers plain text and HYPERLINK fields, legacy and Mac
profiles, long-tail fallback, and DOCX save/reload with reserved example.invalid
addresses. Private sample documents and font binaries remain outside Git.

Left-aligned and centered table text snapped to a strict line grid now obeys the Word 2013
punctuation setting, including whole-portion fitting before line breaking.
`testWordMacStrictGridTablePunctuation` checks the enabled/disabled setting
and DOCX save/reload with pinned Segoe UI and SimSun fonts.
The private font pack additionally pins native Courier New and Tahoma faces.
Missing Chinese Tahoma glyphs prefer SimSun; missing FangSong_GB2312 glyphs
prefer Courier New. Installed primary faces remain first in the pattern.
Font binaries and sample documents remain outside Git.

In the Mac profile, PDF export selects artificial bold for each actual glyph
font, including fallback faces. A native bold primary face no longer suppresses
needed synthesis on its fallback, and native bold fallback glyphs avoid a
second stroke. The generated `testWordMacPdfFallbackBold` checks mixed Latin/CJK
fonts, horizontal/vertical layout, outline text, and the unchanged default profile.

Cached body-grid paragraphs rebuild their position-dependent line heights when
they move. Fitting and remaining-height accounting use the same lower-leading
allowance. `testWordMacCachedGridBottom` checks backward movement after editing,
nonnegative remaining space, and a visible-font-box overflow that must still
break the page. Tables, floating frames, and the default profile are excluded.

Top-level Mac-profile AutoFit tables stay within the page text width unless
OOXML `growAutofit` explicitly permits margin overflow. That compatibility
setting and the AutoFit layout mode survive DOCX save/reload. The generated
`testWordMacAutoFitPageWidth` checks both settings through two save/reload cycles,
including wrapping oversized content inside the page. Legacy-profile and fixed
table behavior are unchanged. Private sample documents remain outside Git.

Runtime COPY inputs receive the existing read/execute permission contract in the
private build context. Image recipes no longer run recursive chmod over the
installed engine, avoiding duplicate full-engine layers. Source files and
symlink targets outside that context keep their original permissions.

The Mac profile also keeps an ordinary space-delimited ASCII word intact when
a CJK break iterator cuts after its first character, provided the complete word
fits the next line. Explicit character-level wrapping, fields, hyphenation, URLs
and longer tokens retain their prior behavior. `testWordMacWordWrap` covers
English/Chinese language tags, both kinsoku flags, two widths, direct/inherited
and omitted wordWrap values, and DOCX save/reload.

Horizontal body text fitting one grid row now centers glyphs in its full
proportional pitch. This also applies to the first line, as in table cells,
while multi-row text retains its existing grid pitch.
`testWordMacSmallBodyGridProportional` verifies three-line paragraphs, the
unchanged legacy profile, and DOCX save/reload with generated documents.
