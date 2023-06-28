from markdown_it import MarkdownIt
from rich.style import Style
from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Markdown
from textual.widgets._markdown import MarkdownBlock, TableOfContentsType, HEADINGS, MarkdownHorizontalRule, MarkdownParagraph, MarkdownBlockQuote, \
    MarkdownBulletList, MarkdownOrderedList, MarkdownOrderedListItem, MarkdownUnorderedListItem, MarkdownTable, MarkdownTBody, MarkdownTHead, \
    MarkdownTR, MarkdownTH, MarkdownTD, MarkdownFence, MarkdownViewer, MarkdownTableOfContents


class SpeedyMarkdown(Markdown):
    """A version of the markdown object that is thread-safe for updating

    This works by allowing the end-user to generate the markdown objects within the thread, then use the main thread to update the screen. This
    has a massive advantage when using _very_ large markdown files because it allows the screen to stay updating whilst markdown is being generated.
    There is a small hiccup whilst the screen is repainted, but it is far better than before.
    """

    def generate_markdown_objs(self, markdown: str):
        output: list[MarkdownBlock] = []
        stack: list[MarkdownBlock] = []
        parser = (
            MarkdownIt("gfm-like")
            if self._parser_factory is None
            else self._parser_factory()
        )

        content = Text()
        block_id: int = 0

        table_of_contents: TableOfContentsType = []

        for token in parser.parse(markdown):
            if token.type == "heading_open":
                block_id += 1
                stack.append(HEADINGS[token.tag](self, id=f"block{block_id}"))
            elif token.type == "hr":
                output.append(MarkdownHorizontalRule(self))
            elif token.type == "paragraph_open":
                stack.append(MarkdownParagraph(self))
            elif token.type == "blockquote_open":
                stack.append(MarkdownBlockQuote(self))
            elif token.type == "bullet_list_open":
                stack.append(MarkdownBulletList(self))
            elif token.type == "ordered_list_open":
                stack.append(MarkdownOrderedList(self))
            elif token.type == "list_item_open":
                if token.info:
                    stack.append(MarkdownOrderedListItem(self, token.info))
                else:
                    item_count = sum(
                        isinstance(block, MarkdownUnorderedListItem)
                        for block in stack
                    )
                    stack.append(
                        MarkdownUnorderedListItem(
                            self,
                            self.BULLETS[item_count % len(self.BULLETS)],
                        )
                    )

            elif token.type == "table_open":
                stack.append(MarkdownTable(self))
            elif token.type == "tbody_open":
                stack.append(MarkdownTBody(self))
            elif token.type == "thead_open":
                stack.append(MarkdownTHead(self))
            elif token.type == "tr_open":
                stack.append(MarkdownTR(self))
            elif token.type == "th_open":
                stack.append(MarkdownTH(self))
            elif token.type == "td_open":
                stack.append(MarkdownTD(self))
            elif token.type.endswith("_close"):
                block = stack.pop()
                if token.type == "heading_close":
                    heading = block._text.plain
                    level = int(token.tag[1:])
                    table_of_contents.append((level, heading, block.id))
                if stack:
                    stack[-1]._blocks.append(block)
                else:
                    output.append(block)
            elif token.type == "inline":
                style_stack: list[Style] = [Style()]
                content = Text()
                if token.children:
                    for child in token.children:
                        if child.type == "text":
                            content.append(child.content, style_stack[-1])
                        if child.type == "hardbreak":
                            content.append("\n")
                        if child.type == "softbreak":
                            content.append(" ")
                        elif child.type == "code_inline":
                            content.append(
                                child.content,
                                style_stack[-1]
                                + self.get_component_rich_style(
                                    "code_inline", partial=True
                                ),
                            )
                        elif child.type == "em_open":
                            style_stack.append(
                                style_stack[-1]
                                + self.get_component_rich_style("em", partial=True)
                            )
                        elif child.type == "strong_open":
                            style_stack.append(
                                style_stack[-1]
                                + self.get_component_rich_style("strong", partial=True)
                            )
                        elif child.type == "s_open":
                            style_stack.append(
                                style_stack[-1]
                                + self.get_component_rich_style("s", partial=True)
                            )
                        elif child.type == "link_open":
                            href = child.attrs.get("href", "")
                            action = f"link({href!r})"
                            style_stack.append(
                                style_stack[-1] + Style.from_meta({"@click": action})
                            )
                        elif child.type == "image":
                            href = child.attrs.get("src", "")
                            alt = child.attrs.get("alt", "")

                            action = f"link({href!r})"
                            style_stack.append(
                                style_stack[-1] + Style.from_meta({"@click": action})
                            )

                            content.append("🖼  ", style_stack[-1])
                            if alt:
                                content.append(f"({alt})", style_stack[-1])
                            if child.children is not None:
                                for grandchild in child.children:
                                    content.append(grandchild.content, style_stack[-1])

                            style_stack.pop()

                        elif child.type.endswith("_close"):
                            style_stack.pop()

                stack[-1].set_content(content)
            elif token.type in ("fence", "code_block"):
                (stack[-1]._blocks if stack else output).append(
                    MarkdownFence(
                        self,
                        token.content.rstrip(),
                        token.info,
                    )
                )
            else:
                external = self.unhandled_token(token)
                if external is not None:
                    (stack[-1]._blocks if stack else output).append(external)

        self.post_message(Markdown.TableOfContentsUpdated(self, table_of_contents))
        return output

    def mnt(self, output):
        with self.app.batch_update():
            self.query("MarkdownBlock").remove()
            self.mount_all(output)


class SpeedyMarkdownViewer(MarkdownViewer):
    @property
    def document(self) -> SpeedyMarkdown:
        """The SpeedyMarkdown document object."""
        return self.query_one(SpeedyMarkdown)

    def compose(self) -> ComposeResult:
        markdown = SpeedyMarkdown(parser_factory=self._parser_factory)
        yield MarkdownTableOfContents(markdown)
        yield markdown
