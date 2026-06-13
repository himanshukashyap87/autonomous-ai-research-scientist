import time
import json
import arxiv
from requests.exceptions import ConnectionError


def search_papers(topic, max_results=5, retries=5, backoff_seconds=5):
    """
    Search papers from ArXiv with retry and rate-limit handling.
    """

    client = arxiv.Client(
        page_size=20,
        delay_seconds=3,
        num_retries=3
    )

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    for attempt in range(1, retries + 1):

        try:

            papers = []

            for result in client.results(search):

                papers.append({
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "summary": result.summary,
                    "pdf_url": result.pdf_url,
                    "published": str(result.published.date()),
                    "categories": result.categories
                })

            return papers

        except arxiv.HTTPError as exc:

            if "429" in str(exc):

                print("\nArXiv rate limit reached.")
                print("Please wait a few minutes and try again.")

                return []

            if attempt == retries:
                raise

            wait_time = backoff_seconds * attempt

            print(
                f"ArXiv request failed "
                f"(attempt {attempt}/{retries}): {exc}"
            )

            print(f"Retrying in {wait_time} seconds...\n")

            time.sleep(wait_time)

        except ConnectionError as exc:

            if attempt == retries:
                raise

            wait_time = backoff_seconds * attempt

            print(
                f"Connection failed "
                f"(attempt {attempt}/{retries}): {exc}"
            )

            print(f"Retrying in {wait_time} seconds...\n")

            time.sleep(wait_time)

    return []


def save_results(
    papers,
    output_file="data/papers/search_results.json"
):
    """
    Save results for downstream agents.
    """

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            papers,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":

    topic = input("\nEnter research topic: ")

    try:

        papers = search_papers(
            topic=topic,
            max_results=5
        )

        if not papers:

            print(
                "\nNo papers found "
                "or ArXiv rate limit reached."
            )

        else:

            print(f"\nFound {len(papers)} papers.\n")

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
                print(
                    paper['summary'][:500]
                    + "..."
                )

                print("\nPDF:")
                print(paper['pdf_url'])

                print("=" * 80)

            save_results(papers)

    except Exception as exc:

        print("\nFailed to retrieve papers:")
        print(exc)