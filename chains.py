import base64
import urllib.parse

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from models import VibeProfile, PlaylistResponse

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEXT_MODEL = "llama-3.3-70b-versatile"


def get_llm(model: str = TEXT_MODEL):
    return ChatGroq(model=model, temperature=0.9)


def get_vision_llm():
    return ChatGroq(model=VISION_MODEL, temperature=0.9)


# ---------------------------------------------------------------------------
# Chain 1 — Vision analysis → VibeProfile
# ---------------------------------------------------------------------------

VISION_PROMPT = """You are a vibe analyst with supernatural aesthetic instincts.
Look at this image and extract the VIBE. Be dramatic, specific, and fun.

Return your analysis as valid JSON with exactly these fields:
- "mood": the dominant emotional mood (e.g., "melancholic main character energy", "chaotic brunch energy")
- "energy": integer from 1 (comatose chill) to 10 (unhinged hype)
- "aesthetic": the aesthetic/vibe name (e.g., "dark academia", "coastal grandmother", "feral goblincore")
- "era": the decade or era this feels like (e.g., "late 90s", "2010s Tumblr", "Y2K")
- "color_palette": list of 3-5 dominant color names from the image
- "vibe_summary": a single punchy sentence capturing the whole vibe

Be creative and entertaining. Think like a Gen-Z astrology girlie who moonlights as a film critic.
Return ONLY valid JSON, no markdown formatting, no code blocks."""


def analyze_image(image_bytes: bytes) -> VibeProfile:
    """Use Groq Vision to extract the vibe from an uploaded image."""
    llm = get_vision_llm()
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    message = HumanMessage(
        content=[
            {"type": "text", "text": VISION_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ]
    )

    parser = JsonOutputParser(pydantic_object=VibeProfile)
    response = llm.invoke([message])
    profile_dict = parser.parse(response.content)
    return VibeProfile(**profile_dict)


# ---------------------------------------------------------------------------
# Chain 2 — VibeProfile → Vibe Story
# ---------------------------------------------------------------------------

STORY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a cinematic narrator who speaks like a mix of Wes Anderson, "
        "a horoscope writer, and a chaotic bestie. Write a short 3-4 sentence "
        "'vibe story' based on the vibe profile below. Make it dramatic, funny, "
        "a little over-the-top, and deeply relatable. It should read like a "
        "movie voiceover narrating someone's main character moment.\n\n"
        "Rules:\n"
        "- Use vivid imagery and metaphors\n"
        "- Reference the mood, aesthetic, and era\n"
        "- Make the reader feel SEEN\n"
        "- Keep it to 3-4 sentences max\n"
        "- No emojis in the story itself — just pure cinematic prose"
    )),
    ("human", (
        "Vibe Profile:\n"
        "Mood: {mood}\n"
        "Energy: {energy}/10\n"
        "Aesthetic: {aesthetic}\n"
        "Era: {era}\n"
        "Colors: {colors}\n"
        "Vibe Summary: {vibe_summary}\n\n"
        "Write the vibe story:"
    )),
])


def generate_vibe_story(profile: VibeProfile) -> str:
    """Chain 2: Generate a cinematic vibe story from the profile."""
    llm = get_llm()
    chain = STORY_PROMPT | llm | StrOutputParser()
    return chain.invoke({
        "mood": profile.mood,
        "energy": profile.energy,
        "aesthetic": profile.aesthetic,
        "era": profile.era,
        "colors": ", ".join(profile.color_palette),
        "vibe_summary": profile.vibe_summary,
    })


# ---------------------------------------------------------------------------
# Chain 3 — VibeProfile → Playlist (10 songs)
# ---------------------------------------------------------------------------

PLAYLIST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a legendary music curator who can match any vibe to the perfect "
        "playlist. You know every genre, every era, every hidden gem.\n\n"
        "Rules:\n"
        "- Recommend exactly 10 songs that match the given vibe\n"
        "- Songs MUST be real, well-known songs by real artists\n"
        "- Each song needs: name, artist, genre, and a one-line 'why' explanation\n"
        "- The 'why' should be fun and specific to the vibe (not generic)\n"
        "- For youtube_url: format as https://www.youtube.com/results?search_query={{url_encoded_song}}+{{url_encoded_artist}}\n"
        "- Mix mainstream and slightly underground picks\n"
        "- Make sure the songs actually MATCH the mood, energy, and aesthetic\n"
        "{genre_lock_instruction}"
        "\n\nReturn ONLY valid JSON with this exact structure:\n"
        '{{"vibe_story": "ignore this field, put empty string", '
        '"songs": [{{"name": "...", "artist": "...", "genre": "...", '
        '"why": "...", "youtube_url": "..."}}]}}\n'
        "No markdown, no code blocks, just raw JSON."
    )),
    ("human", (
        "Vibe Profile:\n"
        "Mood: {mood}\n"
        "Energy: {energy}/10\n"
        "Aesthetic: {aesthetic}\n"
        "Era: {era}\n"
        "Colors: {colors}\n"
        "Vibe Summary: {vibe_summary}\n"
        "{opposite_instruction}"
        "\nGenerate the playlist:"
    )),
])


