import requests
from bs4 import BeautifulSoup
import os
import logging

class LinkExtractor:
    def __init__(self, start_page, end_page, base_url, output_file):
        self.start = start_page
        self.end = end_page
        self.base_url = base_url
        self.output = output_file
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def extract_links(self):
        all_links = []
        for page in range(self.start, self.end + 1):
            url = f"{self.base_url}{page}"
            logging.info(f"Scraping page {page} -> {url}")
            try:
                resp = requests.get(url, headers=self.headers)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                question_blocks = soup.find_all("div", class_="sabai-entity")
                for block in question_blocks:
                    title_div = block.find("div", class_="sabai-questions-title")
                    if title_div:
                        a_tag = title_div.find("a", href=True)
                        if a_tag and a_tag["href"].startswith("http"):
                            all_links.append(a_tag["href"])
            except Exception as e:
                logging.warning(f"[!] Failed page {page}: {e}")
        return all_links


    def save_links(self, links):
        os.makedirs(os.path.dirname(self.output), exist_ok=True)
        with open(self.output, "w", encoding="utf-8") as f:
            for link in links:
                f.write(link + "\n")
        logging.info(f"[✓] Saved {len(links)} links to {self.output}")
