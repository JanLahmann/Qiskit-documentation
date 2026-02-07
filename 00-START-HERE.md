# Run Qiskit notebooks interactively on Binder

This is a fork of [Qiskit/documentation](https://github.com/Qiskit/documentation) that adds Binder support for running notebooks in your browser. For reading the Qiskit documentation, we recommend the official IBM websites — they are more current, better maintained, and have a much better layout and design:

- **Learning:** [quantum.cloud.ibm.com/learning](https://quantum.cloud.ibm.com/learning/)
- **Tutorials:** [quantum.cloud.ibm.com/docs/en/tutorials](https://quantum.cloud.ibm.com/docs/en/tutorials)
- **Source repo:** [github.com/Qiskit/documentation](https://github.com/Qiskit/documentation)

Use this fork (q-docs) when you want to **execute notebooks interactively** — no local setup required:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main)

Click the badge above, or jump directly into content:

- **Tutorials:** [mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=docs/tutorials](https://mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=docs/tutorials)
- **Courses:** [mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=learning/courses](https://mybinder.org/v2/gh/JanLahmann/Qiskit-documentation/main?filepath=learning/courses)

See also [doQumentation.org](https://doQumentation.org) — an open-source documentation platform built on this repository, with deployment options for [RasQberry](https://rasqberry.org), Docker (self-hosted, full features), and [GitHub Pages](https://doQumentation.org) (simplified static deployment).

## Pre-installed packages

The Binder environment includes these core packages:

| Package | Version |
|---------|---------|
| qiskit (with visualization extras) | ~2.3.0 |
| qiskit-aer | ~0.17 |
| qiskit-ibm-runtime | ~0.43.1 |
| pylatexenc | latest |

This also brings in **matplotlib**, **numpy**, **scipy** (via qiskit dependencies), and other standard scientific Python libraries.

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
