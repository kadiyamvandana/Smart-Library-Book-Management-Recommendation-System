# Project Defence Guide

## Problem and decomposition
A library needs a catalogue, availability counts, borrowing/return tracking, and book discovery. Web routes, models, database access, recommendation logic, and tests are separate modules.

## Algorithm mapping
- Greedy recommendation: prioritize the chosen category, then sort by title. O(n log n) time and O(n) space.
- Dynamic programming: 0/1 knapsack selects a high-value set under carrying capacity. O(nW) time and space.
- Backtracking: recursively tries include/exclude choices and rejects over-capacity choices. O(2^n) worst case.
- Branch-and-bound: prunes branches using an optimistic upper bound. Exponential worst case.
- Divide-and-conquer: merge sort splits the list and merges sorted halves. O(n log n) time and O(n) auxiliary space.
These are educational algorithm demonstrations for different tasks, not claims that all algorithms power the live recommendation page.

## Programming and design
`LibraryItem` is an abstract base class; `Book` and `EBook` inherit from it. `LibraryRepository` encapsulates database operations (Repository pattern). Lists/dictionaries store records; comprehensions filter; `available_book_stream` is a generator; `timed` is a decorator; `iter_batches` is a lazy batch generator; SQLite connections use `with` context managers. `apply_filter` is a pure helper and accepts a higher-order predicate.

## Concurrency and GIL
`ThreadPoolExecutor` overlaps simulated catalogue I/O waits. Threads are useful for I/O-bound waits; standard CPython's GIL means threads generally do not speed up CPU-bound Python bytecode. The normal library web app does not need concurrency for its small local database. Multiprocessing/async are alternatives to discuss, not falsely claim as implemented.

## Quality and DevOps
Run `pytest --cov=library_system --cov-report=term-missing`, `ruff check .`, and `mypy library_system`. Hypothesis generates lists to check the merge-sort property. GitHub Actions runs tests and Ruff. A Dockerfile is included.

## AI-assisted engineering
See `AI_REVIEW_CHECKLIST.md`. Save the specification, prompts, test outputs, and code review notes. Review all generated suggestions before accepting them; do not claim unverified code is correct.

## Performance evaluation
Run `python notebooks/algorithm_demo.py`. It prints actual local timings. Do not invent benchmark numbers. Compare solution value and runtime for increasing input sizes. DP is O(nW); exhaustive backtracking and branch-and-bound have exponential worst cases.

## Live demo
1. Open catalogue. 2. Add printed book and e-book. 3. Search/filter. 4. Borrow a book and show copies decrement. 5. Record return and show copies increment. 6. Use category recommendations. 7. Show admin loan history. 8. Run tests and algorithm demo.

## Limitations
Educational demo only. No login/role permissions, due dates, fines, or production security. Recommendation is rule-based, not trained AI.
