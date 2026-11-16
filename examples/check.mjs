// Ask ChatGPT, Perplexity, Claude, Gemini and Google AI Overviews one question and see whether they cite your brand.
// Node.js 18+, no dependencies, no AI keys needed.
//
//   RAPIDAPI_KEY=your-key node check.mjs hubspot.com "best CRM for small business" salesforce.com pipedrive.com
//   RAPIDAPI_KEY=your-key node check.mjs yourbrand.com "your question" --engines=chatgpt,perplexity
//
// Free key (10 checks a month):
// https://rapidapi.com/highbrowfame/api/ai-visibility-api-chatgpt-perplexity-claude-gemini

const HOST = 'ai-visibility-api-chatgpt-perplexity-claude-gemini.p.rapidapi.com';
const BASE = `https://${HOST}`;

// options: { engines: 'chatgpt,perplexity', language: 'de', country: 'gb', answer: 'true' }
export async function check(brand, query, competitors = [], options = {}) {
    const params = new URLSearchParams({ brand, query, answer: 'false', ...options });
    if (competitors.length) params.set('competitors', competitors.join(','));
    const response = await fetch(`${BASE}/ai-visibility/check?${params}`, {
        headers: { 'x-rapidapi-key': process.env.RAPIDAPI_KEY, 'x-rapidapi-host': HOST },
        // All engines are asked at once; an answer usually takes 30 to 60 seconds.
        signal: AbortSignal.timeout(180_000),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    return response.json(); // { visibilityScore, scoreByEngine, leaderboard, results: [...], problems: [...] }
}

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
if (args.length >= 2) {
    const [brand, query, ...competitors] = args;
    const flags = process.argv.slice(2).filter((a) => a.startsWith('--') && a.includes('='));
    const answer = await check(brand, query, competitors, Object.fromEntries(flags.map((a) => a.slice(2).split('='))));
    console.log(`AI Visibility Score for ${answer.brand}: ${answer.visibilityScore}/100   "${query}"`);
    for (const r of answer.results) {
        const how = [r.brandInSources && 'in sources', r.brandNamedInAnswer && (r.brandMentionRank ? `named #${r.brandMentionRank}` : 'named')].filter(Boolean);
        const text = r.brandCited ? `cited: ${how.join(', ')}` : 'not cited';
        console.log(`  ${r.engine.padEnd(20)} ${text.padEnd(34)} ${r.citationCount ?? 0} sources`);
    }
    console.log('Leaderboard');
    for (const row of answer.leaderboard ?? []) {
        console.log(`  ${row.rank}. ${row.domain.padEnd(22)} ${String(row.score).padStart(3)}   named by ${row.mentionRatePct}% of engines${row.isBrand ? '  (you)' : ''}`);
    }
}
