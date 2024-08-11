# Zotero-Subscription-Helper

This project is designed to crawl paper metadata from computer science conference websites and convert it into `.xml` and `.bib` files for Zotero import.

> [!NOTE]
> Currently, we only support IEEE conference/jounral. We would add more in the future.

> [!WARNING]
> Due to the unknown restricted format for Zotero RSS, the current `.xml` file can not import properly. Use `.bib` instead. We are going to pay efforts to fix this issue.

## Features

- Web scraping of conference websites for paper metadata
- Conversion of scraped data into Zotero-compatible formats (`.xml` and `.bib`)

[CVF Open Access (thecvf.com)](https://openaccess.thecvf.com/menu)

| Conference Name | RSS Link(.xml) [not work often, you may fix the format of these file] | Bibtex Link(.bib)                                |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| CVPR 2024       | <https://bili-sakura.github.io/rss/CVPR2024.xml>             | <https://bili-sakura.github.io/bib/CVPR2024.bib> |
| WACV 2024       | <https://bili-sakura.github.io/rss/WACV2024.xml>             | <https://bili-sakura.github.io/bib/WACV2024.bib> |
| ICCV 2023       | <https://bili-sakura.github.io/rss/ICCV2023.xml>             | <https://bili-sakura.github.io/bib/ICCV2023.bib> |
| CVPR 2023       | <https://bili-sakura.github.io/rss/CVPR2023.xml>             | <https://bili-sakura.github.io/bib/CVPR2023.bib> |
| WACV 2023       | <https://bili-sakura.github.io/rss/WACV2023.xml>             | <https://bili-sakura.github.io/bib/WACV2023.bib> |

For journal, the official provide RSS subscription link, you can access them from their main page, here we provide several heating RSS subscription link.

| Jounral Name                                                 | Official RSS Link                         |
| ------------------------------------------------------------ | ----------------------------------------- |
| [TPAMI](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=34) | <https://ieeexplore.ieee.org/rss/TOC34.XML> |
| [TGRS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=36) | <https://ieeexplore.ieee.org/rss/TOC36.XML> |

## Installation (only if you are going to generate your own file)

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

## Usage

### Option 1: Using a YAML Configuration File

You can provide a configuration file in YAML format to specify the conference name, year, and other settings.

1. Create a YAML configuration file (e.g., `config/config.yaml`):

   ```yaml
   conference: ICCV
   year: 2023
   max_papers: 5000  # Optional, defaults to 5000 if not provided
   ```

2. Run the script with the configuration file:

   ```bash
   python main.py --config config/config.yaml
   ```

### Option 2: Using Command-Line Arguments

Alternatively, you can provide the necessary information directly through command-line arguments.

#### Required Arguments

- `--conference`: The name of the conference (e.g., ICCV, CVPR).
- `--year`: The year of the conference.

#### Optional Arguments

- `--max-papers`: The maximum number of papers to scrape. Default is 5000.
- `--config`: Path to a YAML configuration file. If provided, this overrides command-line arguments.

#### Example Command

```bash
python main.py --conference ICCV --year 2023 --max-papers 5000
```

### Notes

- If both a configuration file and command-line arguments are provided, the configuration file will take precedence.
- Ensure that the output directory (`out/`) is writable and has enough space to store the `.bib` and `.xml` files.

## Acknowledge

This project is strongly inspired by the work of [CPR-RSS](https://github.com/CPR-RSS/CPR-RSS.github.io) repository [@XgDuan](https://github.com/XgDuan).

## Future Work

### Fix

- [ ] restart from existing file and skip existing items and continue
- [ ] fix `.xml` format for rss to zotero
- [ ] use multiprocess to accelerate
