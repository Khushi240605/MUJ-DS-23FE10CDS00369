# ClaimLens

**Claim → Evidence Gap Analyzer.** Paste any text and ClaimLens uses the Gemini API to break it into individual claims and show how well the text supports each one.

For every claim it returns:
- **Type:** statistical, causal, factual, predictive, or opinion
- **Evidence needed:** the kind of evidence that would support it
- **Gap in the text:** what is missing from the text itself (no source, no numbers, correlation presented as cause, etc.)
- **Verdict:** unsupported, weak, partial, or well supported
- **Hidden assumptions:** what the claim silently depends on
- **Clearer version:** a more specific, testable rewrite of the claim

It also writes a short overall summary of the evidence quality.

## Example

Input:
> Studies show turmeric cures arthritis. I think winter is the best season.

Output (shortened):

| Claim | Type | Verdict | Hidden assumptions |
|---|---|---|---|
| Turmeric cures arthritis. | causal | unsupported | The unspecified studies are reliable |
| Winter is the best season. | opinion | well supported | None |

## Setup

Requires Python 3.10+ and a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env              # then open .env and replace your_key_here
```

## Run

```bash
streamlit run app.py              # web UI at http://localhost:8501
python3 eval.py                   # run the sample checks
```

## Project structure

```
├── app.py            # Streamlit UI
├── llm_client.py     # Gemini API call, retries, JSON parsing and validation
├── schemas.py        # Pydantic models for the LLM output
├── prompts.yaml      # System prompt, rules, output format, few-shot example
├── config.yaml       # Model name, temperature, token limit, retry counts
├── eval.py           # Runs sample texts and checks the output
├── samples/          # Sample texts used by eval.py
├── requirements.txt
└── .env.example      # Placeholder for the API key
```

## How it works

1. The text is sent to Gemini with the system prompt from `prompts.yaml`, using the settings in `config.yaml`.
2. The model is asked to return JSON only, following a fixed format with a worked example.
3. The response is cleaned and validated against the Pydantic models in `schemas.py`.
4. If the JSON is invalid, the error is sent back to the model for one corrective retry.
5. API errors (network, rate limits) are retried with exponential backoff, and any final failure is shown as a readable message in the UI.

## Design choices

- **Prompts live outside the code**, in `prompts.yaml`, so they can be improved without touching Python.
- **Settings live in `config.yaml`**, so the model or temperature can be changed in one place.
- **Low temperature (0.2)** keeps the analysis consistent between runs.
- **The prompt limits the model to the text it is given.** It must not add outside facts or decide whether a claim is true; it only judges the support provided in the text.
- **Strict schema validation** means the UI never receives malformed output.

## Limitations

- ClaimLens judges only the evidence present in the text. It does not fact-check claims against outside sources.
- Claim types and verdicts are LLM judgments, so borderline cases (for example, "mid university" as fact vs opinion) can vary between runs.
- The summary wording can occasionally be looser than the table.
- Input is limited to 6000 characters (set in `config.yaml`).

## Disclaimer

This tool is for analysis and learning. Its output is not a substitute for professional fact-checking.

Author: Khushi