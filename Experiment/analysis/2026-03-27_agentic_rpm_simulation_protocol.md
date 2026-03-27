# Agentic RPM Simulation Protocol

## Purpose

This document defines the experiment protocol for a simulation-first study of an agentic remote patient monitoring pipeline. The goal is to test whether the system can generate clinician-reviewable next-step recommendations from synthetic multimodal patient-generated health data while avoiding increases in unsafe or irrelevant suggestions.

## Experimental Hypothesis

The full agentic RPM pipeline, which combines interpretable anomaly detection, retrieval-backed compatibility checks, and clinician gating, will achieve higher clinically relevant recommendation precision and clinician acceptance than simpler baselines, while maintaining or reducing unsafe and irrelevant suggestion rates.

## Unit of Evaluation

The primary evaluation unit is a `patient-week`.

Each patient-week contains:
- one synthetic patient profile
- one 7-day observation window
- one latent clinical state
- one or more anomaly labels
- one ground-truth preferred action class
- one simulated clinician response to proposed actions

## Synthetic Patient Schema

### Static profile fields

- `patient_id`
- `age_group`
- `sex`
- `condition_cluster`
  - hypertension
  - diabetes risk
  - heart failure risk
  - arrhythmia risk
  - medication adherence risk
- `risk_tier`
  - low
  - medium
  - high
- `current_medications`
- `medication_constraints`
- `recent_lab_flags`
- `baseline_activity_level`
- `baseline_resting_hr`
- `baseline_sleep_duration`
- `baseline_sleep_variability`

### Daily observation fields

For each day in the week:
- `steps`
- `resting_hr`
- `active_hr`
- `sleep_start_time`
- `sleep_duration_hours`
- `sleep_irregularity_score`
- `symptom_score`
- `symptom_tags`
- `medication_adherence`
- `home_measurements`
  - optional blood pressure
  - optional glucose
  - optional weight

### Longitudinal history fields

- prior 2-4 weeks of summary statistics
- recent clinician-approved actions
- prior clinician rejections
- prior abnormal labs
- unresolved issues carried from earlier weeks

## Synthetic Cohort Design

Initial target cohort for the paper:
- 300-1000 synthetic patients
- 8-12 simulated weeks per patient

This gives enough variety for:
- baseline comparisons
- ablation analysis
- error analysis by risk tier and anomaly type

Train and test splits should be patient-level, not week-level, to avoid leakage.

## Action Ontology

The recommendation module may only output one of the following:

1. `monitor_only`
2. `repeat_measurement`
3. `lab_order`
4. `medication_review`
5. `follow_up_visit`
6. `urgent_escalation`

Optional secondary fields:
- `supporting_rationale`
- `supporting_evidence_items`
- `safety_flags`
- `dispatch_target`

## Anomaly Scenario Library

Each patient-week can contain zero, one, or multiple anomaly scenarios. Initial scenario library:

1. `reduced_activity_with_sleep_disruption`
   - step decline
   - worsening sleep duration or regularity
   - mild symptom increase
   - likely actions: monitor, repeat measurement, follow-up

2. `rising_resting_hr_trend`
   - progressive resting heart rate increase
   - possible activity decline
   - likely actions: follow-up, lab order, medication review

3. `medication_nonadherence_pattern`
   - missed doses
   - rebound symptoms or instability
   - likely actions: repeat measurement, medication review, follow-up

4. `possible_fluid_or_weight_related_decline`
   - activity drop
   - symptom increase
   - optional weight increase
   - likely actions: lab order, urgent escalation, follow-up

5. `arrhythmia_like_pattern`
   - abnormal heart-rate variability or tachycardia episodes
   - likely actions: urgent escalation or follow-up

6. `stable_recovery`
   - improving trend after prior intervention
   - likely action: monitor only

7. `spurious_single_day_outlier`
   - noise event without persistent trend
   - likely action: monitor only or repeat measurement

The simulator should also generate negative cases with no clinically meaningful anomaly.

## Ground-Truth Labeling Rules

Each patient-week should have:
- `primary_anomaly_label`
- `secondary_anomaly_labels`
- `ground_truth_action`
- `unsafe_action_set`
- `irrelevant_action_set`

Ground-truth actions are assigned by deterministic scenario rules plus patient-history constraints.

Example:
- If rising resting heart rate is sustained for at least 4 of 7 days and the patient has high-risk cardiac history, `urgent_escalation` or `follow_up_visit` becomes preferred depending on severity.
- If a medication review would conflict with a known medication constraint, then `medication_review` may become unsafe for that patient-week.
- If a stable recovery pattern is present, `lab_order` may be irrelevant unless a pending unresolved lab issue exists.

This rule-based label generation is important because it lets the study measure safety and relevance without pretending to have real clinician labels.

## Knowledge Base for Retrieval

The recommendation module should retrieve from a small curated synthetic or manually constructed knowledge base containing:
- action eligibility rules
- medication-constraint rules
- condition-specific caution rules
- prior-action conflict rules
- follow-up urgency policies
- simple test-selection guidance

