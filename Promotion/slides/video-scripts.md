# Narration Script: Agentic RPM for BIBM 2026

## Slide 1

This talk presents a simulation-first agentic remote patient monitoring workflow that converts multimodal patient-generated data into clinician-reviewable weekly summaries and next-step recommendations.

## Slide 2

Remote patient monitoring systems now collect continuous data such as activity, sleep, heart rate, and symptoms. The workflow bottleneck is no longer only data collection. The harder problem is transforming these signals into safe, reviewable actions without overloading clinicians.

## Slide 3

The central question is whether an agentic system can draft clinician-reviewable next-step recommendations from RPM data without increasing unsafe or irrelevant suggestions. Prior work gives us pieces of the solution, but usually not the full integrated workflow.

## Slide 4

Our workflow starts with multimodal patient data, generates a structured weekly summary, detects anomalies, retrieves compatibility-relevant context, proposes a constrained next action, sends that proposal through clinician review, and only then dispatches downstream tasks.

## Slide 5

The system is intentionally constrained. It can recommend monitoring only, repeat measurement, lab work, medication review, follow-up, or urgent escalation. This keeps the action space auditable and avoids overclaiming autonomous clinical decision-making.

## Slide 6

We evaluate the workflow in a synthetic patient-week simulator. Each example includes daily multimodal observations, short longitudinal history, anomaly scenarios, and ground-truth labels for preferred, unsafe, and irrelevant actions.

## Slide 7

We compare three main systems: a Threshold plus Template baseline, a Summary-Only Assistant, and the full Agentic RPM model. We also run ablations without retrieval, without patient history, and without the clinician gate.

## Slide 8

Against the Threshold plus Template baseline, the full Agentic RPM model improves clinically relevant precision from 0.5542 to 0.6708, reduces unsafe suggestion rate from 0.1417 to 0.0958, and raises clinician acceptance from 0.3125 to 0.4479.

## Slide 9

A stronger comparison comes from the Summary-Only Assistant. It reaches a similar relevance score, but the full Agentic RPM model still produces fewer unsafe suggestions and substantially higher clinician acceptance. That suggests the main gain is safety-oriented recommendation shaping, not just raw relevance.

## Slide 10

The ablations support that interpretation. Removing retrieval or patient history degrades both precision and safety. Removing the clinician gate makes every proposal dispatchable by definition, but workflow-safe dispatch drops sharply, reinforcing the importance of human review.

## Slide 11

The current study remains limited. All data are synthetic, the recommendation logic is still heuristic, anomaly recall is low, and the presented results come from a single seed. These constraints should stay explicit in the paper.

## Slide 12

The next steps are stronger anomaly modeling, repeated-seed analysis, richer retrieval sources, and eventually real data integration through systems such as OpenClaw or Apple Health once the workflow is validated in simulation.

## Slide 13

In summary, a simulation-first agentic RPM workflow appears feasible, and the most credible contribution is safer, clinician-reviewable action drafting rather than autonomous treatment recommendation.
