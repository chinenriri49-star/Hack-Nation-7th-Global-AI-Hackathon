# Hack-Nation-7th-Global-AI-Hackathon

## Buffalo Rare Disease One Search

A Streamlit hackathon prototype that helps patient communities discover related diseases, evidence, researchers, and research-planning actions. The curated demo covers STXBP1-related disorder, Dravet syndrome, and CDKL5 deficiency disorder.

- Search once by disease, gene, or symptom.
- Combine Disease similarity, Mechanism path, and Evidence map views.
- Select a disease for symptoms, Ask ChatGPT, publication links ordered by verified journal IF, and patient groups.
- Select an edge for its source, confidence, and plain-language explanation.
- Rank researchers by directly relevant authored papers in this dataset; expand related disease and gene researchers with Show more.
- See Suggested Action as the first results tab: contact relevant researchers, discuss adapting study designs, and open official hospital or university contact pages.
- Prepare an outreach message with supporting publications and concrete questions.
- Find current public contacts with ChatGPT web search and clickable source citations.
- Generate optional plain-language explanations with the OpenAI Responses API.

### Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

### Deploy on Streamlit Community Cloud

Select repository `chinenriri49-star/Hack-Nation-7th-Global-AI-Hackathon`, branch `main`, entry point `app.py`, and Python 3.12. The app works without an API key and displays official directory links. To enable live explanations and contact web search, set `OPENAI_API_KEY` in the platform's secrets settings; never commit the key. Contact search uses `gpt-4.1-mini` by default, configurable with `OPENAI_SEARCH_MODEL`. Live API search has not been verified with a configured key.

Suggested Action functionality takes inspiration from [Asclepius](https://asclepius.avinash.social/next-step): concrete next steps, evidence, applicability questions, and an outreach draft.

### Submission

- [Detailed README](APP_README.md)
- [60-second captioned screenshot walkthrough](demo.mp4)
- [English narration](demo_script.md)
- [Render deployment configuration](render.yaml)

```bash
python -m unittest discover -s . -p test_app.py
```

This is an independent hackathon prototype, not an official Buffalo Initiative service or medical advice. The researcher counts cover only the curated dataset. Missing IF values and unsupported routes are explicit. The 10x comparison is a planning target, not a measured drug-development outcome.
