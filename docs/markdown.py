from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

class CleanMarkdownConverter(MarkdownConverter):
    """
    Override the default MarkdownConverter for improved cleaning
    """
    def convert(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # we are only interested in the body (if present)
        body = soup.find('body') or soup

        for tag in body(["script", "style"]):  # remove all javascript and stylesheet code
            tag.decompose()

        return self.process_tag(body, convert_as_inline=False, children_only=True)