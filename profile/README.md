<div align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/fractalyze-logo-white.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/fractalyze-logo-black.svg" />
    <img alt="Fractalyze" src="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/fractalyze-logo-black.svg" height="80" />
  </picture>
</div>

<br/>

**The confidential and verifiable computing layer.**

We build, optimize, and operate production systems, transforming trust-based digital systems into cryptographically verifiable infrastructure.

## The Computing Layer

A unified platform that automatically transforms high-level cryptographic applications into optimized execution for any target hardware.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/computing-layer-dark.png" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/computing-layer-light.png" />
  <img alt="Today, an application reaches the hardware through five specialist teams, five rounds of handwork and a hardware-specific implementation. With Fractalyze, it reaches the same hardware through one orchestration and compiler layer." src="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/computing-layer-light.png" />
</picture>

Today, getting confidential and verifiable systems into production means cryptography, security, compiler, GPU and infrastructure specialists working in separate silos, months of manual integration and tuning, and starting over for every new scheme or hardware target. We replace that with one compiler that optimizes and generates execution code, a runtime that handles execution and memory, and orchestration that scales the same workload across CPU, GPU, TPU and FPGA.

## The Compiler

Build cryptographic applications in Python. Compile them into highly optimized execution for modern hardware.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/pipeline-dark.png" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/pipeline-light.png" />
  <img alt="Pipeline: Zorch, FRX, StableHLO, XLA, PrimeIR, CPU and GPU." src="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/pipeline-light.png" />
</picture>

**[Zorch]**: Build a SNARK in Python, defining your IOP rounds and composing them. You write the protocol, and never touch the kernels. The blocks it gives you (hashing, Merkle commitment, Reed–Solomon LDE, transcript) hold no scheme-specific knowledge by rule, so a new prover adds only its own glue on top.

**FRX**: Fractalyze's fork of JAX. Traces your Python into a graph and lowers it to StableHLO, carrying field types, not floats. Finite fields are a native dtype here rather than a convention layered over `u32`, so the graph that reaches the compiler still knows it is doing modular arithmetic.

**[XLA]**: Runs a full optimization pipeline over the whole graph, from fusion and layout to lazy reduction, treating it as one program. Stock XLA reshapes programs around tensor algebra over floats and has no way to say that a `u32` is a field element; ours is a fork that can, which is what puts an optimization like lazy reduction on the table at all.

**[PrimeIR]**: Prime Intermediate Representation, an intermediate language based on [MLIR] (Multi-Level Intermediate Representation), dedicated to cryptographic optimization for ZK proofs. It is the level at which `a * b % p` is one field operation instead of three integer instructions, which a general-purpose backend cannot recover, because the language never let you say it.

Provers and proving systems built on this stack:

- **[sp1-zorch]**: A lean SP1 prover on Zorch's blocks, adding only SP1's own commitment and prove glue: SMCS, the shard prover, and the FFI.
- **[openvm-zorch]**: A SWIRL prover and verifier, byte-matched against OpenVM's stark-backend.
- **[zisk-zorch]**: A ZisK prover carrying pil2-stark's Poseidon2–Goldilocks parameters and transcript, with the stage-1 trace commitment byte-matched against pil2-proofman.
- **[pico-zorch]**: A Pico prover, a Plonky3-style univariate STARK, FRI over KoalaBear with Poseidon2, byte-matched against the reference prover.
- **[groth16-zorch]**: A Groth16 prover written in Python on Zorch.
- **[bellman-zorch]**: A GPU Groth16 prover for bellman (BN256/alt_bn128): the h-FFT and all five MSMs in a single fused call, byte-identical to `groth16::create_proof`.
- **[flock-zorch]**: A GPU prover for flock's binary-field R1CS PIOP ([eprint 2026/1329]), authored once in Python and compiled to both CPU and GPU from the same source.
- **[accumulation-zorch]**: A GPU accumulation prover over Pasta: arkworks' `r1cs_nark_as` + `hp_as` prove path as one fused kernel, byte-identical to the reference.

## Benchmarks

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/benchmark-dark.png" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/benchmark-light.png" />
  <img alt="Eleven measured workloads plotted as our speed relative to the baseline, from 3.09x down to 0.94x, crossing parity between msm_bn254_g2 and sp1_logup_gkr." src="https://raw.githubusercontent.com/fractalyze/.github/main/profile/assets/benchmark-light.png" />
</picture>

Our speed as a multiple of the baseline's, measured against ICICLE, SP1 and Binius, with parity at 1, including the two workloads where we are still behind.

---

Read the [blog] and the [docs], or see the whole picture at [fractalyze.io][Fractalyze].

<!-- Reference Links -->
[Fractalyze]: https://fractalyze.io
[Zorch]: https://github.com/fractalyze/zorch
[PrimeIR]: https://github.com/fractalyze/prime-ir
[sp1-zorch]: https://github.com/fractalyze/sp1-zorch
[openvm-zorch]: https://github.com/fractalyze/openvm-zorch
[zisk-zorch]: https://github.com/fractalyze/zisk-zorch
[pico-zorch]: https://github.com/fractalyze/pico-zorch
[groth16-zorch]: https://github.com/fractalyze/groth16-zorch
[bellman-zorch]: https://github.com/fractalyze/bellman-zorch
[flock-zorch]: https://github.com/fractalyze/flock-zorch
[accumulation-zorch]: https://github.com/fractalyze/accumulation-zorch
[eprint 2026/1329]: https://eprint.iacr.org/2026/1329
[XLA]: https://openxla.org/xla
[MLIR]: https://mlir.llvm.org
[blog]: https://www.fractalyze.io/blog
[docs]: https://fractalyze.gitbook.io/intro
