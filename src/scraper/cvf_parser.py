import sys
import requests
from collections import defaultdict
from tqdm import tqdm
import os
import time
import re
from requests.exceptions import ConnectionError, ReadTimeout
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper
from ..utils.logger import get_logger
from ..parser.paper import Paper

logger = get_logger(__name__)


class CVFParser(BaseScraper):
    def __init__(self, config):
        conference = config["conference"]
        year = config["year"]

        if conference.upper() == "ICCV":
            assert year % 2 == 1, "ICCV is held in odd years only!"

        self.base_url = f"http://openaccess.thecvf.com/{conference.upper()}{year}"
        self.website_url = "http://openaccess.thecvf.com/"
        super().__init__(self.base_url)

    def scrape(self, filename_base, batch_size=10, max_papers=20):
        """
        Scrapes the conference website, processes papers in batches, and saves results incrementally.
        Processes only the first `max_papers` papers.
        """
        base_url = self.base_url
        logger.info(f"Parsing: {base_url}")

        try:
            response = self.session.get(base_url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch the page {base_url}: {e}")
            return []

        _content = response.content.decode("utf-8")
        found_urls = [
            self.website_url + dda.get("href")
            for dda in BeautifulSoup(_content, features="html.parser").select("dd >a")
        ]
        contents = [
            requests.get(url, timeout=5).content.decode("utf-8")  # 5 seconds timeout
            for url in found_urls
        ]

        paper_list = []
        parse_log = defaultdict(lambda: 0)

        if "all" in [found_url.lower() for found_url in found_urls]:
            found_urls = found_urls[:-1]
            contents = contents[:-1]

        logger.info("Found the following containers:")
        for url, content in zip(found_urls, contents):
            soup = BeautifulSoup(content, features="html.parser")
            lists, log = self.parse(soup, url)  # Call to parse method
            paper_list.extend(lists)
            parse_log = {key: parse_log[key] + log[key] for key in log}

            # Stop if we've reached the maximum number of papers
            if len(paper_list) >= max_papers:
                paper_list = paper_list[:max_papers]
                break

        # Process and save papers in batches
        for i in tqdm(range(0, len(paper_list), batch_size), desc="Processing batches"):
            batch = paper_list[i : i + batch_size]
            self.process_and_save_batch(batch, filename_base)

        # logger.info(
        #     f"{self.base_url}, Overall: {parse_log['overall']}, failed: {parse_log['failed']}"
        # )

    def parse(self, html_soup, url=None):
        """
        Parses the HTML soup to extract paper information.
        """
        all_container = html_soup.select("dt.ptitle")
        paper_list = []
        overall = 0
        failed = 0

        # Logging the progress bar to file
        progress_bar = tqdm(
            all_container,
            desc="" if url is None else url,
            file=sys.stdout,  # By default, the progress bar is printed to stdout
        )

        for container in progress_bar:
            try:
                title = container.select("a")[0].get_text()
                paper_url = container.select("a")[0].get("href")
                paper_list.append((title, paper_url))
                overall += 1
            except Exception as e:
                logger.error(f"Line ({sys._getframe().f_lineno}): {e}")
                failed += 1

        return paper_list, {"overall": overall, "failed": failed}

    def process_and_save_batch(self, batch, filename_base):
        """
        Processes a batch of papers and saves them to the output files.
        """
        for paper_info in batch:
            paper = self.cook_paper(paper_info)
            if paper:
                self.export_single_paper(paper, filename_base)

    def export_single_paper(self, paper, filename_base):
        """
        Exports a single paper's data to the .bib and .xml files.
        """
        if paper:
            # Export to .bib
            bib_filename = f"out/{filename_base}.bib"
            new_bib_content = paper.to_bib() + "\n\n"
            self.save_to_file(bib_filename, new_bib_content)

            # Export to .xml
            xml_filename = f"out/{filename_base}.xml"
            new_xml_content = paper.to_xml() + "\n"
            self.save_to_file(xml_filename, new_xml_content)
        else:
            logger.warning(
                f"Paper object is empty, skipping export for {filename_base}"
            )

    def save_to_file(self, filename, content):
        """
        Saves content to a file in append mode.
        """
        if content.strip():  # Ensure that there is content to write
            try:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(content)
                # logger.info(f"Successfully wrote to {filename}")
            except Exception as e:
                logger.error(f"Failed to write to {filename}: {e}")
        else:
            logger.warning(f"No content to write for {filename}")

    def cook_paper(self, paper_info, retries=3, delay=5):
        """
        Attempts to fetch and process the paper details, with retry logic in case of connection errors.
        """
        for attempt in range(retries):
            try:
                page_content = requests.get(
                    self.website_url + paper_info[1], timeout=20
                ).content.decode("utf-8")
                soup = BeautifulSoup(page_content, features="html.parser")

                # Extract authors
                author_list = soup.select("#authors >b >i")[0].get_text().split(",")
                author_list = [self.text_process(author) for author in author_list]

                # Extract abstract
                abstract = self.text_process(soup.select("#abstract")[0].get_text())

                # Extract PDF link
                pdf_link = None
                supp_link = None
                for link in soup.select("a"):
                    if "pdf" in link.get_text().lower():
                        pdf_link = self.website_url + link.get("href")
                    elif (
                        "supplemental" in link.get_text().lower()
                        or "supp" in link.get_text().lower()
                    ):
                        supp_link = self.website_url + link.get("href")

                # Extract BibTeX entry directly from the page
                bibtex_div = soup.find("div", class_="bibref pre-white-space")
                if bibtex_div:
                    bibtex_content = bibtex_div.get_text().strip()
                else:
                    bibtex_content = None

                return Paper(
                    title=self.text_process(paper_info[0]),
                    abstract=abstract,
                    pdf_url=pdf_link,
                    supp_url=supp_link,
                    authors=author_list,
                    bibtex=bibtex_content,
                )

            except Exception as e:
                # Handle any errors and return a Paper object with minimal data
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    logger.error(f"All {retries} attempts failed for {paper_info[0]}")
                    return Paper(
                        title=paper_info[0],
                        # abstract=str(e),
                        abstract=None,
                        pdf_url=self.website_url + paper_info[1],
                        supp_url=None,
                        authors=[],
                        bibtex=None,
                    )

    def text_process(self, text):
        """
        Process and clean text: strip extra whitespace and normalize text.
        """

        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace("'", "&apos;")
        text = text.replace('"', "&quot;")
        text = text.replace("’", "'")
        # re.sub(u"[\x01-\x1f|\x22|\x26|\x27|\x2f|\x3c|\x3e]+",u"",sourceString)
        text = re.sub("[^!-~]+", " ", text).strip()

        return text.strip()
