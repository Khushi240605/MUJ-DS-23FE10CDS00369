# MUJ-DS-23FE10CDS00369

| | |
|---|---|
| **Name** | Jain Khushi Sanjay |
| **Registration Number** | 23FE10CDS00369 |
| **Branch** | B.Tech CSE (Data Science) |
| **Batch** | E | 
| **Project Title** | ClaimLens: Claim → Evidence Gap Analyzer |
| **GitHub Username** | Khushi240605 |
| **Training Program** | <NLP project - DSE4150> |

## About the project

ClaimLens uses the Gemini API to break any text into individual claims and show how well the text itself supports each one: claim type, evidence needed, gaps, verdict, hidden assumptions, and a clearer rewrite. It judges the evidence inside the text and does not fact-check against outside sources.

Full project details, setup steps, and usage are in [capstone/README.md](capstone/README.md).

## Repository structure

- `assignments/`: training assignments
- `notebooks/`: notebooks
- `code/`: practice code
- `resources/`: reference material
- `presentations/`: project presentation
- `capstone/`: ClaimLens source code, prompt file, config file, and sample tests

## Quick start

```bash
cd capstone
pip install -r requirements.txt
cp .env.example .env     # add your Gemini API key
streamlit run app.py
```

## Contributions

This project was completed individually by Jain Khushi Sanjay.

- **Dataset and sample texts:** `capstone/samples/samples.json` (issue #1)
- **Prompt design and LLM client:** `capstone/prompts.yaml`, `capstone/llm_client.py`, `capstone/schemas.py` (issue #2)
- **Testing:** `capstone/eval.py` and a fresh-clone install check (issue #3)
- **Documentation:** `README.md` files and setup guide (issue #4)
- **Frontend:** Streamlit interface in `capstone/app.py` (issue #5)