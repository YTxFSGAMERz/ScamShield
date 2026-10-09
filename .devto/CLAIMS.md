# ScamShield — Factual Claims & Verification (CLAIMS.md)

Every factual claim in [.devto/post.md](file:///C:/Users/Admin/Documents/GitHub/hacktoberfest-ScamShield/.devto/post.md) has been cross-referenced against the repository source code, git history, or verified command executions.

| # | Post Claim | Evidence / Proof Source | Status |
|---|---|---|---|
| 1 | Challenge submission for "Build for a Friend" (Weekend Challenge) | Challenge prompt URL `https://dev.to/challenges/hacktoberfest-weekend-2026-10-01` | ✅ Verified |
| 2 | Built for a design persona: "my dadi" | Explicit user instructions (`STORY INPUTS`) | ✅ Verified |
| 3 | No real person handed over before deadline, no fabricated quotes | Verified in `.devto/post.md`, strictly adhered to persona mode | ✅ Verified |
| 4 | Sample SBI KYC block message text and prompt | `api/index.py:168`, `tests/samples/kyc_scam.png` | ✅ Verified |
| 5 | Multimodal screenshot vision analysis via Gemma | `scamshield/analyzer.py:41`, `scamshield/llm.py:291` | ✅ Verified |
| 6 | Phishing URL and homoglyph inspection | `scamshield/scanner_url.py:118` | ✅ Verified |
| 7 | Conversational AI Safety Assistant | `scamshield/chat.py:20` | ✅ Verified |
| 8 | Golden Hour Recovery Wizard & 1930 Helpline | `scamshield/victim_recovery.py:62` | ✅ Verified |
| 9 | 10 major Indian retail banks with emergency numbers | `scamshield/victim_recovery.py:10` (`len(BANK_NUMBERS) == 10`) | ✅ Verified |
| 10 | Automated FIR complaint generator | `scamshield/victim_recovery.py:85` | ✅ Verified |
| 11 | Family Alert Center with Discord webhook and WhatsApp copy | `scamshield/alert.py:63`, `public/app.js:1290` | ✅ Verified |
| 12 | 15 situational questions in scam awareness quiz | `scamshield/quiz_data.py:10` (`len(QUIZ_QUESTIONS) == 15`) | ✅ Verified |
| 13 | 10-point personal security hygiene scorecard | `scamshield/hygiene.py:10` (`len(HYGIENE_CHECKS) == 10`) | ✅ Verified |
| 14 | Live demo URL `https://hacktoberfest-scamshield.vercel.app` | HTTP 200 via `requests.head` | ✅ Verified |
| 15 | GitHub repository `https://github.com/YTxFSGAMERz/hacktoberfest-ScamShield` | HTTP 200 via `requests.head` | ✅ Verified |
| 16 | MIT License | `LICENSE` file in repository root | ✅ Verified |
| 17 | Architecture: Flask backend + Vanilla PWA | `api/index.py`, `public/index.html`, `public/manifest.json` | ✅ Verified |
| 18 | Model configuration: Google Gemma 4 26B IT & Ollama gemma4:e4b | `.env.example`, `scamshield/llm.py:35` | ✅ Verified |
| 19 | Automatic failover chain from Gemini to Ollama | `scamshield/llm.py:321`, verified via terminal execution | ✅ Verified |
| 20 | Thought-token stripping for Gemma (`thought` part filter) | `scamshield/llm.py:317`, `scamshield/llm.py:406` | ✅ Verified |
| 21 | Multi-stage JSON extractor for markdown code fences | `scamshield/llm.py:127` (`_extract_json`) | ✅ Verified |
| 22 | Git history bug fix: `SUPPORTED_LANGUAGES` circular import in `ed6883f` | `git log -1 ed6883f` | ✅ Verified |
| 23 | 54 passed tests across 4 modules in 27.22s | `pytest` run (54 passed in 27.22s on Python 3.13) | ✅ Verified |
| 24 | Local hardware specs: Ryzen 5 6600H, 16GB RAM, RTX 3050 6GB Laptop GPU | `Get-CimInstance Win32_Processor`, `PhysicalMemory`, `VideoController` | ✅ Verified |
| 25 | Local Ollama `gemma4:e4b` model weight (6.6 GB) | `ollama list` output (`6.6 GB`) | ✅ Verified |
| 26 | Sample benchmark: 100% agreement, median latency 8.07s | Empirical test execution over 4 samples (14.84s, 7.59s, 6.98s, 8.55s) | ✅ Verified |
| 27 | Permanent raw GitHub image URLs pinned to commit `de8c599` | All 8 URLs verified returning HTTP 200 | ✅ Verified |
| 28 | No secrets, tokens, or private credentials leaked | Regex secret audit passed (0 matches) | ✅ Verified |
