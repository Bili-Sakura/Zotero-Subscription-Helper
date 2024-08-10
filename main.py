from src.scraper.conference_scraper import ConferenceScraper


def main():
    url = "https://example-conference.org"  # Replace with the actual conference URL
    scraper = ConferenceScraper(url)
    papers = scraper.scrape()

    # For now, just print the extracted metadata
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {paper['authors']}")
        print(f"Abstract: {paper['abstract']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
