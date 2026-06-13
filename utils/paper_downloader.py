import json
import requests
from pathlib import Path


def load_search_results(
    file_path="data/papers/search_results.json"
):
    """
    Load paper metadata from JSON.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        papers = json.load(file)

    return papers


def download_pdf(
    pdf_url,
    output_path
):
    """
    Download a PDF file.
    """

    try:

        response = requests.get(
            pdf_url,
            timeout=30
        )

        response.raise_for_status()

        with open(
            output_path,
            "wb"
        ) as pdf_file:

            pdf_file.write(
                response.content
            )

        print(
            f"Downloaded: {output_path.name}"
        )

    except Exception as exc:

        print(
            f"Failed to download "
            f"{pdf_url}"
        )

        print(exc)


def download_papers():

    papers = load_search_results()

    papers_dir = Path(
        "data/papers"
    )

    papers_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for index, paper in enumerate(
        papers,
        start=1
    ):

        pdf_url = paper["pdf_url"]

        filename = (
            f"paper_{index}.pdf"
        )

        output_path = (
            papers_dir / filename
        )

        download_pdf(
            pdf_url,
            output_path
        )


if __name__ == "__main__":

    download_papers()