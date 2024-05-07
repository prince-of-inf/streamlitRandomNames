import re  # regullar expression
import string
from collections import Counter
from string import digits

import numpy as np
import pandas as pd
from nltk import ngrams
from unidecode import unidecode

def load_names(nations=["spanish"]):
    names = []
    for nation in nations:
        name = pd.read_csv(f"names/{nation}.csv")
        # name = name['0'].apply(lambda x: x.translate(str.maketrans('', '', digits))) # remove digits
        name = name["0"].apply(
            lambda x: x.split(" ")[0]
        )  # remove second names and digits
        name = name.apply(lambda x: unidecode(x))  # remove accents, e.g. spanish ñ
        name = name.apply(
            lambda x: re.sub("[^a-zA-Z]+", "", x)
        )  # leave only letters, omit for e.g.'
        names += list(name.values)
    return names


def prepare_ngrams(names, ngram_order):
    ngrams_arr = []
    for name in names:
        ngrams_arr += list(ngrams(name + " ", ngram_order))  # name with space on end
    df = pd.DataFrame(ngrams_arr)
    df = (
        df.iloc[:, :-1].sum(axis=1).to_frame().join(df.iloc[:, -1])
    )  # 2 columns - all letters except last, last letter
    df = df.set_axis([0, 1], axis=1)
    df = df.groupby(0)[1].apply(np.array)  # ngram + possible letters
    starts = [s[: ngram_order - 1] for s in names]  # list of possible starting letters
    return df, starts


def generate_names_markov_chain(df, starts, names, ngram_order, n=10, name_exist_flag=True, return_list=True):
    l = []
    i = 0
    while i < n:
        word = np.random.choice(starts, 1)[0]  # choose starting letters
        state = word  # current Markov state
        # loop until word ends with space
        while word[0][-1] != " ":
            try:
                word += np.random.choice(
                    df.loc[state], 1
                )  # add random letter from current state
                state = word[0][-ngram_order + 1 :]  # go to the next state
            except KeyError:  # problem with reaching next state
                break
        if return_list:
            # if only non-existing names - check if exists
            if name_exist_flag == False:
                if (re.sub('[^a-zA-Z]+', '', word[0]) in names) == True:
                    continue
            l.append(word[0])
            i += 1
    if return_list:
        return l
    else:
        print(return_list)