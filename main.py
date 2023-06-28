import sqlite3
import webbrowser

from textual import work, on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Header

from commentaries_to_markdown import commentaries_to_markdown
from custom_markdown import SpeedyMarkdown
from database_api.code_verse import reference
from database_api.errors import GenericReferencePassingError, BookNotFoundError, ReferenceStyleNotRecognisedError
from database_api.sql import commentaries
from spinner import SpinnerWidget


class CatenaVetus(App):
    """View what the Church Fathers wrote about a verse"""

    CSS_PATH = "main.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search for a verse")
        with VerticalScroll(id="results-container"):
            yield SpinnerWidget(id="spinner")
            yield SpeedyMarkdown(id="results")

    def on_mount(self) -> None:
        """Called when app starts."""

        # see: https://ricardoanderegg.com/posts/python-sqlite-thread-safety/
        self.connection = sqlite3.connect("test.db", check_same_thread=False)
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()
        self.query_one("#spinner").visible = False

    async def on_input_submitted(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_verse(message.value)
        else:
            # Clear the results
            self.query_one("#results", SpeedyMarkdown).update("")

    # async needs to be removed from this function, but currently that is not working in textual
    @work(exclusive=True)
    def lookup_verse(self, verse: str) -> None:
        self.query_one("#spinner").visible = True
        self.refresh()

        try:
            book_name, start_id, end_id = reference(verse)
        except GenericReferencePassingError as e:
            if isinstance(e, BookNotFoundError):
                self.threaded_update_markdown(f"# Error: could not find book in `{verse}`: {e}")
            elif isinstance(e, ReferenceStyleNotRecognisedError):
                self.threaded_update_markdown(f"# Error: Reference style `{verse}` not understood: {e}")
            else:
                raise e
            self.query_one("#spinner").visible = False
            return
        comms = commentaries(self.connection, book_name, start_id, end_id)

        if verse == self.query_one(Input).value:
            markdown_txt = commentaries_to_markdown(comms) if comms else "# No results found!"
            self.threaded_update_markdown(markdown_txt)

        self.query_one("#spinner").visible = False

    def threaded_update_markdown(self, markdown_txt: str):
        markdown_widget = self.query_one("#results", SpeedyMarkdown)
        output = markdown_widget.generate_markdown_objs(markdown_txt)
        self.call_from_thread(markdown_widget.mnt, output)

    @on(SpeedyMarkdown.LinkClicked)
    def link_clicked(self, event: SpeedyMarkdown.LinkClicked):
        webbrowser.open(event.href)


if __name__ == '__main__':
    app = CatenaVetus()
    app.run()
