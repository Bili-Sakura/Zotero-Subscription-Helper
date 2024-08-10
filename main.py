import yaml
import os
from src.scraper.cvf_parser import CVFParser
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def initialize_file(filename_base):
    """
    Create the files initially to ensure they exist before writing.
    """
    try:
        open(f"out/{filename_base}.bib", "w", encoding="utf-8").close()
        open(f"out/{filename_base}.xml", "w", encoding="utf-8").close()
        logger.info(f"Initialized {filename_base}.bib and {filename_base}.xml")
    except Exception as e:
        logger.error(
            f"Failed to initialize files {filename_base}.bib and {filename_base}.xml: {e}"
        )


def main():
    # Load configuration
    config = load_config()

    # Prepare the filename base using the conference name and year
    conference = config["conference"].upper()
    year = config["year"]

    # Ensure the output directory exists
    output_dir = "out"
    if not os.path.exists(output_dir):
        logger.info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # Initialize the CVFParser with the configuration
    scraper = CVFParser(config)

    # Create output files for storing the results
    filename_base = f"{conference}{year}"
    logger.info(f"Filename base: {filename_base}")
    initialize_file(filename_base)

    # Start scraping and processing
    scraper.scrape(filename_base, max_papers=5000)

    logger.info("All papers have been processed and saved.")


if __name__ == "__main__":
    main()
