# Zotero-Subscription-Helper

This project is designed to crawl paper metadata from computer science conference websites and convert it into `.xml` and `.bib` files for Zotero import.

## Features

- Web scraping of conference websites for paper metadata
- Conversion of scraped data into Zotero-compatible formats (`.xml` and `.bib`)

## Installation

To get started with this project, follow the steps below to set up your development environment.

### 1. Clone the Repository

```bash
git clone https://github.com/bili-sakura/Zotero-Subscription-Helper.git
cd Zotero-Subscription-Helper
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. Run the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Run the Project

You can now run the main script to start scraping:

```bash
python main.py
```

### 5. Deactivate the Virtual Environment

Once you're done working, you can deactivate the virtual environment:

```bash
deactivate
```

## Acknowledge

This project is strongly inspired by the work done in the [CPR-RSS](https://github.com/CPR-RSS/CPR-RSS.github.io) repository. We would like to express our gratitude to the contributors of CPR-RSS for their efforts in creating and sharing their work. Their project provided a valuable reference and foundation for the development of this project, [Zotero-Subscription-Helper](https://github.com/Bili-Sakura/Zotero-Subscription-Helper).
