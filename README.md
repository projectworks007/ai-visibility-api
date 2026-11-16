# AI Visibility API: is your brand in ChatGPT, Perplexity, Claude and Gemini answers?

One GET request asks **ChatGPT, Perplexity, Claude, Gemini and Google AI Overviews** the same buyer question and tells you, per engine, whether your brand is cited, where it ranks against your competitors, and which pages the AI used as sources. JSON back in about 30 to 60 seconds. **No AI API keys needed.**

**[Get a free key on RapidAPI (10 checks a month)](https://rapidapi.com/highbrowfame/api/ai-visibility-api-chatgpt-perplexity-claude-gemini)** and check your own brand in two minutes.

This repository holds ready-to-run examples in Python, Node.js and curl: a one-off brand check, a competitor leaderboard and a tracker that logs your AI visibility to CSV day by day.

## Quick start

```bash
curl --get "https://ai-visibility-api-chatgpt-perplexity-claude-gemini.p.rapidapi.com/ai-visibility/check" \
  --data-urlencode "brand=hubspot.com" \
  --data-urlencode "query=best CRM for small business" \
  --data-urlencode "competitors=salesforce.com,pipedrive.com,zoho.com" \
  -H "x-rapidapi-key: YOUR_KEY" \
  -H "x-rapidapi-host: ai-visibility-api-chatgpt-perplexity-claude-gemini.p.rapidapi.com"
```

| Parameter | Required | Meaning |
| --- | --- | --- |
| `brand` | yes | Your website domain, e.g. `hubspot.com` |
| `query` | yes | The question as people ask an AI assistant, e.g. `best CRM for small business` |
| `competitors` | no | Up to 5 competitor domains, comma separated; each gets a place on the leaderboard |
| `engines` | no | `chatgpt`, `perplexity`, `claude`, `gemini`, `google-ai-overviews` (default: all five) |
| `language` | no | Language of the question and the answers, 24 supported (`en`, `de`, `fr`, `es`, `it`, `pt`, ...) |
| `country` | no | 2-letter country for Google AI Overviews (default `us`) |
| `answer` | no | `false` leaves out the full answer texts for a smaller response |

`GET /ai-visibility/engines` describes the engines, the limits and every field of an answer.

## Python: check a brand against its competitors

[`examples/check.py`](examples/check.py), no dependencies:

```bash
RAPIDAPI_KEY=your-key python examples/check.py hubspot.com "best CRM for small business" salesforce.com pipedrive.com zoho.com
```

```text
AI Visibility Score for hubspot.com: 75/100   "best CRM for small business"
  chatgpt              cited: named #1                    7 sources
  perplexity           cited: in sources, named #1        15 sources
  claude               cited: named #1                    10 sources
  gemini               cited: named #1                    7 sources
  google-ai-overviews  cited: named #1                    3 sources
Leaderboard
  1. hubspot.com             75   named by 100% of engines  (you)
  2. zoho.com                68   named by 100% of engines
  3. salesforce.com          67   named by 100% of engines
  4. pipedrive.com           67   named by 100% of engines
```

A real answer from 16 November 2026. Node.js 18+ version: [`examples/check.mjs`](examples/check.mjs).

## Track your AI visibility over time

AI answers change from week to week. [`examples/track.py`](examples/track.py) runs your list of buyer questions and appends the result to a CSV file, so a daily or weekly cron job gives you a trend line for every question and every engine:

```bash
RAPIDAPI_KEY=your-key python examples/track.py yourbrand.com examples/questions.txt rival1.com rival2.com
```

```text
 75/100  cited by 2 of 2 engines  best CRM for small business
 78/100  cited by 2 of 2 engines  best free CRM for startups
Appended to visibility-log.csv
```

```csv
date,question,engine,cited,in_sources,named,rank,engine_score,visibility_score
2026-11-16,best CRM for small business,chatgpt,True,False,True,1,75,75
2026-11-16,best free CRM for startups,chatgpt,True,True,True,1,78,78
```

Open the CSV in a spreadsheet or feed it to your dashboard. The day a competitor overtakes you in ChatGPT, you see it.

## Other languages and markets

Buyers in Germany, France or Spain get different answers. Ask in their language:

```bash
RAPIDAPI_KEY=your-key python examples/check.py yourbrand.de "bestes CRM für kleine Unternehmen" --language=de
```

## What an answer holds

A real answer, shortened: [`sample-response.json`](sample-response.json).

| Field | Meaning |
| --- | --- |
| `visibilityScore`, `scoreByEngine` | One 0-100 AI Visibility Score, and a score per engine |
| `leaderboard` | You and your competitors ranked by score, with the share of engines that name each |
| `results[].brandCited` | Is the brand in this engine's answer at all |
| `results[].brandInSources`, `brandNamedInAnswer` | Linked as a source, named in the text, or both |
| `results[].brandMentionRank` | Who is named first: your place among the brands in the answer |
| `results[].citations` | Every source the engine used: URL, domain, title. These are the pages AI trusts |
| `results[].shareOfSources` | How many of the sources belong to you and to each competitor |
| `results[].competitors` | The same cited / in sources / named checks for every competitor |
| `results[].answer` | The engine's full answer text |

## What people build with it

- GEO and AEO reporting for SEO agencies: one score per client, per question, per engine
- LLM brand monitoring dashboards and weekly "share of AI voice" reports
- Alerts when a competitor starts to be recommended instead of you
- Content gap finders: which sources does ChatGPT cite for your category, and are you on them?
- AI agents that check a brand's visibility as one step of a larger workflow

## Plans

| Plan | Price | Checks per month |
| --- | --- | --- |
| Basic | free | 10 |
| Pro | $9.99 | 75 |
| Ultra | $29.99 | 250 |

One check = one question to all five engines. Figures as shown on the [pricing page](https://rapidapi.com/highbrowfame/api/ai-visibility-api-chatgpt-perplexity-claude-gemini/pricing) on 16 November 2026; the pricing page always has the current ones.

## Prefer a no-code tracker?

The same checks run as a ready-made tool on Apify: paste your brand, your competitors and a list of prompts, schedule it, and get a table you can export or send to Google Sheets. Pay per result, no subscription: **[AI Search Visibility Tracker on Apify](https://apify.com/highbrow_fame/ai-search-visibility-tracker)**.

## FAQ

**Do I need OpenAI, Anthropic, Perplexity or Google keys?** No. One RapidAPI key covers all five engines.

**How long does a check take?** All engines are asked at once, so about as long as the slowest one: usually 30 to 60 seconds. Set your client timeout to three minutes. Fewer engines answer faster.

**Do the engines search the web?** Yes. ChatGPT, Perplexity, Claude and Gemini answer with web search switched on, as they do for real users, and Google AI Overviews is read from Google's results (English only; many searches have none).

**Does the free plan include every engine?** Yes, with one limit: ChatGPT is included while the month's free ChatGPT allowance lasts. After that a free check returns the other four engines and tells you so. Paid plans do not draw on that allowance.

**Why does the score change between runs?** AI answers are not fixed: the same question can name different brands an hour later. That is why tracking over time tells you more than a single check.

**Something missing?** Open an issue here or use the Discussions tab on the RapidAPI page.

## Start now

**[Subscribe to the free plan on RapidAPI](https://rapidapi.com/highbrowfame/api/ai-visibility-api-chatgpt-perplexity-claude-gemini)**, copy your key, and run `examples/check.py` with your own domain and the question your buyers ask. Ten checks a month cost nothing; the Pro plan tracks two questions every day for $9.99.

---

The example code is MIT licensed. This project is independent and is not affiliated with OpenAI, Perplexity, Anthropic or Google. Maintained by highbrow_fame.
