# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
**VibeFinder 1.0** - a content-based music recommender that scores songs against a user's taste profile.

---

## 2. Intended Use  

VibeFinder is a simplified, content-based music recommender built for classroom
tinkering, not real users. Given a user "taste profile" (a favorite genre, a favorite
mood, and target energy level), it scores every song in a small catalog and returns a
ranked 'Top 5' with plain-language reasons for each pick. It assumes the user can be
represented by a single fixed set of preferences and that a song's genre, mood, and energy
are enough to judge fit. It is meant to demonstrate how a recommender turns data into
ranked predictions, not to power an actual production app.

Classroom Exploration:
    - It should not be used to make real recommendations for actual listeners, to judge the quality of any artist or song, or in any setting where a biased or missed recommendation would matter. It is a learning demo, not a production system.
---

## 3. How the Model Works  

Each song carries some select attributes: its genre, its mood, and a numeric energy level from
0.0 to 1.0. The user's profile lists a favorite genre, a favorite mood, and an ideal
energy level. To score a song, the model will check for matches and then reward closeness:

- If the song's genre matches the user's favorite, it earns 2 points.
- If the song's mood matches, it earns 1 point.
- For energy, the closer the song's energy is to the user's target, the more points it
  earns (a song right on target earns close to a full point; a song far away earns almost
  nothing).

Every song's points are added into a total score, and the model sorts all songs from
highest to lowest and shows the top few. The only change from the starter logic was
filling in the scoring and ranking rules so the system actually produces explained,
ranked recommendations.

---

## 4. Data  

The catalog contains 18 songs. Genres are: pop, indie pop, lofi, rock, metal, jazz,
classical, reggae, folk, blues, electronic, synthwave, r&b, ambient, and world. Moods
range from happy / chill to intense, melancholic, aggressive, serene, and romantic.
I expanded the original 10-song starter file with 8 additional songs to cover genres and
moods that were missing. Still, the dataset is small and uneven, as some styles appear
only once. So, whole regions of real musical taste (regional scenes, sub-genres, mixed-
genre tracks) are not represented.

---

## 5. Strengths  

The system works well for users with a clear and single-genre taste. A "high-energy pop"
profile reliably curates upbeat pop tracks, and a "chill lofi" profile correctly adjusts
to calm, low-energy songs, matching my own intuition about what those listeners want.
Because each recommendation lists its reasons (genre match, mood match, energy
similarity), the output is transparent: you can always see exactly why a song was chosen,
which is a genuine strength over a black-box system.

---

## 6. Limitations and Bias 

Because a genre match (2 points) is worth double a mood match (1 point), the system leans
heavily on genre and can bury songs that are a perfect mood fit in a different genre. This
produces a filter-bubble effect: a pop listener keeps seeing pop and rarely discovers
adjacent styles.

Genre and mood are matched by exact wording, so near-identical labels will count as unrelated.
"Rooftop Lights" is tagged "indie pop" and is clearly happy and poppy, yet it loses all
genre points for a "pop" listener purely because the label isn't an exact match.

Energy points are added to every song, even when nothing else matches, so a song with no
real relevance can still collect up to a full point from energy alone, which is enough to outrank
a genuine taste fit. This is why the contradictory "high energy + sad" profile quietly
ignores the sad request and just returns loud songs. Combined with the small, uneven
catalog, the system favors well-represented genres and users with simple, mainstream taste. 

---

## 7. Evaluation  

I stress-tested the recommender with four profiles: high-energy pop, chill lofi, deep
intense rock, and a deliberately contradictory profile (pop genre, melancholic mood, high
energy).

What surprised me most: for the High-Energy Pop listener, "Gym Hero" ranked second even
though its mood is "intense," not "happy." It beat the genuinely happy "Rooftop Lights"
because a genre match plus near-perfect energy outweighed Rooftop's mood match, showing
my weights let genre and energy override the mood the user actually asked for.

I also ran a weight-shift experiment, halving the genre weight and doubling the energy
term. The rankings changed clearly, as high-energy tracks from any genre rose to the top.
But, the results felt less accurate, not more, because they blended unrelated genres. That
confirmed the original genre weight is what keeps the lists coherent.

Comparing profiles: High-Energy Pop vs Chill Lofi pulled toward opposite ends of the
energy scale, as expected. Deep Intense Rock vs High-Energy Pop both wanted high energy,
but the genre weight cleanly split rock to one list and pop to the other. The
Contradiction profile returned nearly the same songs as High-Energy Pop. In plain terms,
when someone asks for "sad but high-energy," the system can't honor the sad part and just
gives them loud pop anyway.

---

## 8. Future Work  

In the future, I would add more of the features to the score --> valence, danceability, and acousticness are already in the dataset and would capture "vibe" better than energy alone. I would replace exact string matching with a similarity check so "indie pop" and "pop" are treated as
related rather than unrelated. To fight filter bubbles, I would maybe add a diversity rule that
limits how many songs from the same genre can appear in the Top 5. I'd also let energy
points only count when there's at least a partial genre or mood match, so irrelevant songs
can't ride energy coincidence to the top. Finally, a larger, more balanced catalog and
profiles that can change over time would make the recommendations more realistic.

---

## 9. Personal Reflection  

My biggest learning moment was realizing a recommender is really just scoring and
ranking, which is to turn preferences and song attributes into numbers, then sort them. Once
that clicked, the whole system stopped feeling like magic.

AI tools sped up the boilerplate, i.e. loading the CSV, formatting terminal output, and were
useful for explaining concepts like .sort() vs sorted(). But I had to double-check them
routinely: the AI left a duplicate load_songs function in my file that silently returned
an empty list, and I had to trace why "Loaded songs: 0" was happening myself. That taught
me AI is good for drafting but can't be trusted blindly, I needed to stay in control of the logic.

What surprised me most is how a handful of simple if-statements and one subtraction can
produce rankings that genuinely "feel" like real recommendations. There's no machine
learning here, yet the output still looks personalized.

If I extended this, I would add a diversity rule so the Top 5 isn't dominated by one genre,
use fuzzy matching so "indie pop" counts toward "pop," and bring in the valence and
danceability columns I already have to capture "vibe" more fully.
