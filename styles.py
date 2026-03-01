MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
}

.main-header {
    text-align: center;
    padding: 1rem 0 0.5rem 0;
}

.main-header h1 {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.main-header p {
    font-size: 1.1rem;
    color: #888;
    margin-top: 0.25rem;
}

.vibe-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 1.5rem;
    color: white;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    margin: 1rem 0;
}

.vibe-card h3 {
    margin-top: 0;
    font-size: 1.4rem;
    color: #a78bfa;
}

.vibe-card .vibe-tag {
    display: inline-block;
    background: rgba(167, 139, 250, 0.2);
    border: 1px solid rgba(167, 139, 250, 0.4);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    margin: 0.2rem;
    font-size: 0.85rem;
    color: #c4b5fd;
}

.vibe-story {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    border-left: 4px solid #a78bfa;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem;
    color: #e2e8f0;
    font-style: italic;
    font-size: 1.05rem;
    line-height: 1.7;
    margin: 1rem 0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.song-card {
    background: linear-gradient(145deg, #1e1e2f 0%, #2a2a40 100%);
    border-radius: 14px;
    padding: 1.2rem;
    color: white;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    margin-bottom: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
    height: 100%;
}

.song-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(167, 139, 250, 0.15);
}

.song-card .song-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.2rem;
}

.song-card .song-artist {
    font-size: 0.95rem;
    color: #a78bfa;
    margin-bottom: 0.5rem;
}

.song-card .song-genre {
    display: inline-block;
    background: rgba(167, 139, 250, 0.15);
    border: 1px solid rgba(167, 139, 250, 0.3);
    border-radius: 20px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    color: #c4b5fd;
    margin-bottom: 0.5rem;
}

.song-card .song-why {
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.4;
    margin-bottom: 0.7rem;
}

.song-card a {
    display: inline-block;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    transition: opacity 0.2s;
}

.song-card a:hover {
    opacity: 0.85;
}

.energy-meter {
    font-size: 1.8rem;
    text-align: center;
    padding: 0.5rem;
    letter-spacing: 4px;
}

.color-swatch {
    display: inline-block;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin: 0 4px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    vertical-align: middle;
}

.battle-winner {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 16px;
    padding: 1.5rem;
    color: white;
    text-align: center;
    box-shadow: 0 8px 32px rgba(245, 87, 108, 0.3);
    margin: 1rem 0;
}

.battle-winner h3 {
    margin-top: 0;
    font-size: 1.5rem;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #a78bfa;
    margin: 1.5rem 0 0.5rem 0;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

div[data-testid="stSidebar"] .stMarkdown {
    color: #e2e8f0;
}
</style>
"""
