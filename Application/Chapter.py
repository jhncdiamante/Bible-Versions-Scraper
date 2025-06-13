from Chapter.IChapter import IChapter
from bs4 import BeautifulSoup
import requests
import re
from selenium.webdriver.remote.webelement import WebElement


class Chapter(IChapter):
    def __init__(self, chapter_ref: WebElement, chapter_number):
        self._chapter_ref = chapter_ref # <a> tag
        self._chapter_number = chapter_number

    def getChapterAbbreviation(self) -> str:
        url = self._chapter_ref.get_attribute("href").strip()
        match = re.search(r"/bible/[^/]+/([^.]+)\.\d+", url)
        if match:
            return match.group(1)
        raise ValueError("Chapter ABV not found in URL:", url)

    def getAllVerses(self) -> list[str]:
        href = self._chapter_ref.get_attribute("href")
        if not href:
            raise ValueError("Chapter href is empty or invalid")

        print(f"Fetching chapter from: {href}")

        try:
            response = requests.get(href, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch chapter page: {e}")

        soup = BeautifulSoup(response.text, "html.parser")

        BASE_ID = f"{self.getChapterAbbreviation()}.{self._chapter_number}."

        verses = []
        i = 1

        while True:
            verse_id = f"{BASE_ID}{i}"

            verse_elems = soup.find_all(attrs={"data-verse-org-id": verse_id})

            if not verse_elems:
                break  # No more verses

            verse_text = " ".join(v.get_text(strip=True) for v in verse_elems)
            verses.append(verse_text)
            i += 1

        return verses



