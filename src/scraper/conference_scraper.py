from .base_scraper import BaseScraper


class ConferenceScraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)

    def scrape(self):
        # Fetch the main conference page
        html = self.get_page(self.base_url)
        soup = self.parse_html(html)

        # Example: Let's say papers are listed under <div class="paper-entry">
        papers = soup.find_all("div", class_="paper-entry")

        paper_metadata = []
        for paper in papers:
            title = paper.find("h2").text
            authors = paper.find("p", class_="authors").text
            abstract = paper.find("div", class_="abstract").text

            # Add extracted data to the list
            paper_metadata.append(
                {"title": title, "authors": authors, "abstract": abstract}
            )

        return paper_metadata
