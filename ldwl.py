import inflect
import nltk
from pattern.en import conjugate
from tqdm import tqdm
from itertools import product, combinations
from collections import OrderedDict

p = inflect.engine()

english = set(w.lower() for w in nltk.corpus.wordnet.words()) | set(w.lower() for w in nltk.corpus.words.words())


tenses = ['past', 'infinitive', 'present', 'future']
persons = range(1, 3)
moods = ['indicative', 'imperative', 'conditional', 'subjunctive']
aspects = ['imperfective', 'perfective', 'progressive']

conj_types = list(product(*[tenses, persons, moods, aspects]))

#for word in tqdm(list(english)):
#    for ct in conj_types:
#        conj = conjugate(word, tense=ct[0], person=ct[1], mood=ct[2], aspect=ct[3])
#        if conj is not None:
#            english.add(conj)
#            english.add(p.plural(conj))

full_english = english

#cur_len = 2
#len_limit = 5
#english = set()
#while cur_len < len_limit:
#    for word in tqdm(full_english):
#        if len(word) != cur_len:
#            continue
#        include = True
#        sword = OrderedDict.fromkeys(list(word))
#        for word2 in full_english:
#            if len(word2) <= cur_len:
#                continue
#            sword2 = OrderedDict.fromkeys(list(word2))
#            if sword.issubset(sword2):
#                include = False
#                break
#        if include:
#            included.add(word)

def drop_letter(word, pos):
    return (word[:pos] + word[(pos + 1):])

def ldwl(word, drop_list, dictionary):
    drop_possibilities = product(*drop_list[len(drop_list) - len(word) + 2:])

    for hl in range(2, len(word) - 1):
        heuristic = combinations(list(range(len(word))), hl)
        check = False
        for h in heuristic:
            if ''.join([word[x] for x in h]) in dictionary:
                check = True
                break
        if not check:
            return None

    for dp in drop_possibilities:
        ladder = True
        new = word
        for pos in dp:
            new = drop_letter(new, pos)
            if new not in dictionary:
                ladder = False
                break
        if ladder:
            return make_ladder(word, dp)
        else:
            continue

def make_ladder(word, drops):
    lad = [word]
    new = word
    for d in drops:
        new = drop_letter(new, d)
        lad.append(new)

    return lad

max_len = 3
len_limit = 11
drop_list = list(reversed([range(i) for i in range(3, len_limit + 1)]))
best = None

while max_len <= len_limit:
    limited_english = set([x for x in full_english if len(x) == max_len])
    reduced_english = set([x for x in full_english if len(x) < max_len])
    for word in tqdm(limited_english):
        ladder = ldwl(word, drop_list, reduced_english)
        if ladder is not None:
            best = ladder
            tqdm.write(', '.join(best))
            break
    max_len += 1
