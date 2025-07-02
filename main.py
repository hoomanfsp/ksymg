import logging
from app.config import *
from app.link_extractor import LinkExtractor
from app.qa_scraper import QAScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    linker = LinkExtractor(
        start_page=START_PAGE,
        end_page=END_PAGE,
        base_url=LISTING_URL,
        output_file=LINK_OUTPUT
    )
    links = linker.extract_links()
    linker.save_links(links)

    scraper = QAScraper(link_file=LINK_OUTPUT, output_file=QA_OUTPUT)
    scraper.run()

if __name__ == "__main__":
    main()
