# Slide Outline: Agentic RPM for BIBM 2026

## Slide 1. Title

- Title: Agentic Remote Patient Monitoring with Clinician-Reviewable Next-Step Recommendations from Synthetic Multimodal Patient Data
- Subtitle: Simulation-first workflow for safe and reviewable RPM action drafting
- Footer: BIBM 2026 submission draft

## Slide 2. Clinical Problem

- RPM systems generate continuous wearable and symptom data
- Clinicians still face dashboards, alerts, and manual triage burden
- Missing workflow step: converting weekly patient data into reviewable next actions

## Slide 3. Research Question and Gap

- Research question:
  - Can an agentic system draft clinician-reviewable next-step recommendations from RPM data without increasing unsafe or irrelevant suggestions?
- Gap:
  - prior work addresses RPM, anomaly detection, LLM CDS, and medication safety separately
  - few integrated clinician-in-the-loop workflows

## Slide 4. Proposed Workflow

- Multimodal synthetic patient data
- Weekly structured summary
- Interpretable anomaly detection
- Retrieval-backed compatibility checking
- Constrained action proposal
- Clinician review
- Downstream task dispatch

## Slide 5. Action Space and Safety Design

- Action classes:
  - monitor only
  - repeat measurement
  - lab order
  - medication review
  - follow-up visit
  - urgent escalation
- Safety design:
  - constrained ontology
  - compatibility retrieval
  - clinician gate
  - no autonomous prescribing claim

## Slide 6. Simulation Environment

- Patient-week as unit of evaluation
- Synthetic cohort with multimodal trajectories and short history
- Scenario library:
  - stable recovery
  - spurious outlier
  - activity and sleep decline
  - rising heart-rate trend
  - medication nonadherence
  - fluid-related decline
  - arrhythmia-like pattern

## Slide 7. Baselines and Ablations

- Threshold+Template
- Summary-Only Assistant
- Agentic RPM
- No retrieval
- No patient history
- No clinician gate

## Slide 8. Main Results

- Threshold+Template:
  - relevant precision 0.5542
  - unsafe rate 0.1417
  - clinician acceptance 0.3125
- Agentic RPM:
  - relevant precision 0.6708
  - unsafe rate 0.0958
  - clinician acceptance 0.4479

## Slide 9. Safety Comparison

- Summary-Only Assistant has similar relevance precision
- Agentic RPM lowers unsafe suggestion rate
- Agentic RPM increases clinician acceptance
- Interpretation: safety and reviewability are the main gain

## Slide 10. Ablation Findings

- Removing retrieval increases unsafe suggestions
- Removing patient history degrades precision and safety
- Removing clinician gate harms dispatch safety

## Slide 11. Limitations

- synthetic data only
- single-seed prototype results
- heuristic recommendation policies
- anomaly recall remains low

## Slide 12. Future Work

- repeated-seed evaluation and stronger anomaly models
- richer retrieval and compatibility sources
- OpenClaw and Apple Health integration after simulation validation

## Slide 13. Conclusion

- Simulation-first agentic RPM workflow is feasible
- Safety-aware recommendation drafting is a stronger claim than autonomous treatment generation
- Clinician review remains essential
