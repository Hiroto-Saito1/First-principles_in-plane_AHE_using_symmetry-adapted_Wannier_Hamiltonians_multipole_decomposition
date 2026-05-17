# Unstrained bcc Fe DFT Inputs

This directory contains initial Quantum ESPRESSO input templates for the bcc Fe
workflow used as the base calculation before Wannierization, SAMB
decomposition, magnetization rotation, and AHC post-processing.

The templates are portable versions of the production inputs: private absolute
paths have been replaced by local relative paths.

Expected pseudopotential:

```text
pseudopotentials/Fe.pbe-spn-rrkjus_psl.0.2.1.UPF
```

The pseudopotential itself is not committed until redistribution permissions
are confirmed.

## Files

- `scf.in`: self-consistent field input.
- `nscf.in`: non-self-consistent input for Wannierization.

Generated `outdir` contents and wavefunction files are not committed.
