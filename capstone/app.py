import pandas as pd
import streamlit as st

from llm_client import analyze

BADGE = {"unsupported": "🔴 unsupported", "weak": "🟠 weak", "partial": "🟡 partial", "well_supported": "🟢 well supported"}

st.set_page_config(page_title="ClaimLens", layout="wide")
st.title("🔎 ClaimLens", anchor=False)
st.subheader("Claim → Evidence Gap Analyzer", anchor=False)
st.caption("Paste any text. Get each claim, what evidence it needs, and what's missing.")

text = st.text_area("Text to analyze", height=200, placeholder="Paste a news paragraph, post, or essay excerpt...")

if st.button("Analyze", type="primary"):
    try:
        with st.spinner("Analyzing..."):
            result = analyze(text)
    except (ValueError, RuntimeError) as e:
        st.error(str(e))
        st.stop()

    st.subheader("Summary", anchor=False)
    st.write(result.summary)

    if not result.claims:
        st.info("No checkable claims found.")
    else:
        df = pd.DataFrame(
            [
                {
                    "Claim": c.claim,
                    "Type": c.type,
                    "Evidence needed": c.evidence_needed,
                    "Gap in the text": c.gap,
                    "Verdict": BADGE[c.verdict],
                    "Hidden assumptions": "; ".join(c.hidden_assumptions) or "None",
                    "Clearer version": c.rewritten_claim,
                }
                for c in result.claims
            ]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download JSON", result.model_dump_json(indent=2), "analysis.json", "application/json")