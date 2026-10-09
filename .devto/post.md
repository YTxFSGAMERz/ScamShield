*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

## What I Built

Here is a built-in sample text message from ScamShield's test suite:

> *"URGENT: Your SBI net banking account has been BLOCKED due to incomplete KYC. Click immediately to restore access: http://sbi-kyc-update.xyz/verify or call 9876543210."*

Imagine receiving that at 7:00 AM on a basic smartphone. If you spent decades writing paper checks and visiting branch tellers, a text threatening to freeze your pension triggers immediate dread. The reflex is to tap the link or call the number before morning tea gets cold.

### Who It's For

I built ScamShield around a clear design persona: **my dadi** (paternal grandmother).

To be transparent before the deadline: I did not have a real family member test this interface over the weekend, nor do I have real user quotes to share. I chose not to invent reactions or pretend someone tested this who did not. Instead, I treated my dadi as an anchor persona: someone who relies on WhatsApp and SMS to stay connected with family, has no interest in inspecting URL top-level domains, and needs plain, reassuring guidance in her own language when a message feels suspicious. The immediate next step is a real, sit-down handover with her before installing it on her phone.

The problem ScamShield addresses is simple: modern cyber fraud in India—from fake electricity disconnections to "digital arrest" intimidation calls—weaponizes artificial urgency. Older adults are targeted because they respect authority and fear penalties. When panic sets in, they do not need a twenty-page security guide; they need one place to drop a screenshot, paste a confusing message, or look up a strange number and receive a clear answer: **Is this real, or is someone trying to trick me?**

ScamShield groups its core protections into five headline features:

1. **Multimodal Screenshot Vision Scanner**: Users upload a screenshot of an SMS, WhatsApp chat, fake UPI QR code, or banking alert. Google's Gemma multimodal model analyzes layout, typography, sender cues, and manipulation tactics to assign a risk score from 0 to 100.
2. **Text & Phishing URL Inspection**: Direct analysis of raw message text and links, checking lookalike domains (homoglyphs), non-standard extensions (`.xyz`), IP hosts, and coercive phrasing.
3. **Conversational AI Defense Assistant**: A dedicated chat helper powered by Gemma where users ask questions in plain language ("A caller claiming to be police says a parcel has drugs in it; what do I do?") and receive calm, step-by-step guidance.
4. **Golden Hour Victim Recovery Wizard & FIR Generator**: When money has already been sent, the first few hours decide whether funds can be frozen before leaving the banking network. The wizard guides reporting to the 1930 National Cyber Crime helpline, provides direct emergency numbers for ten major Indian retail banks, and drafts a formal police FIR complaint letter.
5. **Family Alert Center**: One-click dispatch that posts formatted fraud alerts to a family Discord channel or generates copy-ready summaries for WhatsApp family groups.

Supporting features include a 15-question scam awareness quiz, an active threat intelligence feed backed by Ministry of Home Affairs advisories, an interactive 10-point security hygiene scorecard, a local phone carrier lookup tool, and a crowdsourced fraud reporting database.

## Demo

