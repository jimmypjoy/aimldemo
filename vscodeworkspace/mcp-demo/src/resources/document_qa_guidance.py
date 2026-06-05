DOCUMENT_QA_GUIDANCE = """
# Document Q&A Guidance
# MCP Resource: document-qa://guidance

## Purpose
Answer any user question from the content of an ingested PDF document.
Supported question types:
- Specific factual questions ("What was revenue in 2024?")
- Page summaries ("Summarise page 68")
- Comparisons ("How did X change year-over-year?")
- Open-ended explanations ("Explain the risk management approach")
- List extraction ("What are the main business segments?")

---

## Step-by-Step Process

### Step 1 — Understand the Question Type
Classify the question as one of:
- SPECIFIC_VALUE: user wants a number, date, name, or single fact
- PAGE_SUMMARY: user wants a summary of a specific page
- COMPARISON: user wants a year-over-year or segment-to-segment comparison
- EXPLANATION: user wants a concept or approach explained
- LIST: user wants a list of items, segments, or points

### Step 2 — Query the Document Store
Query the document service with a search phrase derived from the question.
- For SPECIFIC_VALUE: use the exact subject as the query (e.g. "Markets division average loans")
- For PAGE_SUMMARY: query with "page <N>" or the section heading if known
- For COMPARISON: query with the metric and time periods mentioned
- For EXPLANATION or LIST: query with the key concept or topic
Retrieve enough chunks (top_k 5–10) to cover the relevant content.

### Step 3 — Extract the Answer from Chunks
For each retrieved chunk:
- Note the page_start value — this is the page number for citation
- Note the file_name — this is the source document
- Extract only information explicitly stated in the chunk text
- Do not infer, estimate, or combine with external knowledge

### Step 4 — Format the Answer
Respond in exactly the format the user requested:
- If they asked for bullet points → use bullet points
- If they asked for a number → give just the number with its unit
- If they asked for a summary → write a concise paragraph
- If they asked for a comparison → show both values side by side with the change
- Default to a clear, concise paragraph if no format was specified

### Step 5 — Add Page Citations
After every specific fact, number, or statement, add a page citation:
- Format: (p. N) where N is the page_start from the chunk
- If a point spans multiple pages: (p. N, M)
- If page_start is null: (page unknown)
- At the end of the response, list all cited pages under a "Sources" heading

---

## Notes for the Agent
- Only use information explicitly present in the retrieved chunks.
- If the answer is not found in any chunk, say so clearly — do not guess.
- Every factual claim MUST have a (p. N) citation.
- If the user asks for a page summary, retrieve chunks from that specific page and
  summarise all content found there.
- Keep answers focused and proportionate to the question — a specific value question
  needs one sentence, not a paragraph.
"""
