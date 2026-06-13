import json
import re
from pathlib import Path

import fitz
from transformers import pipeline


print("Loading summarization model...")

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

print("Model loaded!")


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF.
    """

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as exc:

        print(
            f"Error reading {pdf_path}: {exc}"
        )

    return text


def clean_text(text):
    """
    Clean whitespace.
    """

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_key_sections(text):
    """
    Extract:
    - Abstract
    - Introduction
    - Conclusion

    Fallback:
    first 6000 words.
    """

    lower = text.lower()

    abstract_match = re.search(
        r"abstract(.*?)(introduction|1\s*introduction)",
        lower,
        re.DOTALL
    )

    conclusion_match = re.search(
        r"(conclusion|conclusions)(.*?)(references|bibliography|$)",
        lower,
        re.DOTALL
    )

    extracted = ""

    if abstract_match:

        extracted += text[
            abstract_match.start():
            abstract_match.end()
        ]

    intro_pos = lower.find("introduction")

    if intro_pos != -1:

        extracted += text[
            intro_pos:
            min(
                intro_pos + 12000,
                len(text)
            )
        ]

    if conclusion_match:

        extracted += text[
            conclusion_match.start():
            conclusion_match.end()
        ]

    if len(extracted.split()) < 500:

        words = text.split()

        extracted = " ".join(
            words[:6000]
        )

    return extracted


def limit_text_size(
    text,
    max_words=4000
):
    """
    Hard cap.
    Prevents huge papers
    from creating 70+ chunks.
    """

    words = text.split()

    if len(words) > max_words:

        words = words[:max_words]

    return " ".join(words)


def chunk_text(
    text,
    chunk_size=500
):
    """
    Safe chunking.
    """

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[
                i:i + chunk_size
            ]
        )

        chunks.append(chunk)

    return chunks


def generate_summary(text):

    chunks = chunk_text(text)

    summaries = []

    print(
        f"Total Chunks: {len(chunks)}"
    )

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        if len(chunk.split()) < 40:
            continue

        try:

            print(
                f"Summarizing chunk "
                f"{index}/{len(chunks)}"
            )

            result = summarizer(
                chunk,
                max_length=120,
                min_length=30,
                truncation=True,
                do_sample=False
            )

            summaries.append(
                result[0]["summary_text"]
            )

        except Exception as exc:

            print(
                f"Chunk {index} failed:"
            )

            print(exc)

    return " ".join(summaries)


def process_pdfs():

    papers_dir = Path(
        "data/papers"
    )

    pdf_files = list(
        papers_dir.glob("*.pdf")
    )

    if not pdf_files:

        print(
            "No PDF files found."
        )

        return

    all_results = []

    for pdf_file in pdf_files:

        print("\n" + "=" * 80)

        print(
            f"Processing "
            f"{pdf_file.name}"
        )

        text = extract_text_from_pdf(
            pdf_file
        )

        text = clean_text(text)

        text = extract_key_sections(
            text
        )

        text = limit_text_size(
            text,
            max_words=4000
        )

        word_count = len(
            text.split()
        )

        print(
            f"Word Count: "
            f"{word_count}"
        )

        summary = generate_summary(
            text
        )

        paper_result = {

            "file_name":
                pdf_file.name,

            "word_count":
                word_count,

            "summary":
                summary,

            "research_problem":
                "Not extracted yet",

            "methodology":
                "Not extracted yet",

            "limitations":
                "Not extracted yet",

            "future_work":
                "Not extracted yet"
        }

        all_results.append(
            paper_result
        )

    output_file = (
        papers_dir /
        "paper_summaries.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved summaries to:")
    print(output_file)


if __name__ == "__main__":

    process_pdfs()

