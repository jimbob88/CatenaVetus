from pathlib import Path
import webbrowser

from textual import on
from textual.widgets import Markdown, MarkdownViewer


class LinkableMarkdownViewer(MarkdownViewer):
    """URI supported markdown viewer.

    Source: https://github.com/Textualize/textual/discussions/3836
    """

    @on(Markdown.LinkClicked)
    def handle_link(self, event: Markdown.LinkClicked) -> None:
        if Path(event.href).exists():
            return

        event.prevent_default()
        webbrowser.open(event.href)
