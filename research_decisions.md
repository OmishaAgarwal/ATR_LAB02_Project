# Research Decisions Log
## Project: Planning-Quality Degradation in Long-Horizon Autonomous Research Agents

**Owner:** Omisha Agarwal  
**Log status:** Initial / provisional  
**Last updated:** 2026-10-30

> Evidence labels: **VERIFIED** = directly supported by an inspected source or observed output; **INFERRED** = a reasoned interpretation or proposal requiring validation; **UNKNOWN** = evidence is not yet available.

---

## 1. Project source documents

| Document | Description | Current understanding |
|---|---|---|
| `ORIGINAL PAPER.pdf` | Original literature review, 11 pages | Narrative review of long-horizon agent planning degradation |
| `ACM FORMAT PAPER.pdf` | Updated ACM-style paper, 17 pages | Expanded narrative review with a formal model, taxonomy, mitigation comparison and research agenda |

**VERIFIED:** Both documents are reviews, not reports of a completed implementation-based experiment. The updated ACM-format document identifies itself as a review and discusses future research directions.

## 2. Initial scope audit

**VERIFIED — source: both uploaded papers**

The review studies degradation in the ability of LLM-based agents to form, maintain, revise and execute coherent plans as task horizon, trajectory length or context grows.

The review covers:
1. Long-horizon planning and reasoning.
2. Context growth and information retrieval.
3. Autoregressive error compounding.
4. Myopic step-wise reasoning versus lookahead.
5. Failure propagation across modules and agents.
6. Research-specific methodological drift in scientific workflows.
7. Mitigation approaches and measurement limitations.

### Five-mechanism taxonomy

| ID | Mechanism | Summary |
|---|---|---|
| M1 | Context-induced degradation | Relevant information becomes harder to use as context grows or distractors accumulate. |
| M2 | Autoregressive error compounding | Earlier mistakes influence and amplify later decisions. |
| M3 | Myopic step-wise reasoning | Locally attractive actions are selected without sufficient downstream lookahead. |
| M4 | Cross-module / cross-agent propagation | Errors spread between memory, reflection, planning, action or agents. |
| M5 | Research-specific methodological drift | Benchmark choice, leakage, metric misuse and post-hoc selection undermine scientific validity. |

## 3. Comparison of the two versions

**VERIFIED — based on the uploaded documents**

The updated ACM-format paper expands the original review. Notable additions or elaborations include:
- A formal model using cumulative success `S(n)` and effective per-step reliability `p̄(n)`.
- A dedicated explanation of interactions among the five mechanisms.
- A more explicit mitigation coverage comparison.
- An evidence-strength assessment.
- Proposed planning-quality measurements, including first invalid-step position `t*` and post-error recovery ratio `R_k`.
- A more detailed research agenda and suggested indicators of progress.

**UNKNOWN:** Whether every cited work, reported number, publication status and repository claim has been independently verified. A separate reference audit is required before relying on them in a new paper.

## 4. Current research status

| Component | Status | Notes |
|---|---|---|
| Topic and motivation | VERIFIED | Present in both reviews. |
| Literature taxonomy | VERIFIED | Five mechanisms M1–M5. |
| Mitigation literature | VERIFIED | Lookahead, verification, memory/context management, reflection, diagnostics and auditing are discussed. |
| Candidate research gaps | VERIFIED | Research-workflow benchmarks, context mechanisms, plan-quality metrics, verifiable planning and cross-session memory. |
| Chosen primary mechanism | UNKNOWN | Not selected yet. |
| Research question and hypotheses | UNKNOWN | Must be derived from a feasible controlled experiment. |
| Dataset / benchmark | UNKNOWN | No benchmark has yet been selected for this implementation project. |
| Baseline system | UNKNOWN | No implementation has yet been verified. |
| Proposed intervention | UNKNOWN | No new method has yet been selected. |
| Code and execution environment | UNKNOWN | Need the user's available hardware, software and compute constraints. |
| Experimental results | UNKNOWN | No experiments have been run for this project. |

## 5. Provisional decisions

### Decision 001 — Treat the ACM paper as an expanded literature review, not an implementation paper

**Status:** VERIFIED  
**Decision:** Use the ACM-format paper as the current literature foundation, while retaining the original paper as a comparison record.  
**Reason:** The updated document contains a review taxonomy, literature synthesis, mitigation discussion and future directions, but no demonstrated implementation or experimental results.  
**Evidence:** `ORIGINAL PAPER.pdf`; `ACM FORMAT PAPER.pdf`.  
**Next actions:**
- Audit the bibliography and verify key references.
- Extract candidate research gaps and map each to measurable experiments.

### Decision 002 — Do not attempt to implement all five mechanisms at once

**Status:** INFERRED  
**Decision:** Select one primary mechanism and, if feasible, one or two secondary mechanisms for the first study.  
**Reason:** The five mechanisms span context, sequential errors, planning policy, architecture and scientific methodology. Studying all simultaneously would make causal attribution and project scope difficult.  
**Evidence:** Five-mechanism taxonomy and measurement-confounding discussion in the updated review.  
**Next actions:**
- Compare candidate mechanisms by experimental controllability, implementation cost and measurable outcomes.
- Select only after feasibility analysis.

### Decision 003 — Treat planning quality as distinct from final task success

**Status:** INFERRED / grounded in the review's proposed measurement agenda  
**Decision:** Investigate intermediate plan-quality measures alongside end-task success.  
**Reason:** Binary success alone may hide where a plan first becomes invalid and whether an agent recovers after an error.  
**Candidate measures from the review:** `t*`, `R_k`, `p̄(n)`, plan coherence, revision cost and constraint satisfaction.  
**Next actions:**
- Define operational scoring rules.
- Check inter-rater or evaluator reliability.
- Test whether metrics remain meaningful across task lengths.

## 6. Open questions and evidence required

1. Which primary mechanism should the implementation isolate?
2. Which task environment permits horizon length to vary independently of task difficulty?
3. What baseline agent can be installed and executed reproducibly?
4. Which model/API and budget are available?
5. What compute and time constraints apply?
6. Can we obtain ground-truth plans or independently verifiable constraints?
7. What evaluation protocol and number of trials are feasible?

## 7. Next actions

- [ ] Audit and verify the most important references in the ACM-format paper.
- [ ] Build a literature-to-experiment matrix.
- [ ] Compare candidate research gaps by novelty evidence and feasibility.
- [ ] Formulate research questions and falsifiable hypotheses.
- [ ] Select a controlled benchmark and baseline.
- [ ] Run a baseline pilot and save raw outputs/configurations.
- [ ] Implement one intervention only after baseline behavior is established.
- [ ] Run controlled comparisons and ablations.
- [ ] Record all results, including negative results, without fabrication.
- [ ] Prepare manuscript and reproducibility package.

## 8. Experiment record template

For every run, record:

- **Run ID:**
- **Date/time:**
- **Code commit/version:**
- **Model and version:**
- **Prompt/configuration:**
- **Benchmark/task IDs:**
- **Horizon / number of steps:**
- **Context length or token count:**
- **Intervention condition:**
- **Random seed:**
- **Raw output/log location:**
- **Metrics:**
- **Failures and anomalies:**
- **Interpretation:** VERIFIED / INFERRED / UNKNOWN
- **Reproduction instructions:**

---

**Log maintenance rule:** Never enter a proposed result as an observed result. Every substantive decision must include its reason, evidence source and next action. Update this file whenever the research scope, method, benchmark, baseline or evaluation protocol changes.
