# Repository Agent Instructions

PyDSA is a terminal app for learning data structures and algorithms. Keep implementations correct, learning material easy to understand, and diagrams useful in both colorful and plain output.

## Start with context

- Read the README, the relevant source and tests, and any plan named by the user before changing code.
- Check `git status` and recent commit messages. Preserve the user's changes and staging choices.
- When a plan is provided, implement the requested phase completely, including its learning content and verification. Do not move to another phase unless requested.
- Use the existing architecture and conventions. Keep changes focused; avoid unrelated refactoring or new dependencies without a concrete need.

## Repository layout

- `pydsa/core/`: data structures.
- `pydsa/algorithms/`: algorithms and trace events.
- `pydsa/ui/screens/`: topic flows, input and menus.
- `pydsa/ui/render.py`: diagrams, tables and learning views.
- `pydsa/content/`: Markdown guides, complexity tables, operation notes, narration, quizzes and ASCII titles.
- `pydsa/practice/`: predictions checked by real implementations and bounded work-count experiments.
- `pydsa/topics.py`: topic IDs, categories and screen entry points.
- `tests/`: model, content, screen and packaging checks.
- `docs/plans/`: active roadmaps and audit records.

## Implementation conventions

- Keep core code independent of terminal input, output and saved settings. Put prompts in screens and drawing in renderers.
- Preserve existing `--topic` IDs when regrouping menus.
- Follow the existing `Menu`, `Nav`, operation-note and playback patterns. Check cancellation, Back, New, Main Menu and Exit through nested flows.
- Optional traces must describe the actual work and retain snapshots that later mutations cannot change.
- Show user values consistently, preserving string input where whitespace matters. Escape control characters and keep brackets from becoming Rich markup.
- Provide text markers for highlights when colors are off. Wide diagrams and tables should fall back to a compact layout.
- Bound interactive recursion and exhaustive searches so examples stay readable and responsive.
- Explain measured work honestly: distinguish comparisons, calls, table cells or other counts from elapsed time, and state excluded work and assumptions.
- Maintain Python 3.10 compatibility, as declared in `pyproject.toml`.

## Completing a topic

A new topic includes all applicable parts of PyDSA's learning framework:

- Pure core implementation and tests against an independent model or reference.
- A screen with typed input, a preloaded example and random inputs.
- A registered topic, README feature entry and ASCII title in the existing `flower_power` font.
- A guide with a short summary and these sections, in order: What it is, How it works, Real-life analogy, When to use it, When to avoid it, In PyDSA.
- Accurate complexity tables, operation notes, pseudocode and real source references for computational operations.
- Trace narration for every multi-step operation and captions for every emitted event kind.
- At least five explained quiz questions and one prediction checked by the implementation.
- Bounded growth experiments where the work is worth comparing.

Use the completeness tests to check integration, and review the explanations for accuracy as well as presence. Update the README, release text and version when the requested plan calls for them.

## Verification

Use the project's virtual environment. Install the test dependencies when needed:

```sh
python -m pip install -e ".[test]"
python -m pytest
```

On Windows, the existing environment's interpreter is `.venv\Scripts\python.exe`; on other platforms it is `.venv/bin/python`.

- Add meaningful regression tests for bugs. Use model tests for algorithm behavior rather than duplicating the implementation in assertions.
- Run relevant tests while developing and the full suite before handing over code changes. Documentation-only edits need document review and `git diff --check`, not a full test run.
- For screen changes, check scripted input, navigation, practice and playback controls. Render at 45 and 90 columns with `NO_COLOR`; lines should fit except for ASCII titles.
- Keep manual-session settings and progress isolated with `PYDSA_HOME`, using an ignored scratch directory such as `.venv/`.
- For new modules or packaged guides, check imports with warnings treated as errors and inspect a built wheel for the required code and content.
- Finish with `git diff --check` and a review of the final diff. Report checks actually run, their outcomes and any unresolved gaps.

## Plans and audits

- Keep roadmap files through implementation and the final audit, even if a plan's wrap-up originally says to delete them, when the user has asked to retain them.
- A final audit checks every phase and shared requirement, including core behavior, diagrams, learning content, practice and packaging. Fix issues found and verify the fixes.
- Distinguish verified coverage from assumptions. Do not claim that passing tests alone proves every requirement is implemented.
- Audit reports are optional working records. Remove completed roadmaps or audit reports when the user requests cleanup, and preserve `docs/plans/.gitkeep`.

## Handoff and commit messages

The user normally makes the commit. Unless explicitly requested, do not stage, commit or push changes. End implementation work with a brief outcome, validation results and a proposed commit message.

- Follow recent repository history: a conventional subject such as `feat: ...`, `fix: ...` or `docs: ...` that names the actual change.
- Explain what was implemented or fixed in simple language, in one or two paragraphs. Each paragraph must be a single line, with a blank line between paragraphs; do not hard-wrap the body or replace it with bullets.
- Include relevant verification and plan cleanup when useful. Match the final work, including any change in scope.
- For Codex work, use this exact attribution trailer:

```text
Co-authored-with: Codex, GPT-6.1 Sol
```
