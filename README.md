# AITR Lab 02 Project

Research project evaluating whether independent state-consistency verification helps long-horizon LLM agents recover from deliberately injected belief-state errors.

> **Evidence status:** This repository assembles the supplied project artifacts. It is not a claim that the confirmatory experiment is complete or that the current codebase can be reproduced from a clean checkout without further work. Two notebook stages are preserved separately. The 36-episode run is exploratory and its current recovery metric is not valid as task recovery.

## Research question

How does independent state-consistency verification affect the performance, error recovery and robustness of long-horizon LLM agents compared with direct execution and reflection-only self-correction, under controlled belief-state errors?

## Repository structure

```text
AITR_Lab02_Project/
├── README.md
├── requirements.txt
├── configs/
├── data/
│   ├── README.md
│   ├── manifests/
│   └── task_templates/
├── notebooks/
├── src/atr/
├── scripts/
├── results/
│   ├── logs/
│   └── figures/
├── paper/
├── research_decisions.md
├── baseline_validation.md
└── ai_assistance_log.md
```

## Experimental conditions

The later exploratory notebook uses three conditions: B1 direct execution, B2 reflection-only, and P reflection plus a report-only independent verifier. The verifier reports mismatches between current authoritative state and agent belief; it must not repair or mutate the belief itself. See the notebook and `paper/frozen_evaluation_protocol.md` for the distinct protocol stages.

## Setup

Primary environment evidenced in the saved pilot output: Google Colab, Python 3.13.16, PyTorch 2.11.0+cu130, CUDA 13.0, NVIDIA Tesla T4 (15 GiB reported). This is a recorded runtime snapshot, not a guarantee of future Colab availability.

`requirements.txt` preserves package pins from the supplied scaffold, but they are **not a verified clean-install set**. An environment smoke test recorded dependency conflicts. Do not run a blind install and assume success.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip check
```

**[TEST REQUIRED]** The commands above have not been verified as a clean local installation. The notebook uses Colab-specific setup and model-loading cells. Prefer a fresh Colab runtime until a consistent environment is frozen.

## Dataset preparation and access

The available materials describe a custom deterministic research-workflow simulator embedded in notebooks; no separate external dataset, raw data package, task manifest or dataset license was supplied. See `data/README.md`. Do not add restricted raw data or claim a third-party dataset license without checking its terms.

## Running tests and experiments

The Cycle 1/Cycle 2 tests are included as scripts. From the repository root, try:

```bash
python scripts/test_reflexion_memory.py
python scripts/test_reflexion_agent.py
python scripts/environment_test.py
```

**[TEST REQUIRED]** These commands have not been run from this assembled root directory in a clean environment. The prompt-to-code log records passing outputs for earlier cycle tests; see `baseline_validation.md`.

The pilot implementations are notebook-based. Open the notebooks in Google Colab and run cells in order only after reviewing the runtime and configuration. The 4-action setup/pilot notebook and the later 36-episode exploratory notebook are separate versions and must not be treated as one run. There is no verified standalone `train.py`, `run_experiment.py` or `evaluate.py` entrypoint in the supplied files.

## Evaluation and figures

No standalone metric export or final figure file is included in `results/`. The notebook code may write files to Colab runtime paths. Export genuine episode-level records and aggregate metrics from a new run before generating figures. Do not reconstruct missing CSVs from rounded tables or screenshots. The exploratory pilot's `recovered` flag measures belief equality at some point, not valid task recovery; it must be corrected and retested before use.

## Compute requirements

A GPU is recommended for local inference with `Qwen/Qwen2.5-1.5B-Instruct`; the recorded exploratory pilot used a Tesla T4. CPU execution may be slow. Actual VRAM, RAM and runtime needs depend on model revision, library versions and Colab allocation. No guaranteed minimum is established by the supplied evidence.

## Limitations

- Exploratory sample size is only two trials per condition/horizon/fault cell.
- Horizons 4/8/12 in the exploratory notebook are prefixes of one linear workflow.
- Recovery metric implementation is not valid as task recovery.
- Environment/package snapshots differ across notebook stages.
- Model revision is not immutably pinned.
- Task templates and manifests are not separately versioned.
- The verifier/repair implementation and full confirmatory pipeline require further validation.

## Credits, license and citation

The project builds on the supplied literature review and the Reflexion-style baseline concept documented in the cycle notes. Model: `Qwen/Qwen2.5-1.5B-Instruct`; check the model card and applicable license/terms before redistribution or use. The repository currently has no project-wide `LICENSE` file. Do not assume that absence means unrestricted reuse. Add a license only after confirming ownership and third-party compatibility.

A provisional BibTeX entry is in `paper/references.bib`; bibliographic metadata requires independent verification before publication. Cite the project paper only after its final version and results are approved.

## Reproduction checklist

- [ ] Clone/download this repository and inspect README, protocol and validation notes.
- [ ] Use a fresh runtime; record hardware and package versions.
- [ ] Resolve dependencies and obtain a clean `pip check`.
- [ ] Pin model revision and record model license/terms.
- [ ] Freeze task manifest, seeds, prompts, budgets and configuration.
- [ ] Run unit tests for environment, belief isolation and verifier behavior.
- [ ] Validate recovery metric against known success/failure examples.
- [ ] Run matched conditions on identical task instances.
- [ ] Save raw episode logs, metrics, config, environment record and generated figures.
- [ ] Compare outputs with the paper and document every deviation.

## AI use and research integrity

See [`ai_assistance_log.md`](ai_assistance_log.md). AI support was used for scaffolding, tests, documentation, analysis assistance and LaTeX formatting. The preserved prompt log and change history are incomplete; missing provenance is disclosed rather than reconstructed. Human review remains responsible for code verification, metric validity, experimental decisions and claims.

### Research planning data

- `data/manifests/research_gap_matrix.csv` contains the research-gap mapping used to motivate the study; it is not experimental results.
