import json
import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

# Add project root to path

sys.path.append(
os.path.dirname(
os.path.dirname(
os.path.abspath(__file__)
)
)
)

from config.settings import (
OPENROUTER_MODEL,
MAX_RETRIES,
RETRY_DELAY
)

load_dotenv()

INPUT_FILE = "data/papers/hypotheses.json"
OUTPUT_FILE = "data/papers/experiments.json"

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_experiment(hypothesis_data):
    prompt = f"""
You are a senior AI Research Scientist.

Design a realistic research experiment for the hypothesis below.

Research Gap:
{hypothesis_data.get("research_gap", "")}

Hypothesis:
{hypothesis_data.get("hypothesis", "")}

Potential Contribution:
{hypothesis_data.get("potential_contribution", "")}

Research Direction:
{hypothesis_data.get("research_direction", "")}

Return ONLY valid JSON:

{{
"experiment_title": "...",
"objective": "...",
"dataset": "...",
"baseline": "...",
"proposed_method": "...",
"evaluation_metrics": [
"...",
"...",
"..."
],
"expected_outcome": "...",
"risk_factors": [
"...",
"..."
]
}}
"""

    for attempt in range(MAX_RETRIES):

        try:

            response = client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert researcher "
                            "specialized in experimental design."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5
            )

            return response.choices[0].message.content

        except Exception as e:

            print(
                f"Attempt {attempt + 1}/{MAX_RETRIES} failed:"
            )
            print(e)

            time.sleep(RETRY_DELAY)

    return None


def main():
    print("\\nLoading hypotheses...\\n")

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    hypotheses = json.load(f)

results = []

total = len(hypotheses)

print(f"Found {total} hypotheses.\\n")

for index, hypothesis in enumerate(hypotheses, start=1):

    print("=" * 80)
    print(
        f"Designing experiment "
        f"{index}/{total}: "
        f"{hypothesis['file_name']}"
    )

    response = generate_experiment(
        hypothesis
    )

    if not response:
        continue

    try:

        experiment_data = json.loads(
            response
        )

    except Exception:

        experiment_data = {
            "experiment_title": "",
            "objective": "",
            "dataset": "",
            "baseline": "",
            "proposed_method": "",
            "evaluation_metrics": [],
            "expected_outcome": "",
            "risk_factors": [],
            "raw_response": response
        }

    experiment_data["file_name"] = (
        hypothesis["file_name"]
    )

    results.append(
        experiment_data
    )

    print("Completed")

os.makedirs(
    os.path.dirname(
        OUTPUT_FILE
    ),
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

print("\\nSaved to:")
print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
