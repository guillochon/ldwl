import inflect
import nltk
from pattern.en import conjugate
from tqdm import tqdm
from itertools import product

p = inflect.engine()

english = set(w.lower() for w in nltk.corpus.wordnet.words()) | set(
    w.lower() for w in nltk.corpus.words.words())


tenses = ['past', 'infinitive', 'present', 'future']
persons = range(1, 3)
moods = ['indicative', 'imperative', 'conditional', 'subjunctive']
aspects = ['imperfective', 'perfective', 'progressive']

conj_types = list(product(*[tenses, persons, moods, aspects]))

for word in tqdm(list(english)):
    for ct in conj_types:
        conj = conjugate(
            word, tense=ct[0], person=ct[1], mood=ct[2],
            aspect=ct[3])
        if conj is not None:
            english.add(conj)
            english.add(p.plural(conj))

full_english = english


def insert_letter(word, letter, pos):
    return word[:pos] + letter + word[pos:]


known_ladders = [[x] for x in full_english if len(x) == 2]

max_depth = 20

drop_list = list(reversed([range(i) for i in range(3, max_depth + 1)]))

a_ladder = []

lb = 0
for depth in tqdm(range(2, max_depth)):
    le = len(known_ladders)
    for li in tqdm(range(lb, le)):
        base = known_ladders[li][-1]
        for pos in range(len(base) + 1):
            for c in range(ord('a'), ord('z') + 1):
                let = chr(c)
                new = insert_letter(base, let, pos)
                if new in english and new not in [
                        x[-1] for x in known_ladders[le:]]:
                    known_ladders.append(known_ladders[li] + [new])
    lb = le

print(known_ladders[-1])
