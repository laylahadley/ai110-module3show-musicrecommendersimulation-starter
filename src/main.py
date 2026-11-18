"""Command-line entry point for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Load the catalog, score it against a user profile, and print the top recommendations."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default "pop/happy" taste profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print(
        f"Top {len(recommendations)} recommendations for: "
        f"{user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
        f"energy {user_prefs['target_energy']:.2f}"
    )
    print("=" * 60)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 4.50")
        for reason in reasons:
            print(f"   - {reason}")
    print()


if __name__ == "__main__":
    main()
    