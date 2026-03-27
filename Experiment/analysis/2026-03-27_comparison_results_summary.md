# Initial Comparison Results Summary

## Run Configuration

- patients: 60
- weeks per patient: 8
- total patient-weeks: 480
- seed: 7

## Compared Systems

- `threshold_template`
- `summary_only_assistant`
- `agentic_rpm`
- `ablation_no_retrieval`
- `ablation_no_patient_history`
- `ablation_no_clinician_gate`

## Main Metrics

| Model | Relevant Precision | Unsafe Rate | Irrelevant Rate | Clinician Acceptance |
|---|---:|---:|---:|---:|
| Threshold+Template | 0.5542 | 0.1417 | 0.3042 | 0.3125 |
| Summary-Only Assistant | 0.6729 | 0.1479 | 0.1792 | 0.3021 |
| Agentic RPM | 0.6708 | 0.0958 | 0.2333 | 0.4479 |
| No Retrieval | 0.5917 | 0.1458 | 0.2625 | 0.4708 |
| No Patient History | 0.5979 | 0.1417 | 0.2604 | 0.4375 |
| No Clinician Gate | 0.6708 | 0.0958 | 0.2333 | 1.0000 |

## Interpretation

The initial comparison supports the proposed paper direction. Relative to the Threshold+Template baseline, the full Agentic RPM system improves clinically relevant precision from 0.5542 to 0.6708, reduces unsafe suggestion rate from 0.1417 to 0.0958, and increases clinician acceptance from 0.3125 to 0.4479.

The strongest non-agentic comparator in this run is the Summary-Only Assistant. It reaches similar relevance precision, but the full Agentic RPM system still produces a substantially lower unsafe suggestion rate and higher clinician acceptance. This provides a viable paper story: retrieval-backed compatibility checks and history-aware recommendation logic may improve safety and clinician trust even when raw relevance is roughly tied.

The ablations behave in the expected direction. Removing retrieval or patient history increases unsafe suggestions and lowers relevant precision. Removing the clinician gate makes all proposals dispatchable by definition, but effective dispatch precision drops to 0.4479, which reinforces the need for clinician review.

These are still early simulated results from a single seed. They are enough to justify drafting the paper around a prototype result set, but they should be expanded with repeated seeds and stronger anomaly modeling before being treated as final numbers.
