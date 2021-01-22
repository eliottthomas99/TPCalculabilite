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
