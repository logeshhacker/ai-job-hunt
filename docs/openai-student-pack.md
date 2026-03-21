# OpenAI API credits via the GitHub Student Developer Pack (2026)

This project relies on OpenAI’s API for the AI agents in `backend/app/agents`. Students can obtain limited OpenAI API credits through the GitHub Student Developer Pack. The offer details can change, so always read the current terms shown during redemption.

## What the offer typically includes (as of 2026)
- One-time promotional OpenAI API credits (commonly $50 USD) for verified students.
- Credits apply to API usage (e.g., GPT-4o/3.5 models) — not ChatGPT Plus subscriptions.
- Credits expire; check the expiration date shown in your OpenAI Billing page.
- The offer is available once per OpenAI account and requires GitHub Student verification.

## How to redeem the OpenAI credits
1. **Join the GitHub Student Developer Pack** with a verified school email or upload proof of enrollment.
2. **Log in to your OpenAI account** and open **Billing** → **Promotions / Credits**.
3. Click **Verify with GitHub** (or **Redeem Student Pack offer**) and authorize GitHub.
4. Wait for the confirmation banner that shows the credited amount and expiration date.
5. Note your **OpenAI API key** from **API keys**; you’ll need it for this project.

If you do not see the button, refresh the Billing page or try a desktop browser. If the promotion is not available in your region or has changed, the Billing page will state that.

## Key restrictions to keep in mind
- **Non-transferable & one-time**: The credit can be redeemed only once per OpenAI account.
- **Expiration**: Unused credit expires on the date shown in Billing. Set a reminder.
- **Overage risk**: Usage beyond the credit will charge your payment method (if on file).
- **Region and compliance limits**: Availability depends on your country/region and OpenAI’s acceptable use policies.
- **API-only**: The promo is meant for API usage, not ChatGPT Plus or other consumer plans.

## Using the credits with this project (LangChain + Flask backend)
1. After redeeming, create an API key in the OpenAI **API keys** page.
2. In the backend, set the environment variable (do **not** commit it):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
3. Start the Flask app; the agents in `backend/app/agents/*` will pick up `OPENAI_API_KEY`.
4. To control costs while using LangChain:
   - Prefer cheaper models (e.g., GPT-3.5) when acceptable.
   - Lower `temperature` for deterministic, shorter outputs.
   - Trim prompts (resume/job text) before sending to the model.

## Quick checklist for students
- [ ] Verified GitHub Student Developer Pack account.
- [ ] Redeemed OpenAI promotion in Billing → Promotions.
- [ ] Noted credit amount and expiration date.
- [ ] Generated an API key (kept private).
- [ ] Set `OPENAI_API_KEY` locally/hosted environment for this app.

For the latest terms, always rely on the text presented during redemption in the OpenAI Billing portal.
