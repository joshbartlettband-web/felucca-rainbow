# SPDX-License-Identifier: GPL-3.0-only
"""Check the links the Pages job builds with and without FM-1 packages."""
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from make_rainbow_pages import ROOT, main

LANGUAGES = ("pt", "de", "fr", "es", "it", "nl", "sv", "no", "da", "ja")
BROWSER = "webapp/try/"
INSTALLER = "webapp/installer/"
EDITOR = "webapp/editor/"


class Links(HTMLParser):
    def __init__(self, page, site):
        super().__init__()
        self.url = "/" + "/".join(page.parent.relative_to(site).parts)
        self.url = self.url.rstrip("/") + "/"
        self.hrefs = set()
        self.feed(page.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        if tag == "a" and (href := dict(attrs).get("href")):
            self.hrefs.add(urljoin(self.url, href))


class RainbowPagesTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.site = Path(temp.name)
        self.roots = (self.site, *(self.site / lang for lang in LANGUAGES))
        for root in self.roots:
            browser = root / BROWSER / "index.html"
            browser.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "web" / "emu" / "index.html", browser)

    def add_page(self, root, route):
        page = root / route / "index.html"
        page.parent.mkdir(parents=True)
        page.touch()

    def check_links(self, root, has_installer, has_editor):
        landing = Links(root / "index.html", self.site)
        browser_path = root / BROWSER / "index.html"
        browser = Links(browser_path, self.site)
        self.assertTrue(browser_path.is_file())
        self.assertIn(landing.url + BROWSER, landing.hrefs)
        self.assertEqual(landing.url + INSTALLER in landing.hrefs, has_installer)
        self.assertEqual(landing.url + INSTALLER in browser.hrefs, has_installer)
        self.assertEqual(landing.url + EDITOR in browser.hrefs, has_editor)

    def test_browser_only_pages_have_no_installer_or_editor_links(self):
        main(self.site, LANGUAGES, "")
        for root in self.roots:
            with self.subTest(locale=root.relative_to(self.site)):
                self.check_links(root, False, False)
        for lang, notice in ((".", "The FM-1 installer is down for now."),
                             ("pt", "O instalador do FM-1 está indisponível por enquanto."),
                             ("ja", "現在、FM-1 用インストーラーは使えません。")):
            page = (self.site / lang / "index.html").read_text(encoding="utf-8")
            self.assertIn(notice, page)
            self.assertNotIn("<!--BROWSER-ONLY", page)

    def test_pages_with_packages_keep_the_links_and_pin_note(self):
        for root in self.roots:
            self.add_page(root, INSTALLER)
            self.add_page(root, EDITOR)
        main(self.site, LANGUAGES, "12345")
        for root in self.roots:
            with self.subTest(locale=root.relative_to(self.site)):
                self.check_links(root, True, True)
        self.assertIn("last version while we check the new one",
                      (self.site / "index.html").read_text(encoding="utf-8"))

    def test_missing_locale_package_only_changes_its_pages(self):
        self.add_page(self.site, INSTALLER)
        self.add_page(self.site, EDITOR)
        self.add_page(self.site / "de", EDITOR)
        main(self.site, LANGUAGES, "")
        self.check_links(self.site, True, True)
        self.check_links(self.site / "pt", False, False)
        self.check_links(self.site / "ja", False, False)
        self.check_links(self.site / "de", False, True)
        self.assertNotIn("last version while we check the new one",
                         (self.site / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
