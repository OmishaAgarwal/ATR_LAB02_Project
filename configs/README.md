# Configuration status

`experiment.yaml` is the initial scaffold configuration, not a validated frozen run configuration.
The supplied pilot notebooks do not share one identical protocol: `ATR_Early_Error_Recovery_Pilot_Final.ipynb` documents a two-condition, four-action pilot scaffold, while `36_episode_exploratory_pilot_Untitled4_4.ipynb` contains a later 36-episode exploratory run with three conditions and horizons 4/8/12. Do not combine their settings or outputs.

Before a confirmatory run, create a dated immutable config, record model revision, seeds, runtime, budgets, prompt version and task manifest hash, and preserve the exact config used.
