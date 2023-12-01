from typing import Dict, List

class GraphNode:
    def __init__(self, matrix: list, bound: int, path: list, avoid_rows: list, avoid_cols: list) -> None:
        self.matrix = matrix
        self.bound = bound
        self.path = path
        self.avoid_rows = avoid_rows
        self.avoid_cols = avoid_cols
    
    def __gt__(self: 'GraphNode', other: 'GraphNode'):
        a = 1
        b = 15

        this_node_score = a * self.bound + b * len(self.path)
        other_node_score = a * other.bound + b * len(other.path)

        # Less than here because __gt__ menas that self is going to be lower priority
        # in the priority queue
        return this_node_score < other_node_score 

class Heap:
    def __init__(self) -> None:
        self._prev: Dict[GraphNode, GraphNode] = {} # Maps node to previous node
        self._node_to_priority: Dict[GraphNode, int] = {} # Mapping cs312Nodes to their respective priorities


    def get_parent(self, vert: GraphNode) -> GraphNode:
        pass

    def get_length(self, vert: GraphNode) -> float:
        pass
    
    def get_dist(self, node: GraphNode) -> int:
        pass
    
    def set_dist(self, node: GraphNode, dist: int) -> None:
        pass
    
    def set_prev(self, node: GraphNode, prev: GraphNode) -> None:
        pass

    def decrease_key(self, vert: GraphNode) -> None:
        pass

class BinaryHeap(Heap):

    def __init__(self) -> None:
        # self._pointer_array: Dict[GraphNode, int] = {} # Mapping cs312nodes to their respective indices in heap
        self._heap: List[GraphNode] = []
        super().__init__()


    # def make_queue(self, arr: List[GraphNode], start_node: GraphNode) -> None:
    #     self._heap.append(start_node)
    #     self._prev[start_node] = None
    #     self._pointer_array[start_node] = 0
    #     for itm in arr:
    #         if itm == start_node:
    #             self._node_to_priority[itm] = 0
    #         else:
    #             self._heap.append(itm)
    #             self._pointer_array[itm] = len(self._heap) - 1
    #             self._node_to_priority[itm] = float('inf')


    def insert(self, vert: GraphNode) -> None:
        """O(_perc_up)"""
        self._heap.append(vert)
        self._perc_up(len(self._heap) - 1)
    
    def _perc_up(self, cur_idx: int) -> None:
        """O(logn) because we move up a tree height of one at each iteration"""
        while (cur_idx - 1) // 2 >= 0:
            parent_idx = (cur_idx - 1) // 2
            if self._heap[parent_idx] > self._heap[cur_idx]:
                
                self._heap[cur_idx], self._heap[parent_idx] = \
                self._heap[parent_idx], self._heap[cur_idx]

                # must change array pos at each swap
                # self._pointer_array[self._heap[cur_idx]] = cur_idx
                # self._pointer_array[self._heap[parent_idx]] = parent_idx 

            cur_idx = parent_idx
        

    def delete_min(self) -> GraphNode:
        """O(_perc_down)"""
        if len(self._heap) and self._heap[0].bound != float('inf'):
            return_node = self._heap[0]
            new_node: GraphNode = self._heap.pop()
            if len(self._heap):
                self._heap[0] = new_node
                # self._pointer_array[new_node] = 0
                self._perc_down(0)
            return return_node
    
    def _perc_down(self, cur_idx: int) -> None:
        """O(logn) because at eah iteration we are moving down the tree 1 layer (a.k.a moving through array by multiples of two)"""
        while 2 * cur_idx + 1 < len(self._heap):
            small_side: int = self._get_min_child(cur_idx)

            if self._heap[cur_idx] > self._heap[small_side]:
                self._heap[cur_idx], self._heap[small_side] = \
                self._heap[small_side], self._heap[cur_idx]

                # must change array pos at each swap
                # self._pointer_array[self._heap[cur_idx]] = cur_idx
                # self._pointer_array[self._heap[small_side]] = small_side 
            
            else:
                break

            cur_idx = small_side


    # def decrease_key(self, vert: GraphNode) -> None:
    #     """O(_perc_up)"""
    #     cur_idx = self._pointer_array[vert]
    #     self._perc_up(cur_idx)

    def _get_min_child(self, cur_idx: int) -> int:
        """O(1)"""
        if 2 * cur_idx + 2 > len(self._heap) - 1:
            return 2 * cur_idx + 1
        if self._heap[2 * cur_idx + 2] > self._heap[2 * cur_idx + 1]:
            return 2 * cur_idx + 1
        return 2 * cur_idx + 2
    
    # def get_parent(self, vert: GraphNode) -> GraphNode:
    #     """O(1)"""
    #     return self._prev.get(vert, None)
    
    # def get_length(self, vert: GraphNode) -> float:
    #     """O(1)"""
    #     return self._node_to_priority[vert]
    
    # def get_dist(self, node: GraphNode) -> int:
    #     """O(1)"""
    #     return self._node_to_priority[node]
    
    # def set_dist(self, node: GraphNode, dist: int) -> None:
    #     """O(1)"""
    #     self._node_to_priority[node] = dist

    # def set_prev(self, node: GraphNode, prev: GraphNode) -> None:
    #     """O(1)"""
    #     self._prev[node] = prev