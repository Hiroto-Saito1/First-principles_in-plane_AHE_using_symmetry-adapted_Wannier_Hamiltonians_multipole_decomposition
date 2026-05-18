# Quantum ESPRESSO Patch Notes

This directory records the `pw2wannier90.f90` source diff used by the local
SymWannier workflow referenced in this repository.

## Upstream Scope

- Quantum ESPRESSO release family: `7.4.1`
- Patched source file: `PP/src/pw2wannier90.f90`
- Patch file in this repository: `pw2wannier90.patch`

The patch was extracted from the maintainer's local reference trees named
`qe-7.4.1_pw2wan_orig/` and `qe-7.4.1_pw2wan/`.

## What The Patch Changes

The diff captures the modifications that were present in the local production
workflow, including:

- noncollinear atomic-projector spin metadata initialization;
- projector-sign handling in the symmetry rotation matrices for the
  `atom_proj` path;
- array reallocation and projector-list compaction when projector exclusions
  are used;
- the symmetry-loop ordering note needed by the SymWannier IBZ expansion path;
- removal of temporary or unused `atom_proj_sym` plumbing from this local
  branch.

## Applying The Patch

From the root of a clean Quantum ESPRESSO `7.4.1` source tree:

```bash
patch -p0 < /path/to/this/repository/docs/qe_patch/pw2wannier90.patch
```

After applying the patch, rebuild the usual `pw2wannier90.x` target in your
Quantum ESPRESSO build.
