# 📸 Vibe Check Playlist

Upload a photo. We'll read your vibe. You'll get the soundtrack.

## Setup

1. **Clone the repo** and `cd` into it

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your [Google Gemini API key](https://aistudio.google.com/apikey):
   ```
   GOOGLE_API_KEY=your_key_here
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Features

- **Vibe Analysis** — Gemini Vision reads the mood, energy, aesthetic, era, and color palette from any photo
- **Vibe Story** — A cinematic 3-4 sentence narrator-style story about your vibe
- **Playlist Generator** — 10 song recommendations with YouTube links
- **Genre Lock** — Force all recommendations into a specific genre (sidebar)
- **Opposite Day** — Flip your vibe and get the polar opposite playlist
- **Battle Mode** — Upload two photos, compare vibes, and get a fusion playlist

## Tech Stack

- Streamlit
- Google Gemini API (gemini-2.0-flash)
- LangChain (LCEL chains)
- Pydantic (structured output parsing)
