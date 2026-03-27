# Project Homepage Content

## Title

Agentic Remote Patient Monitoring with Clinician-Reviewable Next-Step Recommendations from Synthetic Multimodal Patient Data

## Tagline

Simulation-first workflow for turning patient-generated health data into safer clinician-reviewable next actions.

## Hero Summary

This project studies whether an agentic remote patient monitoring system can convert weekly multimodal patient data into clinician-reviewable next-step recommendations without increasing unsafe or irrelevant suggestions. The current version is fully simulation-based and focuses on weekly summaries, anomaly detection, retrieval-backed compatibility checking, clinician approval, and downstream task dispatch.

## Key Contributions

- A simulation-first workflow for weekly RPM summary generation and next-step action drafting
- A synthetic patient-week benchmark with anomaly scenarios and safety-aware action labels
- A comparison between rule-based, summary-only, and retrieval-backed clinician-in-the-loop systems
- Initial evidence that retrieval and clinician review can improve safety-oriented recommendation quality

## System Overview Section

- Input data: steps, sleep, heart rate, symptoms, medication adherence, longitudinal history
- Core modules: summary generation, anomaly detection, compatibility retrieval, constrained action proposal, clinician review, task dispatch
- Action classes: monitor only, repeat measurement, lab order, medication review, follow-up visit, urgent escalation

## Results Snapshot

- Threshold+Template:
  - relevant precision 0.5542
  - unsafe suggestion rate 0.1417
  - clinician acceptance 0.3125
- Agentic RPM:
  - relevant precision 0.6708
  - unsafe suggestion rate 0.0958
  - clinician acceptance 0.4479

## Important Scope Note

The current project is simulation-only. It does not claim deployment readiness, autonomous prescribing, or live integration with Apple Health or electronic health record systems.

## Assets and Links

- Paper draft
- Simulation protocol
- Comparison results JSON
- Core code runner
- Future slide deck

## Future Work

- repeated-seed evaluation
- stronger anomaly detection
- richer retrieval and compatibility sources
- future OpenClaw and Apple Health integration after simulation validation
