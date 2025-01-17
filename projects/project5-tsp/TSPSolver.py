#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
from pq import BinaryHeap, GraphNode
import heapq
import itertools
from typing import List


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy( self,time_allowance=60.0 ) -> dict:
		start_time = time.time()
		flag = False
		idx = 0
		while not flag and idx < len(self._scenario.getCities()):
			city = self._scenario.getCities()[idx]
			bssf = 0
			path = [city]
			while time.time() - start_time < time_allowance:
				# city = self._scenario.getCities()[itr]
				# for city in self._scenario.getCities():
				# 	bssf = [0]
				# 	lyst = [city]
				if len(path) == len(self._scenario.getCities()):
					if path[-1].costTo(path[0]) != float('inf'):
						bssf += path[-1].costTo(path[0])
						flag = True
						break
					else:
						break


				cities: List[City] = sorted(self._scenario.getCities(), key=lambda x:city.costTo(x))
				itr = 0
				while itr < len(cities) and cities[itr] != float('inf'):
					if cities[itr] not in path:
						break
					
					itr += 1
				
				if itr >= len(cities):
					break
				
				if city.costTo(cities[itr]) != float('inf'):
					bssf += city.costTo(cities[itr])
					path.append(cities[itr])
					city = cities[itr]

				else:
					break
			idx += 1

		if not flag:
			bssf = float('inf')
			path = []
		# if self._greedy_helper(city, lyst, bssf, len(self._scenario.getCities()), start_time, time_allowance):
		end_time = time.time()
		results = {}
		results['cost'] = bssf
		results['time'] = end_time - start_time
		results['count'] = 0
		results['soln'] = TSPSolution(path)
		return results

	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def _get_bound(self, arr: list, avoid_row: int = None, avoid_col: int = None) -> tuple:
		cur_bound = 0

		#returns new reduced matrix and bound corresponding to it
		if avoid_row != None and avoid_col != None:
			if len(avoid_col) != len(avoid_row):
				raise Exception("AVOID ROWS AND COLUMNS DO NOT MATCH")
			for itr in range(len(avoid_row)):
				arr[avoid_col[itr]][avoid_row[itr]] = float('inf')
		
		new_list = []

		for row in range(len(arr)):
			tmp_lyst = []
			if avoid_row and row in avoid_row:
				for col in range(len(arr[0])):
					tmp_lyst.append(float('inf'))
				new_list.append(tmp_lyst)
				continue
			min_val = min(arr[row])
			cur_bound += min_val
			for col in range(len(arr[0])):
				tmp_lyst.append(arr[row][col] - min_val if arr[row][col] != float('inf') else float('inf'))
			new_list.append(tmp_lyst)
		
		for row in range(len(new_list)):
			if avoid_col and row in avoid_col:
				for col in range(len(new_list[0])):
					new_list[col][row] = float('inf')
				continue
			min_col_num = min([new_list[col][row] for col in range(len(new_list[0]))])
			cur_bound += min_col_num
			for col in range(len(new_list[0])):
				if new_list[col][row] != float('inf'):
					new_list[col][row] -= min_col_num


		for row in range(len(new_list)):
			if avoid_row and row not in avoid_row:
				min_val = min(new_list[row])
				if min_val == float('inf'):
					cur_bound = float('inf')
		
		for row in range(len(new_list)):
			if avoid_col and row not in avoid_col:
				min_col_num = min([new_list[col][row] for col in range(len(new_list[0]))])
				if min_col_num == float('inf'):
					cur_bound = float('inf')

		
		return (new_list, cur_bound)

	def _expand(self, cur_element: GraphNode, bssf: list, num_pruned: list, total_states: list):
		expansion = []
		row_num = cur_element.path[-1]
		for col in range(len(cur_element.matrix[row_num])):
			if cur_element.matrix[row_num][col] != float('inf'):
				new_matrix, bound = self._get_bound(cur_element.matrix, cur_element.avoid_rows + [row_num], cur_element.avoid_cols + [col])
				total_states[0] += 1
				if cur_element.bound + cur_element.matrix[row_num][col] + bound < bssf[0]:
					expansion.append(GraphNode(new_matrix, 
											(cur_element.bound + cur_element.matrix[row_num][col] + bound), 
											cur_element.path[:] + [col],
											cur_element.avoid_rows + [row_num],
											cur_element.avoid_cols + [col]
									))
				else:
					num_pruned[0] += 1
		
		return expansion


	def _test(self, visited: list, arr_length: int):
		if len(visited) == arr_length + 1 and visited[0] == visited[-1]:
			return True
		return False


	def branchAndBound( self, time_allowance=60.0 ):
		cities = self._scenario.getCities()

		results = {}
		
		matrix = [[city.costTo(other_city) for other_city in cities] for city in cities]

		greedy_val = self.greedy()
		bssf = [greedy_val['cost'], greedy_val['soln'].route]

		lyst = [0]
		new_list, new_bound = self._get_bound(matrix)

		# q = [GraphNode(new_list, new_bound, lyst)]
		q = BinaryHeap()
		q.insert(GraphNode(new_list, new_bound, lyst, [], []))

		count_of_states = 1
		max_stored_states = 1
		bssf_updates = 0
		num_pruned = [0]
		total_states = [1]

		start_time = time.time()
		while time.time()-start_time < time_allowance:
			if q.get_length() > max_stored_states:
				max_stored_states = q.get_length()
			cur_element = q.delete_min()
			if cur_element == None:
				break
			if cur_element.bound < bssf[0]:
				arr_of_matrices = self._expand(cur_element, bssf, num_pruned, total_states)
				for itm in arr_of_matrices:
					if self._test(itm.path, len(matrix)) and itm.bound < bssf[0]:
						bssf = [itm.bound, itm.path]
						bssf_updates += 1
					elif itm.bound < bssf[0]:
						q.insert(itm)
						count_of_states += 1
					else:
						num_pruned[0] += 1
		
		num_pruned[0] += q.get_length()

		if type(bssf[1][0]) == int:
			bssf[1] = [cities[city_idx] for city_idx in bssf[1]]
			bssf[1].pop()

		end_time = time.time()
		results['cost'] = bssf[0]
		results['time'] = end_time - start_time
		results['count'] = count_of_states
		results['soln'] = TSPSolution(bssf[1])
		results['total'] = total_states[0]
		results['pruned'] = num_pruned[0]
		results['max'] = max_stored_states

		print("BSSF UPDATES: ", bssf_updates)

		return results


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
