"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    print(f"\nTop recommendations for {user_prefs['favorite_genre']}/"
          f"{user_prefs['favorite_mood']} listener:\n")

    results = recommend_songs(user_prefs, songs, k=5)
    for rank, item in enumerate(results, start=1):
        song = item["song"]
        print(f"{rank}. {song['title']} — {song['artist']}  [score: {item['score']}]")
        for reason in item["reasons"]:
            print(f"     - {reason}")
        print()
        
if __name__ == "__main__":
    main()
