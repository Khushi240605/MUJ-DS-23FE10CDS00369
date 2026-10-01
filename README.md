# Claim → Evidence Gap Analyzer

Paste any text; the app uses the Gemini API to extract each claim, classify it (statistical, causal, factual, predictive, opinion), say what evidence would support it, and point out what is missing from the text itself.

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env         # then add your GEMINI_API_KEY (Google AI Studio)
```

## Run
```bash
streamlit run app.py         # web UI
python eval.py               # run sample checks
```

## Design
- `prompts.yaml`: all prompts (task, rules, output format, few-shot example), kept separate from code
- `config.yaml`: model, temperature, token limit, retry counts
- `schemas.py`: Pydantic models; every LLM response is validated against them
- `llm_client.py`: API call with backoff retries, plus one corrective retry if the JSON is invalid
- `eval.py`: sample-based sanity checks

The analyzer judges only the evidence present in the text. It does not fact-check claims.