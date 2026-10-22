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
keep these branches off main until residual layout differences are resolved.
