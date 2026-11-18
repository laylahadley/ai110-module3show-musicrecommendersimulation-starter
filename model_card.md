# Model Card: VibeMatch 1.0

## 1. Model Name
**VibeMatch 1.0**, a simple content-based music recommender.

## 2. Goal / Task
VibeMatch suggests songs a user is likely to enjoy. It compares each song's genre, mood, and energy to the user's "taste profile" and returns the top 5 best matches. It also explains *why* each song was picked.

## 3. Data Used
- **Size:** 20 songs in `data/songs.csv`. The starter file had 10, and I added 10 AI-generated songs to cover more genres and moods.
- **Features per song:** id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness.
- **Features the model actually uses:** genre, mood, and energy.
- **Variety:** 17 genres and 16 moods.
- **Limits:**
  - The dataset is tiny compared to a real app with millions of songs.
  - It's unbalanced: lofi has 3 songs, pop has 2, and every other genre has only 1.
  - Most moods appear only once, so mood matches are rare.
  - The 10 added songs were made up by AI, so their values reflect the AI's guesses about genres (e.g., metal = angry, classical = peaceful), not real audio measurements.
  - There are no real users, listening history, likes, or skips.

## 4. Algorithm Summary
VibeMatch works like a judge giving out points to every song:
- If the song is the user's favorite **genre**, it gets **2 points**.
- If the song is the user's favorite **mood**, it gets **1 point**.
- It gets **up to 1.5 points** for **energy**, based on how *close* the song's energy is to the energy the user wants. A perfect match gets the full 1.5, and the further away the song is, the fewer points it gets.

The best possible score is 4.5. After every song is scored, VibeMatch sorts them from highest to lowest and shows the top 5, along with the reasons for each score (for example, "genre match: pop (+2.0)").

## 5. Limitations and Biases
My system gives a genre match +2.0 points, which is more than a mood match and usually more than energy can make up, so a song in the user's favorite genre almost always ranks near the top even when its mood is wrong. For example, Gym Hero, an intense workout song, ranked #2 for a "happy pop" listener just because it is labeled pop and is high energy. This is made worse by an uneven catalog: lofi has 3 songs while 15 genres have only one, so a lofi fan gets three strong matches but a blues or classical fan gets one match followed by unrelated songs picked only by energy. Exact string matching also hides good matches, since "indie pop" earns no genre credit for a pop fan even though it sounds similar. In my adversarial test, a user who wanted sad but high-energy music got a slow 0.38-energy blues song first, which shows that category labels can override what the user said about energy and push users into a genre "filter bubble."

Other patterns I noticed:
- **Energy gap bias:** users who want medium energy (around 0.5) are never far from any song, so energy barely changes their rankings. Users who want extreme energy see much bigger differences.
- **No warnings:** if a user picks a genre that isn't in the catalog (like k-pop), the system doesn't say anything. It just quietly ranks by mood and energy.

