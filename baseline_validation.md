# Baseline validation and reproduction checks

## Evidence available

- Cycle 1 reflection-memory test: prompt-to-code log records a Colab output `REFLEXION_MEMORY_TEST: PASS`, two reflections for task A, one for task B, and a 558-character prompt.
- Cycle 2 actor/reflection test: project notes record `REFLEXION_AGENT_TEST: PASS` and task-scoped memory checks. The prompt-to-code log also notes that the local sanity test was to be run and Colab test was pending at that point; preserve this chronology rather than treating all tests as one run.
- The 36-episode exploratory notebook contains saved outputs and pilot aggregate results. The prior analysis records n=2 per condition/horizon/fault cell, zero injected task success, and a `recovered` flag that tests belief equality rather than task recovery. Treat these as descriptive exploratory evidence only.
- `ATR_Early_Error_Recovery_Pilot_Final.ipynb` explicitly describes itself as a setup/pilot scaffold, not a completed experiment, and includes a four-action, two-condition pilot design.

## Known deviations and limitations

1. The two notebooks represent different stages/protocols and must not be combined.
2. The 36-episode notebook uses 4/8/12 prefixes of a single linear workflow, not independent task graphs.
3. The `recovered` variable in the exploratory pilot is not equivalent to successful task recovery.
4. n=2 per cell is too small for confirmatory inference.
5. An earlier environment smoke test recorded package conflicts; a later pilot runtime recorded Python 3.13.16, PyTorch 2.11.0+cu130, CUDA 13.0 and Tesla T4. Runtime records must be tied to the exact run.
6. The model ID is recorded as `Qwen/Qwen2.5-1.5B-Instruct`; an immutable model revision/hash was not established in the supplied evidence.
7. No standalone results CSV/JSON exports were supplied in the assembled folder.
8. No complete Git commit history or unified diffs were supplied.

## Required checks before a new reproduction

- [ ] Start from a fresh runtime and record Python, PyTorch, CUDA, GPU, Transformers and Accelerate versions.
- [ ] Resolve dependency conflicts and save a successful `pip check` output.
- [ ] Pin an immutable model revision and record its license/terms and checksum where feasible.
- [ ] Extract task definitions into versioned files and hash the manifest.
- [ ] Unit-test environment preconditions/effects and fault isolation.
- [ ] Unit-test verifier report-only behavior and confirm it never mutates belief.
- [ ] Correct the recovery metric and validate it on hand-constructed episodes.
- [ ] Run matched conditions with the same tasks, seeds, model, prompts and budgets.
- [ ] Save episode-level CSV/JSON, aggregate metrics, logs and figures to `results/`.
- [ ] Record deviations before interpreting results.

Commands that have not been demonstrated against a clean checkout should be labelled `[TEST REQUIRED]`.