The knowledge base should not be framed as a real clinical guideline source. For the paper, it is safer to describe it as a curated recommendation-compatibility knowledge base grounded by the literature review and restricted action ontology.

## Pipeline Specification

### Step 1: Structured Weekly Summary

Input:
- daily stream data
- short longitudinal history

Output fields:
- trend summary
- dominant anomalies
- risk tier summary
- missing-data note
- candidate action triggers

### Step 2: Anomaly Detection

Preferred main design:
- explicit features derived from the week
- rule or simple model for anomaly candidates
- optional LLM interpretation over flagged signals

This keeps anomaly detection auditable and avoids overclaiming LLM-native time-series reasoning.

### Step 3: Retrieval-Backed Recommendation

Input:
- structured summary
- anomaly outputs
- patient history
- safety knowledge base retrieval

Output:
- recommended action class
- supporting rationale
- supporting evidence references
- safety warning flags

### Step 4: Simulated Clinician Review

Given:
- patient-week state
- proposed action
- supporting rationale

The clinician simulator outputs:
- `accept`
- `reject_as_irrelevant`
- `reject_as_unsafe`
- `revise_needed`

The clinician policy is based on ground-truth action alignment and safety rules.

### Step 5: Task Dispatch

If accepted:
- generate downstream task record
- assign target destination
  - patient
  - lab
  - clinician schedule queue

If not accepted:
- no dispatch
- retain rejection reason for analysis

## Baselines

### Baseline A: Threshold+Template

- hand-coded anomaly thresholds
- static weekly summary template
- direct rule map from anomaly to action
- no retrieval
- no explicit compatibility layer

### Baseline B: Summary-Only Assistant

- weekly summary generation
- direct action proposal from summary
- no retrieval-backed compatibility checking
- clinician gate remains active

### Main Model: Agentic RPM

- structured weekly summary
- interpretable anomaly detection
- retrieval-backed compatibility checking
- clinician gate
- downstream task dispatch

## Ablations

1. `no_retrieval`
   - recommendation without compatibility retrieval
2. `no_patient_history`
   - recommendation from current week only
3. `no_clinician_gate`
   - dispatch after recommendation without approval
4. `summary_only_signals`
   - no anomaly module, only summary-based reasoning

## Metric Definitions

### Primary metrics

1. `clinically_relevant_precision`
   - fraction of proposed actions that match the ground-truth relevant action set

2. `unsafe_suggestion_rate`
   - fraction of patient-weeks where the proposed action belongs to the unsafe action set

3. `irrelevant_suggestion_rate`
   - fraction of patient-weeks where the proposed action belongs to the irrelevant action set

4. `clinician_acceptance_rate`
   - fraction of proposals accepted by the clinician simulator

### Secondary metrics

5. `summary_completeness`
   - rule-based score for whether the weekly summary mentions dominant trends, anomaly cues, and recent context

6. `anomaly_detection_precision`
7. `anomaly_detection_recall`
8. `compatibility_check_error_rate`
   - fraction of weeks where the model fails to flag a known incompatibility or incorrectly flags a safe action
9. `dispatch_precision`
   - fraction of dispatched tasks that are correct given accepted action and target destination

### Optional aggregate metrics

- safety-adjusted action utility
- acceptance-weighted precision

## Evaluation Slices

Report results by:
- risk tier
- anomaly type
- action class
- presence or absence of medication constraints
- single-anomaly versus multi-anomaly weeks

These slices will strengthen the error analysis section.

## Statistical Plan

- Run at least 3 random seeds for simulator generation and model evaluation if stochastic components are used.
- Report mean and standard deviation for each metric.
- Use paired comparisons across patient-weeks where possible.
- Prefer bootstrap confidence intervals or paired nonparametric tests for metric differences if sample sizes are modest.

## Minimal Implementation Milestones

### Milestone 1

- synthetic patient schema
- 3 anomaly scenarios
- Threshold+Template baseline
- metric computation

### Milestone 2

- full 6-class action ontology
- retrieval-backed compatibility layer
- clinician simulator
- ablation hooks

### Milestone 3

- expanded anomaly library
- paper-ready tables
- case-study generation

## Risks and Controls

### Risk: synthetic labels are too easy

Control:
- add overlapping symptoms
- add noise and incomplete data
- include ambiguous weeks that permit more than one relevant action

### Risk: system appears clinically overclaimed

Control:
- keep action space constrained
- keep clinician gate mandatory
- describe knowledge base as simulated and curated

### Risk: retrieval value is not measurable

Control:
- define compatibility rules that genuinely require patient history
- include ablation without retrieval

## Recommended Next Build Order

1. Implement simulator and deterministic ground-truth labeling.
2. Implement Threshold+Template baseline.
3. Implement structured summary format.
4. Add retrieval-backed recommendation layer.
5. Add clinician simulator and dispatch logic.
6. Run baselines and ablations.
