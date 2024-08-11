# ./src/parser/paper.py


class Paper:
    def __init__(self, title, abstract, pdf_url, supp_url, authors, bibtex=None):
        self.title = title
        self.abstract = abstract
        self.pdf_url = pdf_url
        self.supp_url = supp_url
        self.authors = authors
        self.bibtex = bibtex

        # Initialize fields extracted from BibTeX
        self.booktitle = None
        self.month = None
        self.year = None
        self.pages = None
        self.start_page = None
        self.end_page = None

        # Parse the BibTeX entry if available
        if bibtex:
            self.parse_bibtex(bibtex)

    def parse_bibtex(self, bibtex):
        """
        Parses a BibTeX entry to extract additional information like booktitle, month, year, and pages.
        """
        lines = bibtex.splitlines()
        for line in lines:
            if "booktitle" in line:
                self.booktitle = line.split("=", 1)[1].strip().strip("{},")
            elif "month" in line:
                self.month = line.split("=", 1)[1].strip().strip("{},")
            elif "year" in line:
                self.year = line.split("=", 1)[1].strip().strip("{},")
            elif "pages" in line:
                self.pages = line.split("=", 1)[1].strip().strip("{},")
                if "-" in self.pages:
                    self.start_page, self.end_page = self.pages.split("-")

    def __repr__(self):
        return f"<Paper(title={self.title}, authors={', '.join(self.authors)})>"

    def to_bib(self):
        """
        Returns the BibTeX entry if available, and appends the supp_url as a note if present.
        """
        if self.bibtex:
            bibtex_entry = self.bibtex.rstrip("}")  # Remove the newline
            bibtex_entry = bibtex_entry.strip("\n")
            # bibtex_entry += ","
            if self.supp_url:
                bibtex_entry += f",\n  note={{Supplemental material: {self.supp_url}}}"
            if self.pdf_url:
                bibtex_entry += f",\n  url={{ {self.pdf_url} }}"
            bibtex_entry += "\n}"
            return bibtex_entry
        else:
            # Fallback if BibTeX wasn't provided; construct one manually (not recommended)
            authors_bib = " and ".join(
                [self.format_author(author) for author in self.authors]
            )
            return f"""@article{{,\n  
            title={{ {self.title} }},\n 
              author={{ {authors_bib} }},\n 
                abstract={{ {self.abstract} }},\n  
                url={{ {self.pdf_url} }}\n
                }}"""

    def format_author(self, author):
        """
        Formats the author name as 'Last, First'.
        """
        parts = author.split()
        if len(parts) > 1:
            # Assume the last part is the last name
            last_name = parts[-1]
            first_names = " ".join(parts[:-1])
            return f"{last_name}, {first_names}"
        return author  # Return the name as-is if it doesn't follow 'First Last' pattern

    def to_xml(self):
        """
        Converts the Paper object into an XML format, omitting fields that are not available.
        """
        # xml_parts = [
        #     "<item>",
        #     f"    <title><![CDATA[{self.title}]]></title>",
        #     f"    <link><![CDATA[{self.pdf_url}]]></link>",
        #     f"    <description><![CDATA[{self.abstract}]]></description>",
        # ]
        xml_parts = [
            "<item>",
            f"    <title>{self.title}</title>",
            f"    <link>{self.pdf_url}</link>",
            f"    <description>{self.abstract}</description>",
        ]

        # if self.year and self.month:
        #     xml_parts.append(
        #         f"    <pubDate><![CDATA[{self.month} {self.year}]]></pubDate>"
        #     )
        # if self.year:
        #     xml_parts.append(f"    <pubYear><![CDATA[{self.year}]]></pubYear>")
        # if self.start_page and self.end_page:
        #     xml_parts.append(f"    <startPage>{self.start_page}</startPage>")
        #     xml_parts.append(f"    <endPage>{self.end_page}</endPage>")

        # authors_xml = ";".join(self.authors)
        # xml_parts.append(f"    <authors><![CDATA[{authors_xml}]]></authors>")

        # if self.booktitle:
        #     xml_parts.append(f"    <booktitle><![CDATA[{self.booktitle}]]></booktitle>")

        xml_parts.append("</item>")

        return "\n".join(xml_parts)
