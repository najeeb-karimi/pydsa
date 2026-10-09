"""Question types and quiz sessions, with shuffled answers and a separate retry round."""

import random
from dataclasses import dataclass

from rich.text import Text

from pydsa import progress
from pydsa.ui.console import ask_code, console, info, result, success


@dataclass(frozen=True)
class Question:
    id: str
    topic: str
    prompt: str
    choices: tuple[str, ...]
    answer: int
    explanation: str


@dataclass(frozen=True)
class QuizResult:
    correct: int
    total: int
    missed: tuple[Question, ...]


def ask_question(question, rng):
    """Shuffle indexes rather than answer text, so the correct answer follows its choice."""
    order = list(range(len(question.choices)))
    rng.shuffle(order)
    code = ask_code(question.prompt, [[(chr(97 + i), question.choices[index]) for i, index in enumerate(order)]])
    correct = order[ord(code) - 97] == question.answer
    if correct:
        success("Correct.")
    else:
        info(f"The correct answer is: {question.choices[question.answer]}")
    console.print(Text(question.explanation))
    return correct


def run(questions, rng=None):
    """Record only a completed first round; retries teach missed material without inflating its score."""
    rng = rng or random.Random()
    questions = list(questions)
    if not questions:
        info("No questions are available for this session yet.")
        return QuizResult(0, 0, ())
    rng.shuffle(questions)
    missed, scores = [], {}
    for number, question in enumerate(questions, 1):
        result(f"Question {number} of {len(questions)}")
        correct = ask_question(question, rng)
        score = scores.setdefault(question.topic, [0, 0])
        score[0] += correct
        score[1] += 1
        if not correct:
            missed.append(question)
    session = QuizResult(len(questions) - len(missed), len(questions), tuple(missed))
    result(f"Quiz score: {session.correct}/{session.total} ({100 * session.correct / session.total:.0f}%).")
    notices = {progress.record_quiz(topic, *score) for topic, score in scores.items()}
    for notice in notices - {None}:
        info(notice)
    if missed:
        choice = ask_code("Retry the questions you missed?", [[("1", "Yes, retry"), ("0", "No, finish")]])
        if choice == "1":
            retry = sum(ask_question(question, rng) for question in missed)
            result(f"Retry score: {retry}/{len(missed)}. Your saved score is from the first round.")
    return session
