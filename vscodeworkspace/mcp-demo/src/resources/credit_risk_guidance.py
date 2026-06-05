CREDIT_RISK_GUIDANCE = """
# Credit Risk Summary Guidance
# MCP Resource: credit-risk://guidance

## Purpose
Extract a concise credit risk summary from a corporate financial document
(e.g. annual report, 10-K) already ingested in the document store.
The goal is to produce 5 bullet points capturing the key credit risk picture.

---

## Step-by-Step Process

### Step 1 — Retrieve the Credit Risk Section
Query the document store for chunks related to "credit risk overview" or "credit risk management".
Focus on the section that describes the organisation's exposure to credit risk,
how it is managed, and the composition of the credit portfolio.

### Step 2 — Identify Credit Risk Sources and Exposure
From the retrieved text, identify:
- The main sources of credit risk (e.g. lending, derivatives, securities financing, structured finance)
- Total credit exposure or loan portfolio size if stated
- Geographic or segment mix (consumer vs. corporate, domestic vs. international)

### Step 3 — Assess Credit Risk Management Framework
Note how the organisation manages credit risk:
- Governance or oversight body responsible for credit risk
- Key risk controls or limits in place
- Credit quality indicators or internal rating approach mentioned

### Step 4 — Identify Key Risk Drivers and Concerns
Look for explicit statements about:
- Areas of elevated or concentrated credit risk
- Changes in credit quality year-over-year (improvements or deterioration)
- External factors cited as risk drivers (economic conditions, sector stress, etc.)

### Step 5 — Produce the 5-Bullet Credit Risk Summary
Based on steps 1–4, write exactly 5 bullet points summarising the credit risk profile:
- Bullet 1: Primary source(s) and overall scale of credit risk exposure
- Bullet 2: Portfolio composition (geographic / counterparty / segment mix)
- Bullet 3: Credit risk management approach and governance
- Bullet 4: Key risk drivers or areas of concern highlighted in the document
- Bullet 5: Overall credit risk assessment (stable / improving / deteriorating) with evidence

---

## Notes for the Agent
- Only use information explicitly stated in the retrieved document chunks.
- Set any field to null if the information is not present in the document.
- Do not infer or estimate values not stated in the document.
- Keep each bullet point concise (1–2 sentences).
- Every bullet point MUST end with a page citation in the format (p. N) using the page_start
  value from the chunk the information was retrieved from.
- If a page number is not available for a chunk, write (page unknown) — never omit the citation.
"""
