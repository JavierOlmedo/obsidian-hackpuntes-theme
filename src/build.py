"""Build theme.css from src/theme.src.css, embedding the subset JetBrains Mono (woff2, base64) at the end.

The fonts in src/fonts are made by src/subset_fonts.py.

Usage: python src/build.py
"""
import base64
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
FONTS = (("normal", "JetBrainsMono-wght-subset.woff2"), ("italic", "JetBrainsMono-Italic-wght-subset.woff2"))


def main():
    css = (SRC / "theme.src.css").read_text(encoding="utf-8").rstrip() + "\n"
    for style, name in FONTS:
        data = base64.b64encode((SRC / "fonts" / name).read_bytes()).decode()
        css += ("\n@font-face {\n  font-family: 'JetBrains Mono';\n  font-style: %s;\n  font-weight: 100 800;\n"
                "  font-display: swap;\n  src: url(data:font/woff2;base64,%s) format('woff2');\n}\n") % (style, data)
    out = ROOT / "theme.css"
    out.write_text(css, encoding="utf-8", newline="\n")
    print(f"{out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
