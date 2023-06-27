import sqlite3

from textual import work, on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.validation import Function
from textual.widgets import Input, Markdown, Pretty, Header

from commentaries_to_markdown import commentaries_to_markdown
from database_api.code_verse import reference
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
            yield Markdown(id="results")

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
            self.query_one("#results", Markdown).update("")

    # async needs to be removed from this function, but currently that is not working in textual
    @work(exclusive=True)
    async def lookup_verse(self, verse: str) -> None:
        self.query_one("#spinner").visible = True
        self.refresh()
        book_name, start_id, end_id = reference(verse)
        comms = commentaries(self.connection, book_name, start_id, end_id)

        if verse == self.query_one(Input).value:
            if comms:
                markdown = commentaries_to_markdown(comms)
            else:
                markdown = "# No results found!"
            self.query_one("#results", Markdown).update(markdown)
        self.query_one("#spinner").visible = False


if __name__ == '__main__':
    app = CatenaVetus()
    app.run()
