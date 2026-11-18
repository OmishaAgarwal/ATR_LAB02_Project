# AI-Use and Research-Integrity Report
## ATR project: independent state-consistency verification for early-error recovery

**Evidence basis:** the available ATR prompt-to-code log, Cycle 1/Cycle 2 project archives, Colab notebook `Untitled4 (4).ipynb`, saved notebook outputs, and the current Overleaf source `main.tex`. This report distinguishes recorded facts from reconstruction and missing evidence.

**Important record limitation:** The available project archive contains a short `paper/prompt_to_code_log.md` with two entries, not a complete prompt transcript. No Git repository, commit history, patch files, or separately maintained debugging diary was supplied in the inspected project files. Therefore, exact prompts and AI responses are not recoverable for every later notebook change. Where the original wording is unavailable, the task is described as a summary of the recorded instruction, not a verbatim prompt. Historical ChatGPT model/version identifiers are not recorded in the prompt-to-code log.

---

## 1. Significant AI-assisted activities

| Activity | Tool and prompt/version evidence | AI contribution / proposal | Human decision and verification | Code/result change and outcome |
|---|---|---|---|---|
| **1. Reflexion-style memory baseline (Cycle 1, 30 Oct 2026)** | ChatGPT assistance is documented in `prompt_to_code_log.md`. The logged instruction asked for a Reflexion baseline in short cycles, minimal executable code, explanation of shapes, a sanity test, and waiting for genuine execution output. Exact model version and full verbatim prompt are not preserved. | Proposed a bounded, task-scoped verbal reflection memory and a function to build a reflection prompt. | The implementation was deliberately limited to memory and prompt construction. Model inference, environment, task loading, training, metrics and plots were deferred. The user ran the supplied test in Colab; the log records `REFLEXION_MEMORY_TEST: PASS`, two retained reflections for task A, one for task B, and a 558-character prompt. | Added `src/atr/reflexion_memory.py`, `scripts/test_reflexion_memory.py`, and `paper/code_understanding.md`. The isolated unit test passed. The project log explicitly labels this as an adaptation, not an exact reproduction of all Reflexion experiments. |
| **2. Actor + self-reflection interface (Cycle 2)** | The Cycle 2 project log records this as the next short-cycle implementation. The exact full prompt transcript and model version are not preserved. | Proposed an actor/reflection interface using a replaceable text-generation callable, task-scoped reflection memory, and a deterministic fake generator for testing. | The human-facing design notes deliberately kept action proposals as plain text at this stage and deferred structured parsing, environment execution, evaluator and real model inference. The Colab notebook records `REFLEXION_MEMORY_TEST: PASS` and `REFLEXION_AGENT_TEST: PASS`; task-memory isolation and memory inclusion in the actor prompt were checked. | Added `src/atr/reflexion_agent.py` and `scripts/test_reflexion_agent.py`. The tests passed. The documentation states this is a minimal Reflexion-style adaptation, not a complete reproduction of the published system. |
| **3. Connecting the model, workflow environment, belief state and fault injection** | Successive `%%writefile` cells in the uploaded Colab notebook show the implementation sequence. The notebook is execution evidence, but it is not a full prompt transcript; exact prompts and authorship of each line cannot be reconstructed reliably. | The saved code includes a Hugging Face generation wrapper, a small three-action research-workflow environment, a separate belief state, a Boolean fault injector, and smoke-test scripts. | Human/project verification is visible in the notebook: environment smoke tests, true-state isolation assertions, action-generation tests, and end-to-end episode tests. The notebook also contains explicit comments that early substring mapping was only for a smoke test, not the final parser. | Added `hf_generator.py`, `workflow_env.py`, `belief_state.py`, `fault_injector.py` and test scripts in successive notebook cells. Some tests passed technically, but successful test completion did not always mean task completion; see the limitations below. No Git diff is available to establish a complete line-by-line attribution. |
| **4. Pilot experiment and analysis** | The final cell of `Untitled4 (4).ipynb` contains the actual pilot code and saved outputs. The exact ChatGPT prompt that produced or modified this cell is not present in the preserved prompt log. The local experimental model is `Qwen/Qwen2.5-1.5B-Instruct`; it is distinct from the historical ChatGPT authoring model. | The saved implementation runs B1 (direct), B2 (reflection) and P (reflection plus verifier report), at horizons 4, 8 and 12, with two trials for each clean/injected setting. It writes episode and aggregate CSVs and a recovery plot. | The recorded execution output shows 36/36 episodes reached in the loop and a `PILOT RUN FINISHED` message. The aggregate table is the verification evidence. A later integrity review of the code is essential because the variable named `recovered` is not a sound measure of task recovery. | A 36-episode pilot was executed on a Colab Tesla T4, CUDA 13.0, PyTorch 2.11.0+cu130 in the pilot runtime output. The saved aggregate reports zero injected task success/recovery in all cells. The result is descriptive only (n=2 per cell); the recovery variable is semantically flawed, so it must not support a substantive recovery-effect conclusion. |
| **5. LaTeX table formatting assistance (18 Nov 2026 conversation)** | The exact user request was to improve the table code. The first assistant response assumed an IEEE two-column document. After the user reported compilation failure, the actual `main.tex` was inspected and showed `\\documentclass[acmsmall]{acmart}`. | The first proposed replacement used `table*` and `tabularx` with an IEEE-oriented layout; this did not respect the actual ACM class context. | The user rejected the failed result. The source file was then inspected; the document class was used to correct the diagnosis. This is direct human feedback and source-based verification. | A later ACM-oriented replacement was supplied. The episode demonstrates that AI-generated LaTeX should be checked against the actual preamble and document class before use. There is no saved Overleaf compilation log proving that the later replacement compiled successfully. |

