<div align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/Fractalyze-logo-light.svg" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/Fractalyze-logo-dark.svg" />
    <img alt="Fractalyze" src="./assets/Fractalyze-logo-dark.svg" height="80" />
  </picture>
</div>

<br/>

[Fractalyze] builds the core compiler infrastructure to accelerate the ZK R&D cycle. We use advanced AI tools to optimize large, memory-bound ZK workloads and suggest proven, high-performance framework for proving schemes. This establishes the next ZK engineering paradigm, shrinking the research-to-production lifecycle from years to months.

This GitHub organization hosts our Python proving scheme framework ([Zorch]) and compiler stack ([PrimeIR], [ZKX]), enabling automatic optimization for various target environments.

## From Craft to Compiler: AI and ZK

<div align="center">
  <img src="./assets/ai-compiler.png" alt="AI Compiler Evolution" width="60%" />
  <br/>
  <img src="./assets/zk-compiler.png" alt="ZK Compiler Evolution" width="60%" />
</div>

Just as [PyTorch] + [XLA] freed ML engineers from manual GPU tuning, [Zorch] + [ZKX]/[PrimeIR] frees ZK researchers from manual proving system engineering.

## Core Projects
<div align="center">
  <img src="./assets/compiler-pipeline.png" alt="Compiler Pipeline" width="60%" />
</div>

**[ZKX]**: ZKX(ZKAccelerator) is a compiler for ZK proofs, analogous to [XLA] for machine learning. [ZKX] enables end-to-end optimization across diverse proving schemes, custom circuits, and zkVMs, automatically targeting multiple hardware backends (GPU, TPU, FPGA, mobile GPU).

**[PrimeIR]**: PrimeIR(Prime Intermediate Representation) is an intermediate language based on **[MLIR]**(Multi-Level Intermediate Representation) dedicated to cryptographic optimization for ZK proofs.

**[Zorch]**: A Python-first frontend for ZK proving schemes. Inspired by [PyTorch]'s ergonomics, [Zorch] allows researchers to write frontend(e.g., circuit, zkVM) in intuitive Python while automatically generating optimized backend through our compiler stack.

## Learn More

Explore our [blog] and [gitbook] to understand how we're accelerating the path to a verifiable world where proof replaces trust.

<!-- Reference Links -->
[Fractalyze]: https://fractalyze.io
[ZKX]: https://github.com/fractalyze/zkx
[PrimeIR]: https://github.com/fractalyze/prime-ir
[Zorch]: https://github.com/fractalyze/zorch
[PyTorch]: https://pytorch.org
[XLA]: https://openxla.org/xla
[MLIR]: https://mlir.llvm.org
[blog]: https://www.fractalyze.io/blog
[gitbook]: https://fractalyze.gitbook.io/intro
