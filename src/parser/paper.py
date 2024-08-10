# ./src/parser/paper.py


class Paper:
    def __init__(self, title, abstract, pdf_url, supp_url, authors, bibtex=None):
        self.title = title
        self.abstract = abstract
        self.pdf_url = pdf_url
        self.supp_url = supp_url
        self.authors = authors
        self.bibtex = bibtex

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
        Converts the Paper object into an XML format.
        """
        authors_xml = "".join([f"<author>{author}</author>" for author in self.authors])
        return f"""
        <paper>
            <title>{self.title}</title>
            <abstract>{self.abstract}</abstract>
            <pdf_url>{self.pdf_url}</pdf_url>
            <supp_url>{self.supp_url}</supp_url>
            <authors>
                {authors_xml}
            </authors>
        </paper>
        """
