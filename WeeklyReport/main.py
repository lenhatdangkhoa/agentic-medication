"""
main.py — Weekly Health Report Generator
Hybrid approach: Python computes stats, Gemini Flash writes narrative.

Usage:
    python main.py                          # uses GOOGLE_API_KEY env var
    python main.py --api-key YOUR_KEY
    python main.py --patient "Jane Smith" --seed 99
    python main.py --demo                   # skips LLM, uses placeholder text
"""

import argparse
import sys
import os
from pathlib import Path

# Make src importable
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_generator import generate_weekly_data, compute_stats
from llm_reporter import generate_llm_narrative
from renderer import render_html_report


DEMO_NARRATIVE = {
    "executive_summary": (
        "[DEMO MODE — no API key provided] "
        "This section would contain a Gemini-generated paragraph summarising "
        "the patient's overall week based on the computed statistics above."
    ),
    "key_trends": (
        "This section would highlight notable patterns across sleep, steps, "
        "heart rate, HRV, stress, and hydration with specific day references."
    ),
    "concerns": (
        "This section would flag any metrics that fell outside healthy ranges "
        "and offer context for why they might matter."
    ),
    "recommendations": (
        "This section would provide 4-5 personalised, actionable suggestions "
        "derived from the week's data, written by Gemini Flash."
    ),
}


def main():
    parser = argparse.ArgumentParser(description="Weekly Health Report Generator")
    parser.add_argument("--api-key",  default=None,         help="Google Gemini API key")
    parser.add_argument("--patient",  default="Alex Johnson", help="Patient name")
    parser.add_argument("--seed",     type=int, default=42,  help="RNG seed for synthetic data")
    parser.add_argument("--output",   default="output/weekly_report.html", help="Output HTML path")
    parser.add_argument("--demo",     action="store_true",   help="Skip LLM, use placeholder text")
    args = parser.parse_args()

    print("\n── Weekly Health Report Generator ──────────────────")
    print(f"  Patient : {args.patient}")
    print(f"  Seed    : {args.seed}")
    print(f"  Output  : {args.output}")
    print(f"  Mode    : {'DEMO (no LLM)' if args.demo else 'LangChain + Gemini Flash'}\n")

    # ── Step 1: Generate & compute (pure Python, deterministic) ──────────────
    print("  [1/3] Generating synthetic health data...")
    df = generate_weekly_data(seed=args.seed, patient_name=args.patient)

    print("  [2/3] Computing statistics...")
    stats = compute_stats(df)
    print(f"        Week: {stats['week_start']} – {stats['week_end']}")
    print(f"        Avg steps: {stats['avg_steps']:,} | Avg sleep: {stats['avg_sleep']}h | Avg HR: {stats['avg_resting_hr']} bpm")

    # ── Step 2: LLM narrative (Gemini Flash via LangChain) ───────────────────
    if args.demo:
        print("  [3/3] Skipping LLM (demo mode)...")
        narrative = DEMO_NARRATIVE
    else:
        api_key = args.api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("\n  ⚠️  No API key found. Re-running in demo mode.")
            print("     Set GOOGLE_API_KEY or pass --api-key to use Gemini.\n")
            narrative = DEMO_NARRATIVE
        else:
            print("  [3/3] Sending stats to Gemini Flash for narrative...")
            try:
                narrative = generate_llm_narrative(stats, api_key=api_key)
                print("        ✓ Narrative generated successfully")
            except Exception as e:
                print(f"        ✗ LLM call failed: {e}")
                print("        Falling back to demo narrative.")
                narrative = DEMO_NARRATIVE

    # ── Step 3: Render HTML ────────────────────────────────────────────────
    render_html_report(stats, narrative, output_path=args.output)
    print("\n── Done! Open the HTML file in your browser to view the report.\n")


if __name__ == "__main__":
    main()
