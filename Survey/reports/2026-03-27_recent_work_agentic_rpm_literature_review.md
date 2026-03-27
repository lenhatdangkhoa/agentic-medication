# Recent Work Review for Agentic Remote Patient Monitoring

## Scope

This review surveys recent work relevant to a BIBM 2026 paper on a simulation-first agentic remote patient monitoring system that converts multimodal patient-generated health data into weekly clinician summaries, detects concerning trends, and drafts clinician-reviewable next-step recommendations. The search emphasis was 2024-2025 work spanning four linked areas:

1. Remote patient monitoring and patient-generated health data integration.
2. Wearable and multivariate time-series anomaly detection.
3. Large language models and retrieval-augmented generation for clinical decision support.
4. Medication recommendation and medication-safety support.

## Executive Summary

Recent work supports the feasibility of the individual components of the proposed system, but not the full end-to-end workflow. Existing literature shows that RPM systems can collect and visualize wearable data for clinicians, AI can analyze longitudinal health signals, and LLM or RAG systems can support parts of clinical reasoning and medication safety. However, the reviewed papers do not establish a mature benchmark for a clinician-in-the-loop agentic workflow that starts with multimodal patient-generated data and ends with clinician-reviewable next-step recommendations plus downstream task orchestration.

The clearest opening for this project is therefore not to claim real-world deployment, but to evaluate the workflow in simulation: whether an agentic system can improve recommendation relevance and actionability while keeping unsafe or irrelevant suggestions low relative to simpler baselines.

## Key Findings

- **RPM systems already ingest wearable data, but usually stop at monitoring and visualization** [1][2][3][4].
- **PGHD and EHR integration is recognized as promising for clinical decision support, but heterogeneous data handling and workflow integration remain open problems** [5][6].
- **Anomaly detection for healthcare time series is active, but the literature is still dominated by detection-centric methods rather than recommendation-centric workflows** [7][8][9].
- **LLM-based clinical decision support is moving toward guideline-grounded and retrieval-augmented designs, especially for constrained reasoning tasks** [10][11][12][13].
- **Medication recommendation and medication-safety studies show that patient history, specialty context, and safety knowledge matter, but they are usually evaluated separately from RPM streams** [14][15][16][17][18].

## Thematic Analysis

### 1. Remote Patient Monitoring and PGHD Integration

Remote patient monitoring studies increasingly emphasize continuous wearable collection and clinician-facing dashboards rather than episodic manual review. `RemoteHealthConnect` presents a web-based platform coupled with wearable biosensors and custom visualizations intended to support clinician monitoring and faster decision-making [1]. A smartwatch-based RPM system built around the `activeDCM` trial similarly focuses on collection, feedback, and usability in a real trial context [2]. These papers are useful system references for data flow and clinician presentation, but they do not appear to generate explicit next-step care recommendations.

At the policy and informatics layer, PGHD integration is now well recognized as clinically important. Nazi et al. characterize PGHD as a rapidly expanding data source created between visits through consumer health technologies and RPM systems [5]. Ye et al. review AI for integrated EHR and PGHD decision support and report that the literature already points to benefits such as improved risk classification and more precise recommendations, while also highlighting major barriers in interoperability, security, interpretation, and meaningful workflow use [6]. This review is especially relevant because it directly supports the premise that patient-generated data can contribute to clinical decision support, but also implies that the main unsolved issue is not raw access to data alone. The harder issue is how to transform longitudinal heterogeneous data into clinically useful decisions without overloading or misleading clinicians.

Together, these papers suggest that your project should not position itself as another RPM dashboard. The stronger claim is a workflow contribution: weekly synthesis and action proposal from multimodal longitudinal data, with clinician review retained as the decision boundary.

### 2. Wearable and Multivariate Time-Series Anomaly Detection

