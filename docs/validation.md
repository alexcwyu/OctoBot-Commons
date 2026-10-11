# OctoBot-Commons maintenance validation

Recorded 2026-10-12T01:32:43.353468+08:00. Branch `feature/ayu_develop`; upstream default `upstream/master` is merged: **true**. Branch/tag synchronization records are retained in the workspace maintenance evidence. Feature branch publication is coordinated separately.

Runtime: **CPython 3.15.0**, uv **0.13.0**, build backend `hatchling.build`. Python 3.15.0 installs the complete environment.

Existing suite: **322 passed in 13.66s** (exit `0`). Existing test suite passes. CounterClientSession composes a standard aiohttp session, preserving counting and instance checks without deprecated inheritance; corrupted-ciphertext fixtures now always change a bit.

No test cases were added. Existing assertions and strict warning behavior remain active; repaired fixtures own their loops, sessions, files and configuration paths. Existing upstream platform skips and configured deselections are reported exactly.

## Final build commands

| Check | Exact command | Exit | Seconds |
| --- | --- | ---: | ---: |
| lock | `uv lock --upgrade` | 0 | 0.4 |
| sync | `uv sync --all-extras --frozen --python 3.15.0` | 0 | 0.04 |
| build | `uv build --python 3.15.0` | 0 | 1.04 |
| compile | `.venv/bin/python -m compileall -q src` | 0 | 0.07 |

## Existing test and compatibility evidence

| Check | Exact command | Exit | Result |
| --- | --- | ---: | --- |
| lock-3.15 | `uv lock --upgrade --python 3.15` | 0 | Check completed; see exact exit code. |
| sync-3.15 | `uv sync --all-extras --python 3.15` | 0 | Check completed; see exact exit code. |
| tests | `/Users/alex/workspaces/trading/OctoBot-Commons/.venv/bin/python -m pytest tests` | 2 | 20 errors in 2.57s |
| tests-2 | `.venv/bin/python -m pytest tests` | 2 | 1 error in 1.92s |
| tests-3 | `.venv/bin/python -m pytest tests` | 1 | 2 failed, 320 passed in 28.64s |
| tests-4 | `.venv/bin/python -m pytest tests` | 1 | 1 failed, 321 passed in 31.03s |
| tests-5 | `.venv/bin/python -m pytest tests` | 1 | 1 failed, 321 passed in 19.09s |
| tests-6 | `.venv/bin/python -m pytest tests` | 0 | 322 passed in 14.22s |
| counter-final-tests | `.venv/bin/python -m pytest tests` | 0 | 322 passed in 13.66s |

Raw logs remain in the workspace maintenance evidence directory. The [portable verification record](maintenance/verification.json) retains exact command arrays, exits, timing, runtime inventory and log filenames. Earlier failed attempts remain recorded and are not treated as successful final validation.

## Installed dependency versions

This is the selected environment after locked synchronization; isolated wheel build dependencies are resolved by the build backend and recorded in build output.

| Distribution | Version |
| --- | --- |
| aiohappyeyeballs | 2.7.1 |
| aiohttp | 3.14.5 |
| aiosignal | 1.4.0 |
| aiosqlite | 0.22.1 |
| attrs | 26.1.0 |
| certifi | 2026.7.22 |
| cffi | 2.1.1 |
| charset-normalizer | 3.5.2 |
| coverage | 7.16.2 |
| cryptography | 50.0.2 |
| execnet | 2.1.2 |
| frozenlist | 1.8.0 |
| idna | 3.20 |
| iniconfig | 2.3.1 |
| jsonschema | 4.26.0 |
| jsonschema-specifications | 2025.9.1 |
| mock | 5.2.0 |
| multidict | 7.1.0 |
| numpy | 2.5.4 |
| octobot-commons | 1.10.6 |
| packaging | 26.3 |
| pluggy | 1.6.0 |
| propcache | 0.5.4 |
| psutil | 7.2.2 |
| pycparser | 3.11 |
| Pygments | 2.21.0 |
| pytest | 9.1.1 |
| pytest-asyncio | 1.4.0 |
| pytest-cov | 7.1.0 |
| pytest-timeout | 2.4.0 |
| pytest-xdist | 3.8.0 |
| referencing | 0.37.0 |
| requests | 2.34.2 |
| rpds-py | 2026.9.1 |
| ruff | 0.17.0 |
| sortedcontainers | 2.4.0 |
| urllib3 | 2.8.0 |
| yarl | 1.25.1 |

See [architecture](ayu-develop.md) for source-linked component/sequence/workflow diagrams and [development](development.md) for reproducible uv commands.
