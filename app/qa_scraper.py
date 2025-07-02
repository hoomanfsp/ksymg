import requests
from bs4 import BeautifulSoup
import json
import os
import logging
import time

class QAScraper:
    def __init__(self, link_file, output_file):
        self.link_file = link_file
        self.output_file = output_file
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.data = []

    def fetch_html(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.text
            logging.warning(f"[!] Failed: {url} (status {resp.status_code})")
            return None
        except Exception as e:
            logging.error(f"[!] Request error: {url} -> {e}")
            return None
    def parse_page(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")

            # === Extract question body ===
            question_container = soup.find("div", class_="sabai-entity-bundle-type-questions")
            q_body = ""
            if question_container:
                q_body_div = question_container.find("div", class_="sabai-questions-body")
                if q_body_div:
                    q_body = q_body_div.get_text(strip=True)

            # === Extract all answers ===
            answers = []
            answer_blocks = soup.find_all("div", class_="sabai-entity-bundle-type-questions-answers")
            for ans in answer_blocks:
                ans_body_div = ans.find("div", class_="sabai-questions-body")
                if ans_body_div:
                    ans_text = ans_body_div.get_text(strip=True)
                    if ans_text:
                        answers.append(ans_text)

            return {
                "question_body": q_body,
                "answers": answers
            }

        except Exception as e:
            logging.warning(f"[!] Parsing failed: {e}")
            return None


    def run(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.link_file, encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]

        for i, url in enumerate(links, 1):
            logging.info(f"[{i}/{len(links)}] Parsing: {url}")
            html = self.fetch_html(url)
            if html:
                parsed = self.parse_page(html)
                if parsed:
                    self.data.append(parsed)

            if i % 50 == 0:
                self.save()
                logging.info(f" Auto-saved at {i} entries")
            time.sleep(1)

        self.save()
        logging.info(f"[✓] Done! Parsed {len(self.data)} items.")

    def save(self):
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
