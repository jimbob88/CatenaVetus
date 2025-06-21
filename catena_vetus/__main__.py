from pathlib import Path
import sqlite3
import webbrowser

from textual import work, on
from textual.app import App, ComposeResult
from textual.widgets import Input, Header, Footer

from catena_vetus.commentaries_to_markdown import commentaries_to_markdown
from catena_vetus.custom_markdown import SpeedyMarkdown, SpeedyMarkdownViewer
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
        ("d", "toggle_dark", "Toggle dark mode"),
        ("t", "toggle_toc", "Toggle Table of Contents"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search for a verse")

        # with VerticalScroll(id="results-container"):
        yield SpinnerWidget(id="spinner")
        yield SpeedyMarkdownViewer(id="results", show_table_of_contents=False)
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
        if message.value:
            self.lookup_verse(message.value)
        else:
            # Clear the results
            self.query_one("#results", SpeedyMarkdownViewer).document.update("")

    # async needs to be removed from this function, but currently that is not working in textual
    @work(exclusive=True)
    def lookup_verse(self, verse: str) -> None:
        self.query_one("#spinner").visible = True
        self.refresh()

        try:
            book_name, start_id, end_id = reference(verse)
        except GenericReferencePassingError as e:
            if isinstance(e, BookNotFoundError):
                self.threaded_update_markdown(
                    f"# Error: could not find book in `{verse}`: {e}"
                )
            elif isinstance(e, ReferenceStyleNotRecognisedError):
                self.threaded_update_markdown(
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
            self.threaded_update_markdown(markdown_txt)

        self.query_one("#spinner").visible = False

    def threaded_update_markdown(self, markdown_txt: str):
        markdown_widget = self.query_one("#results", SpeedyMarkdownViewer).document
        output = markdown_widget.generate_markdown_objs(markdown_txt)
        self.call_from_thread(markdown_widget.mnt, output)

    @on(SpeedyMarkdown.LinkClicked)
    def link_clicked(self, event: SpeedyMarkdown.LinkClicked):
        webbrowser.open(event.href)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_toggle_toc(self) -> None:
        mkdown_viewer = self.query_one("#results", SpeedyMarkdownViewer)
        mkdown_viewer.show_table_of_contents = not mkdown_viewer.show_table_of_contents
        if mkdown_viewer.show_table_of_contents:
            mkdown_viewer.table_of_contents.focus()
        else:
            mkdown_viewer.document.focus()
        self.refresh()


if __name__ == "__main__":
    app = CatenaVetus()
    app.run()
