import json
import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

# Project root

sys.path.append(
os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from config.settings import OPENROUTER_MODEL, MAX_RETRIES, RETRY_DELAY

load_dotenv()

INPUT_FILE = "data/papers/research_gaps.json"
OUTPUT_FILE = "data/papers/hypotheses.json"

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_hypothesis(paper):
    prompt = f"""
```

You are a world-class AI Research Scientist.

Based on the following paper analysis:

Research Problem:
{paper.get('research_problem', '')}

Methodology:
{paper.get('methodology', '')}

Limitations:
{paper.get('limitations', '')}

Research Gaps:
{chr(10).join(paper.get('research_gaps', []))}

Generate ONE novel research hypothesis.

Return ONLY valid JSON:

{{
"research_gap": "...",
"hypothesis": "...",
"novelty_score": "Low/Medium/High",
"potential_contribution": "...",
"research_direction": "..."
}}
"""


    for attempt in range(MAX_RETRIES):

        try:

            response = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert AI researcher."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"Attempt {attempt + 1}/{MAX_RETRIES} failed:")
            print(e)

            time.sleep(RETRY_DELAY)

    return None


def main():
    print("\nLoading research gaps...\n")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)

    results = []

    total = len(papers)

    print(f"Found {total} papers.\n")

    for index, paper in enumerate(papers, start=1):

        print("=" * 80)
        print(
            f"Generating hypothesis {index}/{total}: "
            f"{paper['file_name']}"
        )

        response = generate_hypothesis(paper)

        if not response:
            continue

        try:
            hypothesis_data = json.loads(response)

        except Exception:

            hypothesis_data = {
                "research_gap": "",
                "hypothesis": "",
                "novelty_score": "",
                "potential_contribution": "",
                "research_direction": "",
                "raw_response": response
            }

        hypothesis_data["file_name"] = paper["file_name"]

        results.append(hypothesis_data)

        print("Completed")

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
