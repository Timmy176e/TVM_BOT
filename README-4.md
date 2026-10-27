# TVM Bot — Rule-Based AI Chatbot

**Project 1** of the DecodeLabs AI Engineering Industrial Training (Batch 2026).
Built by Tim Visual.

TVM Bot is a rule-based chatbot: every reply comes from an explicit rule, not
a trained model. The goal of this project isn't broad language understanding —
it's control flow, decision-making logic, and showing why a dictionary lookup
beats a long `if/elif` chain.

## Files

| File             | Purpose                                                              |
|-------------------|-----------------------------------------------------------------------|
| `tvm_bot.py`       | Original console version — runs in a terminal with `input()`         |
| `app.py`           | Streamlit web version — same logic, chat UI, deployable              |
| `requirements.txt` | Python dependencies for `app.py`                                     |

## How it meets the Project 1 spec

| Requirement        | Where it's met                                                   |
|---------------------|---------------------------------------------------------------------|
| Input loop           | `while True` (console) / Streamlit rerun-on-input (web)            |
| Sanitization          | `.lower().strip()` on every message before matching                |
| Knowledge base         | 10 intents, 35+ trigger phrases, well past the 5+ minimum          |
| Fallback                | `"I don't understand that yet."` for anything unmatched            |
| Exit strategy             | `bye` / `goodbye` / `exit` / `quit` / `see you`                    |

## Design notes

- **Dictionary over if-elif**: responses are grouped by intent in a dict, and
  matching is `keyword in message` rather than one `elif` per phrase. This
  keeps lookup flat and easy to extend — adding an intent means adding one
  dict entry, not another branch in a growing chain.
- **Keyword matching, not exact match**: lets "hi there" and "hi" both hit the
  greeting intent. Trade-off: it's a short scan over intents rather than a
  strict O(1) `.get()`, but far more forgiving for a real conversation.
- **Follow-up state (`pending`)**: a couple of intents (the joke and the
  "I'm sad" response) ask a yes/no follow-up and remember it for the next
  message — the bot reacts differently to "yes" depending on what it just
  asked.
- **Name memory**: saying "my name is ___" is remembered for the rest of the
  conversation and used in the goodbye message.

## Running the console version

```bash
python3 tvm_bot.py
```

## Running the Streamlit version locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

This opens the chat UI in your browser at `http://localhost:8501`.

## Deploying to Streamlit Community Cloud

1. Push `app.py` and `requirements.txt` to a GitHub repo (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, pick the repo/branch, and set the main file path to `app.py`.
4. Click **Deploy** — Streamlit installs `requirements.txt` and gives you a
   public URL for TVM Bot.

No secrets or API keys are needed — everything runs on the bundled rules.
