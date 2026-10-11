# OctoBot-Commons: architecture and development

Commons provides shared configuration, profiles, databases, cryptography, DSL evaluation, and asynchronous utilities for the standalone OctoBot ecosystem. It has no exchange execution loop of its own.

## Components and boundaries

Small modules own focused utilities, while profile and database objects define the persistent boundaries. The DSL Interpreter dispatches expression nodes through operator implementations and explicit parameters/dependencies. FlexibleDataclass supports structured conversion; MinimizableDataclass inherits that behavior to omit default fields. HTTP counting is implemented with aiohttp tracing on a standard ClientSession, preserving client behavior without subclassing an unsupported library class.


```mermaid
flowchart LR
  A0["Configuration or expression"]
  A1["Profile and parameter context"]
  A2["Utility or operator dispatch"]
  A3["Database or network adapter"]
  A4["Structured result"]
  A0 --> A1
  A1 --> A2
  A2 --> A3
  A3 --> A4
```

The following class view names implementation classes. Cross-package types are supplied by the host ecosystem; arrows describe inheritance or usage, not copied ownership.

```mermaid
classDiagram
  class Interpreter
  class FlexibleDataclass
  class MinimizableDataclass
  class UpdatableDataclass
  MinimizableDataclass --|> FlexibleDataclass
  MinimizableDataclass ..> UpdatableDataclass : independent conversion APIs
```

## Runtime workflow

A caller loads configuration and profile data, resolves runtime identifiers, opens the required database or network resource, and consumes structured results. DSL evaluation receives an expression and parameter context, recursively evaluates supported operators, and returns a value. Database adapters and resource owners are closed by their callers.


```mermaid
sequenceDiagram
  participant Caller
  participant P1 as Profile and parameter context
  participant P2 as Utility or operator dispatch
  participant P3 as Database or network adapter
  Caller->>P1: Configure context and inputs
  P1->>P2: Initialize owned components
  P2->>P3: Process observation or command
  P3-->>P2: Result and state update
  P2-->>Caller: Report or event
  Caller->>P1: Stop and release resources
```

This sequence is an architectural view of responsibility and resource ownership. Individual plugin, connector, and strategy implementations can add asynchronous events and error branches. The lifecycle below is a conceptual operating workflow, rather than a claim that every component has one shared state enum.

```mermaid
stateDiagram-v2
  [*] --> Configured
  Configured --> Initialized: validate inputs
  Initialized --> Processing: start
  Processing --> Processing: next data or event
  Processing --> Stopping: finish or cancel
  Initialized --> Stopping: initialization error
  Stopping --> Closed: release owned resources
  Closed --> [*]
```

## Features and extension points

Profile import/export; authenticated AES-GCM encryption; SQLite-backed run data; DSL custom operators; configuration schemas; request rate counters; time-frame conversion and logging helpers.

Extend the owning component behind its existing public interface. Keep metadata and configuration alongside plugin/strategy resources. Exchange-specific behavior belongs in an adapter; strategy decisions belong in the strategy/evaluator layer; persistence schema and migrations belong with the storage implementation. Review the source map below before changing a boundary, and exercise the existing tests associated with that boundary.

## Packaging and dependency design

The standalone library is distinct from the newer Commons copy in the OctoBot monorepo. Its uv sources are consumed by Backtesting, Evaluators, and Trading. Python 3.15 works with the upgraded direct dependencies. Existing crypto corruption fixtures now flip a bit so randomized ciphertext cannot accidentally remain unchanged; assertions and test count are preserved.

The lock records exact package versions, hashes, platform markers, and local source mappings. Path sources deliberately bind related repositories in this workspace; clone sibling repositories at the documented names before synchronization. Published packaging metadata describes public dependencies, while uv source settings select this development workspace. Resolve dependency changes with uv lock --upgrade and retain the generated lock, then verify the same locked environment.

```mermaid
flowchart LR
  Source["src/octobot_commons"] --> Backend["PEP 517 build backend"]
  Metadata["pyproject.toml"] --> Backend
  Lock["uv.lock"] --> Env["Managed Python environment"]
  Backend --> Wheel["Wheel and sdist"]
  Env --> Existing["Existing tests"]
  Source --> Existing
  Wheel --> Inspect["Inspect modules and resources"]
```

## Maintenance workflow

All upstream branches and tags are fetched. Fork updates use nonforce pushes; a divergent branch is merged without erasing fork history. The default branch is merged into feature/ayu_develop with package/resource conflicts reconciled in their installed locations. Build and test evidence is recorded before a local maintenance commit. Feature branch publication is a separate root-level action.

```mermaid
flowchart TD
  F["Fetch upstream branches and tags"] --> C["Compare fork refs"]
  C --> M["Nonforce ref sync and default merge"]
  M --> L["uv lock --upgrade"]
  L --> P["Try managed Python 3.15"]
  P --> Q{"All required dependencies build?"}
  Q -->|yes| S["Sync complete environment"]
  Q -->|no| B["Record evidence and select supported fallback"]
  B --> S
  S --> W["Build wheel and sdist"]
  W --> T["Run existing tests and compile"]
  T --> R["Record failures, fixes, and exact results"]
  R --> D["Render MD and HTML documentation"]
  D --> G["Commit locally on feature/ayu_develop"]
```

No existing test assertions are removed and no new test cases are introduced in this maintenance pass. Corrected fixtures preserve coverage while making paths, corruption inputs, and resource cleanup compatible with the selected interpreter. A failed test or unsupported dependency is reported explicitly in [validation](validation.md); package build success does not imply strategy correctness, profitability, or successful live connectivity.

## Source map

| Source | Responsibility and location |
| --- | --- |
| [interpreter.py](../src/octobot_commons/dsl_interpreter/interpreter.py) | src/octobot_commons/dsl_interpreter/interpreter.py |
| [operator.py](../src/octobot_commons/dsl_interpreter/operator.py) | src/octobot_commons/dsl_interpreter/operator.py |
| [operator_parameter.py](../src/octobot_commons/dsl_interpreter/operator_parameter.py) | src/octobot_commons/dsl_interpreter/operator_parameter.py |
| [binary_operator.py](../src/octobot_commons/dsl_interpreter/operators/binary_operator.py) | src/octobot_commons/dsl_interpreter/operators/binary_operator.py |
| [flexible_dataclass.py](../src/octobot_commons/dataclasses/flexible_dataclass.py) | src/octobot_commons/dataclasses/flexible_dataclass.py |
| [minimizable_dataclass.py](../src/octobot_commons/dataclasses/minimizable_dataclass.py) | src/octobot_commons/dataclasses/minimizable_dataclass.py |
| [updatable_dataclass.py](../src/octobot_commons/dataclasses/updatable_dataclass.py) | src/octobot_commons/dataclasses/updatable_dataclass.py |
| [aiohttp_util.py](../src/octobot_commons/aiohttp_util.py) | src/octobot_commons/aiohttp_util.py |
| [html_util.py](../src/octobot_commons/html_util.py) | src/octobot_commons/html_util.py |
| [profile.py](../src/octobot_commons/profiles/profile.py) | src/octobot_commons/profiles/profile.py |
| [pyproject.toml](../pyproject.toml) | pyproject.toml |
| [uv.lock](../uv.lock) | uv.lock |
| [README.md](../README.md) | README.md |

## Further reading

Use [development.md](development.md) for reproducible commands and [validation.md](validation.md) for exact interpreter, dependency, build, test, and blocker evidence. The equivalent [HTML architecture document](ayu-develop.html) supports browsing and rendered diagrams.
