""" @author Louri Noël , basé sur le travail de Arnaud Delhay-Lorrain """

import sys
from timeit import Timer
from typing import *

Universe = Set[int]  # éléments numérotés de 1 à n
Subset = Set[int]
Cost = int


# https://stackoverflow.com/questions/20974147/timeit-eats-return-value
def time_that_once(func, *args, **kwargs) -> Tuple[float, Any]:
    output = [None]

    def wrapper():
        output[0] = func(*args, **kwargs)

    timer = Timer(wrapper)
    delta = timer.timeit(1)
    return delta, output[0]


class ScpParsingException(Exception):
    pass


# format du fichier :
#
# nombre_d_elements nombre_de_subsets
# poids (1 par subset)
# (repeat par élément de l'univers)
# nombre de subsets le couvrant
# numéros des subsets le couvrant (txt : commencent à 1, py : (indexes) commencent à 0)
def load_scp(filename: str) -> Tuple[Universe, List[Subset], List[Cost]]:
    with open(filename, "r") as myfile:  # ferme le fichier automatiquement en sortant
        # read m (elnt nr) and n (subset nr)
        tab = myfile.readline().strip().split(" ")
        elnt_nr = int(tab[0])  # nombre d'éléments de l'univers
        subset_nr = int(tab[1])  # nombre de subsets

        if len(tab) != 2:
            raise ScpParsingException('La première ligne ne contient pas exactement 2 éléments.')

        universe: Universe = set(range(1, elnt_nr + 1))  # max idx is not included
        subsets: List[Subset] = [set() for _ in range(subset_nr)]
        subset_cost_vect: List[Cost] = []

        # Reading the costs
        cost_nr = 0  # nombre de coûts lus
        while cost_nr < subset_nr:
            tab = myfile.readline().strip().split(" ")
            subset_cost_vect.extend([int(elt) for elt in tab])  # à décommenter si pas utilisé (donc laisser cost_nr)
            cost_nr += len(tab)

        if cost_nr != subset_nr:
            raise ScpParsingException('Il y a plus de coûts que de subsets.') ## TODO

        print("nombre d'éléments :", elnt_nr)
        print('nombre de sous-ensembles :', subset_nr)

        # Reading the contents : which subsets cover each element

        for element_cpt in range(1, elnt_nr + 1):  # les éléments de l'univers commencent à 1
            # Read subsets_nr
            tab = myfile.readline().strip().split(" ")
            set_nr = int(tab[0])  # nombre de subsets couvrant cet élément
            # print(set_nr)

            if len(tab) > 1:
                print("La ligne indiquant le nombre de subsets couvrant contient plus de 1 élément, ceux-cis seront ignorés.", sys.stderr)

            # Read Subsets that cover element 'element_cpt'
            set_tab = []  # numéros des subsets commencant à 1
            while len(set_tab) < set_nr:
                set_tab.extend([int(setidx) for setidx in myfile.readline().strip().split(" ")])

            if len(set_tab) > set_nr:
                print('Il y a plus de subsets couvrants que prevus.', sys.stderr)

            for setidx in set_tab:
                subsets[setidx - 1].add(element_cpt)

    return universe, subsets, subset_cost_vect


def main(filename: str, timeit=False) -> None:
    if timeit:
        delta, (universe, subsets, subset_cost_vect) = time_that_once(load_scp, filename)
        print('parsing time:', delta, 'seconds')
    else:
        universe, subsets, subset_cost_vect = load_scp(filename)

    print('Universe:', universe)
    print('Coûts (si pris en compte) :', subset_cost_vect)
    print('Subsets: (subset : éléments couverts)')
    for i, subset in enumerate(subsets):
        print(i+1, ':', subset)


if __name__ == '__main__':
    # main('data/scpcyc06.txt', True)
    main('data/scpd5.txt', True)
