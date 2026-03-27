# Paper Outline for BIBM 2026

## Tentative Title

Agentic Remote Patient Monitoring with Clinician-Reviewable Next-Step Recommendations from Synthetic Multimodal Patient Data

## Abstract

- Clinical motivation: RPM generates growing volumes of patient-generated data, but clinicians still lack workflow-ready tools that translate these signals into safe, reviewable next-step recommendations.
- Gap: prior work studies RPM, anomaly detection, LLM-based clinical support, and medication safety largely in isolation.
- Method: simulation-first agentic RPM pipeline with weekly summarization, anomaly detection, retrieval-backed compatibility checking, clinician review, and downstream task dispatch.
- Results: full agentic system improves clinically relevant precision and reduces unsafe suggestions versus Threshold+Template while increasing clinician acceptance.
- Contribution: simulation framework, workflow architecture, safety-oriented comparison, and future roadmap toward real OpenClaw integration.

## 1. Introduction

### 1.1 Motivation

- RPM and wearable systems generate continuous streams of patient-generated health data.
- Clinician burden remains high because raw time series do not directly translate into action.
- Pure alerting systems are insufficient; clinicians need concise summaries and reviewable next steps.

### 1.2 Problem Statement

- The target problem is not just anomaly detection.
- The operational task is transforming weekly multimodal patient data into action proposals that remain clinically relevant while avoiding unsafe or irrelevant suggestions.

### 1.3 Research Question

- Can an agentic system draft clinician-reviewable next-step recommendations from RPM data without increasing unsafe or irrelevant suggestions?

### 1.4 Contributions

- A simulation-first agentic RPM workflow for weekly summary generation, recommendation drafting, clinician review, and downstream task dispatch.
- A synthetic patient-week evaluation framework with anomaly scenarios, ground-truth action labels, safety constraints, and clinician-review simulation.
- A comparison across rule-based, summary-only, and retrieval-backed agentic systems with ablations.

### 1.5 Paper Organization

- Related work
- System design
- Simulation protocol
- Results
- Discussion and future work

## 2. Related Work

### 2.1 Remote Patient Monitoring and PGHD

- RPM platforms and clinician dashboards
- integration of patient-generated data into decision support

### 2.2 Wearable Anomaly Detection

- healthcare time-series anomaly detection
- explainability challenges

### 2.3 LLM and RAG Clinical Decision Support

- guideline-grounded LLM systems
- retrieval-augmented clinical support

### 2.4 Medication Recommendation and Safety

- medication recommendation from longitudinal history
- medication-safety co-pilots
- DDI and compatibility modeling

### 2.5 Gap Summary

- no strong end-to-end benchmark connecting RPM streams to clinician-reviewable action proposals with safety checks

## 3. System Overview

### 3.1 Workflow

- data ingestion
- weekly summary generation
- anomaly detection
- retrieval-backed recommendation generation
- clinician review
- task dispatch

### 3.2 Action Ontology

- monitor only
- repeat measurement
- lab order
- medication review
- follow-up visit
- urgent escalation

### 3.3 Safety Design Principles

- constrained action space
- compatibility layer
- clinician gate
- simulation-only claims

## 4. Simulation Environment and Experimental Protocol

### 4.1 Patient-Week Formulation

- patient-week as unit of evaluation

### 4.2 Synthetic Patient Schema

- static profile
- daily observations
- longitudinal history

### 4.3 Scenario Library

- stable recovery
- spurious outlier
- activity and sleep decline
- rising heart-rate trend
- medication nonadherence
- fluid or weight decline
- arrhythmia-like pattern

### 4.4 Ground-Truth Labeling

- preferred action
- relevant action set
- unsafe action set
- irrelevant action set

### 4.5 Baselines and Ablations

- Threshold+Template
- Summary-Only Assistant
- Agentic RPM
- no retrieval
- no patient history
- no clinician gate

### 4.6 Metrics

- clinically relevant precision
- unsafe suggestion rate
- irrelevant suggestion rate
- clinician acceptance rate
- anomaly precision and recall
- dispatch precision

## 5. Results

### 5.1 Main Comparison

- Agentic RPM vs Threshold+Template
- Agentic RPM vs Summary-Only Assistant

### 5.2 Safety and Acceptance

- lower unsafe rate
- higher clinician acceptance

### 5.3 Ablation Analysis

- effect of retrieval
- effect of patient history
- effect of clinician gate

### 5.4 Error Analysis

- remaining irrelevant suggestions
- anomaly recall bottleneck
- failure modes by scenario type

## 6. Discussion

### 6.1 Interpretation

- agentic workflow appears most valuable through safety and reviewability rather than raw relevance alone

### 6.2 Limitations

- synthetic data only
- heuristic recommendation policies
- single-seed initial results
- simplified clinician simulator

### 6.3 Threats to Validity

- simulator realism
- evaluation label bias
- constrained action ontology

### 6.4 Future Work

- stronger anomaly models
- repeated seeds and statistical testing
- richer retrieval sources
- OpenClaw and Apple Health integration

## 7. Conclusion

- summarize workflow contribution
- summarize main safety and acceptance findings
- emphasize simulation-first scope and future deployment path

## Figures and Tables

- Figure 1: system architecture and clinician-review loop
- Figure 2: example synthetic patient-week trajectories
- Table 1: recent-work capability comparison
- Table 2: main experimental comparison
- Table 3: ablation and error analysis