The wearable-health literature confirms that signal complexity is large enough to justify automated anomaly detection. Ferrara's 2024 survey argues that wearable sensor data have already outgrown simple heuristic analysis pipelines and now motivate more advanced modeling for health monitoring and behavioral interpretation [7]. Abdelaal et al. review explainability in wearable analytics and show that interpretability remains a major concern when these models are used in health settings [8]. That concern matters for your paper because anomaly flags that feed a recommendation pipeline need to be understandable to a clinician, not just statistically strong.

Khanizadeh et al. specifically frame anomaly detection in healthcare time series as a decision-support problem, but the output remains anomaly identification rather than downstream action generation [9]. The gap is important. Detecting abnormal sleep, step, heart-rate, or symptom trajectories is only the first half of your proposed workflow. The second half is deciding what action, if any, should be suggested and whether that suggestion is compatible with patient history and medication context.

This theme supports a design choice for the experiment section: treat anomaly detection as a modular component with interpretable outputs that can be ablated independently from recommendation generation.

### 3. LLM and RAG Clinical Decision Support

Recent LLM-CDS work is relevant, but the strongest papers are still mostly task-bounded. Oniani et al. show that incorporating clinical practice guidelines into LLM prompting can improve decision support for a constrained outpatient treatment task, using structured strategies such as decision trees and graph-based representations [10]. Li et al. extend this direction by combining generation with retrieval and clinical guidelines for diagnosis support [11]. Prabha et al. examine adaptive retrieval for RAG-based clinical decision support and argue that retrieval quality is a central determinant of performance [12]. Noll et al. apply RAG to emergency-care decision-making, again in a bounded guideline-intensive setting [13].

These studies support the technical instinct behind your proposal: recommendation generation should not rely on a free-running LLM alone. It should be grounded in retrieved context such as prior history, medication knowledge, and possibly guideline or policy constraints. They also imply that a simulation-first study can be methodologically strong if it evaluates not only final recommendations, but also the effect of retrieval or safety constraints through ablations.

Separate from RAG, emerging evaluation studies show both promise and risk in LLM clinical use. Wang et al. compare LLMs on actual clinical cases and report that clinical decision performance is improving but remains variable across models and cases [19]. Schwieger et al. show LLM utility for structured discharge summary generation from EHR data [20]. These are adjacent to your weekly-summary task and suggest that clinician-facing narrative synthesis is plausible, but should still be measured for usefulness and error rather than assumed.

### 4. Medication Recommendation and Medication Safety

Medication recommendation literature is mature enough to inform the recommendation module, but most models use EHR visit histories instead of RPM streams. ACDNet and the hierarchical network by Chairat et al. both use longitudinal visit information to improve personalized medication recommendation [14][15]. These studies are useful references for modeling patient history, but they do not directly address clinician review, PGHD-triggered actions, or deployment safety in RPM settings.

Safety-aware clinical support is a closer match. Bucker et al. study AI-assisted pharmacotherapy decision-making as a feasibility problem, indicating that this area is clinically important but not solved [16]. Ong et al. provide especially relevant evidence: in 2025 they evaluated an LLM-based medication-safety CDS pipeline across 16 specialties using prescribing-error scenarios, and the best results came from a human-plus-LLM co-pilot mode rather than autonomous use [17]. That finding aligns closely with your proposed clinician-review loop and supports human oversight as a central system design principle rather than a limitation.

Drug-drug interaction work adds another layer. Luo et al. review deep-learning and knowledge-graph approaches to DDI prediction [18], while several 2024 papers push interpretability and knowledge-based DDI modeling [21][22]. This literature suggests that a compatibility-checking stage should be treated as its own knowledge-grounded safety layer, not merely folded into generic recommendation prompting.

## Areas of Consensus

- PGHD and RPM data have substantial clinical potential, especially when integrated with clinical context [5][6].
- Longitudinal wearable and health-log data are complex enough to warrant AI-based analysis rather than simple static review [7][9].
- LLM-based clinical support is more defensible when grounded in retrieved evidence or explicit guidelines [10][11][12][13].
- Medication-related recommendation systems need patient history and safety context, and human oversight remains important [14][15][17][18].

