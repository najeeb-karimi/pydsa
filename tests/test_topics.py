"""The topic registry behind the category menus and the --topic option."""

import re

from pydsa import topics


def test_ids_are_unique_and_command_line_friendly():
    ids = [topic.id for topic in topics.TOPICS]
    assert len(ids) == len(set(ids))
    assert all(re.fullmatch(r"[a-z]+(-[a-z]+)*", topic_id) for topic_id in ids)


def test_categories_and_parents():
    by_id = {topic.id: topic for topic in topics.TOPICS}
    for topic in topics.TOPICS:
        assert topic.category in topics.CATEGORIES
        assert callable(topic.open)
        if topic.parent is not None:
            parent = by_id[topic.parent]
            assert parent.parent is None and parent.category == topic.category


def test_category_menus():
    assert [topic.title for topic in topics.listed("linear")] == ["Array", "Stack", "Queue", "Deque", "Linked List"]
    assert [topic.title for topic in topics.listed("algorithms")] == ["Sorting", "Searching", "Graph Algorithms"]
    assert len(topics.listed("non-linear")) == 6


def test_find():
    assert topics.find("AVL-Tree").title == "AVL Tree"
    assert topics.find("bubble-sort").parent == "sorting"
    assert topics.find("nope") is None
