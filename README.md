# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Music platforms like Spotify predict what each user will enjoy by combining collaborative filtering (finding patterns across many users’ listening behavior, such as likes, skips, and shared playlists) with content-based filtering (comparing the attributes of songs: genre, energy, tempo, and mood,  to the songs a user already enjoys). My version focuses on a more simpliefied content-based approach --> it represents each user as a “taste profile” of preferred attributes, scores every song by how closely its attributes match the user's profile, then ranks the results to surface the best matches. It prioritizes transparency and explainability over pure scale (each recommendation can be traced back to a clear, weighted reason).

Features Used:


**Song object:**
- genre
- mood
- energy
- tempo_bpm


**UserProfile object:**
- preferred_genre
- preferred_mood
- preferred_energy
- preferred_tempo_bpm


### Algorithm Recipe

My music recommender scores every song in the catalog against a fixed user taste profile and returns the top-ranked matches

User taste profile:
- favorite_genre: "rock"
- favorite_mood: "energetic"
- target_energy: 0.8

Scoring rules (applied to each song):
- +2.0 points if the song's genre matches favorite_genre
- +1.0 point if the song's mood matches favorite_mood
- Energy similarity: 1.0 maximum

Ranking rule:
- Sort all songs by total score (highest first) and return the Top K recommendations.

Data flow:
Input (user preferences) --> Process (loop over every song in songs.csv and apply the scoring rules) --> Output (rank by score, return Top K).

### Potential Biases

Because a genre match is worth twice a mood match, my  system may over-prioritize genre and overlook good songs that strongly match the user's mood but belong to a different genre. Also, it can create a "filter bubble," i.e., repeatedly favoring the user's known favorite genre and rarely surfacing new styles. A fixed single-profile design further ignores how taste changes with context (time of day, activity, etc.).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output
'''
Loaded songs: 18

Top recommendations for pop/happy listener:

1. Sunrise City — Neon Echo  [score: 3.98]
     - Genre match: pop (+2.0)
     - Mood match: happy (+1.0)
     - Energy similarity (+0.98)

2. Gym Hero — Max Pulse  [score: 2.87]
     - Genre match: pop (+2.0)
     - Energy similarity (+0.87)

3. Rooftop Lights — Indigo Parade  [score: 1.96]
     - Mood match: happy (+1.0)
     - Energy similarity (+0.96)

4. Neon Mirage — Crystal Circuit  [score: 0.99]
     - Energy similarity (+0.99)

5. Night Drive Loop — Neon Echo  [score: 0.95]
     - Energy similarity (+0.95)
'''


## Sample Recommendation Output (stress test)
'''
Loaded songs: 18

============================================================
PROFILE: High-Energy Pop  (genre=pop, mood=happy, energy=0.9)
============================================================
1. Sunrise City — Neon Echo  [score: 3.92]
     - Genre match: pop (+2.0)
     - Mood match: happy (+1.0)
     - Energy similarity (+0.92)
2. Gym Hero — Max Pulse  [score: 2.97]
     - Genre match: pop (+2.0)
     - Energy similarity (+0.97)
3. Rooftop Lights — Indigo Parade  [score: 1.86]
     - Mood match: happy (+1.0)
     - Energy similarity (+0.86)
4. Storm Runner — Voltline  [score: 0.99]
     - Energy similarity (+0.99)
5. Iron Horizon — Black Meridian  [score: 0.94]
     - Energy similarity (+0.94)

============================================================
PROFILE: Chill Lofi  (genre=lofi, mood=chill, energy=0.3)
============================================================
1. Library Rain — Paper Lanterns  [score: 3.95]
     - Genre match: lofi (+2.0)
     - Mood match: chill (+1.0)
     - Energy similarity (+0.95)
2. Midnight Coding — LoRoom  [score: 3.88]
     - Genre match: lofi (+2.0)
     - Mood match: chill (+1.0)
     - Energy similarity (+0.88)
3. Focus Flow — LoRoom  [score: 2.9]
     - Genre match: lofi (+2.0)
     - Energy similarity (+0.9)
4. Spacewalk Thoughts — Orbit Bloom  [score: 1.98]
     - Mood match: chill (+1.0)
     - Energy similarity (+0.98)
5. Autumn Letters — Willow Hart  [score: 0.99]
     - Energy similarity (+0.99)

============================================================
PROFILE: Deep Intense Rock  (genre=rock, mood=intense, energy=0.9)
============================================================
1. Storm Runner — Voltline  [score: 3.99]
     - Genre match: rock (+2.0)
     - Mood match: intense (+1.0)
     - Energy similarity (+0.99)
2. Gym Hero — Max Pulse  [score: 1.97]
     - Mood match: intense (+1.0)
     - Energy similarity (+0.97)
3. Iron Horizon — Black Meridian  [score: 0.94]
     - Energy similarity (+0.94)
4. Sunrise City — Neon Echo  [score: 0.92]
     - Energy similarity (+0.92)
5. Neon Mirage — Crystal Circuit  [score: 0.89]
     - Energy similarity (+0.89)

============================================================
PROFILE: Contradiction  (genre=pop, mood=melancholic, energy=0.9)
============================================================
1. Gym Hero — Max Pulse  [score: 2.97]
     - Genre match: pop (+2.0)
     - Energy similarity (+0.97)
2. Sunrise City — Neon Echo  [score: 2.92]
     - Genre match: pop (+2.0)
     - Energy similarity (+0.92)
3. Autumn Letters — Willow Hart  [score: 1.41]
     - Mood match: melancholic (+1.0)
     - Energy similarity (+0.41)
4. Storm Runner — Voltline  [score: 0.99]
     - Energy similarity (+0.99)
5. Iron Horizon — Black Meridian  [score: 0.94]
     - Energy similarity (+0.94)
'''
---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
