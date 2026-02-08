<!-- Keep in sync with pages/index.html -->

# q-docs: Interactive Execution for IBM's Qiskit Documentation

## We recommend IBM's official platform

For reading and learning, IBM's official [Quantum Platform](https://quantum.cloud.ibm.com/) and their [Qiskit documentation](https://github.com/Qiskit/documentation) is the best place to start:

- **[Learning](https://quantum.cloud.ibm.com/learning/)** — 13 structured courses covering quantum basics through utility-scale computing, VQE, quantum machine learning, error correction, and more
- **[Tutorials](https://quantum.cloud.ibm.com/docs/en/tutorials)** — 40+ advanced tutorials on transpilation, circuit cutting, error mitigation, Hamiltonian simulation, QAOA, and more
- **[Guides](https://quantum.cloud.ibm.com/docs/en/guides)** — Practical how-to guides for common Qiskit tasks
- **[API Reference](https://quantum.cloud.ibm.com/docs/en/api)** — Versioned documentation for Qiskit and all addons
- **[Source repo](https://github.com/Qiskit/documentation)** — All content is open source (CC BY-SA 4.0)

IBM's platform is always up-to-date, well-designed, and the best place to **read** the documentation.

## What this project adds: interactive execution

This fork ([q-docs](https://github.com/JanLahmann/Qiskit-documentation)) adds [Binder](https://mybinder.org) support so you can **run every notebook in your browser** — no local Python installation, no environment setup. Just click and run.

This is useful when you want to:
- **Learn by doing** — modify code, change parameters, and see results immediately
- **Run a workshop or class** — share a link, and participants are coding in seconds on any device
- **Experiment freely** — try variations on tutorials without worrying about breaking your local setup

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main)

Click the badge above, or jump directly into content:

- **Tutorials:** [mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=docs/tutorials](https://mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=docs/tutorials)
- **Courses:** [mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=learning/courses](https://mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=learning/courses)

## Running notebooks on Binder

### Setting up your IBM Quantum account

Many notebooks connect to IBM Quantum backends. To set this up:

1. **Register** at [quantum.cloud.ibm.com/registration](https://quantum.cloud.ibm.com/registration) — no credit card required for the first 30 days
2. **Sign in** at [quantum.cloud.ibm.com](https://quantum.cloud.ibm.com/) and select region **us-east** (required for the free Open Plan)
3. **Create an instance** (free Open Plan) at [Instances](https://quantum.cloud.ibm.com/instances) if you don't have one yet
4. **Create an API key** at [quantum.cloud.ibm.com](https://quantum.cloud.ibm.com/) (or at [cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys))
5. **Copy your CRN** (Cloud Resource Name) from your [Instances](https://quantum.cloud.ibm.com/instances) page
6. **Save your credentials once per Binder session** — in any notebook, add a new cell and run:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    token="<your-api-key>",
    instance="<your-crn>",
    overwrite=True
)
```

Binder sessions are ephemeral, so you need to re-enter your credentials each time.

**Troubleshooting:** If you can't see any instances or backends, check that your region is set to **us-east** and try switching accounts (menu in the upper-right corner). See the [IBM Cloud setup guide](https://quantum.cloud.ibm.com/docs/en/guides/cloud-setup) for more details.

### No token? Use local testing mode

You can run most notebooks without an IBM Quantum account by replacing the backend with a local simulator. Replace `service = QiskitRuntimeService()` and `backend = service.least_busy(...)` with one of:

**FakeBackend (simulates real device noise):**
```python
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
backend = FakeManilaV2()
```

**AerSimulator (ideal, no noise):**
```python
from qiskit_aer import AerSimulator
backend = AerSimulator()
```

Both work with `SamplerV2` and `EstimatorV2` from `qiskit_ibm_runtime` — no other code changes needed. See the [local testing mode guide](https://quantum.cloud.ibm.com/docs/en/guides/local-testing-mode) for more details.

---

### doQumentation.org — run code inline

Or use [doQumentation.org](https://doQumentation.org) to **run code inline** — browse any tutorial as a rendered page, click **Run** on a code block, and it executes right there. No Jupyter interface needed. Available as:

- **[RasQberry](https://github.com/JanLahmann/RasQberry-Two)** — Self-hosted on Raspberry Pi with local Jupyter kernel (full features)
- **[Docker](https://github.com/JanLahmann/doQumentation/pkgs/container/doqumentation)** — Run the full stack locally with `docker compose up`
- **[GitHub Pages](https://doQumentation.org)** — Static site using [Binder](https://mybinder.org) for remote code execution

## Pre-installed packages

The Binder environment includes these core packages:

| Package | Version |
|---------|---------|
| qiskit (with visualization extras) | ~2.3.0 |
| qiskit-aer | ~0.17 |
| qiskit-ibm-runtime | ~0.43.1 |
| pylatexenc | latest |

This also includes **matplotlib**, **numpy**, **scipy**, and other standard scientific Python libraries via Qiskit dependencies.

## Installing additional packages

Some notebooks require packages beyond the core set. Install them in a notebook cell:

```python
!pip install -q scipy scikit-learn plotly
```

Or install everything at once:

```python
!pip install -q scipy scikit-learn qiskit-ibm-transpiler qiskit-experiments plotly sympy qiskit-serverless qiskit-ibm-catalog qiskit-addon-sqd qiskit-addon-utils qiskit-addon-mpf qiskit-addon-aqc-tensor[aer,quimb-jax] qiskit-addon-obp qiskit-addon-cutting pyscf ffsim gem-suite python-sat
```

## How it works

- **`binder/requirements.txt`** — Minimal dependencies kept small so the image fits within MyBinder's registry limits.
- **`binder/runtime.txt`** — Pins the Python version (3.12).
- **`.github/workflows/binder.yml`** — Daily build to keep the image cached, so launches are fast.

The full dependency list used for CI notebook testing is in [`scripts/nb-tester/requirements.txt`](scripts/nb-tester/requirements.txt).

---

Tutorial content &copy; IBM Corp, licensed under CC BY-SA 4.0.
This project is not affiliated with, endorsed by, or sponsored by IBM Corporation.
IBM, IBM Quantum, and Qiskit are trademarks of IBM Corporation.
q-docs is part of the [RasQberry](https://rasqberry.org) project and the basis for [doQumentation.org](https://doQumentation.org).