---

## 2. Real limitations, corrections and verification examples

The following examples are supported by the saved files or the visible project conversation. They are not presented as successful fixes unless the evidence shows success.

### Example A — Environment smoke test failed despite model files loading
The notebook's `environment_test.py` output reports successful imports for PyTorch, Transformers and Accelerate, and successful loading/tokenization of the Qwen configuration. However, the overall smoke test status is **FAILED** because `pip check` reported dependency conflicts: missing `jedi` for IPython, and incompatible installed `huggingface-hub` / `safetensors` versions for Gradio and Diffusers. The same notebook later shows a different runtime state with PyTorch `2.11.0+cu130`, CUDA 13.0 and a Tesla T4, while the earlier smoke-test subprocess reported CPU-only PyTorch. This inconsistency means environment claims must be tied to the exact cell/runtime, not generalized across the notebook. No complete, independently verified dependency-resolution fix is documented.

### Example B — The model returned malformed or mixed conversational output
In the saved baseline episode test, the model output included an action label followed by assistant/user-style conversational text. The parser returned `invalid_action`; the environment rejected it as an unknown action and the task remained incomplete. A subsequent notebook cell introduced a more restrictive regular-expression parser that first looks for an explicit `Action:` label and otherwise accepts exactly one unique allowed action. This is a genuine parser-hardening change visible in the notebook. However, the later saved retry test still did not recover the task, so the parser change must not be described as solving the underlying reasoning/recovery problem.

### Example C — Reflection did not correct the underlying state/action choice
The saved `test_reflection_retry.py` output records:
- injected field: `dataset_validated`;
- true environment state unchanged by injection;
- first proposal: `download_dataset`, rejected because the dataset was already downloaded;
- second proposal after reflection: `check_schema`, rejected because the schema was already checked;
- `task_done_after_retry: False`;
- `true_validation_state: False`.

This demonstrates that producing a reflection and storing it did not guarantee a correct next action or successful recovery. It is evidence against treating a successful reflection call as proof of recovery.

### Example D — AI formatting advice initially ignored the actual document class
In the current conversation, the assistant first supplied an IEEE-style `table*` replacement. The user reported that the document stopped compiling. Inspection of the uploaded `main.tex` then established that the document uses `acmart` with the `acmsmall` option, not IEEE. The initial advice was therefore based on an incorrect assumption. The corrected response was tailored to the actual class, but no subsequent successful Overleaf compile log is available. This is a real example of human correction and the need to inspect source configuration before accepting generated code.

### Example E — Pilot metric name overstated what the code measured
In the pilot code, `recovered` becomes true when the corrupted belief field equals the authoritative field at any point. This is not equivalent to completing the task or successfully recovering after an error. The code also checks this equality after each action, while the injected field and workflow-state semantics can make the equality test misleading. The aggregate labels the mean of this variable as `recovery_rate`, but all injected task-success rates are also zero. This is a metric-validity issue found by inspecting the implementation and outputs, not evidence of a performance gain. The recovery-rate values should not be interpreted as a valid causal measure until the metric is corrected and the experiment rerun.

**Count of concrete examples:** five are available in the current record. Examples A–C are notebook execution/debugging evidence; D is a documented assistant limitation corrected after human feedback; E is a code/measurement validity issue found through manual inspection. No unsupported claim is made that all were fixed.

---

## 3. Decisions that depended on human reasoning

The following decisions are attributable to the project design and documented human choices, rather than being established by model output alone:

1. **Scope of the baseline:** The Cycle 1 log explicitly limited the implementation to task-scoped memory and prompt construction. It also labels the implementation a simulator-specific adaptation rather than an exact reproduction of Reflexion.
2. **Separation of true state and agent belief:** The experiment's fault-injection design and tests distinguish authoritative environment state from the agent's belief. The notebook includes an assertion that the true state remains unchanged by injection.
3. **Choice of experimental comparison:** B1, B2 and P represent distinct conditions; the proposed verifier is report-only rather than an automatic state mutator. The interpretation of what the intervention can establish requires human methodological judgment.
4. **Treatment of pilot findings:** The 36-episode output has only two trials per condition/horizon/fault cell. The choice to report it as a small descriptive pilot, not as statistically established evidence, is a human integrity decision.
5. **Recognition of invalid recovery measurement:** The code's `recovered` flag is not task success. Distinguishing a variable's implementation from the scientific construct in its name requires manual code and metric review.
6. **Document-format correction:** The ACM `acmsmall` class was established from the actual `main.tex` after the first generated table advice failed. The source file, not the assistant's assumption, determined the correct format.

