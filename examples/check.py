"""Ask ChatGPT, Perplexity, Claude, Gemini and Google AI Overviews one question and see whether they cite your brand.

Usage:
    RAPIDAPI_KEY=your-key python check.py hubspot.com "best CRM for small business" salesforce.com pipedrive.com zoho.com
    RAPIDAPI_KEY=your-key python check.py yourbrand.de "bestes CRM für kleine Unternehmen" --language=de
    RAPIDAPI_KEY=your-key python check.py yourbrand.com "your question" --engines=chatgpt,perplexity

First argument: your domain. Second: the question as buyers ask it. The rest: up to 5 competitor domains.
No dependencies (Python 3.8+), no AI keys needed. Free key (10 checks a month):
https://rapidapi.com/highbrowfame/api/ai-visibility-api-chatgpt-perplexity-claude-gemini
"""
import json
import os
import sys
import urllib.parse
import urllib.request

HOST = "ai-visibility-api-chatgpt-perplexity-claude-gemini.p.rapidapi.com"
BASE = "https://" + HOST


def check(brand, query, competitors=(), answer=False, **options):
    """One request = one question to every engine. Returns the API answer as a dict.

    options: engines="chatgpt,perplexity", language="de", country="gb".
    """
    params = {"brand": brand, "query": query, "answer": "true" if answer else "false"}
    if competitors:
        params["competitors"] = ",".join(competitors)
    params.update({key: value for key, value in options.items() if value})
    request = urllib.request.Request(
        BASE + "/ai-visibility/check?" + urllib.parse.urlencode(params),
        headers={"x-rapidapi-key": os.environ["RAPIDAPI_KEY"], "x-rapidapi-host": HOST},
    )
    # All engines are asked at once; an answer usually takes 30 to 60 seconds.
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)


def describe(result):
    """'cited: in sources, named #2' for one engine's result."""
    if not result.get("brandCited"):
        return "not cited"
    how = []
    if result.get("brandInSources"):
        how.append("in sources")
    if result.get("brandNamedInAnswer"):
        rank = result.get("brandMentionRank")
        how.append(f"named #{rank}" if rank else "named")
    return "cited: " + ", ".join(how)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(args) < 2:
        sys.exit(__doc__)
    brand, query, competitors = args[0], args[1], args[2:]
    answer = check(brand, query, competitors, **options)
    print(f'AI Visibility Score for {answer["brand"]}: {answer["visibilityScore"]}/100   "{query}"')
    for result in answer["results"]:
        print(f'  {result["engine"]:<20} {describe(result):<34} {result.get("citationCount", 0)} sources')
    print("Leaderboard")
    for row in answer.get("leaderboard", []):
        you = "  (you)" if row.get("isBrand") else ""
        print(f'  {row["rank"]}. {row["domain"]:<22} {row["score"]:>3}   named by {row["mentionRatePct"]}% of engines{you}')
    for problem in answer.get("problems", []):
        print("  problem:", problem.get("error") or problem)


if __name__ == "__main__":
    main()
