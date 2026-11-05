import csv

def load_songs(path="data/songs.csv"):
    """Load songs from a CSV into a list of dicts, converting numeric fields to floats."""
    numeric_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numeric_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"



def score_song(user_prefs, song):
    """
        Scores a single song against user preferences.
        Required by recommend_songs() and src/main.py
        """
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += 2.0
        reasons.append(f"Genre match: {song['genre']} (+2.0)")

    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += 1.0
        reasons.append(f"Mood match: {song['mood']} (+1.0)")

    energy_points = round(1.0 - abs(song["energy"] - user_prefs["target_energy"]), 2)
    score += energy_points
    reasons.append(f"Energy similarity (+{energy_points})")

    return round(score, 2), reasons


def recommend_songs(user_prefs, songs, k=5):
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append({"song": song, "score": score, "reasons": reasons})
    ranked = sorted(scored, key=lambda item: item["score"], reverse=True)
    return ranked[:k]
