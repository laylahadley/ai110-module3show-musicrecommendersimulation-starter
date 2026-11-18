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