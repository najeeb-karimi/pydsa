"""Quiz completeness, shuffled choices, completed scoring and retries."""

import random

import pytest

from pydsa import progress, topics
from pydsa.content import quizzes
from pydsa.practice import quiz
from pydsa.ui.console import BackRequested


def test_every_topic_has_five_valid_questions():
    ids = {topic.id for topic in topics.TOPICS}
    assert {question.topic for question in quizzes.QUESTIONS} == ids
    assert len({question.id for question in quizzes.QUESTIONS}) == len(quizzes.QUESTIONS)
    for topic in ids:
        questions = quizzes.for_topic(topic)
        assert len(questions) >= 5
        assert len({question.prompt for question in questions}) == len(questions)
        for question in questions:
            assert question.prompt and question.explanation
            assert len(question.choices) == 4 and len(set(question.choices)) == 4
            assert all(question.choices) and 0 <= question.answer < 4


def test_shuffled_choice_preserves_answer(monkeypatch, capsys):
    question = quizzes.for_topic("stack")[0]
    letters = set()
    def answer(prompt, groups):
        code = next(code for code, text in groups[0] if text == question.choices[question.answer])
        letters.add(code)
        return code
    monkeypatch.setattr(quiz, "ask_code", answer)
    for seed in range(20):
        assert quiz.ask_question(question, random.Random(seed))
    assert letters == set("abcd")
    assert question.explanation in capsys.readouterr().out


def test_mixed_scores_and_retry_are_saved_once(monkeypatch, capsys):
    questions = [quizzes.for_topic("stack")[0], quizzes.for_topic("queue")[0]]
    answers = iter([True, False, True])
    monkeypatch.setattr(quiz, "ask_question", lambda *args: next(answers))
    monkeypatch.setattr(quiz, "ask_code", lambda *args: "1")
    class KeepOrder:
        def shuffle(self, values):
            pass
    session = quiz.run(questions, KeepOrder())
    assert (session.correct, session.total) == (1, 2)
    assert session.missed == (questions[1],)
    assert progress.current.quizzes["stack"] == progress.QuizScore(100, 1)
    assert progress.current.quizzes["queue"] == progress.QuizScore(0, 1)
    assert "Retry score: 1/1" in capsys.readouterr().out


def test_cancelled_quiz_does_not_save_a_partial_score(monkeypatch):
    questions = quizzes.for_topic("stack")
    count = 0
    def answer(*args):
        nonlocal count
        count += 1
        if count == 2:
            raise BackRequested
        return True
    monkeypatch.setattr(quiz, "ask_question", answer)
    with pytest.raises(BackRequested):
        quiz.run(questions)
    assert not progress.current.quizzes and not progress.path().exists()


def test_wrong_answer_explains_and_empty_quiz_has_no_score(monkeypatch, capsys):
    question = quizzes.for_topic("stack")[0]
    monkeypatch.setattr(quiz, "ask_code", lambda prompt, groups: next(
        code for code, choice in groups[0] if choice != question.choices[question.answer]))
    assert not quiz.ask_question(question, random.Random(1))
    assert question.choices[question.answer] in capsys.readouterr().out
    assert quiz.run([]) == quiz.QuizResult(0, 0, ())
    assert not progress.current.quizzes
