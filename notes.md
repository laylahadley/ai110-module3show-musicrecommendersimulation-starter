## How Streaming Platforms Predict What You'll Love

### 1. Collaborative Filtering (using other users' behavior)
How it works: The system finds users whose listening history looks like yours, then recommends songs they liked that you haven't heard yet. It doesn't need to know anything about the song itself — only who listened to what.
Example: You and another user both play the same 20 indie songs on repeat. That user also loves a band you've never heard. The system recommends that band to you, assuming your tastes overlap.
Weaknesses: The "cold start" problem (new songs/users have no history), and popular songs get recommended more because they have more data.

### 2. Content-Based Filtering (using song attributes)
How it works: The system describes every song with features (genre, mood, energy, tempo) and recommends songs whose features resemble the songs you already like. It only looks at you and the songs — not other users.
Example: You keep playing high-energy, upbeat pop songs around 120 BPM. The system recommends other songs with high energy, happy mood, and similar tempo — even a brand-new song nobody has played yet.
Weaknesses: It can trap you in a "filter bubble" — it only recommends more of what you already like and rarely surprises you.

### 3. Main Data Types
User behavior signals:
- Likes / saves (strong positive signal)
- Skips, especially in the first 30 seconds (strong negative signal)
- Playlist adds (shows how the user groups songs)
- Replays (strong positive signal)
- Listening time / completion rate
- Follows, shares, search history

Song attributes:
- Genre
- Mood
- Energy (how intense or active a song feels, 0–1)
- Tempo (BPM — speed of the beat)
- Valence (how happy vs. sad a song sounds, 0–1)
- Danceability, acousticness

### Summary
Collaborative filtering recommends songs based on what similar *people* enjoyed, while content-based filtering recommends songs that are similar to what *you* already enjoyed. Collaborative filtering is great at surprising discoveries but struggles with new songs that have no listening history. Real platforms like Spotify combine both approaches, and my simulation will focus on the content-based side.


## Feature Analysis of songs.csv (10 songs)

### Most effective features for a simple content-based recommender

1. genre (categorical) — The strongest "taste" signal. People often identify with a genre (lofi listener, rock fan). Easy to match exactly.
   Data: pop (2), lofi (3), rock, ambient, jazz, synthwave, indie pop.

2. mood (categorical) — Captures the situation the listener is in (working out vs. studying). Often matters as much as genre.
   Data: chill (3), happy (2), intense (2), relaxed, moody, focused.

3. energy (0.0–1.0) — Captures how intense or calm a song feels. Ranges from 0.28 (Spacewalk Thoughts) to 0.93 (Gym Hero), so it separates songs well. Best scored by CLOSENESS to the user's target, not "higher is better."

4. valence (0.0–1.0) — Captures happy vs. sad/dark. Ranges 0.48–0.84. Useful for telling apart two high-energy songs: Gym Hero (intense but upbeat, 0.77) vs. Storm Runner (intense and darker, 0.48).

5. acousticness (0.0–1.0) — Captures organic/acoustic vs. electronic sound. Useful if a user says they like acoustic music. Ranges 0.05–0.92.

### Less useful or potentially misleading features

