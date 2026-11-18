"""Core logic for the Music Recommender sim."""

import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

# ---- Algorithm Recipe weights ----
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_MAX_POINTS = 1.5

INT_FIELDS = ["id", "tempo_bpm"]
FLOAT_FIELDS = ["energy", "valence", "danceability", "acousticness"]


@dataclass
class Song:
    """A single song and its audio features."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A user's taste preferences used for scoring songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool = False


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into a list of dicts, converting numeric fields to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue  # skip any blank rows
            for field in INT_FIELDS:
                row[field] = int(float(row[field]))
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            row["genre"] = row["genre"].strip()
            row["mood"] = row["mood"].strip()
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, list of reasons)."""
    score = 0.0
    reasons = []

    favorite_genre = str(user_prefs.get("favorite_genre", "")).lower()
    favorite_mood = str(user_prefs.get("favorite_mood", "")).lower()
    target_energy = user_prefs.get("target_energy")

    if song["genre"].lower() == favorite_genre:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    if song["mood"].lower() == favorite_mood:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    if target_energy is not None:
        energy_points = ENERGY_MAX_POINTS * (1 - abs(song["energy"] - target_energy))
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_points:.2f})"
        )

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song and return the top k as (song, score, reasons), highest score first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


class Recommender:
    """Object-oriented wrapper that recommends Song objects for a UserProfile."""

    def __init__(self, songs: List[Song]):
        """Store the catalog of Song objects."""
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile into the user_prefs dictionary used by score_song."""
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, highest score first."""
        prefs = self._prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song received its score."""
        score, reasons = score_song(self._prefs(user), asdict(song))
        detail = "; ".join(reasons) if reasons else "no matching features"
        return f"Score {score:.2f}: {detail}"