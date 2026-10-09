"""Practice menus: topic quizzes, fresh predictions, mixed sessions and work-count experiments."""

import random

from rich import box
from rich.table import Table
from rich.text import Text

from pydsa import progress, topics
from pydsa.content import quizzes
from pydsa.practice import challenges, experiments, quiz
from pydsa.ui import render
from pydsa.ui.console import ask, info, page, result, success
from pydsa.ui.menu import Menu, Nav, back_option


def run():
    menu = Menu("🧩 What would you like to practice?", [
        [("Mixed Quiz on Visited Topics", mixed_quiz),
         ("Predict a Result on a Visited Topic", mixed_prediction),
         ("Big-O Experiments", lambda: pick_experiment(experiments.EXPERIMENTS)),
         ("Browse Practice Topics", browse),
         ("View Progress", show_progress)],
        [back_option()],
    ])
    while menu.select() is not Nav.BACK:
        pass


def topic(topic_id):
    entry = topics.find(topic_id)
    options = [("Quiz", lambda: quiz.run(quizzes.for_topic(topic_id))),
               ("Predict the Result", lambda: prediction(topic_id))]
    available = experiments.for_topic(topic_id)
    if available:
        options.append(("Big-O Experiments", lambda: pick_experiment(available)))
    menu = Menu(f"🧩 Practice: {entry.title}", [options, [back_option()]])
    while menu.select() is not Nav.BACK:
        pass


def visited():
    return [entry.id for entry in topics.TOPICS if entry.id in progress.current.visited]


def mixed_quiz():
    ids = visited()
    if not ids:
        info("Visit a topic first, or choose Browse Practice Topics to start learning.")
        return
    rng = random.Random()
    # Rotate through topics before selecting a second question from any one topic.
    rng.shuffle(ids)
    banks = {topic: list(quizzes.for_topic(topic)) for topic in ids}
    for bank in banks.values():
        rng.shuffle(bank)
    selected = []
    prompts = set()
    while len(selected) < 10 and any(banks.values()):
        for topic_id in ids:
            if banks[topic_id]:
                question = banks[topic_id].pop()
                if question.prompt not in prompts:
                    selected.append(question)
                    prompts.add(question.prompt)
            if len(selected) == 10:
                break
    quiz.run(selected, rng)


def mixed_prediction():
    ids = visited()
    if not ids:
        info("Visit a topic first, or choose Browse Practice Topics to start learning.")
        return
    prediction(random.choice(ids))


def browse():
    menu = Menu("📚 Which practice topics do you want?", [
        [(title, lambda category=category: pick_topic(category)) for category, title in topics.CATEGORIES.items()],
        [back_option()],
    ])
    while menu.select() is not Nav.BACK:
        pass


def pick_topic(category):
    while True:
        def open_practice(topic_id):
            notice = progress.visit(topic_id)
            if notice:
                info(notice)
            topic(topic_id)
        menu = Menu("📖 Which topic would you like to practice?", [
            [(progress_label(entry), lambda entry=entry: open_practice(entry.id))
             for entry in topics.TOPICS if entry.category == category],
            [back_option()],
        ])
        if menu.select() is Nav.BACK:
            return


def progress_label(entry):
    return ("✓ " if entry.id in progress.current.visited else "") + ("↳ " if entry.parent else "") + entry.title


def prediction(topic_id):
    challenge = challenges.make(topic_id)
    info(f"Predict the result: {topics.find(topic_id).title}. This is fresh practice data.")
    challenge.draw()
    info("Enter a value, true/false, or a list such as [1, 2, 3]. Use quotes around words in a list.")
    answer = ask(challenge.prompt)
    if challenge.check(answer):
        success("Correct prediction.")
        notice = progress.record_challenge(topic_id)
        if notice:
            info(notice)
    else:
        info(f"The result is {challenge.answer!r}.")
    render.show(Text(challenge.explanation))


def pick_experiment(available):
    if not available:
        info("There are no work-count experiments for this topic.")
        return
    menu = Menu("📈 Which Big-O experiment would you like to run?", [
        [(experiment.name, lambda experiment=experiment: run_experiment(experiment)) for experiment in available],
        [back_option()],
    ])
    while menu.select() is not Nav.BACK:
        pass


def run_experiment(experiment):
    mode = Menu("How should the input be arranged?", [
        [(label, lambda mode=mode: mode) for mode, label in (
            ("random", "Random"), ("sorted", "Sorted"), ("reversed", "Reversed"))],
        [back_option()],
    ]).select()
    if mode in (None, Nav.BACK):
        return
    rows = experiments.measure(experiment, mode)
    notice = progress.visit(experiment.topic)
    if notice:
        info(notice)
    render.experiment(experiment, rows, mode)


def show_progress():
    result(progress.summary())
    table = Table(title="Your progress", box=box.SIMPLE_HEAVY, header_style="muted")
    table.add_column("Topic")
    table.add_column("Practice")
    for entry in topics.TOPICS:
        if entry.id not in progress.current.visited and entry.id not in progress.current.quizzes:
            continue
        score = progress.current.quizzes.get(entry.id)
        details = f"Best quiz {score.best:.0f}% · {score.attempts} attempts" if score else "No quiz yet"
        details += f" · {progress.current.challenges.get(entry.id, 0)} predictions solved"
        table.add_row(Text(progress_label(entry)), Text(details))
    page(table)
    info("Quiz averages use each topic's best completed first-round score. Retries do not raise saved scores. "
         "Settings can reset all progress.")
