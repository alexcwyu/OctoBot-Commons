# OctoBot-Commons: portable verification records

<!-- current-documentation-provenance -->
Documentation reviewed: 2026-10-13 · Git source base: `c457d7838387127f54cbf9c98a36376c5a222b56` · [Current architecture and feature guide](../ayu-develop.md).
Historical execution commands/results below retain their original dates and scope; this metadata update is not a new application test run.
<!-- /current-documentation-provenance -->


Full raw logs are retained in the workspace maintenance evidence, not distributed here. Hashes identify those original logs. A successful build or selected test subset does not imply a full test-suite pass. Commands containing <workspace> describe the original execution environment.

[Machine-readable records](verification.json) · [Repository validation summary](../validation.md)

## Executed commands

| Check | Exit | Duration | Command | Outcomes |
| --- | ---: | ---: | --- | --- |
| build | 0 | 1.0s | `uv build --python 3.15` | Successfully built dist/octobot_commons-1.10.6.tar.gz<br>Successfully built dist/octobot_commons-1.10.6-py3-none-any.whl |
| compile | 0 | 0.18s | `<workspace>/OctoBot-Commons/.venv/bin/python -m compileall -q src` | See exit status; no test-count assertion. |
| counter-final-tests | 0 | 14.27s | `.venv/bin/python -m pytest tests` | 322 passed in 13.66s |
| final-build | 0 | 1.52s | `uv build --python 3.15.0` | Successfully built dist/octobot_commons-1.10.6.tar.gz<br>Successfully built dist/octobot_commons-1.10.6-py3-none-any.whl |
| final-build-2 | 0 | 1.04s | `uv build --python 3.15.0` | Successfully built dist/octobot_commons-1.10.6.tar.gz<br>Successfully built dist/octobot_commons-1.10.6-py3-none-any.whl |
| final-compile | 0 | 0.14s | `.venv/bin/python -m compileall -q src` | See exit status; no test-count assertion. |
| final-compile-2 | 0 | 0.07s | `.venv/bin/python -m compileall -q src` | See exit status; no test-count assertion. |
| final-lock | 0 | 0.19s | `uv lock --upgrade` | See exit status; no test-count assertion. |
| final-lock-2 | 0 | 0.4s | `uv lock --upgrade` | See exit status; no test-count assertion. |
| final-sync | 0 | 0.05s | `uv sync --all-extras --frozen --python 3.15.0` | See exit status; no test-count assertion. |
| final-sync-2 | 0 | 0.04s | `uv sync --all-extras --frozen --python 3.15.0` | See exit status; no test-count assertion. |
| lock-3.15 | 0 | 0.28s | `uv lock --upgrade --python 3.15` | See exit status; no test-count assertion. |
| sync-3.15 | 0 | 0.94s | `uv sync --all-extras --python 3.15` | See exit status; no test-count assertion. |
| tests | 2 | 3.4s | `<workspace>/OctoBot-Commons/.venv/bin/python -m pytest tests` | See exit status; no test-count assertion. |
| tests-2 | 2 | 3.2s | `.venv/bin/python -m pytest tests` | See exit status; no test-count assertion. |
| tests-3 | 1 | 29.49s | `.venv/bin/python -m pytest tests` | 2 failed, 320 passed in 28.64s |
| tests-4 | 1 | 31.8s | `.venv/bin/python -m pytest tests` | 1 failed, 321 passed in 31.03s |
| tests-5 | 1 | 19.59s | `.venv/bin/python -m pytest tests` | 1 failed, 321 passed in 19.09s |
| tests-6 | 0 | 14.69s | `.venv/bin/python -m pytest tests` | 322 passed in 14.22s |
| tls-diagnostic | 0 | 4.24s | `.venv/bin/python -m pytest tests/test_aiohttp_util.py tests/test_async_job.py::test_run_stop_run -s --log-cli-level INFO` | ============================== 5 passed in 3.82s =============================== |
