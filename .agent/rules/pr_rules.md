---
trigger: always_on
---

# PR Formatting Guidelines

When writing Pull Request titles and descriptions for this repository, ALWAYS adhere to the guidelines in `CONTRIBUTING.md` alongside the following team standards:

- **Language**: Always use simple, clear English words. Avoid complex vocabulary or jargon unless absolutely necessary.

## 1. Subject Rules
- **Format**: `<type>: <Subject>`
- **Types allowed**: build, ci, docs, feat, fix, perf, refactor, style, test, meta, license
- **Style**: Capitalize the first letter of the subject. Do NOT end with a period. Prefer 70 characters or fewer.
- **Tense**: Use imperative, present tense (e.g., `Add`, `Fix`, `Update`).
- **Focus**: Describe behavior or capability, not implementation details. Do NOT mention internal structure (e.g., domain code, utils, refactor details).

### Bug Fixes vs. New Features
- **Bug Fixes**: Describe the incorrect behavior being corrected, not the solution.
  - When describing a problem in the imperative tense, ensure it doesn't sound like a command to introduce a bug. Use wording that clearly identifies the flaw and avoids sounding like a requested action.
- **New Features**: Describe the capability introduced. Do NOT imply something was broken unless it actually was.

## 2. Description Rules
- **Format**: Use bullet points only. Do NOT use any headings (no "Issue", "Cause", "Fix", "Summary", etc.).
- **Content**: The description as a whole should cover:
  - the problem or context
  - why the change is needed
  - the resulting behavior
- **Constraints**:
  - Do NOT mention file names, functions, classes, or code structure.
  - Do NOT describe diffs or implementation steps.
  - Keep sentences concise, developer-focused, and avoid vague or filler wording.
- **Feature Specifics**: Focus on what capability is introduced and how the system behaves now. Do NOT say "previously not supported" or similar phrasing.
- **Bug Fix Specifics**: Clearly describe what was going wrong and what behavior is corrected.

## 3. Response Format
- Provide both a PR subject and description.
- Use bullet points for the description.