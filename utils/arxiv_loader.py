import json
from pathlib import Path


def load_papers(
    file_path="data/papers/search_results.json"
):
    """
    Load papers from the JSON file generated
    by search_agent.py
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        papers = json.load(file)

    return papers


def display_papers(papers):
    """
    Display loaded papers.
    """

    print(f"\nLoaded {len(papers)} papers.\n")

    for i, paper in enumerate(
        papers,
        start=1
    ):

        print("=" * 80)

        print(f"Paper {i}")
        print(f"Title      : {paper['title']}")

        print(
            f"Authors    : "
            f"{', '.join(paper['authors'])}"
        )

        print(
            f"Published  : "
            f"{paper['published']}"
        )

        print(
            f"Categories : "
            f"{', '.join(paper['categories'])}"
        )

        print("\nAbstract:")
        print(paper['summary'][:500] + "...")

        print("\nPDF:")
        print(paper['pdf_url'])

        print("=" * 80)


if __name__ == "__main__":

    try:

        papers = load_papers()

        display_papers(papers)

    except Exception as exc:

        print("\nFailed to load papers:")
        print(exc)