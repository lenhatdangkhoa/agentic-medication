# BIBM 2026 Submission Checklist

## Manuscript

- [x] Title aligned with simulation-first contribution
- [x] Abstract reports the problem, method, and initial quantitative results
- [x] Introduction states the research question and contribution scope
- [x] Related work covers RPM, PGHD, anomaly detection, LLM or RAG clinical support, and medication safety
- [x] Method section describes the workflow, action ontology, and clinician-review boundary
- [x] Experiment section defines the patient-week unit, simulator, baselines, ablations, and metrics
- [x] Results section reports the current comparison outcome
- [x] Discussion states limitations and threats to validity
- [x] Conclusion keeps OpenClaw and Apple Health integration in future work

## Results and Claims

- [x] Simulation-only scope is explicit throughout the draft
- [x] Main quantitative comparison between Threshold+Template and Agentic RPM is documented
- [x] Strong non-agentic comparator is included through Summary-Only Assistant
- [x] Retrieval, history, and clinician-gate ablations are included
- [x] Safety-oriented metrics are reported explicitly
- [ ] Multi-seed runs and uncertainty estimates still need to be added before final submission
- [ ] Scenario-slice error analysis still needs a paper-ready table

## Figures and Tables

- [x] Figure and table plan is defined
- [ ] Figure 1 system architecture still needs to be drawn
- [ ] Figure 2 synthetic trajectory examples still need to be rendered
- [ ] Table 1 related-work capability comparison still needs to be formatted
- [ ] Table 2 main results table still needs to be formatted
- [ ] Table 3 ablation and failure-mode table still needs to be formatted

## References

- [x] Core references for the paper motivation and method positioning have been verified against PubMed
- [ ] Full bibliography still needs a complete reference audit and venue-specific formatting pass
- [ ] Every in-text claim should be rechecked against the final bibliography before submission

## Reproducibility Package

- [x] Core simulation code is present in `Experiment/core_code`
- [x] Initial comparison results are saved in `Experiment/analysis/comparison_results.json`
- [x] Protocol document is saved in `Experiment/analysis/2026-03-27_agentic_rpm_simulation_protocol.md`
- [ ] Add a lightweight run script or Makefile for one-command reproduction
- [ ] Add environment and dependency documentation if external packages are introduced later

## Recommended Next Publication Actions

1. Convert the current markdown draft into the target BIBM paper template.
2. Add paper-ready tables from the saved JSON metrics.
3. Run repeated seeds and update the Results section with uncertainty estimates.
4. Perform a full citation audit before final submission.