---

## 4. What was learned about vibe coding

The project illustrates both the speed and the risks of prompt-driven coding:

- **Useful for scaffolding:** AI assistance helped create small modules, tests, documentation and initial experiment code in short cycles.
- **Small tests are valuable:** The fake-generator unit test isolated memory behavior without requiring a model download. This made one component independently testable.
- **Passing tests are not enough:** A test can pass because a script ran to completion even when the simulated task did not. The saved baseline/retry outputs make this distinction explicit.
- **Natural-language output needs strict interfaces:** The model's extra prose and conversational continuations broke a naïve action parser. Explicit schemas, strict validation and rejection paths are necessary.
- **Metrics require independent scrutiny:** AI can produce a plausible metric name and plot while the code measures something different. The operational definition must be checked against the research construct.
- **Configuration must be inspected, not guessed:** The failed LaTeX table and inconsistent runtime/package records show why source files and execution logs should be checked before accepting advice.
- **Human accountability remains central:** AI-generated code, explanations and prose are drafts. The researcher must decide whether the design is valid, whether tests actually establish the claim, and whether conclusions are justified.

---

## 5. Remaining risks and evidence gaps

- **Prompt provenance:** Only two entries are preserved in `prompt_to_code_log.md`; full prompts, complete AI responses, model/version metadata and all later prompt iterations are missing.
- **Change provenance:** No Git commit history or machine-readable diffs were supplied. The notebook contains successive code-writing cells, but cannot substitute for a complete version-control history.
- **Execution provenance:** Notebook cells have saved outputs, but several cells have `execution_count: null`. The 36-episode output is saved, but the generated CSV files are not separately present in the inspected uploads.
- **Environment reproducibility:** The notebook shows conflicting package/runtime snapshots. A clean, pinned environment has not been demonstrated by the saved evidence.
- **Metric validity:** The pilot's `recovered` variable is not a valid measure of task recovery. The pilot should not be used to claim that the verifier improved recovery.
- **Experimental scale and design:** Two trials per cell are insufficient for strong inference. The 4/8/12 horizons are prefixes of one linear 12-action workflow in the pilot code, not independently designed task graphs.
- **Verifier implementation:** The pilot verifier reports mismatches, but the saved code does not establish a complete, validated repair loop. Its actual effect cannot be isolated from the current pilot.
- **Model reproducibility:** The model ID is recorded, but a pinned model revision/hash is not established in the available evidence.
- **External validity:** A small custom simulator and one small model do not establish performance on real autonomous research workflows or other models.

---

## 6. Research-integrity statement

AI assistance was used in the ATR project for implementation scaffolding, test creation, code explanation, documentation, experimental scripting and LaTeX formatting. The preserved records do not support a complete prompt-by-prompt attribution for every file or code change, and no Git history was available for a full diff audit. The report therefore identifies the documented cycles and notebook-visible changes while explicitly marking missing provenance.

The researcher remains responsible for the research question, experimental design, interpretation of outputs, verification of code and metrics, and all claims in the paper. The saved pilot is reported as a limited technical run with descriptive outputs, not as proof that independent state-consistency verification improves recovery. No performance gain is claimed. The unresolved metric, small sample size, runtime inconsistency and incomplete prompt/change logs must be addressed before stronger conclusions or a reproducibility claim are made.

---

## 7. Recommended disclosure wording

> Generative AI assistance (ChatGPT; historical model/version not retained in the project log) was used to support iterative code scaffolding, unit-test drafting, code explanation, experimental scripting, documentation and LaTeX formatting. The local experimental agent used `Qwen/Qwen2.5-1.5B-Instruct`. Human review included execution of saved Colab tests, inspection of environment outputs, examination of model-generated action failures, review of the fault-injection isolation checks, inspection of the pilot aggregation logic, and correction of formatting advice after checking the actual ACM source class. The available prompt log is incomplete and no Git commit history was supplied; accordingly, not every AI-assisted code change can be attributed to an exact prompt or diff. All scientific interpretations and claims remain the responsibility of the human researcher.

## 8. Minimum integrity checklist before submission

- [ ] Preserve the complete prompt log, including tool/model version and date for future work.
- [ ] Add Git commits or unified diffs for subsequent code changes; do not backfill invented history.
- [ ] Correct and unit-test the recovery metric against hand-constructed episodes.
- [ ] Rerun the pilot after metric correction and retain the episode-level CSVs and aggregate CSVs.
- [ ] Record one consistent runtime and exact dependency versions for the final run.
- [ ] Keep malformed model outputs and failed episodes in the primary failure accounting.
- [ ] Verify every figure and table directly against saved data.
- [ ] Retain the actual Overleaf compile log for the final LaTeX project.
- [ ] Do not claim exact Reflexion reproduction, statistically significant improvement, or successful recovery unless new evidence supports those claims.
