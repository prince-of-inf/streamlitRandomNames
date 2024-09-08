import re  # regullar expression

import numpy as np
import pandas as pd
from nltk import ngrams
from unidecode import unidecode

def load_names(nations=["spanish"]):
    names = []
    for nation in nations:
        name = pd.read_csv(f"names/{nation}.csv")
        names += list(name[name.columns[-1]]) # concatenate to list of strings
    return names


def prepare_ngrams(names, ngram_order):
    ngrams_arr = []
    names = [str(name).ljust(ngram_order,"!") for name in names] # add ! to short names, let for one ngram
    for name in names:
        ngrams_arr += list(ngrams(name + " ", ngram_order))  # name with space on end
    df = pd.DataFrame(ngrams_arr)
    df = (df.iloc[:, :-1].sum(axis=1).to_frame().join(df.iloc[:, -1]))  # 2 columns - all letters except last, last letter
    df = df.set_axis([0, 1], axis=1)
    df = df.groupby(0)[1].apply(np.array)  # ngram + possible letters
    starts = [s[: ngram_order - 1] for s in names]  # list of possible starting letters
    return df, starts


def generate_names_markov_chain(df, starts, names, ngram_order, n=10, chaos_fact=0.2, name_exist_flag=True):
    l = []
    i = 0
    while i < n:
        # INIT
        word = np.random.choice(starts, 1)[0]  # choose starting letters
        state = word  # current Markov state
        # LOOP
        # loop until word ends with space or next state doesn't exist
        while word[-1] != " ":
            try:
                if np.random.random() > chaos_fact:
                    # add random letter from current state
                    word += str(np.random.choice(df.loc[state], 1)[0])
                else:
                    # add random letter from random state
                    word += str(np.random.choice(df.iloc[np.random.randint(len(df))], 1)[0])
                state = word[-ngram_order + 1:]  # go to the next state
            except KeyError:  # problem with reaching next state
                break
        # PRINT
        word = re.sub("[^a-zA-Z]+", "", word).lower() # remove !
        # if only non-existing names - check if exists
        if name_exist_flag == True:
            if (word in names) == True:
                continue
        # No one letter names
        if len(word) < 2:
            continue
        l.append(word.title())
        i += 1

    return l