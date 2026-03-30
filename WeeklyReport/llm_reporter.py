"""
LangChain + Gemini Flash report generator.
Python handles all stats; the LLM only generates narrative prose.
"""

import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


REPORT_PROMPT = PromptTemplate(
    input_variables=["stats_json"],
    template="""
You are an expert health coach writing a warm, professional weekly health report.
You have been given pre-computed statistics — do NOT recalculate or second-guess the numbers.

Your job is ONLY to write narrative prose that interprets these stats meaningfully.

Health Statistics (pre-computed, authoritative):
{stats_json}

Write a weekly health report with EXACTLY these four sections. Use plain text only — no markdown, 
no bullet points, no asterisks. Write in flowing paragraphs.

SECTION: EXECUTIVE SUMMARY
Write 3-4 sentences giving an overall picture of the week. Be specific, reference 2-3 key numbers.

SECTION: KEY TRENDS & HIGHLIGHTS
Write 4-5 sentences discussing the most notable patterns across sleep, activity, heart rate, 
stress, and hydration. Mention standout days by name. Be conversational but data-grounded.

SECTION: AREAS OF CONCERN
Write 2-3 sentences on anything that warrants attention (poor sleep days, high stress, low HRV, 
calorie imbalance, low SpO2, etc.). Be honest but not alarmist. If everything looks great, say so briefly.

SECTION: PERSONALIZED RECOMMENDATIONS
Write 4-5 sentences with specific, actionable advice based on the data. Tailor to what the numbers show.

End with one short encouraging closing sentence addressed to the patient by first name.

Remember: plain paragraphs only, no formatting symbols.
""",
)


def build_llm(api_key: str = None) -> ChatGoogleGenerativeAI:
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError(
            "No Google API key found. Set GOOGLE_API_KEY env var or pass api_key."
        )
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=key,
        temperature=0.4,
    )


def generate_llm_narrative(stats: dict, api_key: str = None) -> dict:
    """
    Send pre-computed stats to Gemini Flash and get back narrative sections.
    Returns a dict with keys: executive_summary, key_trends, concerns, recommendations.
    """
    llm = build_llm(api_key)

    # Exclude raw daily records from the JSON to keep the prompt tight
    stats_for_prompt = {k: v for k, v in stats.items() if k != "daily_summary"}

    chain = REPORT_PROMPT | llm

    result = chain.invoke({"stats_json": json.dumps(stats_for_prompt, indent=2)})
    raw_text = result.content.strip()

    # Parse the four sections out of the LLM response
    sections = _parse_sections(raw_text)
    return sections


def _parse_sections(text: str) -> dict:
    """Split LLM output into the four named sections."""
    markers = {
        "executive_summary": "SECTION: EXECUTIVE SUMMARY",
        "key_trends": "SECTION: KEY TRENDS & HIGHLIGHTS",
        "concerns": "SECTION: AREAS OF CONCERN",
        "recommendations": "SECTION: PERSONALIZED RECOMMENDATIONS",
    }

    result = {}
    keys = list(markers.keys())
    labels = list(markers.values())

    for i, (key, label) in enumerate(zip(keys, labels)):
        start = text.find(label)
        if start == -1:
            result[key] = ""
            continue
        start += len(label)
        # End is the start of the next section (or end of text)
        end = text.find(labels[i + 1]) if i + 1 < len(labels) else len(text)
        result[key] = text[start:end].strip()

    return result
