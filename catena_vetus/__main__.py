from pathlib import Path
import sqlite3
import webbrowser

from textual import work, on
from textual.app import App, ComposeResult
from textual.widgets import Input, Header, Footer, Markdown, MarkdownViewer

from catena_vetus.commentaries_to_markdown import commentaries_to_markdown
from catena_vetus.database_api.code_verse import reference
from catena_vetus.database_api.errors import (
    GenericReferencePassingError,
    BookNotFoundError,
    ReferenceStyleNotRecognisedError,
)
from catena_vetus.database_api.sql import commentaries
from catena_vetus.spinner import SpinnerWidget


class CatenaVetus(App):
    """View what the Church Fathers wrote about a verse"""

    CSS_PATH = "main.css"
    BINDINGS = [
        ("t", "toggle_toc", "Toggle Table of Contents"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search for a verse")

        # with VerticalScroll(id="results-container"):
        yield SpinnerWidget(id="spinner")
        yield MarkdownViewer(id="results", show_table_of_contents=False)
        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""

        if not Path("commentaries.db").exists():
            raise FileNotFoundError("Could not find commentaries.db")

        # see: https://ricardoanderegg.com/posts/python-sqlite-thread-safety/
        self.connection = sqlite3.connect("commentaries.db", check_same_thread=False)
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()
        self.query_one("#spinner").visible = False

    async def on_input_submitted(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if not message.value:
            # Clear the results
            self.query_one("#results", MarkdownViewer).document.update("")
            return

        self.lookup_verse(message.value)

    @work(exclusive=True)
    async def lookup_verse(self, verse: str) -> None:
        self.query_one("#spinner").visible = True
        self.refresh()

        try:
            book_name, start_id, end_id = reference(verse)
        except GenericReferencePassingError as e:
            if isinstance(e, BookNotFoundError):
                self.update_markdown(f"# Error: could not find book in `{verse}`: {e}")
            elif isinstance(e, ReferenceStyleNotRecognisedError):
                self.update_markdown(
                    f"# Error: Reference style `{verse}` not understood: {e}"
                )
            else:
                raise e
            self.query_one("#spinner").visible = False
            return
        comms = commentaries(self.connection, book_name, start_id, end_id)

        if verse == self.query_one(Input).value:
            markdown_txt = (
                commentaries_to_markdown(comms) if comms else "# No results found!"
            )
            self.update_markdown(markdown_txt)

        self.query_one("#spinner").visible = False

    def update_markdown(self, markdown_txt: str):
        markdown_widget = self.query_one("#results", MarkdownViewer).document
        markdown_widget.update(markdown_txt)

    @on(Markdown.LinkClicked)
    def link_clicked(self, event: Markdown.LinkClicked):
        webbrowser.open(event.href)

    def action_toggle_toc(self) -> None:
        mkdown_viewer = self.query_one("#results", MarkdownViewer)
        mkdown_viewer.show_table_of_contents = not mkdown_viewer.show_table_of_contents
        if mkdown_viewer.show_table_of_contents:
            mkdown_viewer.table_of_contents.focus()
        else:
            mkdown_viewer.document.focus()
        self.refresh()


if __name__ == "__main__":
    app = CatenaVetus()
    app.run()
