## 8. Prompt Engineering & AI Workflow Evidence

AI tools were used throughout this project as a development support tool, not as an unquestioned authority. The prompts evolved over the course of the project as I gained a better understanding of what produced useful, accurate output and what led to generic or incorrect suggestions. This section documents the main techniques used, how prompts were refined, how hallucinations were detected and corrected, and how the overall workflow changed.

### 8.1 Prompt & Decision Log

The table below shows selected prompts from across the SDLC phases. Each entry shows the actual prompt used (edited for length where noted), the AI output, and the manual adjustments made.

---

**Entry 1 — Meta-Prompting (Requirements Phase)**

| Field | Detail |
|---|---|
| **Technique** | Meta-Prompting |
| **Context Provided** | Full project context block pasted at the top of the prompt, including assignment constraints, chosen project (Habit Tracker), and stack (Flask + JSON). |
| **Constraints / Limitations** | "Use 'The system shall...' wording. Keep requirements realistic for a small MVP. Requirements must be testable. Do not introduce external APIs, authentication, cloud storage, notifications, analytics platforms, or multi-user features. Do not over-engineer." |
| **Input** | *ROLE: You are acting as a junior software analyst helping produce a concise SDLC report for a university project. TASK: Generate functional and non-functional requirements for the Habit Tracker Web App. OUTPUT FORMAT: Return: 1. Functional Requirements 2. Non-Functional Requirements. Each requirement must be: clear, specific, testable, aligned with Flask + local JSON storage.* |
| **AI Output** | Produced 17 functional requirements (FR1–FR17) covering habit CRUD, completion tracking, streak calculation, weekly summary, validation, and JSON persistence. Produced 11 non-functional requirements (NFR1–NFR11) covering Flask stack, local storage, server-side validation, error handling, and code structure. Output used "The system shall..." format throughout and stayed within scope. |
| **Manual Adjustment** | Removed two requirements the AI added that were not in scope: one for "habit categories" and one for "data export to CSV." Added an explicit ASSUMPTION label to NFR8 (malformed JSON handling) because the original wording implied advanced file recovery that was beyond MVP scope. Tightened the streak definition in FR9 to specify "consecutive calendar days including today" — the AI's version was vaguer. |
| **Reason for Technique** | Meta-prompting was used to control the AI's role, tone, and output structure from the start. By defining a persona ("junior software analyst") and embedding constraints directly in the prompt, the output stayed aligned with the assignment brief and avoided scope creep. This reduced correction rounds compared to earlier unstructured prompts. |

---

**Entry 2 — Prompt Chaining (MVP Definition Phase)**

| Field | Detail |
|---|---|
| **Technique** | Prompt Chaining |
| **Context Provided** | Short project context block. Pasted the approved (post-reflexion) requirements AND the completed system design output into the prompt as source material. |
| **Constraints / Limitations** | "MVP must remain feasible for a small university project. Preserve the streak engine as the key non-trivial logic feature. Do not contradict the approved requirements without explaining why a feature is deferred." |
| **Input** | *Approved requirements: [pasted final FR1–FR17, NFR1–NFR11]. System design: [pasted design output]. Task: Define the MVP for this project. Include: Designed features (full scope), Implemented features (MVP), Deferred features, Justification for decisions. Output format: Use report-ready headings and concise academic tone.* |
| **AI Output** | Produced a structured MVP definition with five subsections: Full Designed Scope, Implemented MVP, Deferred Features, Justification, and Final MVP Statement. Correctly identified the streak engine as the core non-trivial feature. Deferred items included a dedicated edit page, advanced JSON recovery, and enhanced visual presentation. Listed "weekly analytics chart" as an implemented feature. |
| **Manual Adjustment** | Corrected the "weekly analytics chart" claim — the approved requirements specify a weekly summary (text/table), not a chart. The chart appears in the broader Habit Tracker option description in the assignment brief but was never part of the approved requirements for this project. The AI conflated the two. Added an explicit ASSUMPTION note in the deferred features clarifying this distinction. |
| **Reason for Technique** | Prompt chaining was used because the MVP definition depends directly on the approved requirements and design. By feeding the verified outputs of earlier prompts into this one, the AI had the correct context and was less likely to invent features or contradict earlier decisions. This is where chaining pays off — each phase builds on checked work from the previous phase. |

---

**Entry 3 — Directional Stimulus Prompting (Streak Logic Design)**

