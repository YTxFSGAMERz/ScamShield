# ScamShield Technical Audit & Findings

This document records the exact technical reality of the codebase as verified during Phase 1 & 2 audit. No claims are assumed; everything below is grounded in actual file implementations and test executions.

---

## 1. Screenshot Data Lifecycle & Storage

* **In-Memory Handling**: When a user uploads a screenshot (`/api/analyze`), the image is received in Flask via `request.files['file']` or Base64 payload in JSON. The binary data is validated (`validate_image` in `scamshield/analyzer.py` checking magic numbers PNG/JPEG and max 10MB limit) and resized in-memory using Pillow (`scamshield/llm.py:269`, `_prepare_image`) to a max dimension of 1024x1024.
* **Disk & Database Persistence**: **Zero storage**. The uploaded image is never written to disk, temporary folders, databases, or object storage. Once the HTTP response is dispatched, the in-memory bytes are discarded by garbage collection.
* **Client-Side Storage**: In the frontend (`public/app.js`), the screenshot is loaded into an `<img>` tag via `FileReader.readAsDataURL()` for visual preview. The Base64 preview is **not** stored in `localStorage`; only the analysis verdict metadata (date, type, risk score, summary) is preserved in `localStorage` under `scamshield_history`.
* **Outbound Provider Destinations**:
  * **Gemini Mode** (`LLM_PROVIDER=gemini` or default `auto`): The image bytes are Base64-encoded and sent directly over TLS via HTTPS POST to Google's Generative Language API endpoint (`https://generativelanguage.googleapis.com/v1beta/models/gemma-4-26b-a4b-it:generateContent`).
  * **Ollama Mode** (`LLM_PROVIDER=ollama` or local failover): The image bytes are Base64-encoded and transmitted locally to `http://localhost:11434/api/generate` (or `OLLAMA_BASE_URL` / Ollama Cloud if configured). In pure local mode, zero bytes leave the host machine.

---

## 2. Failover Chain & Asymmetries

* **Screenshot Vision Analysis (`scamshield/analyzer.py` -> `scamshield/llm.py`)**:
  * `analyze_screenshot()` delegates to `scamshield.llm.analyze_image()`.
  * If `LLM_PROVIDER=auto` or `gemini`, it invokes the Gemini API. If an HTTP error (e.g. 400 Bad Request, 403 Forbidden, rate limit, or network drop) occurs, the exception is caught, logged (`logger.warning("Gemini API call failed... Triggering automatic failover...")`), and execution automatically falls through to Ollama (`_ollama_available()` check).
  * If both fail, an `LLMError` is raised containing error details from all attempted providers.
* **Text / SMS Scanner Gap (`scamshield/scanner_text.py` vs `scamshield/llm.py`)**:
  * `api/index.py` routes `/api/scan/text` to `scamshield.scanner_text.analyze_text`.
  * In `scamshield/scanner_text.py` (lines 334–397), text analysis calls Gemini directly via requests without implementing Ollama fallback. If Gemini fails, it raises `RuntimeError("ScamShield text analysis failed: ...")`.
  * Contrast: `scamshield/llm.py` contains a separate `analyze_text()` function (lines 347–448) that *does* implement Gemini-to-Ollama fallback. Because `api/index.py` imports from `scamshield.scanner_text`, the text scanner route lacks the automatic failover capability present in the screenshot vision route.
* **AI Chat Assistant (`scamshield/chat.py`)**:
  * Properly implements fallback: attempts Gemini first, falls back to Ollama if Gemini fails.

---

## 3. UI Input Transmission to AI Models

* **SMS Header / TRAI Header in Screenshot Tab**:
  * In `public/index.html` and `public/app.js`, there is an input field for "TRAI / SMS Header (Optional)" (`#scanner-header-input`).
  * In `public/app.js` (line 369), `sender_id` is appended to FormData and sent to `/api/analyze`.
  * In `api/index.py` (line 199 & 217), `sender_id` is extracted from request.
  * **Finding**: In `api/index.py` line 223, `analyze_screenshot(image_bytes, lang=language)` is called *without passing `sender_id`*. Furthermore, `scamshield/analyzer.py` line 41 `analyze_screenshot` does not accept a `sender_id` argument. As a result, any TRAI sender header entered in the Screenshot tab is silently omitted from the prompt sent to Gemma.
* **Text Scanner Tab**:
  * The text input and sender header *do* reach the model prompt in `scamshield/scanner_text.py`.
* **Heuristic & Offline Tabs**:
  * **URL Scanner (`scamshield/scanner_url.py`)**: Uses local Python regex, domain parsing, and suspicious keyword detection. Does not call LLM.
  * **Phone Scanner (`scamshield/scanner_phone.py`)**: Uses telecom circle dictionary and local fraud prefix regex. Does not call LLM.
  * **Quiz (`scamshield/quiz_data.py`)**: Static dataset of 15 questions with local answer verification. Does not call LLM.
  * **Recovery Wizard (`scamshield/victim_recovery.py`)**: Procedural checklist and template-based FIR complaint generation. Does not call LLM.
  * **Security Hygiene (`scamshield/hygiene.py`)**: Interactive client-side evaluation. Does not call LLM.

---

## 4. Webhook URL Validation & Security

* **Discord Webhook (`scamshield/alert.py:77`)**:
  ```python
  if not webhook_url or webhook_url == "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token":
      return False, "Discord webhook URL not configured..."
  ```
* **Finding**: Validation only ensures the string is non-empty and is not the default `.env.example` placeholder string.
* **Security Risk**:
  * There is no regex or URL parsing to confirm the target domain is `discord.com` or `canary.discord.com`.
  * If a user or malicious actor configures a custom URL (e.g. internal IP or arbitrary webhook), `requests.post()` will issue an unvalidated outbound HTTP POST request (Server-Side Request Forgery risk).
  * Webhook execution does not leak secrets, but requires rigorous domain validation in production.

---

## 5. Multilingual & i18n Reality

* **Supported Languages Count**: 25 languages are registered in `SUPPORTED_LANGUAGES` in `scamshield/i18n.py`.
* **Complete UI Dictionaries**: Native UI string translations (`t(lang, key)`) exist only for **English (`en`)**, **Hindi (`hi`)**, and **Gujarati (`gu`)**.
* **Remaining 22 Languages**: For languages 4 through 25 (Tamil, Telugu, Bengali, Marathi, etc.), UI interface chrome defaults to English, but the language code is forwarded to Gemma's prompt (`scamshield/llm.py`), instructing Gemma to render the `summary`, `threat_signals`, and `actions` in the target language.

---

## 6. Real Test Suite Statistics

* **Test Framework**: `pytest` 8.3.4 with `pytest-asyncio` 0.24.0 and `pytest-mock` 3.16.0.
* **Verified Test Count**: **54 tests collected, 54 passed (100% pass rate)**.
* **Measured Runtime**: **27.22 seconds**.
* **Test Distribution**:
  * `tests/test_analyzer.py`: 11 tests (image validation, scam/safe classification, Hindi/Gujarati outputs, bounds checking, sample existence)
  * `tests/test_chat_intel.py`: 7 tests (emergency contacts, trend data, Golden hour integrity, Gemini & Ollama fallback chat)
  * `tests/test_llm.py`: 19 tests (provider availability checks, JSON markdown fence extraction, Discord alerting, i18n lookups, Gemma failover to Ollama)
  * `tests/test_new_features.py`: 17 tests (quiz data & API, victim recovery & bank directory, hygiene score, community report CRUD, URL/phone scanners, languages API)