## Areas of Debate or Uncertainty

- Whether LLM-centered approaches should be used for anomaly detection directly, versus used only for interpretation of signals detected by classical or neural time-series models.
- How much retrieval and guideline grounding is enough to reduce hallucinated or unsafe clinical suggestions in realistic workflows.
- Whether synthetic data can approximate enough clinical complexity to make recommendation-safety conclusions meaningful for publication.
- How weekly summaries and recommendation proposals should be evaluated when clinician usefulness, safety, and actionability are not fully captured by a single metric.

## Research Gaps Relevant to This Project

1. **No strong end-to-end benchmark**: The reviewed work does not provide a standard evaluation setup for converting multimodal patient-generated streams into clinician-reviewable next-step recommendations with safety checks.
2. **Weak linkage between anomaly detection and action generation**: Existing anomaly-detection studies usually stop at identifying abnormal states rather than proposing or triaging next actions.
3. **Limited clinician-in-the-loop evaluation for RPM recommendations**: Human oversight appears beneficial in medication-safety studies, but this has not been clearly extended to weekly RPM action drafting.
4. **Safety layers are fragmented**: Patient history, guideline retrieval, and DDI or compatibility checks are usually evaluated in separate lines of work rather than as one recommendation pipeline.
5. **Simulation frameworks are underdeveloped**: Synthetic health-data literature exists [23], but there is still room for a simulator that jointly models patient trajectories, action proposals, clinician review, and downstream task routing.

## Implications for Paper Positioning

The paper should be framed as a systems-and-evaluation contribution, not a clinical deployment claim. A defensible contribution statement would be:

- A simulation framework for longitudinal multimodal RPM data and next-step action scenarios.
- An agentic pipeline that combines weekly summarization, anomaly detection, retrieval-backed recommendation drafting, and compatibility checking.
- A clinician-review loop that explicitly measures unsafe or irrelevant suggestion rates against simpler baselines.

This framing is stronger than claiming real-world therapeutic recommendation readiness. It aligns with the current literature, which supports the plausibility of the components but does not yet show a mature end-to-end solution.

## Candidate Comparison Table Fields for the Paper

- Input data type: wearable streams, symptoms, EHR, PGHD, medication history.
- Output type: monitoring dashboard, anomaly alert, summary, diagnosis aid, medication recommendation, safety check.
- Knowledge grounding: none, guidelines, retrieval, knowledge graph, historical visits.
- Human oversight: none, clinician review, pharmacist review, mixed co-pilot.
- Evaluation scope: simulation, retrospective cases, prospective cases, trial deployment.

## Sources

[1] Arun S, Sykes ER, Tanbeer S. RemoteHealthConnect: Innovating patient monitoring with wearable technology and custom visualization. *Digit Health*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39659398/

[2] A Remote Patient Monitoring System With Feedback Mechanisms Using a Smartwatch: Concept, Implementation, and Evaluation Based on the activeDCM Randomized Controlled Trial. *JMIR mHealth and uHealth*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39365164/

[3] Zalawadiya S, Lindenfeld J. Wearable Remote Patient Monitoring Devices: Ready for Prime Time? *JACC Heart Failure*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39632010/

[4] Damera VK, Cheripelli R, Putta N, et al. Enhancing remote patient monitoring with AI-driven IoMT and cloud computing technologies. *Scientific Reports*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/40617852/

[5] Nazi KM, Newton T, Armstrong CM. Unleashing the Potential for Patient-Generated Health Data (PGHD). *Journal of General Internal Medicine*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/38252246/

[6] Ye J, Woods D, Jordan N, Starren J. The role of artificial intelligence for the application of integrating electronic health records and patient-generated data in clinical decision support. *AMIA Joint Summits on Translational Science Proceedings*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/38827061/

