import json
import os
import re
import time

import yaml
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from schemas import Analysis

load_dotenv()


def _load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


CONFIG = _load_yaml("config.yaml")
PROMPTS = _load_yaml(CONFIG["prompt_file"])


def _get_client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set. Copy .env.example to .env and add your key.")
    return genai.Client(api_key=key)


def _strip_fences(text):
    return re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()


def _call_llm(client, text, feedback=None):
    prompt = PROMPTS["user_template"].format(text=text)
    if feedback:
        prompt += f"\n\nYour previous output was invalid: {feedback}\nReturn corrected JSON only."
    cfg = types.GenerateContentConfig(
        system_instruction=PROMPTS["system"],
        temperature=CONFIG["temperature"],
        max_output_tokens=CONFIG["max_output_tokens"],
        response_mime_type="application/json",
    )
    retries = CONFIG["api_retries"]
    for attempt in range(retries + 1):
        try:
            return client.models.generate_content(
                model=CONFIG["model"], contents=prompt, config=cfg
            ).text or ""
        except Exception as e:  # network, quota, auth
            if attempt == retries:
                raise RuntimeError(f"Gemini API call failed: {e}") from e
            time.sleep(2**attempt)


def analyze(text: str) -> Analysis:
    text = text.strip()
    if not text:
        raise ValueError("Please enter some text to analyze.")
    if len(text) > CONFIG["max_input_chars"]:
        raise ValueError(f"Text too long (max {CONFIG['max_input_chars']} characters).")

    client = _get_client()
    feedback = None
    for _ in range(CONFIG["validation_retries"] + 1):
        raw = _call_llm(client, text, feedback)
        try:
            return Analysis.model_validate(json.loads(_strip_fences(raw)))
        except (json.JSONDecodeError, ValidationError) as e:
            feedback = str(e)[:500]
    raise RuntimeError(f"Model returned invalid JSON after retries: {feedback}")