## 6. Evaluation Process
I tested five profiles in `src/main.py`: three normal listeners (High-Energy Pop, Chill Lofi, Deep Intense Rock) and two tricky ones (a sad-but-high-energy blues fan, and a k-pop fan whose genre isn't in the catalog). I checked whether the top 5 matched my own music taste, compared every pair of profiles, and ran one experiment where I doubled the energy weight and halved the genre weight.


### Profiles Tested
I tested five user profiles: three "normal" listeners (High-Energy Pop, Chill Lofi, Deep Intense Rock) and two designed to trick the system (a sad-but-high-energy blues fan, and a k-pop fan whose genre isn't in the catalog).

#### High-Energy Pop
```text
============================================================
Profile: High-Energy Pop
Prefs: genre=pop, mood=happy, energy=0.80
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

#### Chill Lofi
```text
============================================================
Profile: Chill Lofi
Prefs: genre=lofi, mood=chill, energy=0.40
============================================================
1. Midnight Coding by LoRoom
   Score: 4.47 / 4.50
   - genre match: lofi (+2.0)
   - mood match: chill (+1.0)
   - energy 0.42 vs target 0.40 (+1.47)
2. Library Rain by Paper Lanterns
   Score: 4.42 / 4.50
   - genre match: lofi (+2.0)
   - mood match: chill (+1.0)
   - energy 0.35 vs target 0.40 (+1.42)
3. Focus Flow by LoRoom
   Score: 3.50 / 4.50
   - genre match: lofi (+2.0)
   - energy 0.40 vs target 0.40 (+1.50)
4. Spacewalk Thoughts by Orbit Bloom
   Score: 2.32 / 4.50
   - mood match: chill (+1.0)
   - energy 0.28 vs target 0.40 (+1.32)
5. Rainy Crossroads by Muddy Lantern
   Score: 1.47 / 4.50
   - energy 0.38 vs target 0.40 (+1.47)
```

#### Deep Intense Rock
```text
============================================================
Profile: Deep Intense Rock
Prefs: genre=rock, mood=intense, energy=0.90
============================================================
1. Storm Runner by Voltline
   Score: 4.48 / 4.50
   - genre match: rock (+2.0)
   - mood match: intense (+1.0)
   - energy 0.91 vs target 0.90 (+1.48)
2. Gym Hero by Max Pulse
   Score: 2.46 / 4.50
   - mood match: intense (+1.0)
   - energy 0.93 vs target 0.90 (+1.46)
3. Neon Pulse by Voltage Kids
   Score: 1.43 / 4.50
   - energy 0.95 vs target 0.90 (+1.43)
4. Iron Tempest by Grave Signal
   Score: 1.40 / 4.50
   - energy 0.97 vs target 0.90 (+1.40)
5. Sunrise City by Neon Echo
   Score: 1.38 / 4.50
   - energy 0.82 vs target 0.90 (+1.38)

```

#### Adversarial - Sad but High Energy
```text
============================================================
Profile: Adversarial - Sad but High Energy
Prefs: genre=blues, mood=sad, energy=0.90
============================================================
1. Rainy Crossroads by Muddy Lantern
   Score: 3.72 / 4.50
   - genre match: blues (+2.0)
   - mood match: sad (+1.0)
   - energy 0.38 vs target 0.90 (+0.72)
2. Storm Runner by Voltline
   Score: 1.48 / 4.50
   - energy 0.91 vs target 0.90 (+1.48)
3. Gym Hero by Max Pulse
   Score: 1.46 / 4.50
   - energy 0.93 vs target 0.90 (+1.46)
4. Neon Pulse by Voltage Kids
   Score: 1.43 / 4.50
   - energy 0.95 vs target 0.90 (+1.43)
5. Iron Tempest by Grave Signal
   Score: 1.40 / 4.50
   - energy 0.97 vs target 0.90 (+1.40)
```

#### Edge Case - Genre Not in Catalog
```text
============================================================
Profile: Edge Case - Genre Not in Catalog
Prefs: genre=k-pop, mood=happy, energy=0.70
============================================================
1. Rooftop Lights by Indigo Parade
   Score: 2.41 / 4.50
   - mood match: happy (+1.0)
   - energy 0.76 vs target 0.70 (+1.41)
2. Sunrise City by Neon Echo
   Score: 2.32 / 4.50
   - mood match: happy (+1.0)
   - energy 0.82 vs target 0.70 (+1.32)
3. Night Drive Loop by Neon Echo
   Score: 1.42 / 4.50
   - energy 0.75 vs target 0.70 (+1.42)
4. Concrete Crown by Block Theory
   Score: 1.38 / 4.50
   - energy 0.78 vs target 0.70 (+1.38)
5. Island Sunday by Coral Drift
   Score: 1.35 / 4.50
   - energy 0.60 vs target 0.70 (+1.35)
```

### Does it "feel" right?
For Chill Lofi, yes. Midnight Coding, Library Rain, and Focus Flow are exactly what I'd play while studying. For High-Energy Pop, Sunrise City at #1 feels right, but Gym Hero at #2 doesn't: it's a workout song, not a happy one.

### Why does "Gym Hero" show up for people who want Happy Pop? (plain language)
Think of the recommender as a judge handing out points. Being the right genre is worth the most points (2), being the right mood is worth fewer (1), and being close to the right energy level is worth up to 1.5. Gym Hero is labeled "pop" and is very energetic, so it collects the big genre prize plus most of the energy points, even though its mood is "intense," not "happy." Meanwhile, Rooftop Lights is happy, but it's labeled "indie pop," and the judge only gives genre points for an exact word match, so it misses the biggest prize. The result: a pump-up workout song beats a genuinely happy song.

### Comparing Profiles (pairs)
- **High-Energy Pop vs. Chill Lofi:** No songs overlap. The pop profile targets energy 0.80 and the lofi profile 0.40, so they pull from opposite halves of the catalog. That makes sense.
- **High-Energy Pop vs. Deep Intense Rock:** Both include Gym Hero and Sunrise City. High-energy songs cross over, so a rock fan gets Sunrise City (a happy pop song) at #5 just because its energy (0.82) is close to 0.90.
- **High-Energy Pop vs. Adversarial:** Both include Gym Hero, but the adversarial list is led by a slow blues song. The sad user's genre + mood labels beat their energy request.
- **High-Energy Pop vs. Edge Case (k-pop):** Sunrise City and Rooftop Lights swap places. Without any genre match, mood + energy decide, and Rooftop Lights (happy, 0.76) is closest to 0.70.
- **Chill Lofi vs. Deep Intense Rock:** Zero overlap. Genre, mood, and energy all point in opposite directions, so the system clearly tells "chill lofi" apart from "intense rock."
- **Chill Lofi vs. Adversarial:** Both include Rainy Crossroads for completely different reasons: for lofi it's the closest energy (0.38 vs 0.40), and for the adversarial user it's the genre + mood match.
- **Chill Lofi vs. Edge Case:** No overlap. The edge case targets mid-high energy (0.70), so calm lofi songs score low.
- **Deep Intense Rock vs. Adversarial:** 4 of 5 songs are the same (Storm Runner, Gym Hero, Neon Pulse, Iron Tempest). After the one blues/sad song, the only thing left to compare is energy, so the sad user gets treated like a rock fan.
- **Deep Intense Rock vs. Edge Case:** Both include Sunrise City. It's a common "filler" pick for any high-energy profile.
- **Adversarial vs. Edge Case:** No overlap. One wants sad and very high energy, the other happy and moderately high energy.

### What surprised me
- The sad/high-energy user got a slow song (0.38 energy) at #1, the opposite of the energy they asked for.
- The k-pop user got no warning that their genre doesn't exist. The system silently fell back to mood and energy, and every score stayed under 2.5 out of 4.5.
- Sunrise City showed up for a rock fan.

### Experiment: Weight Shift (energy ×2, genre ×0.5)
I changed GENRE_POINTS from 2.0 to 1.0 and ENERGY_MAX_POINTS from 1.5 to 3.0 (new max score = 5.0).

High-Energy Pop with the experimental weights:
```text
============================================================
Profile: High-Energy Pop
Prefs: genre=pop, mood=happy, energy=0.80
============================================================
1. Sunrise City by Neon Echo
   Score: 4.94 / 5.00
   - genre match: pop (+1.0)
   - mood match: happy (+1.0)
   - energy 0.82 vs target 0.80 (+2.94)
2. Rooftop Lights by Indigo Parade
   Score: 3.88 / 5.00
   - mood match: happy (+1.0)
   - energy 0.76 vs target 0.80 (+2.88)
3. Gym Hero by Max Pulse
   Score: 3.61 / 5.00
   - genre match: pop (+1.0)
   - energy 0.93 vs target 0.80 (+2.61)
4. Fuego Lento by Sol Mestizo
   Score: 3.00 / 5.00
   - energy 0.80 vs target 0.80 (+3.00)
5. Concrete Crown by Block Theory
   Score: 2.94 / 5.00
   - energy 0.78 vs target 0.80 (+2.94)
```

**Result:** For High-Energy Pop, Rooftop Lights moved up from #3 to #2 and Gym Hero dropped to #3. That's **more accurate**, since Rooftop Lights is actually a happy song. For Chill Lofi and Deep Intense Rock, the order barely changed. Only the scores changed, so there it was **just different**, not better. For the adversarial user, Rainy Crossroads stayed #1 but its lead shrank a lot, since energy now counts more. I reverted to the original weights for the final version, but this shows the genre weight is the main cause of the "Gym Hero problem."

## 7. Intended Use and Non-Intended Use
**Intended use:**
- A classroom simulation to show how content-based recommenders turn song data and user preferences into ranked suggestions.
- Exploring how weights and data choices create bias.

**Not intended for:**
- Real users or a real music app. The catalog is tiny and partly made up.
- Making decisions about artists, like which songs get promoted or paid.
- Judging what anyone "should" listen to. It only knows three preferences and can't learn or change over time.

## 8. Ideas for Improvement
1. **Fuzzy matching for genres and moods:** give partial credit for similar labels (e.g., "indie pop" gets half credit for "pop," and "relaxed" gets partial credit for "chill").
2. **Let users pick multiple favorite genres and moods**, and add more features like valence (happy vs. sad sound) and acousticness, so the profile isn't so narrow.
3. **Add a diversity rule:** limit the top 5 to one song per artist or genre, and maybe include one "wildcard" song to break the filter bubble. A bigger, more balanced dataset would help too.

## 9. Personal Reflection
**Biggest learning moment:** Honestly, my biggest learning moment was seeing 'Gym Hero' show up as the second pick for a "happy pop" user. I thought my weights made sense, but that one result showed me how just one number (2 points for genre) can totally change user suggestions. It made me realize that the people who build these systems are making choices all the time, even if the code looks "neutral."

**How AI tools helped (and when I double-checked):** AI helped me mostly with speed. It wrote the CSV loading code and suggested edge-case profiles I wouldn't have thought of, like a user whose genre doesn't exist. Copilot Chat kept giving me errors, so I switched to a different AI assistant for most of the prompts. I still had to double-check things: I calculated a few scores by hand to make sure the top results actually matched my recipe, I checked the AI-generated songs to make sure the CSV didn't have extra blank lines or commas that would break it, and I noticed the AI's made-up songs kind of followed stereotypes (every metal song is angry, every classical song is peaceful). 

**What surprised me:** I was surprised that something this simple, just adding up a few points, actually "feels" like a real recommendation. When I ran the 'Chill Lofi' profile, the top 3 were songs I might actuallly use to focus. It made me think that apps like Spotify might be doing something similar at the base level, just with much more data and features.

**What I'd try next:** If I kept working on this, I'd want to add some collaborative filtering, like fake "listening history" for a few users so the system could recommend songs that similar users liked. I'd also want to try fuzzy matching for genres, and maybe build a simple interface where you can move a slider for energy and watch the recommendations change in real time.