| Field | Detail |
|---|---|
| **Technique** | Directional Stimulus Prompting (DSP) |
| **Context Provided** | Short project context block. Pasted the approved MVP section. |
| **Constraints / Limitations** | "One completion per day only. Consecutive days increase the streak. Missing a day resets the streak. The logic must work with dates stored in a local JSON file. Keep the logic simple enough for unit testing." |
| **Input** | *Task: Design the streak calculation logic for the habit tracker. Directional example of desired style: A good answer should: explain the logic in plain English, mention how duplicate dates are handled, explain what happens if today is not completed, include small example scenarios, mention edge cases clearly. Output format: 1. Logic explanation 2. Edge cases 3. Example scenarios 4. Short pseudocode.* |
| **AI Output** | Produced a logic explanation in plain English, six edge cases (duplicate dates, empty history, today not completed, gap in dates, unsorted dates, invalid date value), five worked example scenarios with specific dates and expected streak values, and pseudocode using a simple loop that checks each previous day. The pseudocode matched the approved streak rules. |
| **Manual Adjustment** | The AI's pseudocode used a while loop but did not handle the edge case where completion_dates was None (as opposed to an empty list). Added a guard clause for this. Verified each of the five example scenarios manually by working through the dates on paper — the expected values were all correct. Used the edge case list directly to inform the test cases in test_streaks.py. |
| **Reason for Technique** | DSP was chosen because the streak engine is the most important logic feature in the project and I needed the AI to produce something specific and testable, not generic. By providing directional cues ("a good answer should..."), the output was structured in a way that directly supported both implementation and test case design. Without these cues, earlier attempts produced vague descriptions that were not useful for coding. |

---

**Entry 4 — Self-Consistency / Verifier (Pre-Submission Audit)**

| Field | Detail |
|---|---|
| **Technique** | Self-Consistency / Verifier |
| **Context Provided** | Full project context block. Pasted the approved requirements, approved design, and approved MVP into a single prompt as the source of truth. |
| **Constraints / Limitations** | "Act as a skeptical reviewer and check the current project materials for: contradictions, unsupported assumptions, invented features, drift away from the assignment brief, mismatches between designed and implemented scope." |
| **Input** | *SOURCE OF TRUTH: Approved requirements: [pasted]. Approved design: [pasted]. Approved MVP: [pasted]. TASK: Check the current project materials for hallucinations, contradictions, and alignment issues. OUTPUT FORMAT: Create a table with columns: Item reviewed, Problem found, Issue type (hallucination / assumption / inconsistency / acceptable), Recommended correction. Then provide: Top 3 risks if these issues are left unfixed, A corrected summary paragraph.* |
| **AI Output** | Identified four issues in a table: (1) the report draft mentioned "test_habits.py" but the actual file was test_streaks.py — issue type: inconsistency; (2) the implementation summary claimed the secret key was configurable but the code had it hardcoded — issue type: inconsistency; (3) README.md and requirements.txt were missing from the repository — issue type: inconsistency with submission requirements; (4) one test file name reference in the report did not match the project structure — issue type: inconsistency. Top risk identified: filename mismatches would be immediately visible to an assessor checking the repo against the report. |
| **Manual Adjustment** | All four issues were genuine and were fixed before submission: renamed test references in the report to match actual filenames, added environment variable support for SECRET_KEY with a local default, created README.md and requirements.txt, and aligned all file references between report and code. This prompt directly improved submission readiness. |
| **Reason for Technique** | The verifier/self-consistency approach was used as a final quality check. It simulates a second pair of eyes reviewing the project for consistency. This caught exactly the kind of small mismatches that are easy to miss during writing but that an assessor or viva examiner would notice immediately. |

### 8.2 How Prompts Were Refined

The prompting approach changed significantly over the course of the project. Early prompts were simple and underspecified, which produced output that was technically correct but often too generic or included features outside the project scope. For example, an early prompt asking for "requirements for a habit tracker" returned suggestions for user authentication, cloud sync, and notification systems — none of which are appropriate for a local Flask + JSON MVP.

The main refinement was the introduction of a reusable context block that was pasted at the start of every serious prompt. This block included the project constraints, the chosen stack, and explicit rules such as "do not invent external services" and "label anything unsupported as ASSUMPTION." This single change eliminated most scope-creep issues in later prompts.

A second refinement was moving from single large prompts to chained prompts. Instead of asking the AI to produce requirements, design, and MVP in one go, each phase was handled in a separate prompt, with the verified output of the previous phase provided as input. This made errors easier to catch and kept each prompt focused.

