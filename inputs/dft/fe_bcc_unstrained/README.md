# Unstrained bcc Fe DFT Inputs

This directory contains the portable Quantum ESPRESSO input templates for the
bcc Fe workflow used as the base calculation before Wannierization, SAMB
decomposition, magnetization rotation, and AHC post-processing. The files are
derived from the source `FM_sqa_z/.../symwannier/` production inputs and keep
the same SCF -> SOC NSCF split while removing private workstation paths.

The templates are portable versions of the production inputs: private absolute
paths have been replaced by local relative paths and the pseudopotential names
are documented explicitly.

Expected pseudopotentials:

```text
pseudopotentials/Fe.pbe-spn-rrkjus_psl.0.2.1.UPF
pseudopotentials/Fe.rel-pbe-spn-rrkjus_psl.0.2.1.UPF
```

The pseudopotential itself is not committed until redistribution permissions
are confirmed.

## Files

- `scf.in`: self-consistent field input for the collinear starting point.
- `nscf.in`: non-self-consistent SOC input for Wannierization with
  `noncolin = .true.` and `lspinorb = .true.`.

Generated `outdir` contents and wavefunction files are not committed.