- **Live Application**: [https://hacktoberfest-scamshield.vercel.app](https://hacktoberfest-scamshield.vercel.app)
- **GitHub Repository**: [https://github.com/YTxFSGAMERz/hacktoberfest-ScamShield](https://github.com/YTxFSGAMERz/hacktoberfest-ScamShield)

### Try It in 30 Seconds

1. Open the [live demo](https://hacktoberfest-scamshield.vercel.app).
2. Under the header, click **"SBI KYC Block"** in the *Fraudulent / Threats* row.
3. The screenshot auto-loads into the scanner. Click **"Analyze with Gemma 4"**.
4. Review the verdict card: notice the red **SCAM** badge (Risk Score 98/100), the summary, detected red flags, and the action checklist.
5. Click **"Amazon OTP"** under the *Genuine / Legitimate* row and click Analyze. Notice the green **SAFE** verdict (Risk Score 5/100) explaining why the message is benign.

![ScamShield Hero and Screenshot Vision Scanner](https://raw.githubusercontent.com/YTxFSGAMERz/hacktoberfest-ScamShield/de8c599ad131fc4dac4c50bc09eedd8ea40050ea/docs/devto-images/01-scamshield-hero.png)
*The main vision scanner evaluating an urgent fake SBI KYC message, producing a clear risk verdict and immediate safety steps.*

![Text and SMS Message Analyzer](https://raw.githubusercontent.com/YTxFSGAMERz/hacktoberfest-ScamShield/de8c599ad131fc4dac4c50bc09eedd8ea40050ea/docs/devto-images/02-scam-detection-result.png)
*Text message analysis highlighting red flags: lack of an official 6-character TRAI sender header, deceptive top-level domain, and intimidation tactics.*

![AI Safety Assistant](https://raw.githubusercontent.com/YTxFSGAMERz/hacktoberfest-ScamShield/de8c599ad131fc4dac4c50bc09eedd8ea40050ea/docs/devto-images/04-ai-safety-assistant.png)
*Conversational safety assistant deconstructing the anatomy of a 'Digital Arrest' intimidation scheme.*

![Golden Hour Victim Recovery Checklist](https://raw.githubusercontent.com/YTxFSGAMERz/hacktoberfest-ScamShield/de8c599ad131fc4dac4c50bc09eedd8ea40050ea/docs/devto-images/05-victim-recovery-wizard.png)
*Step-by-step crisis response wizard detailing immediate actions, bank contacts, and National Cyber Crime 1930 reporting.*

![Security Hygiene Audit](https://raw.githubusercontent.com/YTxFSGAMERz/hacktoberfest-ScamShield/de8c599ad131fc4dac4c50bc09eedd8ea40050ea/docs/devto-images/06-security-hygiene-audit.png)
*Personal security posture audit evaluating UPI PIN habits, SIM swap risks, and remote desktop application hygiene.*

![Family Alert Broadcast Center](https://raw.githubusercontent.com/YTxFSGAMERz/hacktoberfest-ScamShield/de8c599ad131fc4dac4c50bc09eedd8ea40050ea/docs/devto-images/08-family-alert-broadcast.png)
*Family alert center allowing users to broadcast an urgent warning to a family Discord channel or copy it for WhatsApp.*

## Code

{% embed https://github.com/YTxFSGAMERz/hacktoberfest-ScamShield %}

The repository is open source under the **MIT License**.

### One-Line Setup

```bash
git clone https://github.com/YTxFSGAMERz/hacktoberfest-ScamShield.git && cd hacktoberfest-ScamShield && pip install -r requirements.txt && python -m flask --app api/index.py run --port 5000
```

Copy `.env.example` to `.env` and configure `GEMINI_API_KEY` or connect a local Ollama instance running Gemma.

## How I Built It

ScamShield pairs a Python Flask backend with a lightweight Single Page Application (vanilla HTML5, CSS3, and JavaScript) designed to load instantly on older mobile hardware.

```
[ Browser Client ]  <--->  [ Flask API (api/index.py) ]  <--->  [ AI Router (scamshield/llm.py) ]
  (Vanilla PWA)             (Rate Limiter, Validators)           |
                                                                 +--> Primary: Google Gemma 4 (API)
                                                                 +--> Failover: Ollama (gemma4:e4b Local)
```

### Model Setup and Resilient Fallback Chain

For hosted deployment, ScamShield uses Google's `gemma-4-26b-a4b-it` model via the Google Generative Language API. Because fraud triage cannot tolerate server crashes during a crisis, `scamshield/llm.py` implements an automated fallback chain.

When `LLM_PROVIDER` is set to `auto`:
1. The app queries the Gemini API for structured JSON containing verdict, risk score, executive summary, detected flags, and guidance.
2. If the API errors out (400 Bad Request, quota limit, or timeout), `scamshield/llm.py` logs a warning and automatically fails over to a local Ollama instance running `gemma4:e4b`.
3. Gemma models often produce separate internal reasoning tokens (`p.get("thought", False)`). The extraction engine strips these so the client receives valid JSON.
4. If the model wraps JSON in markdown fences, `_extract_json()` uses multi-stage parsing (direct parse -> regex -> brace match -> fallback dictionary) to avoid crashes.

### One Real Bug from Git History

During multi-language expansion, I hit an import cycle and startup crash (commit `ed6883f`: *"fix: export SUPPORTED_LANGUAGES at top of i18n.py and add defensive import fallbacks"*).

`api/index.py` imported `SUPPORTED_LANGUAGES` from `scamshield/i18n.py`, but `i18n.py` defined it below helper functions with circular references. On Vercel, this threw `ImportError: cannot import name 'SUPPORTED_LANGUAGES'`. Hoisting the dictionary to the top of `scamshield/i18n.py` and adding defensive dictionary fallbacks in `api/index.py` resolved the crash.

### Verification and Test Suite

To guarantee reliability, the codebase includes an automated test suite:
- **54 passed tests** across 4 modules (`test_analyzer.py`, `test_chat_intel.py`, `test_llm.py`, `test_new_features.py`).
- **27.22 seconds** execution time under `pytest` 8.3.4 on Python 3.13.

## Why Does Open Innovation Matter?

Evaluating open models like Gemma against closed APIs highlights key architectural differences:

### Can It Run on a Laptop with No Internet?
**Yes.** On an ordinary laptop (tested on AMD Ryzen 5 6600H, 16 GB RAM, NVIDIA GeForce RTX 3050 6GB Laptop GPU), the open `gemma4:e4b` model (6.6 GB) runs locally via Ollama with CUDA acceleration. The inference pipeline processes queries without an active network connection, keeping the scanner functional during connectivity outages.

### Keep Data Off a Server I Don't Control?
This is critical for family privacy. When an older person receives a suspicious message, it often contains personal details: partial account numbers, their home address, or their phone number. With closed APIs, every screenshot and text snippet must be transmitted to an external corporate endpoint. In ScamShield's local mode, images are processed in memory on localhost and never leave the device.

*Note on hosted demo vs local mode*: The public Vercel demo connects to Google's API endpoint over HTTPS so anyone can try the tool without downloading 6 GB weights. However, local mode keeps all processing confined to the user's machine.

### Swap Models, Fine-Tune, and Customize Behavior
With open weights, developers are never locked into vendor policy shifts or deprecation schedules. If a regional scam vector appears, Gemma can be fine-tuned on regional dialects (such as Gujarati or Marathi SMS patterns) and served on an edge device without requesting third-party permission.

### Cost
Running Gemma locally costs **$0.00** in API fees. For community initiatives, senior centers, or public libraries providing scam verification kiosks, operating without ongoing per-token billing makes continuous protection sustainable.

### Empirical Label Agreement and Latency
I ran ScamShield's built-in synthetic test vectors through the Gemma pipeline to measure classification consistency and latency:

| Test Sample | Category | Expected Verdict | Gemma Verdict | Risk Score | Latency | Agreement |
|---|---|---|---|---|---|---|
| `safe_login_otp.png` | Amazon 2FA Login | SAFE | SAFE | 5 / 100 | 14.84s | ✅ Yes |
| `safe_bank_alert.png` | HDFC Debit Alert | SAFE | SAFE | 5 / 100 | 7.59s | ✅ Yes |
| `kyc_scam.png` | SBI Account Block | SCAM | SCAM | 98 / 100 | 6.98s | ✅ Yes |
| `lottery_scam.png` | WhatsApp Lucky Draw | SCAM | SCAM | 100 / 100 | 8.55s | ✅ Yes |

Across all tested samples, the model achieved **100% agreement** with expected classifications, with a median latency of **8.07 seconds**.

### Where Open Beat Closed
Open technology won here because of **resilience under failure**. When closed APIs hit billing limits, experience regional outages, or block prompts with overly aggressive filters, closed applications break. With ScamShield's dual-tier architecture, if the cloud endpoint fails, the application falls back to a locally running Gemma instance without interrupting the user.

## What It Can't Do Yet & What's Next

1. **A Real Handover to Older Users**: The immediate next step is sitting down with my dadi to watch her navigate the interface. Observing where she hesitates, which button labels confuse her, and whether the text size is comfortable will guide the next release.
2. **Native Mobile App Wrapper**: Right now ScamShield is a responsive Progressive Web App. Packaging it as an Android APK will let older users share screenshots directly via Android's native "Share" menu.
3. **Automated Offline OCR**: Currently, local vision analysis requires a multimodal model. Adding lightweight local Tesseract OCR as a pre-filter will enable instant text extraction on low-end phones before model inference.

## Prize Categories

### Best Use of Gemma

ScamShield competes in the **Best Use of Gemma** category:
- **Multimodal Vision Reasoning**: Uses `gemma-4-26b-a4b-it` to analyze incoming screenshot artifacts, identifying coercive visual cues and deceptive sender branding.
- **Local Edge Capability**: Supports offline execution via `gemma4:e4b` on Ollama, proving that advanced cyber protection can run on consumer laptop hardware without leaking private messages.
- **Thought Token Management & Extraction**: Implements dedicated handling for Gemma's internal reasoning tokens to deliver clean, structured JSON verdicts and actionable emergency checklists.
