from Chapter.IChapter import IChapter
from bs4 import BeautifulSoup
import requests
import re
from selenium.webdriver.remote.webelement import WebElement
from collections import defaultdict

VERSE_ELEMENTS = "span.verse[observevisibility]"
VERSE_IDENTIFIER = 'data-verse-org-id'

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

        verse_elements = soup.select(VERSE_ELEMENTS)

        verses = defaultdict(str)

        for v_elem in verse_elements:
            verse_number = self._getVerseNumber(verse_element=v_elem)
            verse_content = v_elem.get_text(strip=True)
            verses[verse_number] += f"{verse_content}"

        return verses


    def _getVerseNumber(self, verse_element):
        verse_id = verse_element.get(VERSE_IDENTIFIER)
        if "." in verse_id:
            return verse_id.split(".")[-1]
        raise ValueError(f"Invalid verse ID found: {verse_id}")
