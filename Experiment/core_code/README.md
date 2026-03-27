# Agentic RPM Core Code

Initial simulation-first experiment scaffold for the BIBM 2026 agentic RPM study.

## Files

- `simulator.py`: synthetic patient and patient-week generator
- `baseline.py`: Threshold+Template baseline
- `metrics.py`: evaluation metrics for recommendation quality and safety
- `run_experiment.py`: end-to-end runner for the baseline experiment

## Run

```bash
python3 Experiment/core_code/run_experiment.py
```

Optional arguments:

```bash
python3 Experiment/core_code/run_experiment.py --num-patients 100 --num-weeks 8 --seed 7
```

Default output:

```text
Experiment/analysis/comparison_results.json
```
