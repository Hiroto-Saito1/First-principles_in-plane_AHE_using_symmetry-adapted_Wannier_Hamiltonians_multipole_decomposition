from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import tempfile
from pathlib import Path

from _common import DEFAULT_OUTPUT_DIAGNOSTICS, DEFAULT_OUTPUT_PAPER, REPO_ROOT, get_pyplot


REFERENCE_ROOT = REPO_ROOT / "figures" / "paper"
DEFAULT_CONTACT_SHEET_OUTPUT = (
    DEFAULT_OUTPUT_DIAGNOSTICS / "contact_sheets" / "paper_vs_reference.pdf"
)


class FigurePair:
    def __init__(
        self,
        *,
        figure_file: str,
        reference_pdf: Path,
        generated_pdf: Path,
        generated_rel: Path,
    ) -> None:
        self.figure_file = figure_file
        self.reference_pdf = reference_pdf
        self.generated_pdf = generated_pdf
        self.generated_rel = generated_rel


def inventory_rows() -> list[dict[str, str]]:
    with (REPO_ROOT / "data" / "processed" / "figure_inventory.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        return list(csv.DictReader(handle))


def reproducible_pairs(
    paper_root: Path = DEFAULT_OUTPUT_PAPER,
    reference_root: Path = REFERENCE_ROOT,
) -> list[FigurePair]:
    pairs: list[FigurePair] = []
    for row in inventory_rows():
        if row["reproduction_category"] != "reproducible_plot":
            continue
        generated_rel = Path(row["generated_output"]).relative_to("results/figures_paper")
        pairs.append(
            FigurePair(
                figure_file=row["figure_file"],
                reference_pdf=reference_root / Path(row["included_pdf"]).name,
                generated_pdf=paper_root / generated_rel,
                generated_rel=generated_rel,
            )
        )
    return pairs


def require_ghostscript() -> str:
    gs = shutil.which("gs")
    if gs is None:
        raise RuntimeError(
            "Ghostscript `gs` is required to rasterize PDF pages for the contact sheet."
        )
    return gs


def rasterize_first_page(gs: str, pdf: Path, png: Path, dpi: int) -> None:
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            gs,
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-dTextAlphaBits=4",
            "-dGraphicsAlphaBits=4",
            "-dFirstPage=1",
            "-dLastPage=1",
            "-sDEVICE=pngalpha",
            f"-r{dpi}",
            f"-sOutputFile={png}",
            str(pdf),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def chunked(items: list[FigurePair], size: int) -> list[list[FigurePair]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def render_contact_sheet(
    pairs: list[FigurePair],
    output: Path,
    *,
    dpi: int = 120,
    pairs_per_page: int = 3,
) -> None:
    if pairs_per_page < 1:
        raise ValueError("pairs_per_page must be at least 1")
    if not pairs:
        raise ValueError("No reproducible paper figures were found in the inventory")
    for pair in pairs:
        if not pair.reference_pdf.is_file():
            raise FileNotFoundError(f"Missing reference PDF: {pair.reference_pdf}")
        if not pair.generated_pdf.is_file():
            raise FileNotFoundError(
                f"Missing generated paper PDF: {pair.generated_pdf}. "
                "Run scripts/reproduce_all_figures.sh --paper-only first."
            )

    gs = require_ghostscript()
    plt = get_pyplot()
    import matplotlib.image as mpimg
    from matplotlib.backends.backend_pdf import PdfPages

    output.parent.mkdir(parents=True, exist_ok=True)
    pages = chunked(pairs, pairs_per_page)

    with tempfile.TemporaryDirectory(prefix="paper_contact_sheet_") as tmpdir:
        tmp = Path(tmpdir)
        with PdfPages(output) as pdf:
            for page_index, page_pairs in enumerate(pages, start=1):
                fig, axes = plt.subplots(
                    len(page_pairs),
                    2,
                    figsize=(11.2, 3.8 * len(page_pairs) + 0.6),
                )
                if len(page_pairs) == 1:
                    axes = [axes]

                fig.suptitle(
                    "Paper Figure Contact Sheet: reference vs generated",
                    fontsize=14,
                    y=0.992,
                )
                axes[0][0].set_title("Reference (`figures/paper/`)", fontsize=10)
                axes[0][1].set_title("Generated (`results/figures_paper/`)", fontsize=10)

                for row_index, pair in enumerate(page_pairs):
                    ref_png = tmp / f"page_{page_index:02d}_row_{row_index:02d}_ref.png"
                    gen_png = tmp / f"page_{page_index:02d}_row_{row_index:02d}_gen.png"
                    rasterize_first_page(gs, pair.reference_pdf, ref_png, dpi)
                    rasterize_first_page(gs, pair.generated_pdf, gen_png, dpi)

                    for axis, png_path in zip(axes[row_index], [ref_png, gen_png]):
                        image = mpimg.imread(png_path)
                        axis.imshow(image)
                        axis.axis("off")

                    figure_label = pair.figure_file.removesuffix(".pdf")
                    axes[row_index][0].text(
                        0.0,
                        1.04,
                        figure_label,
                        transform=axes[row_index][0].transAxes,
                        fontsize=10,
                        fontweight="bold",
                        va="bottom",
                    )
                    axes[row_index][1].text(
                        1.0,
                        -0.06,
                        str(pair.generated_rel),
                        transform=axes[row_index][1].transAxes,
                        fontsize=7,
                        ha="right",
                        va="top",
                    )

                fig.text(
                    0.5,
                    0.015,
                    f"page {page_index} of {len(pages)}",
                    ha="center",
                    fontsize=8,
                )
                fig.tight_layout(rect=(0.015, 0.03, 0.985, 0.965))
                pdf.savefig(fig)
                plt.close(fig)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create a PDF contact sheet comparing committed paper-reference PDFs "
            "against generated manuscript-style outputs."
        )
    )
    parser.add_argument(
        "--paper-root",
        type=Path,
        default=DEFAULT_OUTPUT_PAPER,
        help="Root directory that contains generated manuscript-style PDFs.",
    )
    parser.add_argument(
        "--reference-root",
        type=Path,
        default=REFERENCE_ROOT,
        help="Root directory that contains committed paper-reference PDFs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_CONTACT_SHEET_OUTPUT,
        help="Output PDF path for the contact sheet.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=120,
        help="Rasterization DPI for PDF preview images.",
    )
    parser.add_argument(
        "--pairs-per-page",
        type=int,
        default=3,
        help="How many figure pairs to place on each contact-sheet page.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    pairs = reproducible_pairs(
        paper_root=args.paper_root,
        reference_root=args.reference_root,
    )
    render_contact_sheet(
        pairs,
        args.output,
        dpi=args.dpi,
        pairs_per_page=args.pairs_per_page,
    )
    print(f"Wrote paper contact sheet to: {args.output}")


if __name__ == "__main__":
    main()
