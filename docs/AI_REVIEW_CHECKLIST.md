# AI-assisted code review checklist
- Does the code meet the written specification?
- Are empty inputs, invalid values, and edge cases handled?
- Are SQL statements parameterized?
- Is book availability consistent with loan records?
- Are types and complexity documented?
- Is a test added for the change?
- Did I run tests, linting, and type checks?
- Do I understand the code well enough to defend it?

Example prompt: “Review the 0/1 knapsack function for recurrence correctness, capacity edge cases, solution reconstruction, and time/space complexity. Suggest minimal fixes and tests; do not change unrelated modules.”

Specification-first means agreeing on expected inputs, outputs, and invalid-input behavior before coding. Context management means supplying relevant source, tests, requirements, and error output to an AI assistant.
