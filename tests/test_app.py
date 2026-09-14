"""The command-line options, shortcuts, clean exits, settings screen, intro and learning tools."""

import json

import pytest

from pydsa import __version__, app, settings, topics
from pydsa.settings import Settings
from pydsa.ui.console import console


# ---------------------------------------------------------------------------
# Command-line options
# ---------------------------------------------------------------------------

def test_version(capsys):
    with pytest.raises(SystemExit) as stop:
        app.run(["--version"])
    assert stop.value.code == 0
    assert f"PyDSA {__version__}" in capsys.readouterr().out


def test_list_topics(capsys):
    app.run(["--list-topics"])
    out = capsys.readouterr().out
    assert "avl-tree" in out and "dijkstra" in out and "↳ AVL Tree" in out
    assert "pydsa --topic ID" in out
    assert "Goodbye" not in out


def test_unknown_topics_are_rejected_with_a_suggestion(capsys):
    with pytest.raises(SystemExit) as stop:
        app.run(["--topic", "stak"])
    assert stop.value.code == 2
    err = capsys.readouterr().err
    assert "unknown topic 'stak'" in err and "Did you mean stack" in err


def test_topic_opens_directly_then_the_main_menu_follows(play):
    out = play("2", "10", "0", argv=["--topic", "Stack"])  # Use the example, Main Menu, Exit
    assert "Loaded the example stack." in out
    assert "Changelog" not in out
    assert "📂 What do you want to learn?" in out

    out = play("2", "0", argv=["--topic", "avl-tree"])  # Skips the choice between BST and AVL
    assert "🧪 AVL Tree" in out
    assert "Loaded the example AVL tree." in out
    assert "Which type of tree do you want?" not in out


@pytest.mark.parametrize("topic_id", [topic.id for topic in topics.TOPICS])
def test_every_topic_opens_and_goes_back(play, topic_id):
    out = play("0", "0", argv=["--topic", topic_id])
    assert "📂 What do you want to learn?" in out
    assert "Goodbye!" in out


def test_no_color_option(play):
    play("0", argv=["--no-color"])
    assert console.no_color


def test_reset_settings(play):
    settings.path().parent.mkdir(parents=True)
    settings.path().write_text('{"detail": "detailed"}', encoding="utf-8")
    out = play("0", argv=["--reset-settings"])
    assert "Restored the default settings." in out
    assert json.loads(settings.path().read_text(encoding="utf-8"))["detail"] == "brief"


# ---------------------------------------------------------------------------
# Shortcuts and clean exits
# ---------------------------------------------------------------------------

def test_quit_shortcuts(play):
    assert "Goodbye!" in play("q")
    assert "Goodbye!" in play("1", "2", "1", ":q")  # At a typed-value prompt


@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError], ids=["ctrl-c", "ctrl-d"])
def test_ctrl_c_and_ctrl_d_exit_cleanly(play, interrupt):
    out = play("1", "2", "2", interrupt)
    assert "Loaded the example stack." in out
    assert "Goodbye!" in out


def test_help_shortcuts(play):
    out = play("h", "1", "2", "1", ":h", "3", "0")
    assert out.count("❓ Help") == 2
    assert "You're at: 📂 What do you want to learn?" in out
    assert "You're at: ↔️ How many items should the stack be able to hold?" in out
    assert "Created an empty stack that holds up to 3 items." in out


def test_back_shortcuts(play):
    out = play(
        "b",  # Nothing to go back to from the main menu
        "1", "2", "2",  # Linear > Stack > Use the example
        "2", ":b",  # Push, then cancel at the prompt
        "b",  # Back to the linear topics
        "b", "0",  # Back to the main menu, then exit
    )
    assert "You're already at the main menu" in out
    assert "Cancelled." in out and "Pushed" not in out
    assert out.count("🏁 Which linear data structure do you want to learn?") == 2


def test_operation_menus_show_their_title_once(play):
    out = play("1", "2", "2", "7", "5", "0")
    assert out.count("⚔️ What do you want to do with the stack?") == 1
    assert "The stack holds 2 of 5 items." in out