[7] Ferrara E. Large Language Models for Wearable Sensor-Based Human Activity Recognition, Health Monitoring, and Behavioral Modeling: A Survey of Early Trends, Datasets, and Challenges. *Sensors*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39124092/

[8] Abdelaal Y, Aupetit M, Baggag A, Al-Thani D. Exploring the Applications of Explainability in Wearable Data Analytics: Systematic Literature Review. *Journal of Medical Internet Research*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39718820/

[9] Khanizadeh F, Ettefaghian A, Wilson G, et al. Smart data-driven medical decisions through collective and individual anomaly detection in healthcare time series. *International Journal of Medical Informatics*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/39566348/

[10] Oniani D, Wu X, Visweswaran S, et al. Enhancing Large Language Models for Clinical Decision Support by Incorporating Clinical Practice Guidelines. *IEEE International Conference on Healthcare Informatics*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/40092288/

[11] Li W, Zhang H, Zhang H, et al. Refine Medical Diagnosis Using Generation Augmented Retrieval and Clinical Practice Guidelines. *IEEE Journal of Biomedical and Health Informatics*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/41364573/

[12] Prabha S, Gomez-Cabello CA, Haider SA, et al. Enhancing Clinical Decision Support with Adaptive Iterative Self-Query Retrieval for Retrieval-Augmented Large Language Models. *Bioengineering*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/40868407/

[13] Noll R, Windschmitt J, Hofmann E, et al. Retrieval-Augmented Generation for Medical Decision-Making in Emergency Care. *Proceedings of the IEEE Engineering in Medicine and Biology Society*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/41337300/

[14] Mi J, Zu Y, Wang Z, He J. ACDNet: Attention-guided Collaborative Decision Network for effective medication recommendation. *Journal of Biomedical Informatics*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/38096944/

[15] Chairat S, Sae-Ang A, Suvirat K, Ingviya T, Chaichulee S. Enhancing Medication Recommendation with Hierarchical Network and Patient Visit Histories. *Proceedings of the IEEE Engineering in Medicine and Biology Society*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/40039103/

[16] Bucker M, Hoti K, Rose O. Artificial intelligence to assist decision-making on pharmacotherapy: A feasibility study. *Exploratory Research in Clinical and Social Pharmacy*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39252877/

[17] Ong JCL, Jin L, Elangovan K, et al. Large language model as clinical decision support system augments medication safety in 16 clinical specialties. *Cell Reports Medicine*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/40997804/

[18] Luo H, Yin W, Wang J, et al. Drug-drug interactions prediction based on deep learning and knowledge graph: A review. *iScience*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/38405609/

[19] Wang X, Ye H, Zhang S, et al. Evaluation of the Performance of Three Large Language Models in Clinical Decision Support: A Comparative Study Based on Actual Cases. *Journal of Medical Systems*. 2025. PubMed: https://pubmed.ncbi.nlm.nih.gov/39948214/

[20] Schwieger A, Angst K, de Bardeci M, et al. Large language models can support generation of standardized discharge summaries: A retrospective study utilizing ChatGPT-4 and electronic health records. *International Journal of Medical Informatics*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39437512/

[21] Wang Y, Yang Z, Yao Q. Accurate and interpretable drug-drug interaction prediction enabled by knowledge subgraph learning. *Communications Medicine*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/38548835/

[22] Jeong E, Su Y, Li L, Chen Y. Discovering clinical drug-drug interactions with known pharmacokinetics mechanisms using spontaneous reporting systems and electronic health records. *Journal of Biomedical Informatics*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/38583580/

[23] Smolyak D, Bjarnadóttir MV, Crowley K, Agarwal R. Large language models and synthetic health data: progress and prospects. *JAMIA Open*. 2024. PubMed: https://pubmed.ncbi.nlm.nih.gov/39464796/
