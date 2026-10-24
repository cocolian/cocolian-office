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

The shared profile pins 38 private font files, with native Aptos/Segoe UI faces,
Helvetica, Menlo, Wingdings and Apple Color Emoji fallback. No binaries or sample
documents belong in Git. All three deployed renderers use this same profile.
The pipeline additionally enables `COCOLIAN_WORD_MAC_AUTOFIT=1` and
`COCOLIAN_WORD_MAC_GRID_BOTTOM=1`; the source repository contains generated
regressions for their supported layouts and boundary conditions.
The renderer also enables `COCOLIAN_WORD_MAC_FLEX_SCRIPT_GAPS=1` and
`COCOLIAN_WORD_MAC_LINE_BUDGET=1`, covered by generated Word-reference regressions.

`COCOLIAN_WORD_MAC_CLASSIC_METRICS=1` uses measured Mac Word line metrics for
SimSun, SimHei, FangSong and KaiTi, and measured leading for YaHei/DengXian.
The engine pipeline runs 27 bundled-font regressions and 20 native-font
regressions before packaging. The private 15-document/229-page corpus includes
page geometry and visual comparisons; page-count agreement is not full visual
acceptance, and remaining differences stay in local reports.