def test_full_intro_shows_once_per_session(play):
    out = play("1", "2", "2", "10", "0")  # Linear > Stack > Use the example > Main Menu > Exit
    assert out.count("Changelog") == 1
    assert "type h in any menu for help" in out


# ---------------------------------------------------------------------------
# Guides and learning tools
# ---------------------------------------------------------------------------

def test_topics_open_with_a_summary_and_read_the_guide_shows_it_all(play):
    out = play("1", "2", "2", "1", "0")  # Linear > Stack > Use the example > Read the Guide > Exit
    assert "🎯 Stack" in out and "Choose Read the Guide" in out
    assert out.count("What it is") == 1  # Only in the guide
    assert "📖 Stack" in out


def test_read_the_guide_lets_you_pick_a_guide(play):
    out = play("2", "1", "1", "2", "1", "2", "0")  # Non-linear > Tree > BST > Use the example > Read the Guide > Tree
    assert "🧪 Binary Search Tree (BST)" in out
    assert "📖 Which guide do you want to read?" in out
    assert "📖 Tree" in out


def test_algorithm_explanations_follow_the_detail_setting(play):
    out = play("3", "1", "3", "2", "1", "0")  # Algorithms > Sorting > Use the example > Bubble Sort, ascending
    assert "ℹ️ How Bubble Sort Works" in out and "set Explanations to Detailed" in out

    settings.save(Settings(detail="detailed"))  # Saved, because every session loads the settings file
    out = play("3", "1", "3", "2", "1", "0")
    assert "If a whole pass makes no swaps" in out and "set Explanations to Detailed" not in out


def test_learning_tools(play):
    out = play(
        "4",  # Learning Tools
        "1",  # Overview
        "2", "3", "18", "0", "0",  # Browse the Guides > Algorithms > Dijkstra, then back twice
        "3", "1",  # Glossary > List All Terms
        "2", "amort", "2", "vertx", "2", "zzz", "2", " ", "2", ":b",  # Look Up a Term
        "0",
        "4",  # Which Data Structure Should I Use?
        "0", "0",
    )
    assert "Learning Tools" in out
    assert "  1) Overview\n" in out and "🏗️ Data Structures and Algorithms" in out
    assert "↳ Bubble Sort" in out and "📖 Dijkstra's Algorithm" in out
    assert "📘 Glossary" in out and "Union by rank" in out
    assert "Found 1 term matching 'amort'." in out and "Amortized time" in out
    assert "No term matches 'vertx'. Did you mean Vertex (plural: vertices)?" in out
    assert "No term matches 'zzz'. Choose List All Terms to see every term." in out
    assert "Type at least one letter to look up." in out
    assert "Cancelled." in out
    assert "🧭 Which Data Structure Should I Use?" in out
    assert "Goodbye!" in out


# ---------------------------------------------------------------------------
# Settings screen
# ---------------------------------------------------------------------------

def test_settings_are_saved(play):
    out = play(
        "5",  # Settings
        "1", "2",  # Explanations > Detailed
        "3", "2",  # Clear the Screen > Off
        "0", "0",
    )
    assert out.count("Saved your settings.") == 2
    assert "Explanations: Detailed" in out
    saved = json.loads(settings.path().read_text(encoding="utf-8"))
    assert saved == {"version": settings.VERSION, "detail": "detailed", "steps": "ask", "colors": True,
                     "clear_screen": False, "intro": "once"}


def test_intro_every_time(play):
    out = play("5", "4", "2", "0", "1", "2", "2", "10", "0")
    assert out.count("Changelog") == 2


def test_restore_defaults(play):
    settings.save(Settings(detail="detailed", colors=False))
    out = play("5", "5", "1", "0", "0")
    assert "Explanations: Brief" in out
    assert json.loads(settings.path().read_text(encoding="utf-8"))["colors"] is True


def test_settings_that_cannot_be_saved_last_for_the_session(play, monkeypatch, tmp_path):
    blocker = tmp_path / "not-a-folder"
    blocker.write_text("", encoding="utf-8")
    monkeypatch.setenv("PYDSA_HOME", str(blocker))
    out = play("5", "1", "2", "0", "0")
    assert "Couldn't save the settings" in out
    assert settings.current.detail == "detailed"
