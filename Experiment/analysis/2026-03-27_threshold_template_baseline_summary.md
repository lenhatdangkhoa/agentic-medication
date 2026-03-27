# Threshold+Template Baseline Summary

## Run Configuration

- patients: 60
- weeks per patient: 8
- total patient-weeks: 480
- seed: 7

## Metrics

- clinically relevant precision: 0.5542
- unsafe suggestion rate: 0.1417
- irrelevant suggestion rate: 0.3042
- clinician acceptance rate: 0.3125
- dispatch precision: 1.0000
- anomaly detection precision: 0.9960
- anomaly detection recall: 0.3568

## Interpretation

The initial Threshold+Template baseline is conservative and mechanically consistent, but it leaves substantial headroom for the full agentic system. Precision on clinically relevant actions is moderate, while irrelevant suggestions remain common and clinician acceptance is low. The anomaly detector is precise but under-recalls the expected anomaly patterns, which is a useful baseline failure mode for later comparison.

These numbers should not be treated as final paper results. They are an initial end-to-end sanity check confirming that the simulation, rule baseline, and evaluation pipeline are runnable.

## Produced Artifacts

- JSON results: `Experiment/analysis/threshold_template_results.json`
- Code: `Experiment/core_code/simulator.py`, `Experiment/core_code/baseline.py`, `Experiment/core_code/metrics.py`, `Experiment/core_code/run_experiment.py`
