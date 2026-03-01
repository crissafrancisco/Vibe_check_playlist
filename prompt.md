# Claude Code Prompt: "Vibe Check Playlist" — Streamlit App

## What to build

Build a Streamlit app called **"Vibe Check Playlist"**. The user uploads a photo (selfie, room, scenery, outfit, anything), and the AI reads the "vibe" from the image, generates a mood profile, writes a poetic vibe story, and recommends a playlist of 10 songs that match the photo's energy — with YouTube search links for each song.

## Tech stack

- **Streamlit** for frontend
- **Google Gemini API** (gemini-2.0-flash or gemini-2.5-flash) for multimodal vision + text generation
- **LangChain** with `ChatGoogleGenerativeAI` for chaining
- **LangChain sequential chains** (use LCEL with the pipe `|` operator)
- **Pydantic output parser** to get structured JSON for the song recommendations
- Python, deployed locally with `streamlit run app.py`

## How it works (step by step)

1. **User uploads a photo** via `st.file_uploader`
2. **Gemini Vision** analyzes the image and extracts: dominant mood, color palette, energy level (1-10), aesthetic/vibe name, era/decade feel, emotional tone, and a one-line "vibe summary"
3. **Chain 1 — Vibe Profile**: Takes the vision analysis and produces a structured vibe profile (mood, energy, aesthetic, era, vibe summary)
4. **Chain 2 — Vibe Story**: Takes the vibe profile and writes a short, poetic, cinematic 3-4 sentence "vibe story" — as if narrating the user's life like a movie scene. Make it dramatic, funny, and a little over-the-top
5. **Chain 3 — Playlist Generator**: Takes the vibe profile and generates 10 song recommendations. Each song should have: song name, artist, genre, a one-line "why this song matches your vibe" explanation, and a YouTube search URL formatted as `https://www.youtube.com/results?search_query={song}+{artist}` (URL-encoded)
6. **Display everything** in a beautiful Streamlit layout

## Fun features to include

- **"Opposite Day" button**: Regenerates the playlist for the EXACT opposite vibe (if chill → intense, if happy → moody, etc.)
- **Genre Lock dropdown**: Let the user force all recommendations into a specific genre (K-pop, Lo-fi, Reggaeton, Classical, Hip-hop, Indie, Latin, Afrobeats, etc.) — this is a `st.selectbox` in the sidebar
- **"Battle Mode" toggle**: In the sidebar, let users upload TWO photos. The AI compares both vibes and declares a winner with a fun roast of both vibes, then generates a combined "fusion playlist" that merges both vibes
- **Vibe Meter**: A visual emoji energy scale from 🧊 (chill) to 🔥 (intense) based on the energy score

## Streamlit layout and UI requirements

- Use a clean, modern layout with `st.columns` for the song cards
- Show the uploaded image at the top
- Vibe Profile displayed as a styled card (use `st.container` or custom HTML/CSS in `st.markdown`)
- Vibe Story in a highlighted/quoted block
- Songs displayed as a grid of cards (3 columns), each card showing: song name (bold), artist, genre tag, why it matches, and a clickable "▶ Listen on YouTube" link
- Sidebar contains: Genre Lock selector, Opposite Day button, Battle Mode toggle
- Use fun emojis throughout the UI
- Add a catchy header/subtitle like: "📸 Vibe Check Playlist" / "Upload a photo. We'll read your vibe. You'll get the soundtrack."
- Make it look good — add some custom CSS via `st.markdown` for card styling, rounded corners, subtle shadows, nice fonts

## Structured output format for songs (use Pydantic)

```python
class Song(BaseModel):
    name: str
    artist: str
    genre: str
    why: str  # one-line explanation of why this matches the vibe
    youtube_url: str

class VibeProfile(BaseModel):
    mood: str
    energy: int  # 1-10
    aesthetic: str
    era: str
    color_palette: list[str]  # 3-5 colors
    vibe_summary: str

class PlaylistResponse(BaseModel):
    vibe_story: str
    songs: list[Song]
```

## Environment setup

- Use `python-dotenv` for the API key
- The user will have a `.env` file with `GOOGLE_API_KEY=xxxxx`
- Include a `requirements.txt` with all dependencies
- Include a `README.md` with setup instructions

## Important notes

- Do NOT use Spotify API or any external music API — just Gemini for everything
- YouTube links should be search URLs (no API needed), just URL-encode the song + artist
- Make the AI responses fun, Gen-Z friendly, a little dramatic and funny — not corporate or boring
- The vibe story should feel like a movie narrator or a horoscope — entertaining to read
- Song recommendations should be real songs that actually exist (prompt Gemini to only suggest real, well-known songs)
- Handle errors gracefully (no image uploaded, API failure, etc.)
- Add a spinner with a fun message while loading (e.g., "🔮 Reading your aura..." or "🎵 Curating your soundtrack...")

## File structure

```
vibe-check-playlist/
├── app.py              # main Streamlit app
├── chains.py           # LangChain chains and prompts
├── models.py           # Pydantic models
├── styles.py           # custom CSS strings
├── .env.example        # template for API key
├── requirements.txt
└── README.md
```

## Vibe of the project

Think of this as something you'd demo at a hackathon and people would take out their phones to try it. It should be visually fun, the AI output should make people laugh or go "whoa that's accurate", and the whole experience should take less than 30 seconds from upload to playlist. Make it delightful.
