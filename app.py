import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import io

from models import VibeProfile
from chains import (
    analyze_image,
    generate_vibe_story,
    generate_playlist,
    battle_vibes,
    generate_fusion_playlist,
)
from styles import MAIN_CSS

load_dotenv()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Vibe Check Playlist",
    page_icon="📸",
    layout="wide",
)

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Controls")

    genre_options = [
        "No Lock (Any Genre)",
        "K-pop",
        "Lo-fi",
        "Reggaeton",
        "Classical",
        "Hip-hop",
        "Indie",
        "Latin",
        "Afrobeats",
        "R&B",
        "Pop",
        "Rock",
        "Jazz",
        "Electronic",
        "Country",
        "Metal",
    ]
    genre_lock = st.selectbox("🔒 Genre Lock", genre_options)

    st.markdown("---")
    battle_mode = st.toggle("⚔️ Battle Mode", value=False)
    if battle_mode:
        st.caption("Upload TWO photos and watch their vibes clash!")

    st.markdown("---")
    st.markdown(
        "Made with 💜 and vibes\n\n"
        "Powered by Groq + Llama + LangChain"
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="main-header">'
    "<h1>📸 Vibe Check Playlist</h1>"
    "<p>Upload a photo. We'll read your vibe. You'll get the soundtrack.</p>"
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def render_energy_meter(energy: int) -> str:
    """Build an emoji energy scale from ice to fire."""
    emojis = ["🧊", "❄️", "🌊", "🍃", "☁️", "⚡", "✨", "💥", "🔥", "☄️"]
    bar = ""
    for i in range(10):
        if i < energy:
            bar += emojis[i]
        else:
            bar += "⬜"
    return bar


def render_vibe_card(profile: VibeProfile):
    """Render the vibe profile as a styled card."""
    colors_html = " ".join(
        f'<span class="color-swatch" style="background:{c};" title="{c}"></span>'
        for c in profile.color_palette
    )
    energy_bar = render_energy_meter(profile.energy)

    st.markdown(
        f"""<div class="vibe-card">
        <h3>🎯 Your Vibe Profile</h3>
        <p><strong>Mood:</strong> {profile.mood}</p>
        <p><strong>Aesthetic:</strong> <span class="vibe-tag">{profile.aesthetic}</span></p>
        <p><strong>Era:</strong> <span class="vibe-tag">{profile.era}</span></p>
        <p><strong>Color Palette:</strong> {colors_html}</p>
        <p><strong>Vibe Summary:</strong> {profile.vibe_summary}</p>
        <div class="energy-meter">Energy: {energy_bar} ({profile.energy}/10)</div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_song_cards(songs: list):
    """Render song recommendations as a grid of cards."""
    rows = [songs[i : i + 3] for i in range(0, len(songs), 3)]
    for row in rows:
        cols = st.columns(3)
        for idx, song in enumerate(row):
            with cols[idx]:
                st.markdown(
                    f"""<div class="song-card">
                    <div class="song-name">🎵 {song['name']}</div>
                    <div class="song-artist">{song['artist']}</div>
                    <div class="song-genre">{song['genre']}</div>
                    <div class="song-why">"{song['why']}"</div>
                    <a href="{song['youtube_url']}" target="_blank">▶ Listen on YouTube</a>
                    </div>""",
                    unsafe_allow_html=True,
                )


def process_image(uploaded_file) -> tuple[bytes, Image.Image]:
    """Read uploaded file and return bytes + PIL image."""
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    return image_bytes, image


# ---------------------------------------------------------------------------
# Battle Mode
# ---------------------------------------------------------------------------
if battle_mode:
    st.markdown('<p class="section-title">⚔️ Upload Two Photos for Battle Mode</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        file_1 = st.file_uploader("📸 Photo 1", type=["jpg", "jpeg", "png", "webp"], key="battle_1")
    with col_b:
        file_2 = st.file_uploader("📸 Photo 2", type=["jpg", "jpeg", "png", "webp"], key="battle_2")

    if file_1 and file_2:
        bytes_1, img_1 = process_image(file_1)
        bytes_2, img_2 = process_image(file_2)

        col_a2, col_b2 = st.columns(2)
        with col_a2:
            st.image(img_1, caption="Photo 1", use_container_width=True)
        with col_b2:
            st.image(img_2, caption="Photo 2", use_container_width=True)

        if st.button("⚔️ BATTLE!", use_container_width=True, type="primary"):
            with st.spinner("🔮 Analyzing both vibes..."):
                profile_1 = analyze_image(bytes_1)
                profile_2 = analyze_image(bytes_2)

            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.markdown("### Vibe 1")
                render_vibe_card(profile_1)
            with col_v2:
                st.markdown("### Vibe 2")
                render_vibe_card(profile_2)

            with st.spinner("⚔️ The vibes are clashing..."):
                battle_result = battle_vibes(profile_1, profile_2)

            st.markdown(
                f'<div class="battle-winner"><h3>⚔️ Battle Results</h3><p>{battle_result}</p></div>',
                unsafe_allow_html=True,
            )

            with st.spinner("🎵 Creating the fusion playlist..."):
                songs = generate_fusion_playlist(profile_1, profile_2, genre_lock)

            st.markdown('<p class="section-title">🎶 Fusion Playlist</p>', unsafe_allow_html=True)
            render_song_cards(songs)

# ---------------------------------------------------------------------------
# Normal Mode (single photo)
# ---------------------------------------------------------------------------
else:
    uploaded_file = st.file_uploader(
        "📸 Drop your photo here",
        type=["jpg", "jpeg", "png", "webp"],
        help="Selfie, scenery, outfit, room — anything with a vibe",
    )

    if uploaded_file:
        image_bytes, image = process_image(uploaded_file)
        st.image(image, caption="Your vibe, loading...", use_container_width=True)

        # --- Analyze ---
        with st.spinner("🔮 Reading your aura..."):
            profile = analyze_image(image_bytes)

        render_vibe_card(profile)

        # --- Vibe Story ---
        with st.spinner("📝 Writing your origin story..."):
            story = generate_vibe_story(profile)

        st.markdown('<p class="section-title">📖 Your Vibe Story</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="vibe-story">{story}</div>', unsafe_allow_html=True)

        # --- Playlist ---
        with st.spinner("🎵 Curating your soundtrack..."):
            songs = generate_playlist(profile, genre_lock)

        st.markdown('<p class="section-title">🎶 Your Playlist</p>', unsafe_allow_html=True)
        render_song_cards(songs)

        # --- Opposite Day ---
        st.markdown("---")
        if st.button("🔄 Opposite Day — Flip the Vibe!", use_container_width=True):
            with st.spinner("🌀 Flipping your vibe to the shadow realm..."):
                opposite_songs = generate_playlist(profile, genre_lock, opposite=True)

            st.markdown(
                '<p class="section-title">🔄 Opposite Day Playlist</p>',
                unsafe_allow_html=True,
            )
            render_song_cards(opposite_songs)
    else:
        st.markdown(
            "<div style='text-align:center; padding:4rem 0; color:#888;'>"
            "<p style='font-size:3rem;'>📸</p>"
            "<p style='font-size:1.2rem;'>Upload a photo to get started</p>"
            "<p>Selfie, scenery, your messy desk — we don't judge</p>"
            "</div>",
            unsafe_allow_html=True,
        )
