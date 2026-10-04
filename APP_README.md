# Buffalo Rare Disease One Search

Independent hackathon prototype for a mechanism-first rare disease discovery app. Branding references the [Buffalo Initiative](https://buffaloinitiative.org/why-ultra-rare-diseases/); this is not an official Buffalo service.

The demo story follows Maria, a patient advocacy leader for STXBP1-related disorder. Instead of searching only by disease name, Maria can search one box for a disease, gene, or mechanism and discover biologically related diseases, publications, researchers, patient groups, confidence levels, and concrete next actions.

## Why this is different

- **Evidence-first graph:** every edge shows a source and confidence level.
- **No supported route state:** unknown searches are explicitly marked as unsupported instead of hallucinated.
- **10x moonshot story:** the app shows how Maria could reuse Dravet and CDKL5 trial-readiness assets to compress early discovery from years to months.
- **Patient-centered actions:** the UI translates graph edges into this-week tasks for Maria.
- **OpenAI-ready:** if `OPENAI_API_KEY` is available, the app uses an OpenAI model to generate a plain-language synthesis. Without a key, the app still runs with a deterministic fallback explanation.

## Graph Explorer

- The first screen contains only a large centered Buffalo Initiative logo and One Search. Submit a disease, gene, or symptom to reveal results; clearing the search returns to the first screen.
- Check any combination of Disease similarity, Mechanism path, and Evidence map. Their graphs are merged; unchecking all views leaves the graph empty.
- Disease similarity shows connected comparison diseases without researcher nodes.
- Mechanism path shows diseases, genes, and mechanisms; Evidence map adds source publications and patient groups.
- Clicking a disease opens symptoms, Ask ChatGPT, publication links, patient groups, and evidence for its connections. Ask ChatGPT opens ChatGPT; it does not automatically send the disease or symptoms.
- Clicking an edge opens its source link, confidence, and plain-language reason. Keyboard Enter and Space also select a disease or edge.
- Publications sort by verified journal impact factor, descending. Each available IF includes a publisher source and metric year (or an explicit unspecified-year label). Unknown or inapplicable IF values appear last. IF measures journals, not individual evidence quality.
- The Researchers tab ranks directly matched researchers by disease-specific publication count in this dataset. Show more expands related-disease and gene researchers. Topic bars use 100 for direct and 50 for related matches; these are explicit categorical scores, not calibrated probabilities. Ties sort by name. The dataset has one authored publication per included researcher, so it does not support claims about their full careers.
- Suggested Action is the first results tab. It groups direct research contacts and related-disease study-design leads with sources, applicability checks, official contact routes and ready-to-review message drafts. No message is sent automatically.
- Contact details are sourced from the official University of Alberta, Necker Hospital and Children's Hospital Colorado directories, checked 4 October 2026. Clinic phone numbers are labeled separately from research contacts.
- Find current contacts with ChatGPT web search uses the Responses API hosted `web_search` tool with `gpt-4.1-mini` (override with `OPENAI_SEARCH_MODEL`). It sends only matched public disease/researcher names, never patient records or the raw search input. Results have clickable citations; uncited responses are not displayed. No key or API failure leaves the official directory links usable. Live search has not been end-to-end tested without a configured key.
- Explain in plain language calls the OpenAI Responses API only when clicked, using `gpt-4o-mini` by default. A source-based preview is shown without an API key. API failures fall back without exposing error details.

Publisher metric sources: [Brain](https://academic.oup.com/Brain/pages/About), [JAMA Neurology](https://jamanetwork.com/journals/jamaneurology/pages/for-authors). These are dated snapshots and are not normalized to a common metric year.

The curated MVP dataset is in:

```text
data/knowledge_graph.json
```

It focuses on:

- STXBP1-related disorder
- Dravet syndrome
- CDKL5 deficiency disorder
- shared mechanisms such as synaptic vesicle release, excitation-inhibition imbalance, synapse development, and ion channel dysfunction

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Optional OpenAI synthesis:

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="gpt-4o-mini"
streamlit run app.py
```

## Demo script for a 60-second video

`demo.mp4` is a silent, 60-second walkthrough assembled from verified app screenshots with English captions. It is not a live screen recording and does not demonstrate a live API call. `demo.srt` contains the captions; `demo_script.md` contains narration for a recorded version.

1. Open the app and search `STXBP1`.
2. Show the mechanism-first graph. Point out that STXBP1 connects to Dravet and CDKL5 through shared seizure-circuit and synaptic mechanisms.
3. Open the Evidence tab. Show that each edge has a source and confidence label.
4. Search `unknown biomarker`. Show the "No supported route yet" state.
5. Return to `STXBP1` and open Suggested Action. Highlight:
   - email a Dravet clinical trial expert
   - reuse the Dravet trial-readiness checklist
   - compare CDKL5 and STXBP1 outcome measures
6. Open the 10x vision tab and describe the 10x planning target as a hypothesis. See `demo_script.md` for the updated narration.

## Deployment

The contents of this folder are a standalone app. Put `app.py`, `requirements.txt`, `assets/`, `data/`, and `.streamlit/config.toml` at the root of a GitHub repository.

For [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), select that repository, branch, and `app.py`. Set Python 3.12 in Advanced settings. Optional secrets:

```toml
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-4o-mini"
```

For [Render](https://render.com/docs/web-services), use the included `render.yaml` as a Blueprint, or create a Python Web Service with build command `pip install -r requirements.txt` and the start command below. Select the Free plan. Optional `OPENAI_API_KEY` is set in service environment variables. [Free service limitations](https://render.com/docs/free) include idle spin-down.

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

The AI API has separate billing; free hosting does not make model calls free. No public deployment is included until a hosting account and repository are connected.


## Safety note

This is a prototype for discovery and planning. It is not medical advice, and all biomedical claims should be reviewed by clinicians and domain experts before use.

The 60-to-6-month comparison is an illustrative planning target, not a measured acceleration of drug development. No clinical benefit or treatment transfer is established by shared graph mechanisms.

Logo source: the image served in the header of the Buffalo page linked above. Biomedical source links are included in the dataset and UI. OpenAI implementation references: [text generation](https://developers.openai.com/api/docs/guides/text?lang=python) and [web search](https://developers.openai.com/api/docs/guides/tools-web-search). Suggested Action functionality is inspired by [Asclepius](https://asclepius.avinash.social/next-step); no styling or data was copied.
