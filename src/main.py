"""Command line runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs

# Multiple user taste profiles for stress testing
PROFILES = {
    "High-Energy Pop":  {"favorite_genre": "pop",   "favorite_mood": "happy",       "target_energy": 0.9},
    "Chill Lofi":       {"favorite_genre": "lofi",  "favorite_mood": "chill",       "target_energy": 0.3},
    "Deep Intense Rock":{"favorite_genre": "rock",  "favorite_mood": "intense",     "target_energy": 0.9},
    # Adversarial / edge case: wants high energy AND a sad mood (a contradiction)
    "Contradiction":    {"favorite_genre": "pop",   "favorite_mood": "melancholic", "target_energy": 0.9},
}

def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        print("=" * 60)
        print(f"PROFILE: {name}  "
              f"(genre={prefs['favorite_genre']}, mood={prefs['favorite_mood']}, "
              f"energy={prefs['target_energy']})")
        print("=" * 60)
        results = recommend_songs(prefs, songs, k=5)
        for rank, item in enumerate(results, start=1):
            song = item["song"]
            print(f"{rank}. {song['title']} — {song['artist']}  [score: {item['score']}]")
            for reason in item["reasons"]:
                print(f"     - {reason}")
        print()

if __name__ == "__main__":
    main()
    