import os
import sys
import csv
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

if not api_key:
    print("Error: OPEN_API_KEY not found in environmet variable")
    sys.exit(1)

client = OpenAI(api_key = api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

PROMPT_DIR = Path("prompts")
TEST_DATA_FILE = Path("evaluation/rewrite_test_cases.csv")
REPORT_FILE = Path("evaluation/prompt_evaluation_report.csv")

#-------------------------------
# 5. Load prompt template
# -------------------------------
def load_prompt(prompt_name, **variables):
    """
     Load a prompt template from the prompts directory and replace template variables.
    """
    prompt_file = PROMPT_DIR/prompt_name

    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    template = prompt_file.read_text(encoding = "utf-8")

    return template.format(**variables)

#-------------------------------
# 6. Load test cases
# -------------------------------
def load_test_cases():
    if not TEST_DATA_FILE.exists():
        raise FileNotFoundError(f"Test data file not found: {TEST_DATA_FILE}")
    with open(TEST_DATA_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

#-------------------------------
# 6. Call LLM
# -------------------------------
def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model = MODEL,
            messages = [
                {"role": "system", "content": "You are a professional test case writing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=100
        )
        return response
    except AuthenticationError:
        print("Authentication Error: Please check your OPEN_API_KEY")
        sys.exit(1)
    except APIConnectionError:
        print("API Connection Error: Please check your internet connection")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def run_experiment(prompt_file, test_cases):
    results = []
    print("\n")
    print("=" * 70)
    print(f"Running experiment with prompt: {prompt_file}")
    print("=" * 70)

    for test_case in test_cases:
        test_id = test_case["id"]
        input_text = test_case["input_text"]
        prompt = load_prompt(prompt_file, text = input_text)

        response = call_llm(prompt)
        output = response.choices[0].message.content.strip()
        results.append({
            "id": test_id,
            "input": input_text,
            "output": output,
            "prompt": prompt_file
        })
        print(f"\n Test Case {test_id}")
        print("Input :", input_text)
    return results

#-------------------------------
# 7.Simple formatting evaluation
# -------------------------------
def evaluate_formatting(output):
    score = 1
    if not output.strip():
        score = 0

    if len(output.split()) > 50:
        score = 0

    unwanted_phrases = ["here is the rewritten sentence",
                        "sure",
                        "certainly",
                        "the rewritten sentence is"]
    output_lower = output.lower()
    for phrase in unwanted_phrases:
        if phrase in output_lower:
            score = 0
            break
    return score

def save_report(results):
    REPORT_FILE.parent.mkdir(parents = True, exist_ok = True)

    with open(REPORT_FILE, "w", newline = "", encoding = "utf-8") as f:
        fieldnames = [
            "id",
            "prompt",
            "input",
            "output",
            "formatting_score"
        ]
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()

        for result in results:
            result["formatting_score"] = evaluate_formatting(result["output"]) 
            writer.writerow(result)
    print(f"\n Evaulation report saved to: {REPORT_FILE}")

#-------------------------------
# 8. Main application
# -------------------------------
def main():
    test_cases = load_test_cases()
    print(f"Loaded {len(test_cases)} test cases.")

    zero_shot_results = run_experiment("rewrite_zero_shot.txt", test_cases)

    few_shot_results = run_experiment("rewrite_few_shot.txt", test_cases)

    all_results = (zero_shot_results + few_shot_results)

    save_report(all_results)

if __name__ == "__main__":
    main()