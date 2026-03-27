# Figures, Tables, and Reproducibility Package

## Figure 1: Agentic RPM Workflow

### Purpose

Show the full pipeline from synthetic multimodal patient data to clinician-approved downstream action.

### Panels

- synthetic RPM inputs:
  - steps
  - sleep
  - heart rate
  - symptoms
  - medication adherence
- weekly structured summary
- anomaly detection
- retrieval-backed compatibility checking
- constrained action proposal
- clinician review gate
- downstream task dispatch

### Caption Draft

Figure 1. Overview of the proposed simulation-first Agentic RPM workflow. Weekly multimodal patient-generated signals are summarized and analyzed for anomalies, combined with patient-history and compatibility retrieval, and converted into a constrained clinician-reviewable next-step recommendation. Downstream task dispatch occurs only after clinician approval.

## Figure 2: Synthetic Patient-Week Examples

### Purpose

Illustrate representative scenarios and why the action proposals differ.

### Suggested examples

- rising resting heart-rate trend with high-risk profile leading to urgent escalation
- medication nonadherence pattern leading to medication review
- spurious single-day outlier leading to repeat measurement

### Caption Draft

Figure 2. Example synthetic patient-week trajectories used in the simulation. Each case shows multimodal patterns, dominant anomaly cues, and the corresponding preferred action class used for evaluation.

## Table 1: Related-Work Capability Comparison

### Columns

- Work
- RPM or PGHD input
- Anomaly detection
- LLM or RAG support
- Medication-safety or compatibility logic
- Clinician review
- End-to-end action workflow

### Rows

- RemoteHealthConnect
- smartwatch RPM system based on activeDCM
- AI for integrating EHR and PGHD in CDS
- healthcare time-series anomaly detection
- guideline-grounded LLM CDS
- retrieval-augmented diagnosis support
- medication-safety co-pilot study
- this work

## Table 2: Main Experimental Comparison

### Columns

- Model
- Relevant precision
- Unsafe suggestion rate
- Irrelevant suggestion rate
- Clinician acceptance
- Dispatch precision

### Current values

| Model | Relevant Precision | Unsafe Rate | Irrelevant Rate | Clinician Acceptance | Dispatch Precision |
|---|---:|---:|---:|---:|---:|
| Threshold+Template | 0.5542 | 0.1417 | 0.3042 | 0.3125 | 1.0000 |
| Summary-Only Assistant | 0.6729 | 0.1479 | 0.1792 | 0.3021 | 1.0000 |
| Agentic RPM | 0.6708 | 0.0958 | 0.2333 | 0.4479 | 1.0000 |

## Table 3: Ablations and Failure Modes

### Ablation rows

- Agentic RPM
- no retrieval
- no patient history
- no clinician gate

### Metrics

- relevant precision
- unsafe suggestion rate
- clinician acceptance

### Failure-mode bullets

- anomaly recall remains low across all models
- summary-only system stays competitive on relevance but is weaker on safety
- clinician gate is necessary for workflow-safe dispatch

## Reproducibility Artifacts

### Included now

- draft paper: `Publication/paper/2026-03-27_bibm_paper_draft.md`
- paper outline: `Publication/paper/2026-03-27_bibm_paper_outline.md`
- protocol: `Experiment/analysis/2026-03-27_agentic_rpm_simulation_protocol.md`
- baseline summary: `Experiment/analysis/2026-03-27_threshold_template_baseline_summary.md`
- comparison summary: `Experiment/analysis/2026-03-27_comparison_results_summary.md`
- raw results: `Experiment/analysis/comparison_results.json`
- runnable code: `Experiment/core_code/run_experiment.py`

### Still needed later

- venue-formatted manuscript
- rendered figures
- formal bibliography file
- repeated-seed result tables
