"""Subset the official JetBrains Mono woff2 files into the small fonts embedded in theme.css.

The full variable fonts are ~115 KB each; keeping only the characters notes and commands use
(Latin, punctuation, arrows, a few math signs, box drawing and the full block) and dropping the
code ligatures brings each one down to ~27 KB.

Usage (needs `pip install fonttools brotli`):
    python src/subset_fonts.py <JetBrainsMono[wght].woff2> <JetBrainsMono-Italic[wght].woff2>

Official files: https://github.com/JetBrains/JetBrainsMono/tree/master/fonts/webfonts
"""
import sys
from pathlib import Path

from fontTools.subset import main as subset

FONTS = Path(__file__).resolve().parent / "fonts"
TEXT = ("U+0020-007E,U+00A0-00FF,U+0100-017F,U+2000-206F,U+20AC,U+2122,"
        "U+2190-2193,U+2212,U+2260,U+2264-2265,U+FFFD")
BOXES = "U+2500-257F,U+2588"           # tree output, tables drawn with lines and the blinking cursor
FEATURES = "ccmp,locl,mark,mkmk,zero"  # no calt/liga: no ligatures, commands look exactly as typed


def run(src, dst, unicodes):
    subset([str(src), f"--unicodes={unicodes}", "--flavor=woff2", f"--layout-features={FEATURES}",
            f"--output-file={FONTS / dst}"])
    print(f"{dst}: {(FONTS / dst).stat().st_size // 1024} KB")


if __name__ == "__main__":
    regular, italic = map(Path, sys.argv[1:3])
    run(regular, "JetBrainsMono-wght-subset.woff2", f"{TEXT},{BOXES}")
    run(italic, "JetBrainsMono-Italic-wght-subset.woff2", TEXT)
