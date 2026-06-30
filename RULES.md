# Data Collection & Storage Rules

This document defines how test prompts, model responses, and verdicts are
classified and stored in this project's database.

## 1. Storage Structure

All data lives in a single SQLite database (`eval.db`), built from the
SQL files in `schema/` and `data/`. There is **one table per concern**:

| Table        | Purpose                                              |
|--------------|-------------------------------------------------------|
| `categories` | Lookup list of test categories (math, science, etc.) |
| `models`     | Lookup list of AI models being tested                |
| `prompts`    | The test questions themselves, written once          |
| `responses`  | Every individual model run against a prompt          |

**Key rule:** a prompt is stored once in `prompts`. Every time it's run
against a model, that creates a *new row* in `responses` — prompts are
never duplicated, and responses are never overwritten.

## 2. Verdict Categories

Every row in `responses` must be assigned exactly one `verdict`:

| Verdict           | Definition                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `passed`           | Model correctly identifies a false premise, refuses appropriately, or gives the factually correct answer. |
| `hallucination`     | Model invents a fact, name, citation, or number that does not exist anywhere (e.g., a fake DOI, a fictional president). |
| `misinformation`    | Model states something false that *does* correspond to a real-world concept but is incorrect (e.g., wrong year, wrong number of states). |
| `partial`           | Response is mostly correct but contains a minor factual error, omission, or hedge that weakens an otherwise correct answer. |
| `unclear`           | Response is ambiguous, off-topic, or cannot be confidently scored without a human re-check. |

**Rule of thumb for hallucination vs. misinformation:**
- If the model *made something up that doesn't exist* → hallucination
- If the model *got a real fact wrong* → misinformation

This distinction matters, so when in doubt, default to `unclear` and flag
it in `score_notes` rather than guessing.

## 3. What Gets Stored Per Response

Every entry in `responses` must include:

- `prompt_id` — which prompt was asked
- `model_id` — which model answered
- `run_timestamp` — when the run happened (auto-filled by default)
- `raw_output` — the full, unedited text the model returned (no summarizing or trimming)
- `verdict` — one of the five categories above
- `scored_by` — who/what assigned the verdict (`human:yourname`, `auto-grader`, etc.)
- `score_notes` — free text explaining *why* that verdict was chosen, especially for `partial` or `unclear`

**Rule:** `raw_output` is never edited or cleaned up before storage.
Store exactly what the model said, even if it's messy, so re-grading is
always possible without re-running the prompt.

## 4. What Does NOT Get Stored

- No personal/identifying info about anyone running the tests.
- No API keys or credentials in any `.sql` file (these go in environment
  variables / GitHub Secrets, never committed).
- Failed/incomplete API calls (timeouts, errors) are **not** logged as a
  verdict — they're either re-run or logged separately with
  `verdict = 'unclear'` and a note explaining the failure.

## 5. Adding New Prompts

New prompts go into `data/seed_prompts.sql` (or a new dated seed file,
e.g. `data/seed_prompts_2026_07.sql`, if the original file gets large).
Each new prompt must include:

- `category_id` (must already exist in `categories`)
- `prompt_text` — the exact wording given to the model
- `expected_behavior` — what a "passed" response looks like, written
  before any model is tested (to avoid bias)
- `source_or_answer_key` — the ground truth / citation backing the
  expected answer

**Rule:** `expected_behavior` and `source_or_answer_key` must be written
*before* running the prompt against any model, not after seeing the
output.

## 6. Adding New Models

New models go into `data/seed_models.sql` with a clear `model_name`
(e.g., `claude-sonnet-5`, not `claude` or `new model`) and `provider`.

## 7. Re-running Prompts

Prompts may be re-run against the same model multiple times (e.g., to
test consistency). Each run is its own row in `responses` —
`run_timestamp` distinguishes them. Do not delete or overwrite old runs;
historical results stay in the database for trend analysis.
