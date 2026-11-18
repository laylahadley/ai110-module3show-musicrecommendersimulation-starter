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

Real platforms like Spotify and YouTube Music combine two approaches. Collaborative filtering recommends songs based on what similar users liked, using behavior signals like likes, skips, replays, and playlist additions. Content-based filtering recommends songs whose attributes (genre, mood, energy, tempo) resemble what a user already enjoys. At scale, these systems blend both and learn from millions of interactions.

My simulation is a content-based recommender. It compares each song's attributes to a user's "taste profile" and gives the song a score. A genre match is worth the most points, a mood match is worth fewer, and energy is scored by how *close* the song is to the user's target energy, not by how high or low it is. After every song is scored, a ranking rule sorts them from highest to lowest and returns the top recommendations. My version prioritizes genre and mood first, then fine-tunes with energy so the "vibe" feels right.

### Dataset
`data/songs.csv` contains 20 songs. The original 10 were expanded with 10 AI-generated songs covering new genres (hip hop, country, classical, r&b, metal, reggae, edm, folk, latin, blues) and new moods.

**Song features used:** title, artist, genre, mood, energy (0.0–1.0)
Also available for future upgrades: tempo_bpm, valence, danceability, acousticness

### User Profile
```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
}
```
**UserProfile features used:** favorite_genre, favorite_mood, target_energy

### Algorithm Recipe (Scoring Rule)
For each song:
- **+2.0 points** if `song.genre == favorite_genre`
- **+1.0 point** if `song.mood == favorite_mood`
- **+0 to 1.5 points** for energy closeness: `1.5 × (1 − |song.energy − target_energy|)`

Maximum score: 4.5. Genre is weighted highest because it describes the overall sound, mood second because it describes the moment, and energy fine-tunes the vibe by rewarding songs *closest* to the target, not just higher or lower.

### Ranking Rule
Score every song, sort from highest to lowest score, and return the top K (default K = 5).

**Example (lofi / chill / 0.40 profile):**
| Song | Genre | Mood | Energy pts | Total |
|---|---|---|---|---|
| Midnight Coding | +2.0 | +1.0 | 1.47 | 4.47 |
| Library Rain | +2.0 | +1.0 | 1.43 | 4.43 |
| Focus Flow | +2.0 | 0 | 1.50 | 3.50 |
| Spacewalk Thoughts | 0 | +1.0 | 1.32 | 2.32 |
| Storm Runner | 0 | 0 | 0.74 | 0.74 |

### Data Flow
INPUT: user_prefs + songs.csv
↓
PROCESS: loop over every song → apply Scoring Rule → (song, score)
↓
OUTPUT: Ranking Rule sorts by score → Top K recommendations


### Expected Biases
- **Genre over-prioritization:** with genre worth +2.0, a song in the right genre but the wrong mood can outrank a song that perfectly matches the user's mood and energy in a different genre.
- **Exact string matching:** "indie pop" gets no credit for "pop," and "relaxed" or "focused" get no credit for "chill," even though they feel similar.
- **Uneven catalog:** lofi has 3 songs while most genres have only 1, so lofi fans get more good matches than metal or blues fans.
- **Filter bubble:** the system only recommends more of what the user already likes and never suggests something new.
- **AI-generated data:** the 10 added songs reflect the AI's assumptions about genres (e.g., metal = angry and high energy, classical = peaceful), which may reinforce stereotypes.

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

```text
Loaded songs: 20

============================================================
Top 5 recommendations for: pop / happy / energy 0.80
============================================================

1. Sunrise City by Neon Echo
   Score: 4.47 / 4.50
   - genre match: pop (+2.0)
   - mood match: happy (+1.0)
   - energy 0.82 vs target 0.80 (+1.47)

2. Gym Hero by Max Pulse
   Score: 3.30 / 4.50
   - genre match: pop (+2.0)
   - energy 0.93 vs target 0.80 (+1.30)

3. Rooftop Lights by Indigo Parade
   Score: 2.44 / 4.50
   - mood match: happy (+1.0)
   - energy 0.76 vs target 0.80 (+1.44)

4. Fuego Lento by Sol Mestizo
   Score: 1.50 / 4.50
   - energy 0.80 vs target 0.80 (+1.50)

5. Concrete Crown by Block Theory
   Score: 1.47 / 4.50
   - energy 0.78 vs target 0.80 (+1.47)

```



**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



