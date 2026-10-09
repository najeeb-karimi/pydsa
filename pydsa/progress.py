"""Learning progress, saved next to the settings and kept in memory if saving fails."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from pydsa import settings

VERSION = 1


@dataclass
class QuizScore:
    best: float = 0.0
    attempts: int = 0


@dataclass
class Progress:
    visited: dict[str, str] = field(default_factory=dict)
    quizzes: dict[str, QuizScore] = field(default_factory=dict)
    challenges: dict[str, int] = field(default_factory=dict)


current = Progress()


def path():
    return settings.home() / "progress.json"


def _count(value):
    return type(value) is int and value >= 0


def load():
    """Return saved progress and a notice; unknown versions and corrupt records are ignored."""
    from pydsa.topics import TOPICS

    known = {topic.id for topic in TOPICS}
    try:
        data = json.loads(path().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return Progress(), None
    except (OSError, ValueError):
        return Progress(), "Couldn't read your progress, so this session starts with empty progress."
    if not isinstance(data, dict) or type(data.get("version")) is not int or data["version"] != VERSION:
        return Progress(), "Your progress file uses an unsupported format, so this session starts with empty progress."
    result = Progress()
    invalid = False
    for name in ("visited", "quizzes", "challenges"):
        records = data.get(name, {})
        if not isinstance(records, dict):
            invalid = True
            continue
        for topic, record in records.items():
            if topic not in known:
                continue
            if name == "visited":
                try:
                    valid = isinstance(record, str) and datetime.fromisoformat(record).tzinfo is not None
                except ValueError:
                    valid = False
                if valid:
                    result.visited[topic] = record
            elif name == "quizzes":
                valid = (isinstance(record, dict) and _count(record.get("attempts"))
                         and type(record.get("best")) in (int, float)
                         and 0 <= record["best"] <= 100)
                if valid:
                    result.quizzes[topic] = QuizScore(float(record["best"]), record["attempts"])
            else:
                valid = _count(record)
                if valid:
                    result.challenges[topic] = record
            invalid |= not valid
    return result, "Some invalid progress records were ignored." if invalid else None


def load_current():
    global current
    current, notice = load()
    return notice


def save():
    """Write a complete file before replacing the old one; return a notice on failure."""
    file = path()
    temporary = file.with_suffix(".tmp")
    try:
        file.parent.mkdir(parents=True, exist_ok=True)
        temporary.write_text(json.dumps({"version": VERSION, **asdict(current)}, indent=2) + "\n", encoding="utf-8")
        temporary.replace(file)
    except OSError:
        return "Couldn't save your progress, so these changes will only last until you quit."
    return None


def visit(topic):
    """Remember a topic and its parent menus using stable registry IDs."""
    from pydsa.topics import find

    timestamp = datetime.now(timezone.utc).isoformat()
    entry = find(topic)
    while entry is not None:
        current.visited[entry.id] = timestamp
        entry = find(entry.parent) if entry.parent else None
    return save()


def record_quiz(topic, correct, total):
    if type(correct) is not int or type(total) is not int or not 0 <= correct <= total or total < 1:
        raise ValueError("A quiz score needs a positive total and a correct count between zero and the total.")
    score = current.quizzes.setdefault(topic, QuizScore())
    score.best = max(score.best, 100 * correct / total)
    score.attempts += 1
    return save()


def record_challenge(topic):
    current.challenges[topic] = current.challenges.get(topic, 0) + 1
    return save()


def reset():
    global current
    current = Progress()
    return save()


def summary():
    from pydsa.topics import TOPICS

    text = f"{len(current.visited)} of {len(TOPICS)} topics visited"
    scores = [score.best for score in current.quizzes.values() if score.attempts]
    if scores:
        text += f" · best quiz average {sum(scores) / len(scores):.0f}%"
    return text
