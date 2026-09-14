"""Guides, the glossary and the other Learning Tools documents: complete, consistent and packaged."""

import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from pydsa import topics
from pydsa.content import complexity, registry

TOPIC_IDS = [topic.id for topic in topics.TOPICS]


def all_documents():
    """Return the Markdown text of every topic guide and document, by ID or name."""
    texts = {guide_id: registry.read(paths[0]) for guide_id, paths in registry.locations().items()}
    texts.update({name: registry.read(f"{name}.md") for name in registry.DOCUMENTS})
    return texts


def test_every_topic_has_exactly_one_guide():
    locations = registry.locations()
    assert sorted(locations) == sorted(TOPIC_IDS)
    for topic in topics.TOPICS:
        folder = "algorithms/" if topic.category == "algorithms" else ""
        assert locations[topic.id] == [f"{folder}{topic.id}.md"]


@pytest.mark.parametrize("topic_id", TOPIC_IDS)
def test_guides_have_a_summary_and_every_section(topic_id):
    guide = registry.guide(topic_id)
    assert registry.problems(guide) == []
    sentences = re.findall(r"[.!?](?=\s|$)", guide.summary)
    assert 1 <= len(sentences) <= 3, guide.summary


def test_problems_are_reported():
    broken = registry.parse("broken", "Stack\n\n## What it is\n\nA pile.\n\n## How it works\n")
    found = registry.problems(broken)
    assert "the first line must be a '# Title'" in found
    assert "a '> summary' must follow the title" in found
    assert any(problem.startswith("the sections must be") for problem in found)
    assert "the How it works section is empty" in found


def test_guides_leave_big_o_to_the_complexity_tables():
    for name, text in all_documents().items():
        if name != "glossary":  # The glossary explains Big O notation itself
            assert "O(" not in text, name


def test_bold_is_kept_for_glossary_terms():
    for name, text in all_documents().items():
        assert "**" not in text, name


def test_glossary_links_name_real_terms():
    slugs = {term.slug for term in registry.glossary()}
    for name, text in all_documents().items():
        for slug in registry.glossary_links(text):
            assert slug in slugs, f"{name} links to a glossary term that doesn't exist: {slug}"


def test_glossary():
    terms = registry.glossary()
    assert len(terms) >= 50
    assert len({term.slug for term in terms}) == len(terms)
    assert [term.name.casefold() for term in terms] == sorted(term.name.casefold() for term in terms)
    assert all(term.definition for term in terms)
    assert [term.name for term in registry.find_terms(" AMORT ")] == ["Amortized time"]
    assert registry.find_terms("bfs")[0].slug == "breadth-first-search"
    assert registry.slug("Vertex (plural: vertices)") == "vertex"


def test_documents():
    for name in ("overview", "choosing"):
        document = registry.document(name)
        assert document.title and document.summary and document.sections
    ids = re.findall(r"`([a-z]+(?:-[a-z]+)*)`", registry.read("choosing.md"))
    assert len(ids) >= 15 and set(ids) <= set(TOPIC_IDS)


def test_glossary_links_become_bold_text():
    assert registry.markdown("A [node](glossary:node) has [links](glossary:link).") == "A **node** has **links**."


def test_every_topic_has_complexity_tables():
    assert set(complexity.TOPIC_TABLES) == set(TOPIC_IDS)


def test_the_wheel_includes_every_guide(tmp_path):
    pytest.importorskip("setuptools", minversion="70.1")  # Builds wheels without the separate wheel package
    root = Path(__file__).resolve().parents[1]
    project = tmp_path / "project"
    shutil.copytree(root / "pydsa", project / "pydsa", ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("pyproject.toml", "README.md"):
        shutil.copy(root / name, project / name)
    subprocess.run(
        [sys.executable, "-m", "pip", "wheel", str(project), "--no-deps", "--no-build-isolation", "-q", "-w", str(tmp_path / "dist")],
        check=True, capture_output=True,
    )
    wheel, = (tmp_path / "dist").glob("pydsa-*.whl")
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
    expected = {f"pydsa/content/guides/{path}" for paths in registry.locations().values() for path in paths}
    expected |= {f"pydsa/content/guides/{name}.md" for name in registry.DOCUMENTS}
    assert expected <= names
