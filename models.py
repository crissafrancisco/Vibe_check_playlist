from pydantic import BaseModel


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
