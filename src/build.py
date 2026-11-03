"""Build theme.css from src/theme.src.css, embedding the subset JetBrains Mono (woff2, base64) at the end.

To stay under the size the Obsidian review recommends, theme.css drops the comments and the
indentation of src/theme.src.css. It keeps the header, the Style Settings block (which needs its
indentation) and the font license.

The fonts in src/fonts are made by src/subset_fonts.py.

Usage: python src/build.py
"""
import base64
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
FONTS = (("normal", "JetBrainsMono-wght-subset.woff2"), ("italic", "JetBrainsMono-Italic-wght-subset.woff2"))


def compact(css):
    kept = []

    def comment(match):
        text = match.group(0)
        if text.startswith(("/* ====", "/* @settings")) or "Open Font License" in text:
            kept.append(text)
            return f"\0{len(kept) - 1}\0"
        return ""

    css = re.sub(r"/\*.*?\*/", comment, css, flags=re.S)
    css = "\n".join(line.strip() for line in css.split("\n"))
    css = re.sub(r"\n{3,}", "\n\n", css)
    return re.sub(r"\0(\d+)\0", lambda m: kept[int(m.group(1))], css)


def main():
    css = compact((SRC / "theme.src.css").read_text(encoding="utf-8")).strip() + "\n"
    for style, name in FONTS:
        data = base64.b64encode((SRC / "fonts" / name).read_bytes()).decode()
        css += ("\n@font-face {\n  font-family: 'JetBrains Mono';\n  font-style: %s;\n  font-weight: 400 800;\n"
                "  font-display: swap;\n  src: url(data:font/woff2;base64,%s) format('woff2');\n}\n") % (style, data)
    out = ROOT / "theme.css"
    out.write_text(css, encoding="utf-8", newline="\n")
    print(f"{out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
