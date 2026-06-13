import json
import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
OPENROUTER_MODEL,
MAX_RETRIES,
RETRY_DELAY,
SUMMARY_FILE,
GAP_FILE
)

load_dotenv()

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=os.getenv("OPENROUTER_API_KEY")
)

def analyze_paper(summary_text):
    prompt = f"""


You are an expert AI Research Scientist.

Analyze the research paper summary below.

Think like a senior AI researcher.

Identify:

1. Core Research Problem
2. Methodology
3. Limitations

Then generate:

4. Research Gaps
   - gaps not explicitly mentioned
   - overlooked opportunities
   - unresolved scientific questions
   - practical deployment challenges

5. Future Research Directions

Focus on originality and novelty.

Return ONLY valid JSON in this format:

{{
"research_problem": "...",
"methodology": "...",
"limitations": "...",
"research_gaps": [
"...",
"...",
"..."
],
"future_work": [
"...",
"...",
"..."
]
}}

Paper Summary:
{summary_text}
"""

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research analysis expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Attempt {attempt+1}/{MAX_RETRIES} failed:")
            print(e)
            time.sleep(RETRY_DELAY)

    return None


def main():
    print("\nLoading summaries...\n")

    with open(
        SUMMARY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        summaries = json.load(f)

    all_results = []

    total = len(summaries)

    print(f"Found {total} papers.\n")

    for index, paper in enumerate(summaries, start=1):

        print("=" * 80)
        print(
            f"Analyzing {index}/{total}: "
            f"{paper['file_name']}"
        )

        result = analyze_paper(
            paper["summary"]
        )

        if not result:

            continue

        try:

            parsed = json.loads(result)

        except:

            parsed = {
                "research_problem": "",
                "methodology": "",
                "limitations": "",
                "research_gaps": [],
                "future_work": [],
                "raw_response": result
            }

        parsed["file_name"] = paper["file_name"]

        all_results.append(parsed)

        print("Completed")

    os.makedirs(
        os.path.dirname(GAP_FILE),
        exist_ok=True
    )

    with open(
        GAP_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_results,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved to:")
    print(GAP_FILE)


if __name__ == "__main__":
    main()
