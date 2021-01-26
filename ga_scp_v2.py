"""
Simple genetic algorithm for set covering.
"""

from load_scp import load_scp
import greedy_scp as gs
from utils import is_cover,get_random_bit,get_random_individual,get_random_population,weighted_random_order
import random

# Greedy set cover
def greedy_set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set
       Returns a vector describing selected subsets"""
    solvect = [0 for _ in range(len(subsets))] ######
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        subset_idx = subsets.index(subset) ######
        solvect[subset_idx] = 1 ######
        cover.append(subset)
        covered |= subset
        
    return solvect

# utils
def get_individual_fitness(individual):
    """ Compute the fitness of the given individual.
        Growing fitness with the quality of the solution.
        Simply counts numbers of zero : UNICOST SCP """
    fitness = 0
    for c in individual:
        fitness += 1-c
    return fitness

def stats_population_grade(population):
    """ Return the total fitness and the average fitness of all individual in the population. """
    total = 0
    for individual in population:
        total += get_individual_fitness(individual)
    return total,total / len(population)

def grade_population(population):
    """ Grade the population. Return a list of tuple (individual, fitness) sorted from most graded to less graded. """
    graded_individual = []
    for individual in population:
        graded_individual.append((individual, get_individual_fitness(individual)))
    return sorted(graded_individual, key=lambda x: x[1], reverse=True)

def compute_proba(graded_population):

    population=[]
    proba=[]
    total=0

    for (individual,individual_fitness) in graded_population:
        population.append(individual)
        proba.append(1/individual_fitness)
        total = total+(1/individual_fitness)

    proba=[tmp_proba * (1/total) for tmp_proba in proba]

    return population,proba


def proportion_selection(population,proportion):
    print("[GEN] Selection par proportion.")
    assert proportion <= 1

    graded_population = grade_population(population)
    (population,proba)=compute_proba(graded_population)
    graded=weighted_random_order(population,proba)

    return graded[:int(len(graded)*proportion)],graded[int(len(graded)*proportion):]

def fitness_selection(population,proportion):
    print("[GEN] Selection par fitness.")
    # Get individual sorted by grade (top first), the average grade and the solution (if any)
    graded_population = grade_population(population)
    graded_population=[ind for (ind,fit) in graded_population]
    return graded_population[:int(len(graded_population)*proportion)],graded_population[int(len(graded_population)*proportion):]

def diversity(unselected_population,ratio_to_be_retained):
    print("[GEN] Un peu de diversité !")
    parents=[]

    for p in unselected_population:
        if random.random() < ratio_to_be_retained:
            parents.append(p)
    return parents

def mutation(parents,ratio_to_mutate):
    print("[GEN] Mutation en cours.")
    for individual in parents:
        if random.random() < ratio_to_mutate:
            place_to_modify = int(random.random() * len(individual))
            individual[place_to_modify] = get_random_bit(nb_One=1)

def crossover(parents,population_nextgen_size):
    #print("[GEN] Reproduction en cours.")

    desired_len = population_nextgen_size - len(parents)
    middle_length_individual=int(len(parents[0])/2)

    next_gen = []
    while len(next_gen) < desired_len:
        random.shuffle(parents)
        father = parents[0]
        mother = parents[1]

        child = father[:middle_length_individual] + mother[middle_length_individual:]
        next_gen.append(child)

    next_gen.extend(parents)
    return next_gen

def rejets(next_gen,universe, subsets):
    #print("[GEN] Suppression des rejets")

    _next_gen=[]
    z=0
    for p in next_gen:
        if not(is_cover(universe, subsets, p)):
            p = get_random_individual(universe,subsets)
            z=z+1
        _next_gen.append(p)

    print("[INFO] Nombre de rejets:"+str(z))

    return _next_gen

def evolve_population(universe, subsets, population,size_next_gen):
    """ Make the given population evolving to his next generation. """
    total_fitness, avg_fitness = stats_population_grade(population)
    parents,unselected = fitness_selection(population,0.45)
    best_sol=parents[0] # Par convention
    parents.extend(diversity(unselected,0.15))
    
    mutation(parents,0.05)
    
    next_gen = crossover(parents,size_next_gen)
    
    next_gen = rejets(next_gen,universe, subsets)

    return next_gen, avg_fitness, best_sol

## MAIN
def main():
    """
    universe = set(range(1, 11))
    subsets = [{1, 2, 3, 8, 9, 10},
        {1, 2, 3, 4, 5},
        {4, 5, 7},
        {5, 6, 7},
        {6, 7, 8, 9, 10}]

    random_sol = [get_random_bit() for i in range(0,len(subsets))]
    is_cover(universe,subsets,random_sol)

    is_cover(universe,subsets,[1,1,1,1,1])

    """

    print('**************** LOADING ****************')
    universe, subsets, subset_cost_vect = load_scp('./data/scpcyc06.txt')
    #universe, subsets, subset_cost_vect = load_scp('./data/scpd5.txt')
    
    log_avg = []

    print('**************** SOLVING ****************')

    print("GENERATION 0: Tirage aléatoire")
    population = get_random_population(universe,subsets,250)

    
    for i in range(0,2000):
        population,avg_fitness,best_sol =  evolve_population(universe,subsets,population,len(population))
        nb_subsets_inclus = len(population[0]) - avg_fitness
        log_avg.append(avg_fitness)
        print("Avg Fitness = "+str(avg_fitness)+", soit "+str(nb_subsets_inclus)+" sous-ensembles inclus par solution en moyenne.")
        print("Best solution fitness:"+str(get_individual_fitness(best_sol)))
        print("*****************************************")
        print("GENERATION "+str(i))
    
    
    # Pour suivre le fitness au cours des itérations    
    import pygal # pas installé à l'ENSSAT
    line_chart = pygal.Line(show_dots=False, show_legend=False)
    line_chart.title = 'Fitness evolution'
    line_chart.x_title = 'Generations'
    line_chart.y_title = 'Fitness'
    line_chart.add('Fitness', log_avg)
    line_chart.render_to_file('fitness_evolution.svg')
    
    
    greedy_cover = greedy_set_cover(universe, subsets)
    if is_cover(universe, subsets, greedy_cover):
        print("Fitness of greedy solution: "+str(get_individual_fitness(greedy_cover)))
    

if __name__ == '__main__':
    main()