- tempo_bpm — Mostly repeats what energy already says (fast songs here are also high-energy). It's also on a different scale (60–152) than the 0–1 features, so it would overpower them unless normalized. Leaving it out keeps the model simple.
- danceability — Overlaps heavily with energy in this dataset, so it adds little new information.
- id, title, artist — Labels only, not "vibe" features. (Artist could be used later for a "variety" rule so one artist doesn't dominate the results; Neon Echo and LoRoom each appear twice.)

### Data limitations noticed (useful for the bias section later)
- Very small dataset (10 songs), so recommendations will repeat a lot.
- lofi is overrepresented (3 of 10 songs), and lofi users will always get more matches than jazz or ambient users.
- Exact-match problems: "indie pop" won't match "pop," and "chill," "relaxed," and "focused" are similar vibes but count as different moods.
- High energy and low acousticness come together in every song, so there's no "intense acoustic" song, and users who want that combination can't be served.

### Recommended features for my simulator
genre, mood, energy (closeness score), with valence and acousticness as optional extras.

# Personal Take
I would define a vibe as the energy a room is filled with a certain song or genre is played. Vibes exist on a continuum, they can be high or low. 

# Energy Closeness Scoring Weights
For a content-based music recommender, the key is to use distance from the user's preferred value, rather than rewarding larger or smaller feature values. 

Closeness: energy_score = 1 - abs(song_energy - target_energy). A perfect match gives 1.0, and the further away the song is, the lower the score.
Weights (our recipe): genre match = +2.0, mood match = +1.0, energy closeness = up to +1.5.
Ranking: score every song, sort from highest to lowest, return the top K.

# Scoring Rule Design
A Scoring Rule evaluates each song in isolation ("How well does this song match the user?"), while a Ranking Rule evaluates the entire list together ("What is the best order to present these songs?").

# Example
Because a scoring rule is blind to every other track in the catalog, sorting purely by raw score often produces a technically accurate but frustrating playlist.
Suppose my 'Scoring Rule' evaluates four candidate songs for a user:
Song, Artist, Raw Score, Last Played
Track A, Artist X, 92, 2 days ago
Track B, Artist X, 90, 5 days ago
Track C, Artist Y, 88, Yesterday
Track D, Artist Z, 88, Never

If you only sort by raw score, the user gets Track A --> Track B --> Track C --> Track D (two Artist X songs back-to-back, and an arbitrary tie-break between C and D). 

Now apply a Ranking Rule with two policies—(1) no consecutive tracks by the same artist and (2) break ties by favoring less recently played songs:

- Track A (92, Artist X) — highest score, takes #1.

- Track D (88, Artist Z) — Track B is held back to avoid back-to-back Artist X; between the tied 88s, Track D wins the tie-breaker because it has never been played.

- Track B (90, Artist X) — now eligible again without repeating Artist X consecutively.

- Track C (88, Artist Y) — takes #4.

The Scoring Rule did the heavy lifting of finding the best candidates; the Ranking Rule turned those candidates into a better listening experience.

## Phase 2 – Dataset Expansion Prompt
"Here is my songs.csv with headers id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness. Generate 10 additional songs in valid CSV format using the same headers, continuing ids from 11. Use genres and moods NOT already in the file (current genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop; current moods: happy, chill, intense, relaxed, moody, focused). Keep energy, valence, danceability, and acousticness between 0.0 and 1.0 and make the values realistic for each genre. Do not use commas inside titles or artist names."
(Copilot Chat errored, so I sent this prompt to Claude.)

## Phase 2 – User Profile
```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
}
```

### Critique prompt
"Here is my user profile: favorite_genre = lofi, favorite_mood = chill, target_energy = 0.40. Will these preferences let my recommender tell the difference between 'intense rock' and 'chill lofi'? Or is the profile too narrow?"

### AI critique (Claude)
- Yes, it can tell intense rock from chill lofi. Storm Runner (rock, intense, energy 0.91) misses on genre, misses on mood, and is 0.51 away on energy, so it scores very low. Midnight Coding (lofi, chill, 0.42) matches on all three.
- Energy is the key difference. Without target_energy, any non-lofi, non-chill song would score 0, and the system couldn't rank them at all.
- Too narrow in some ways:
  - Only ONE favorite genre. Real people like several, and a lofi fan who also likes jazz gets no credit for jazz.
  - Exact matching: "relaxed" and "focused" feel close to "chill" but earn 0 mood points.
  - No valence, so it can't tell an upbeat intense song (Gym Hero) from a dark intense song (Storm Runner).
- Possible upgrades: a list of favorite genres, a target_valence, or a likes_acoustic flag.

### My take
I agree with Claude's critique. Chill lofi and intense rock are essentially opposite genres and moods, so the profile scope is wide enough to distinguish the two. 

## Phase 2 – Scoring Logic Design (new chat session)

### Prompt
"Using my songs.csv, suggest point-weighting strategies for a content-based recommender that scores genre match, mood match, and energy closeness. How much should a mood match count compared to a genre match? I want a balance where neither feature completely dominates."

### AI answer (Claude)
- Genre should weigh the most, because it describes the overall sound (a metal fan rarely wants classical). Mood is the next most important, since it describes the moment (studying vs. working out).
- With +2.0 for genre and +1.0 for mood, a genre match is worth twice a mood match, but genre does not dominate everything once energy is added.
- Energy closeness formula: energy_points = 1.5 × (1 − |song_energy − target_energy|).
  This gives up to 1.5 points, rewards closeness rather than "higher is better," and stays between 0 and 1.5 because energy runs 0–1.
- Balance check: a song matching only on genre with poor energy (2 + 1.5×0.4 = 2.6) narrowly beats a song matching mood with perfect energy (1 + 1.5 = 2.5). That's close, so energy and mood together can compete with genre alone.
- Alternative strategies: equal weights (1/1/1, so mood matters as much as genre), or energy-heavy (energy ×3) for "vibe-first" listeners.

### Final recipe
- +2.0 for a genre match
- +1.0 for a mood match
- +0 to 1.5 for energy closeness: 1.5 × (1 − |song.energy − target_energy|)
- Max possible score: 4.5

## Phase 3 – Implementation Prompts (Copilot Chat kept timing out, so I used Claude)

### Prompt 1 – load_songs
"Implement load_songs(csv_path) in src/recommender.py. Use Python's csv module to read data/songs.csv and return a list of dictionaries, one per song. Convert id and tempo_bpm to int, and energy, valence, danceability, and acousticness to float so I can do math with them later."

### Prompt 2 – score_song
"Implement score_song(user_prefs, song) using my Algorithm Recipe: +2.0 points for a genre match, +1.0 point for a mood match, and energy closeness points = 1.5 × (1 − |song energy − target_energy|). Return BOTH the numeric score and a list of reasons, such as 'genre match: pop (+2.0)', so users understand why a song was recommended."

### Prompt 3 – recommend_songs
"What's the most Pythonic way to loop through all songs, score each one with score_song, and return the top k sorted from highest to lowest score? Also explain the difference between .sort() and sorted()."

AI answer on .sort() vs sorted():
- `list.sort()` sorts the list IN PLACE (it changes the original list) and returns None. It only works on lists.
- `sorted(iterable)` returns a NEW sorted list and leaves the original unchanged. It works on any iterable.
- I used `sorted()` so the original song catalog stays in its CSV order and isn't modified by the recommender. That's safer if the same list is reused (for example, to score a second user profile).
- `key=lambda item: item[1]` tells it to sort by the score, and `reverse=True` puts the highest scores first. Slicing with `[:k]` keeps the top k.

### Prompt 4 – CLI output
"Format the output in src/main.py as a clean, readable terminal layout that shows each song's rank, title, artist, final score, and the reasons from score_song."

### Prompt 5 – docstrings
"Add 1-line docstrings to every function in recommender.py."

### Prompt 6 – commit message
"Generate a commit message summarizing my implementation. Mention that it's a working CLI-first simulation."

## Phase 4 – System Evaluation (new chat session; used Claude since Copilot Chat errored)

### Prompt 1 – Edge cases
"Here are my recommender.py and songs.csv. Suggest 'adversarial' or 'edge case' user profiles designed to trick my scoring logic or produce unexpected results."

AI answer:
- Conflicting preferences: genre blues, mood sad, target_energy 0.90. The only blues/sad song is slow (0.38 energy), so it tests whether genre+mood labels override the user's energy target.
- Genre not in the catalog: genre "k-pop". No song can earn genre points, so it tests what the system does when its strongest signal is missing.
- Extreme energy (0.0 or 1.0): tests whether the energy formula still separates songs at the edges.
- Capitalization ("POP" vs "pop"): my code lowercases both sides, so this is handled.

### Prompt 2 – Why did a song rank first?
"Using the weights in recommender.py, explain why Sunrise City ranked first for the pop/happy/0.80 profile, and why Gym Hero ranked second even though the user wanted happy songs."

AI answer:
- Sunrise City is the only song that matches all three preferences: genre pop (+2.0), mood happy (+1.0), and energy 0.82, only 0.02 from 0.80 (+1.47). Total 4.47 of a possible 4.50.
- Gym Hero is pop (+2.0) and very energetic (0.93, giving +1.30), but its mood is "intense," so it gets 0 mood points. About 3.30 total.
- Rooftop Lights IS happy, but its genre is "indie pop," which doesn't exactly equal "pop," so it loses the 2.0 genre points and lands 3rd at 2.44. The genre weight is strong enough that a wrong-mood pop song beats a right-mood "indie pop" song.

### Prompt 3 – Experiment
"Apply a weight shift in recommender.py: double the importance of energy (ENERGY_MAX_POINTS 1.5 -> 3.0) and halve genre (GENRE_POINTS 2.0 -> 1.0). Verify the math remains valid."

AI answer:
- Energy points = 3.0 × (1 − |gap|). Since energy and target are both 0–1, the gap is 0–1, so energy points stay between 0 and 3.0. Never negative.
- New max score = 1.0 + 1.0 + 3.0 = 5.0. main.py computes the max from the constants, so the printed "/ max" updates automatically.
- Only the constants change. No logic changes are needed, so the math stays valid.

### Prompt 4 – Bias / filter bubbles
"Using recommender.py and songs.csv, identify potential filter bubbles or biases in my scoring logic. Does my system ignore certain types of users because of how I calculate the energy gap?"

AI answer:
- Genre dominance: +2.0 for genre beats mood (+1.0), so users mostly see their one favorite genre. That's a filter bubble.
- Uneven catalog: lofi has 3 songs, pop 2, and the other 15 genres have 1 each. A lofi fan gets 3 strong matches. A classical or blues fan gets 1, then unrelated filler chosen only by energy.
- Energy gap bias: the gap formula is linear. A mid-energy user (target 0.5) can never be more than 0.5 away from any song, so every song earns at least 0.75 energy points, and energy barely separates songs for them. An extreme user (target 0.95) sees gaps up to 0.75, so energy matters much more. Users in the middle get weaker personalization from energy.
- Exact string matching: "indie pop" ≠ "pop", and "relaxed"/"focused" ≠ "chill". Similar vibes get zero credit.
- Rare moods: 16 moods across 20 songs means most moods have just one song, so mood matches are rare and genre ends up deciding most rankings.