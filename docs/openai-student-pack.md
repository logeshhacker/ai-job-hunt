# OpenAI API Credits — GitHub Student Developer Pack Guide (2026)

This guide explains how OpenAI API access and credits work through the GitHub Student Developer Pack, how to redeem them, key restrictions to know for 2026, and how to use your API key in this project (LangChain + Python).

---

## Table of Contents

1. [Does the Student Pack Include OpenAI Credits?](#1-does-the-student-pack-include-openai-credits)
2. [How to Redeem Your OpenAI Benefit](#2-how-to-redeem-your-openai-benefit)
3. [Key Restrictions for 2026](#3-key-restrictions-for-2026)
4. [Using Your API Key in This Project](#4-using-your-api-key-in-this-project)
5. [High-Level Usage Notes for LangChain and Python](#5-high-level-usage-notes-for-langchain-and-python)
6. [Monitoring and Managing Your Credits](#6-monitoring-and-managing-your-credits)

---

## 1. Does the Student Pack Include OpenAI Credits?

Yes — the GitHub Student Developer Pack includes a free OpenAI API credit grant for verified students. As of 2026:

- **Credit amount:** $5.00 USD in free API credits
- **Model access:** All current OpenAI API models, including `gpt-3.5-turbo` and `gpt-4o-mini`
- **Credit type:** One-time grant (not monthly recurring)
- **Expiry:** Credits expire 1 year from the date they are granted

> **Important:** OpenAI periodically updates the exact credit amount and terms offered through the Student Pack. Always verify the current offer at [education.github.com/pack](https://education.github.com/pack) before redeeming.

---

## 2. How to Redeem Your OpenAI Benefit

Follow these steps exactly to claim your free credits:

### Step 1 — Verify Your GitHub Student Status

1. Go to [education.github.com/pack](https://education.github.com/pack)
2. Click **"Get Student benefits"**
3. Sign in with your GitHub account
4. If prompted, verify your student status by uploading a school ID, enrollment letter, or using your `.edu` email address
5. Wait for verification (usually instant with `.edu` email; up to a few days with a document)

### Step 2 — Find the OpenAI Offer

1. Once verified, return to [education.github.com/pack](https://education.github.com/pack)
2. Scroll through the partner list and find **OpenAI**
3. Click the **"Get access"** button next to the OpenAI offer

### Step 3 — Redeem on OpenAI's Platform

1. You will be redirected to OpenAI's website
2. Sign in or create a free account at [platform.openai.com](https://platform.openai.com)
3. The credit grant will be applied automatically to your account
4. Confirm by going to **Settings → Billing → Usage limits** — you should see a "Free credit" balance of $5.00

### Step 4 — Generate Your API Key

1. In [platform.openai.com](https://platform.openai.com), go to **API Keys** (left sidebar)
2. Click **"Create new secret key"**
3. Give it a name (e.g., `ai-job-hunt-dev`)
4. Copy the key immediately — it will **not** be shown again

---

## 3. Key Restrictions for 2026

Be aware of these restrictions before building or deploying with your Student Pack credits:

| Restriction | Details |
|---|---|
| **One-time grant** | The $5 credit is a single grant, not monthly. It does not renew. |
| **Expiry** | Credits expire 1 year after they are issued. Unused credits are forfeited. |
| **Rate limits** | Free-tier accounts have lower rate limits (e.g., 3 RPM / 200 RPD on some models). Paid tier has much higher limits. |
| **No commercial use** | Student Pack credits are for educational/personal projects only — not commercial products. |
| **One redemption per student** | Each GitHub account can redeem the OpenAI benefit only once. |
| **Account must be verified** | Your OpenAI account must have a verified phone number to create API keys. |
| **Model availability** | Some newer or premium models (e.g., `gpt-4`, `o1`) may require a paid billing plan beyond your free credits. |
| **Country restrictions** | OpenAI API access is unavailable in some countries. Check [openai.com/policies/usage-policies](https://openai.com/policies/usage-policies) for the current list. |

> **Tip:** $5 in credits goes further with `gpt-3.5-turbo` or `gpt-4o-mini` (used by default in this project) than with `gpt-4`. For student projects, stick with `gpt-3.5-turbo` to maximize your credits.

---

## 4. Using Your API Key in This Project

This project uses the `OPENAI_API_KEY` environment variable. Set it as follows:

### Local Development

1. Create a `.env` file in the `backend/` directory (it is already listed in `.gitignore`):

   ```bash
   # backend/.env
   OPENAI_API_KEY=sk-...your-key-here...
   ```

2. The Flask app loads it automatically via `python-dotenv` (see `backend/app/__init__.py`).

3. Start the backend:

   ```bash
   cd backend
   pip install -r requirements.txt
   flask run
   ```

### Production / Deployment

Set `OPENAI_API_KEY` as an environment variable in your hosting platform (DigitalOcean, Render, Railway, etc.) — **never hard-code the key in source code**.

---

## 5. High-Level Usage Notes for LangChain and Python

This project uses `langchain-openai` to connect to the OpenAI API. Here is a summary of the pattern used across all agents:

### How the Agents Work

All agents extend `BaseAgent` (`backend/app/agents/base_agent.py`), which initialises a `ChatOpenAI` LLM:

```python
from langchain_openai import ChatOpenAI

self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",   # Cost-efficient; ideal for student credits
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

Each specific agent (resume, cover letter, chat) builds a `ChatPromptTemplate` and chains it with the LLM and an output parser:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = prompt | self.llm | StrOutputParser()
result = chain.invoke({"input": user_message})
```

### Choosing the Right Model for Your Credits

| Model | Input cost | Output cost | Best for |
|---|---|---|---|
| `gpt-3.5-turbo` | ~$0.50 / 1M tokens | ~$1.50 / 1M tokens | Default — all agents in this project |
| `gpt-4o-mini` | ~$0.15 / 1M tokens | ~$0.60 / 1M tokens | Recommended upgrade — cheaper *and* more capable than gpt-3.5-turbo |
| `gpt-4o` | ~$5.00 / 1M tokens | ~$15.00 / 1M tokens | Highest quality, but burns credits very fast |

With $5 of student credits and `gpt-4o-mini` (assuming ~500 tokens per call — ~300 input + ~200 output), each call costs roughly **$0.00017**, giving you approximately **29,000 calls** before your credits run out. With `gpt-3.5-turbo` at the same token count (~$0.001 per call) you get roughly **5,000 calls** — either is more than enough for development and testing.

### Switching Models

To use a different model, change the `model_name` parameter when instantiating an agent:

```python
# In your Flask route or directly:
from app.agents.chat_agent import ChatAgent

agent = ChatAgent(model_name="gpt-4o-mini")  # cheaper and more capable than gpt-3.5-turbo
```

Or update the default in `BaseAgent.__init__`:

```python
def __init__(self, temperature: float = 0.7, model_name: str = "gpt-4o-mini"):
```

### Environment Variable Quick Reference

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI secret key from the Student Pack |
| `DATABASE_URL` | No | Defaults to `sqlite:///app.db` for local dev |
| `JWT_SECRET_KEY` | No | Defaults to a dev placeholder (change in production) |

---

## 6. Monitoring and Managing Your Credits

To avoid unexpected credit exhaustion:

1. **Check your balance** at [platform.openai.com/usage](https://platform.openai.com/usage)
2. **Set a spending limit** under **Settings → Billing → Usage limits** — set a hard limit of $5 (your total grant) so you are never charged
3. **Enable email alerts** so you receive a notification when you reach 75% and 100% of your credit balance
4. **Use the Usage dashboard** to see which API calls are consuming the most tokens — long prompts are the main cost driver

> **Pro tip:** During development, use short test prompts instead of full resume text to conserve credits. Switch to full inputs only when testing the final flow.

---

## Additional Resources

- [GitHub Student Developer Pack](https://education.github.com/pack) — full list of student benefits
- [OpenAI API Quickstart](https://platform.openai.com/docs/quickstart) — official getting-started guide
- [LangChain + OpenAI docs](https://python.langchain.com/docs/integrations/chat/openai/) — integration reference
- [OpenAI Pricing](https://openai.com/pricing) — current model costs
- [OpenAI Rate Limits](https://platform.openai.com/docs/guides/rate-limits) — free vs. paid tier limits