A third refinement was adding explicit output format instructions. Early prompts produced unstructured paragraphs that were difficult to use directly in the report. Later prompts specified headings, table formats, or numbered lists, which reduced the amount of manual reformatting needed.

### 8.3 How Hallucinations Were Detected and Corrected

Three notable hallucinations or inaccuracies were identified and corrected during the project:

**Hallucination 1: Invented feature — "weekly analytics chart."** During MVP definition, the AI listed a weekly analytics chart as an implemented feature. This was traced back to the project option description in the assignment brief, which mentions a "weekly analytics chart" as part of the full Habit Tracker option. However, the approved requirements for this project specify a weekly summary, not a chart. The AI conflated the two. This was corrected by removing the chart reference and adding an explicit assumption note in the MVP section clarifying the distinction.

**Hallucination 2: Claimed file that did not exist.** When generating the testing section, the AI referenced a test file called "test_habits.py." No such file existed in the project — the actual test files were test_streaks.py, test_storage.py, and test_routes.py. The AI appeared to invent a plausible filename rather than checking the actual project structure. This was corrected by replacing all references with the actual filenames.

**Hallucination 3: Overstated security posture.** In an early draft of the security section, the AI described the application as having "robust input sanitisation" and "secure session management." In reality, the application has basic non-empty name validation and a simple Flask SECRET_KEY. The wording was corrected to accurately reflect the actual level of security, which is proportionate to a local single-user MVP but should not be overstated.

Each of these was caught through manual review — reading the AI output against the actual code and approved documents rather than accepting it at face value.

### 8.4 How Debugging Was Done with AI

AI was used to assist with two debugging tasks during implementation. In both cases, a Chain of Thought approach was used — the AI was asked to reason through the problem step by step rather than immediately proposing a rewrite.

The first was a date comparison bug where streak calculation returned 0 when it should have returned 2. The prompt provided the failing test output, the function code, and the instruction: "Walk through this function line by line. Do not rewrite it — explain the issue first." The AI traced through each line and identified that completion dates were stored as strings ('2026-04-09') but compared against datetime.date objects. The fix was accepted, but the AI's additional suggestion to wrap every date parse in a try/except was rejected — error handling was placed in storage.py instead, keeping the streak function clean and testable.

The second was a Flask routing issue where the edit form submitted to the wrong URL pattern. The AI was given the route definition and the HTML form action, and it identified that the form was posting to `/habits/edit/<id>` while the route expected `/habits/<id>/edit`. This was a straightforward mismatch that the AI caught quickly once given both pieces of context.

In both cases, the approach was to provide the AI with the specific error, the relevant code, and a request to reason through the problem rather than asking it to rewrite the code.

### 8.5 How the Workflow Evolved

The workflow went through three broad phases:

**Phase 1 — Exploration.** Early prompts were loose and experimental. The goal was to get a rough shape for the requirements and design. Output quality was inconsistent, and several responses included features outside the project scope. The main lesson from this phase was that underspecified prompts produce unreliable output.

**Phase 2 — Structured prompting.** After the first few iterations, I introduced the reusable context block, explicit constraints, and chained prompts. This phase covered requirements, design, MVP definition, and streak logic. Output quality improved significantly, and the amount of manual correction dropped. The main lesson was that investing time in prompt structure pays off across all later phases.

**Phase 3 — Verification and refinement.** The final phase focused on catching errors rather than generating new content. The verifier prompt, reflexion-style reviews, and manual cross-checks between report and code were the most valuable activities in this phase. The main lesson was that AI is most dangerous when it sounds confident about something that is subtly wrong, and that a structured review process is essential before submission.

### 8.6 Evidence of Directing the AI

Throughout the project, the AI was directed rather than followed. Key examples of this include:

- Rejecting the AI's suggestion to add "habit categories" and "CSV export" during requirements — these were not in the brief and would have expanded scope unnecessarily.
- Overriding the AI's MVP definition to remove the "weekly analytics chart" and replace it with the correct "weekly summary" as specified in the approved requirements.
- Choosing to apply the date-parsing fix in storage.py rather than in streaks.py, contrary to the AI's suggestion, because it kept the streak function cleaner and more testable.
- Using the verifier prompt output to fix real submission issues (missing files, filename mismatches, hardcoded secret key) rather than treating the AI's "all looks good" responses from earlier prompts as sufficient.

The consistent pattern was: use AI to generate drafts and identify issues, but make all final decisions based on the approved requirements, the actual code, and the assignment brief.