def generate_playlist(
    profile: VibeProfile,
    genre_lock: str | None = None,
    opposite: bool = False,
) -> list:
    """Chain 3: Generate 10 song recommendations from the vibe profile."""
    llm = get_llm()

    genre_lock_instruction = ""
    if genre_lock and genre_lock != "No Lock (Any Genre)":
        genre_lock_instruction = f"\n- ALL songs MUST be from the {genre_lock} genre. No exceptions.\n"

    opposite_instruction = ""
    if opposite:
        opposite_instruction = (
            "\n⚠️ OPPOSITE DAY MODE: Generate the playlist for the EXACT OPPOSITE "
            "vibe. If the mood is chill, make it intense. If happy, make it moody. "
            "If nostalgic, make it futuristic. Flip EVERYTHING. The songs should be "
            "the polar opposite of what this vibe would normally get.\n"
        )

    chain = PLAYLIST_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({
        "mood": profile.mood,
        "energy": profile.energy,
        "aesthetic": profile.aesthetic,
        "era": profile.era,
        "colors": ", ".join(profile.color_palette),
        "vibe_summary": profile.vibe_summary,
        "genre_lock_instruction": genre_lock_instruction,
        "opposite_instruction": opposite_instruction,
    })

    parser = JsonOutputParser(pydantic_object=PlaylistResponse)
    result = parser.parse(raw)
    songs = result.get("songs", [])

    # Fix YouTube URLs if needed
    for song in songs:
        query = f"{song['name']} {song['artist']}"
        song["youtube_url"] = (
            f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
        )

    return songs


# ---------------------------------------------------------------------------
# Battle Mode — Compare two vibes
# ---------------------------------------------------------------------------

BATTLE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a vibe battle referee — think of yourself as a sassy reality TV "
        "judge who roasts contestants with love. You're comparing two vibes head-to-head."
    )),
    ("human", (
        "VIBE 1:\n"
        "Mood: {mood_1} | Energy: {energy_1}/10 | Aesthetic: {aesthetic_1}\n"
        "Era: {era_1} | Summary: {summary_1}\n\n"
        "VIBE 2:\n"
        "Mood: {mood_2} | Energy: {energy_2}/10 | Aesthetic: {aesthetic_2}\n"
        "Era: {era_2} | Summary: {summary_2}\n\n"
        "1. Declare a WINNER (Vibe 1 or Vibe 2) — pick the one with the stronger, "
        "more iconic energy.\n"
        "2. Roast BOTH vibes lovingly (2 sentences each).\n"
        "3. Describe the 'fusion vibe' that combines both — give it a name and a "
        "one-line description.\n\n"
        "Be dramatic. Be funny. Make it entertaining. Keep it under 150 words."
    )),
])


def battle_vibes(profile_1: VibeProfile, profile_2: VibeProfile) -> str:
    """Compare two vibe profiles and declare a winner with roasts."""
    llm = get_llm()
    chain = BATTLE_PROMPT | llm | StrOutputParser()
    return chain.invoke({
        "mood_1": profile_1.mood,
        "energy_1": profile_1.energy,
        "aesthetic_1": profile_1.aesthetic,
        "era_1": profile_1.era,
        "summary_1": profile_1.vibe_summary,
        "mood_2": profile_2.mood,
        "energy_2": profile_2.energy,
        "aesthetic_2": profile_2.aesthetic,
        "era_2": profile_2.era,
        "summary_2": profile_2.vibe_summary,
    })


FUSION_PLAYLIST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a legendary music curator creating a FUSION playlist that blends "
        "two completely different vibes into one cohesive experience.\n\n"
        "Rules:\n"
        "- Recommend exactly 10 songs\n"
        "- Songs MUST be real, well-known songs by real artists\n"
        "- The playlist should feel like a journey between both vibes\n"
        "- Mix songs that lean toward each vibe, plus songs that bridge them\n"
        "- Each song needs: name, artist, genre, and a one-line 'why'\n"
        "- For youtube_url: use https://www.youtube.com/results?search_query={{encoded}}\n"
        "{genre_lock_instruction}"
        "\n\nReturn ONLY valid JSON:\n"
        '{{"vibe_story": "", "songs": [{{"name": "...", "artist": "...", '
        '"genre": "...", "why": "...", "youtube_url": "..."}}]}}'
    )),
    ("human", (
        "VIBE 1: {mood_1}, {aesthetic_1}, {era_1}, energy {energy_1}/10\n"
        "VIBE 2: {mood_2}, {aesthetic_2}, {era_2}, energy {energy_2}/10\n\n"
        "Create the fusion playlist:"
    )),
])


def generate_fusion_playlist(
    profile_1: VibeProfile,
    profile_2: VibeProfile,
    genre_lock: str | None = None,
) -> list:
    """Generate a fusion playlist that merges two vibes."""
    llm = get_llm()

    genre_lock_instruction = ""
    if genre_lock and genre_lock != "No Lock (Any Genre)":
        genre_lock_instruction = f"\n- ALL songs MUST be from the {genre_lock} genre.\n"

    chain = FUSION_PLAYLIST_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({
        "mood_1": profile_1.mood,
        "energy_1": profile_1.energy,
        "aesthetic_1": profile_1.aesthetic,
        "era_1": profile_1.era,
        "mood_2": profile_2.mood,
        "energy_2": profile_2.energy,
        "aesthetic_2": profile_2.aesthetic,
        "era_2": profile_2.era,
        "genre_lock_instruction": genre_lock_instruction,
    })

    parser = JsonOutputParser(pydantic_object=PlaylistResponse)
    result = parser.parse(raw)
    songs = result.get("songs", [])

    for song in songs:
        query = f"{song['name']} {song['artist']}"
        song["youtube_url"] = (
            f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
        )

    return songs
