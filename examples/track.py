"""Track your AI visibility over time: run a list of buyer questions and append the results to a CSV file.

Usage:
    RAPIDAPI_KEY=your-key python track.py yourbrand.com questions.txt rival1.com rival2.com

questions.txt holds one question per line. Every run appends one row per question and engine to
visibility-log.csv (date, question, engine, cited, in sources, named, rank, score), so a daily or weekly
cron job gives you a trend line for every question. One question = one API request.
"""
import csv
import datetime
import os
import sys

from check import check

LOG = "visibility-log.csv"
COLUMNS = ["date", "question", "engine", "cited", "in_sources", "named", "rank", "engine_score", "visibility_score"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(args) < 2:
        sys.exit(__doc__)
    brand, questions_file, competitors = args[0], args[1], args[2:]
    with open(questions_file, encoding="utf-8") as handle:
        questions = [line.strip() for line in handle if line.strip()]
    today = datetime.date.today().isoformat()
    is_new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if is_new:
            writer.writerow(COLUMNS)
        for question in questions:
            answer = check(brand, question, competitors, **options)
            for result in answer["results"]:
                writer.writerow([
                    today, question, result["engine"], result.get("brandCited"), result.get("brandInSources"),
                    result.get("brandNamedInAnswer"), result.get("brandMentionRank"),
                    answer.get("scoreByEngine", {}).get(result["engine"]), answer["visibilityScore"],
                ])
            cited = sum(1 for result in answer["results"] if result.get("brandCited"))
            print(f'{answer["visibilityScore"]:>3}/100  cited by {cited} of {len(answer["results"])} engines  {question}')
    print(f"Appended to {LOG}")


if __name__ == "__main__":
    main()
