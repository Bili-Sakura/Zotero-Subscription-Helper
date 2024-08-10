import yaml
import os
import argparse
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
        # init .xml with
        # <?xml version="1.0" encoding="UTF-8"?>
        # <rss version="2.0">
        # <channel>
        #     <title>ICCV 2023 test</title>
        # end with
        # </channel>
        # </rss>
        open(f"out/{filename_base}.xml", "w", encoding="utf-8").close()
        logger.info(f"Initialized {filename_base}.bib and {filename_base}.xml")
    except Exception as e:
        logger.error(
            f"Failed to initialize files {filename_base}.bib and {filename_base}.xml: {e}"
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Scrape and process conference papers."
    )
    parser.add_argument(
        "--conference", type=str, help="Name of the conference (e.g., ICCV)"
    )
    parser.add_argument("--year", type=int, help="Year of the conference (e.g., 2023)")
    parser.add_argument(
        "--max-papers",
        type=int,
        default=5000,
        help="Maximum number of papers to scrape",
    )
    parser.add_argument(
        "--config", type=str, default=None, help="Path to YAML configuration file"
    )
    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Load configuration either from YAML or command-line arguments
    if args.config:
        logger.info(f"Loading configuration from {args.config}")
        config = load_config(args.config)
    else:
        logger.info("Using command-line arguments for configuration")
        config = {"conference": args.conference, "year": args.year}

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
    max_papers = args.max_papers if not args.config else config.get("max_papers", 5000)
    scraper.scrape(filename_base, max_papers=max_papers)

    logger.info("All papers have been processed and saved.")


if __name__ == "__main__":
    main()
