# BookWise — Library Operations Workspace
A SaaS-style workspace for institutional library teams, built with Flask and SQLite. BookWise brings catalogue management, reader checkouts, returns, and category-based discovery into one responsive dashboard. The interface reports live inventory and circulation data rather than sample dashboard metrics.

## Run on Windows / VS Code
1. Extract ZIP and open the project folder in VS Code.
2. In terminal run:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
3. Open http://127.0.0.1:5000.
If PowerShell blocks activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` then `.venv\Scripts\python.exe app.py`.

## Workspace
- `/` operational overview with live catalogue and circulation metrics, search, category filters, and checkouts
- `/add` add printed books and e-books
- `/recommendations` available titles ordered by category relevance
- `/admin` inventory summary, loan history, and return recording

## Tests and quality
```powershell
pytest -v
pytest --cov=library_system --cov-report=term-missing
ruff check .
mypy library_system
```

## Algorithms
Run `python notebooks/algorithm_demo.py` from the project root to compare dynamic programming, backtracking, and branch-and-bound. Timings are measured on your machine. Read `docs/DEFENCE_GUIDE.md` for the defence mapping.

## Notes
This project uses a local SQLite database and does not include authentication or multi-tenant data isolation; additional security and infrastructure work is required before public or multi-organization deployment. Recommendations are rule-based, not machine learning. Threading is demonstrated using simulated I/O lookups, not real external APIs.
