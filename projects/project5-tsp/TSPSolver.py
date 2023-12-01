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

	def greedy( self,time_allowance=60.0 ):
		pass



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

	def _expand(self, cur_element: GraphNode, bssf: int):
		expansion = []
		row_num = cur_element.path[-1]
		for col in range(len(cur_element.matrix[row_num])):
			if cur_element.matrix[row_num][col] != float('inf'):
				new_matrix, bound = self._get_bound(cur_element.matrix, cur_element.avoid_rows + [row_num], cur_element.avoid_cols + [col])
				if bound != float('nan') and (cur_element.bound + cur_element.matrix[row_num][col] + bound) < bssf:
					expansion.append(GraphNode(new_matrix, 
											(cur_element.bound + cur_element.matrix[row_num][col] + bound), 
											cur_element.path[:] + [col],
											cur_element.avoid_rows + [row_num],
											cur_element.avoid_cols + [col]
									))
		
		return expansion


	def _test(self, visited: list, arr_length: int):
		if len(visited) == arr_length + 1 and visited[0] == visited[-1]:
			return True
		return False

	def _process(self, arr: list):
		bssf = 40000

		lyst = [0]
		new_list, new_bound = self._get_bound(arr)

		# q = [GraphNode(new_list, new_bound, lyst)]
		q = BinaryHeap()
		q.insert(GraphNode(new_list, new_bound, lyst, [], []))

		while True:
			cur_element = q.delete_min()
			if cur_element == None:
				break
			if cur_element.bound < bssf:
				arr_of_matrices = self._expand(cur_element, bssf)
				for itm in arr_of_matrices:
					if self._test(itm.path, len(arr)):
						bssf = itm.bound
					elif itm.bound < bssf:
						q.insert(itm)

		return bssf

	def branchAndBound( self, time_allowance=60.0 ):
		cities = self._scenario.getCities()
		
		matrix = [[city.costTo(other_city) for other_city in cities] for city in cities]

		self._process(matrix)




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
