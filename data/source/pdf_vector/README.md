# PDF Vector Recovery Sources

The multipole-coefficient and minimal-model compact CSV files are recovered
from Matplotlib vector paths embedded in tracked manuscript PDFs because the
original compact source exports were not preserved.

Recovery command:

```bash
python scripts/workflow/extract_pdf_vector_data.py
```

This is a fallback provenance path, not a substitute for first-principles
regeneration. The full desired regeneration path is documented in
`scripts/workflow/generate_large_files.md`.

