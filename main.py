import sqlite3

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown

from commentaries_to_markdown import commentaries_to_markdown
from database_api.code_verse import reference
from database_api.sql import commentaries


class CatenaVetus(App):
    """View what the Church Fathers wrote about a verse"""

    CSS_PATH = "main.css"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.connection = sqlite3.connect("test.db")
        self.query_one(Input).focus()

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_verse(message.value)
        else:
            # Clear the results
            self.query_one("#results", Markdown).update("")

    @work(exclusive=True)
    async def lookup_verse(self, verse: str) -> None:
        try:
            book_name, start_id, end_id = reference(verse)
        except (KeyError, IndexError, ValueError):
            return
        comms = commentaries(self.connection, book_name, start_id, end_id)

        if verse == self.query_one(Input).value:
            if comms:
                markdown = commentaries_to_markdown(comms)
            else:
                markdown = "# No results found!"
            self.query_one("#results", Markdown).update(markdown)


if __name__ == '__main__':
    app = CatenaVetus()
    app.run()
