#from typing import *

def greedy_set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset
 
    return cover

def is_cover(universe, subsets, poss_solution):
	# Subsets and poss_solition must have the same size
	if len(poss_solution) != len(subsets):
		print('Pb with the size of the solution')
		return False
	# If so, continue and compute what the solution covers
	covered = set()
	for i in range(0,len(poss_solution)):
		if poss_solution[i] == 1:
			covered |= subsets[i]
	# If the solution covers the universe then OK
	if universe == covered:
		#print('It is a cover !')
		return True
	else:
		#print('Not a cover')
		return False

def naive_set_cover(universe, subsets):
	"""Find a collection of families of subsets that covers the universal set"""
	solution_collection = []
	best_solution_cost = len(subsets) # worst cost ever
	
	# Explore all the possible solutions by enumeration of integers 
	# between 1 and pow(2,n)-1 in binary representation
	for i in range(1, 2**len(subsets)):
		# built solution (list of ints)
		solution = []
		bit_string =  bin(i)[2:].zfill(len(subsets))
		for c  in bit_string:
			solution.append((int(c)))
		#print('essai:',solution)

		# If a cover is found
		if is_cover(universe, subsets, solution) == True:
			# compute cost: nr of subsets in the solution
			solution_cost = sum(solution)
			
			# if this solution has better or equal cost
			if solution_cost <= best_solution_cost:
				solution_subsets = []
				for idx in range(0,len(solution)):
					if solution[idx] == 1:
						solution_subsets.append(subsets[idx])
				if solution_cost < best_solution_cost:
					best_solution_cost = solution_cost
					# reset of collection of best solutions
					solution_collection = []
				# add a solution to the best solution collection
				solution_collection.append(solution_subsets)
	return(solution_collection)
			
			
def load_scp(filename):
	universe = set()
	subsets = []
	subset_cost_vect = [] ## on laisse tomber pour le moment
	with open(filename,"r") as myfile:
		# read m (elnt nr) and n (subset nr)
		first_line = myfile.readline()
		tab = first_line.split(" ")
		tab.remove('')
		tab.remove('\n')
		elnt_nr = int(tab[0])
		subset_nr = int(tab[1])
		
		universe = set(range(1,elnt_nr+1)) # max idx is not included
		for i in range(0,subset_nr):
			subsets.append(set())
			
		print("nombre de sous-ensembles : ",subset_nr)
		print("nombre d'éléments : ",elnt_nr)
		
		## Reading the costs
		end_of_costs = False
		cost_nr = 0
		while not(end_of_costs):
			current_line = myfile.readline()
			tab = current_line.split(" ")
			tab.remove('')
			tab.remove('\n')
			for elt in tab:
				subset_cost_vect.append(int(elt))
			cost_nr += len(tab)
			if (cost_nr >= subset_nr):
				end_of_costs = True
				
		## Reading the contents : which subsets cover each element		
		end_of_elements = False
		element_cpt = 0
		while not(end_of_elements):
			# Read subsets_nr
			current_line_tab = myfile.readline().split(" ")
			current_line_tab.remove('')
			current_line_tab.remove('\n')
			set_nr = current_line_tab[0]
			element_cpt += 1
			# print(set_nr)
			
			# Read Subsets that cover element 'element_cpt'
			set_tab = myfile.readline().split(" ")
			set_tab.remove('')
			set_tab.remove('\n')
			for setidx in set_tab:
				subsets[int(setidx)-1].add(element_cpt)
			
			if (element_cpt >= elnt_nr):
				end_of_elements = True
			
		if (len(subsets) != len(subset_cost_vect)):
			print("Problem with number of costs")
		myfile.close()
		return universe, subsets, subset_cost_vect
	

def main():
    universe = set(range(1, 11))
    subsets = [{1, 2, 3, 8, 9, 10},
        {1, 2, 3, 4, 5},
        {4, 5, 7},
        {5, 6, 7},
        {6, 7, 8, 9, 10}]
	## Unit Tests
    #print("All:",is_cover(universe, subsets, [1,1,1,1,1]))
    #print("Best:",is_cover(universe, subsets, [0,1,0,0,1]))
    #print("Not a cover:",is_cover(universe, subsets, [0,0,1,1,0]))
    
    #universe, subsets, subset_cost_vect = load_scp('./data/scpcyc06.txt')
    
    print('Subsets: ', subsets)
    print('Universe: ', universe)
    #print('Subset cost vect: ', subset_cost_vect)
    print('**************** SOLVING ****************')

    #best_covers = naive_set_cover(universe, subsets)
    #print('Collection of best covers: ', best_covers)
    
    cover = naive_set_cover(universe, subsets)
    print('naive ', cover)
 
if __name__ == '__main__':
    main()
