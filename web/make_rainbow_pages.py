#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Put the Rainbow mode landing pages next to the staged browser builds."""
import argparse
import re
import shutil
from collections.abc import Sequence
from pathlib import Path

from make_lang_page import ROOT, main as make_lang_page


def section(html: str, name: str, keep: bool) -> str:
    return re.sub(fr"<!--{name}-->(.*?)<!--/{name}-->", r"\1" if keep else "", html, flags=re.S)


def main(site: Path, languages: Sequence[str], pin: str) -> None:
    landing = ROOT / "landing"
    shutil.copytree(landing, site, dirs_exist_ok=True)
    for lang in languages:
        if not (landing / lang / "index.html").is_file():
            make_lang_page(lang, site / lang / "index.html")

    for root in (site, *(site / lang for lang in languages)):
        webapp = root / "webapp"
        installer = (webapp / "installer" / "index.html").is_file()
        editor = (webapp / "editor" / "index.html").is_file()

        page = root / "index.html"
        html = page.read_text(encoding="utf-8")
        html = section(html, "INSTALLER", installer)
        html = section(html, "PIN", bool(pin) and installer)
        html = re.sub(r"<!--BROWSER-ONLY (.*?)-->", "" if installer else r"\1", html, flags=re.S)
        page.write_text(html, encoding="utf-8")

        page = webapp / "try" / "index.html"
        html = page.read_text(encoding="utf-8")
        html = section(html, "INSTALLER", installer)
        html = section(html, "EDITOR", editor)
        page.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("languages", nargs="*")
    parser.add_argument("--pin", default="")
    args = parser.parse_args()
    main(args.site, args.languages, args.pin)
