"""Guides, the glossary and the other Markdown documents, loaded from the package data in content/guides.

Every guide starts with a "# Title" line and a "> summary" quote. Topic guides then have the fixed SECTIONS,
in order, while documents such as the overview can use any "## " sections. A glossary term is linked by
name as [text](glossary:slug), which renders as bold text.
"""

import re
from functools import cache
from importlib.resources import files
from typing import NamedTuple

SECTIONS = ("What it is", "How it works", "Real-life analogy", "When to use it", "When to avoid it", "In PyDSA")
DOCUMENTS = ("overview", "glossary", "choosing")  # Guides folder files that aren't topic guides
ALGORITHMS = "algorithms"  # The folder holding the algorithm guides

GLOSSARY_LINK = re.compile(r"\[([^\]]+)\]\(glossary:([^)]*)\)")


class Guide(NamedTuple):
    """A parsed guide: its title, its summary and its (heading, body) sections, all as Markdown."""

    id: str
    title: str
    summary: str
    sections: tuple

    def section(self, heading):
        """Return the body of the section with the given heading, or an empty string."""
        return next((body for name, body in self.sections if name == heading), "")

    def body(self):
        """Return the summary and every section as one Markdown text, without the title."""
        parts = [f"> {self.summary}"] + [f"## {heading}\n\n{body}" for heading, body in self.sections]
        return "\n\n".join(parts)


class Term(NamedTuple):
    """A glossary entry: its heading, the slug guides link to and its definition."""

    name: str
    slug: str
    definition: str


def _guides():
    return files("pydsa.content") / "guides"


@cache
def locations():
    """Map the ID of every topic guide to the path of its file, relative to the guides folder."""
    found = {}
    for folder in (None, ALGORITHMS):
        directory = _guides() / folder if folder else _guides()
        for item in sorted(directory.iterdir(), key=lambda item: item.name):
            guide_id = item.name.removesuffix(".md")
            if item.name.endswith(".md") and (folder or guide_id not in DOCUMENTS):
                found.setdefault(guide_id, []).append(f"{folder}/{item.name}" if folder else item.name)
    return found


def read(path):
    """Return the text of a file in the guides folder, such as "stack.md" or "algorithms/bubble-sort.md"."""
    return (_guides() / path).read_text(encoding="utf-8")


def parse(guide_id, text):
    """Parse the Markdown text of a guide or document."""
    lines = text.strip().splitlines()
    title = lines[0].removeprefix("# ").strip() if lines and lines[0].startswith("# ") else ""
    position = 1
    while position < len(lines) and not lines[position].strip():
        position += 1
    summary = []
    while position < len(lines) and lines[position].startswith(">"):
        summary.append(lines[position].removeprefix(">").strip())
        position += 1

    sections = []
    for line in lines[position:]:
        if line.startswith("## "):
            sections.append((line.removeprefix("## ").strip(), []))
        elif sections:
            sections[-1][1].append(line)
    return Guide(guide_id, title, " ".join(summary), tuple((heading, "\n".join(body).strip()) for heading, body in sections))


@cache
def guide(guide_id):
    """Return the topic guide with the given ID."""
    return parse(guide_id, read(locations()[guide_id][0]))


@cache
def document(name):
    """Return one of the DOCUMENTS, such as "overview"."""
    return parse(name, read(f"{name}.md"))


def problems(parsed):
    """Return what's wrong with a topic guide's layout, as a list of messages (empty if nothing is)."""
    found = []
    if not parsed.title:
        found.append("the first line must be a '# Title'")
    if not parsed.summary:
        found.append("a '> summary' must follow the title")
    headings = tuple(heading for heading, _ in parsed.sections)
    if headings != SECTIONS:
        found.append(f"the sections must be {', '.join(SECTIONS)}, but they are {', '.join(headings) or 'missing'}")
    found += [f"the {heading} section is empty" for heading, body in parsed.sections if not body]
    return found


def slug(name):
    """Return the slug a glossary heading is linked by: lowercase, without a trailing "(...)" part."""
    name = re.sub(r"\s*\(.*\)$", "", name)
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


@cache
def glossary():
    """Return every glossary term from A to Z."""
    terms = [Term(heading, slug(heading), body) for heading, body in document("glossary").sections]
    return sorted(terms, key=lambda term: term.name.casefold())


def find_terms(query):
    """Return the glossary terms whose name contains query, ignoring letter case."""
    query = query.strip().casefold()
    return [term for term in glossary() if query in term.name.casefold()]


def glossary_links(text):
    """Return the slugs of the glossary terms text links to."""
    return [link_slug for _, link_slug in GLOSSARY_LINK.findall(text)]


def markdown(text):
    """Turn glossary links into bold text, ready for rich's Markdown renderer."""
    return GLOSSARY_LINK.sub(r"**\1**", text)
