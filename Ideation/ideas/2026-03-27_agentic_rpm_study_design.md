# Agentic RPM Study Design for BIBM 2026

## Objective

Define a simulation-first study design for an agentic remote patient monitoring system that converts synthetic multimodal patient-generated health data into weekly clinician summaries and clinician-reviewable next-step recommendations while minimizing unsafe or irrelevant suggestions.

## Final Framing

The paper should be positioned as a workflow-evaluation and safety-analysis study, not as a real-world clinical deployment claim. The core contribution is an end-to-end simulation environment and agentic decision pipeline that links four stages:

1. Longitudinal multimodal patient data ingestion.
2. Weekly summary and anomaly detection.
3. Retrieval-backed recommendation drafting with compatibility checks.
4. Clinician approval and downstream task dispatch.

This framing is stronger than claiming a generic medical agent because it makes the contribution measurable and keeps the study within a publishable, simulation-first scope.

## System Boundary

### In scope

- Synthetic patient cohort generation.
- Daily multimodal signals:
  - step count
  - resting and active heart rate
  - sleep start time, duration, and variability
  - symptom or self-report events
  - medication adherence events
- Synthetic patient history:
  - demographics bucket
  - chronic conditions
  - current medications
  - prior abnormal labs
  - recent clinician actions
- Weekly clinician summary generation.
- Anomaly detection over the weekly window.
- Recommendation generation with retrieval over patient history and a curated action-safety knowledge base.
- Clinician approval or rejection simulation.
- Downstream task dispatch in simulation.

### Out of scope

- Live EHR integration.
- Direct Apple Health access.
- Autonomous prescription changes without clinician review.
- Claims of clinical efficacy in real patients.

## Action Taxonomy

The recommendation space should remain narrow and auditable. Recommended action classes:

1. `monitor_only`
   - No immediate intervention.
   - Continue RPM and reassess next week.
2. `repeat_measurement`
   - Ask patient for extra home measurements or symptom confirmation.
   - Examples: blood pressure check, symptom diary, repeat wearable sync.
3. `lab_order`
   - Suggest blood work or urine testing.
   - Examples: CBC, CMP, HbA1c, lipid panel, thyroid panel.
4. `medication_review`
   - Suggest clinician review of a current medication or possible adjustment candidate.
   - The system drafts a review rationale, not an autonomous prescription.
5. `follow_up_visit`
   - Suggest telehealth or in-person follow-up.
6. `urgent_escalation`
   - Route to urgent clinician attention because trends exceed a high-risk threshold.

This constrained action space is preferable to open-ended treatment generation because it is easier to simulate, safer to evaluate, and better aligned with a clinician-review workflow.

## Recommended Architecture

### Module A: Synthetic Patient Simulator

Generate weekly patient trajectories with:
- baseline health profile
- day-level variation
- injected anomaly events
- medication context
- latent ground-truth recommended action

Examples of anomaly patterns:
- progressive resting-heart-rate elevation with sleep disruption
- reduced activity plus weight or symptom burden increase
- medication nonadherence with rebound symptoms
- persistent tachycardia after a medication change
- abnormal recovery trend after a prior intervention

### Module B: Weekly Summarizer

Input:
- 7-day multimodal observations
- prior 2-4 weeks of context
- key patient history

Output:
- structured weekly report
- trend bullets
- anomaly candidates

Prefer a structured summary template first. An LLM can optionally produce clinician-readable narrative from structured fields.

### Module C: Anomaly Detection

Compare three options:
- `B1 Rule-based baseline`: threshold and delta rules over features.
- `B2 Classical ML baseline`: anomaly score from simple time-series features.
- `M1 Agentic pipeline`: anomaly detection plus LLM-assisted interpretation of flagged patterns.

The LLM should not be the sole anomaly detector in the main claim. A better design is to let explicit signal changes trigger candidate anomalies and use the language model for interpretation and synthesis.

### Module D: Retrieval-Backed Recommendation Layer

Inputs:
- structured weekly summary
- anomaly findings
- patient history
- medication list
- prior labs
- curated safety knowledge base

Retrieved context should include:
- contraindication or incompatibility snippets
- action eligibility constraints
- patient-history compatibility checks
- test-selection guidance

Output:
- top recommended action class
- concise rationale
- supporting evidence items
- explicit safety flags

### Module E: Clinician Review Policy

The clinician is the decision authority. The simulator should label each proposal as:
- `accept`
- `reject_as_irrelevant`
- `reject_as_unsafe`
- `revise_needed`

This makes the paper's main question measurable and gives a principled definition of unsafe versus irrelevant.

### Module F: Task Dispatch

Only after simulated clinician acceptance:
- create a lab task
- create a follow-up scheduling task
- create a patient message
- create a clinician review note

Dispatch precision should be measured separately from recommendation quality.

## Baselines and Ablations

### Baselines

1. `Threshold+Template`
   - Rule-based anomaly detection.
   - Static weekly template.
   - Fixed action mapping rules.

2. `Summary-Only Assistant`
   - Generates weekly summary.
   - No retrieval-backed compatibility checks.
   - No explicit clinician-decision modeling beyond acceptance labeling.

### Main system

3. `Agentic RPM`
   - Structured summary.
   - anomaly detection
   - retrieval-backed compatibility checking
   - explicit clinician review
   - downstream task dispatch

### Ablations

4. `Agentic RPM w/o Retrieval`
   - Removes compatibility retrieval.

5. `Agentic RPM w/o Patient History`
   - Uses current week only.

6. `Agentic RPM w/o Clinician Gate`
   - Measures how unsafe downstream actions increase when approval is removed.

The last ablation is useful analytically even if not presented as a deployable configuration.

## Safety and Relevance Definitions

### Unsafe suggestion

A recommendation is unsafe if it:
- conflicts with known medication or condition constraints,
- proposes escalation inconsistent with the underlying simulated state,
- omits a higher-priority urgent response when one is required,
- or suggests a downstream action that would violate the synthetic patient's compatibility rules.

### Irrelevant suggestion

A recommendation is irrelevant if it:
- does not address the dominant anomaly or trend,
- is not justified by the available weekly evidence,
- duplicates a recently completed action without rationale,
- or adds workflow burden without likely clinical value.

### Actionable suggestion

A recommendation is actionable if the simulated clinician could reasonably review, approve, and dispatch it based on the weekly summary and supporting rationale.

## Evaluation Targets

Primary outcomes:
- unsafe suggestion rate
- irrelevant suggestion rate
- clinically relevant recommendation precision

Secondary outcomes:
- clinician acceptance rate
- summary completeness and usefulness
- anomaly detection recall and precision
- compatibility-check error rate
- downstream task-dispatch precision

## Why This Framing Fits BIBM

- It combines biomedical informatics workflow design with AI reasoning and safety evaluation.
- It is specific enough to implement without overclaiming real-world readiness.
- It produces a clear comparison story: does the full agentic workflow outperform simpler baselines without increasing harmful suggestions?

## Recommended Next Experiment Decisions

1. Use a narrow action ontology with 5-6 action classes.
2. Keep recommendation generation clinician-reviewable, never autonomous.
3. Treat retrieval and patient-history compatibility as the core differentiator.
4. Use a hybrid anomaly module rather than claiming LLM-only anomaly detection.
5. Build simulation labels that support both relevance and safety scoring.
