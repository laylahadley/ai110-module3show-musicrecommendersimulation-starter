"""Command-line entry point for the Music Recommender Simulation."""

from src.recommender import (
    load_songs,
    recommend_songs,
    GENRE_POINTS,
    MOOD_POINTS,
    ENERGY_MAX_POINTS,
)

MAX_SCORE = GENRE_POINTS + MOOD_POINTS + ENERGY_MAX_POINTS

PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
    },
    "Adversarial - Sad but High Energy": {
        "favorite_genre": "blues",
        "favorite_mood": "sad",
        "target_energy": 0.90,
    },
    "Edge Case - Genre Not in Catalog": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.70,
    },
}


def print_recommendations(name, user_prefs, recommendations) -> None:
    """Print one profile's ranked recommendations in a readable layout."""
    print()
    print("=" * 60)
    print(f"Profile: {name}")
    print(
        f"Prefs: genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']:.2f}"
    )
    print("=" * 60)
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / {MAX_SCORE:.2f}")
        for reason in reasons:
            print(f"   - {reason}")


def main() -> None:
    """Load the catalog and print the top 5 recommendations for every test profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)
    print()


if __name__ == "__main__":
    main()
    