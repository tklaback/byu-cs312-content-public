


bssf = float('inf')
lower_bound = 0

def get_bound(arr: list, avoid_row: int = None, avoid_col: int = None) -> tuple:
    cur_bound = 0
    
    #returns new reduced matrix and bound corresponding to it
    if avoid_row != None and avoid_col != None:
        arr[avoid_col][avoid_row] = float('inf')
    
    new_list = []

    for row in range(len(arr)):
        tmp_lyst = []
        if row == avoid_row:
            for col in range(len(arr[0])):
                tmp_lyst.append(float('inf'))
            new_list.append(tmp_lyst)
            continue
        min_val = min(arr[row])
        cur_bound += min_val
        for col in range(len(arr[0])):
            tmp_lyst.append(arr[row][col] - min_val)
        new_list.append(tmp_lyst)
    
    for row in range(len(new_list)):
        if row == avoid_col:
            for col in range(len(new_list[0])):
                new_list[col][row] = float('inf')
            continue
        min_col_num = min([new_list[col][row] for col in range(len(new_list[0]))])
        cur_bound += min_col_num
        for col in range(len(new_list[0])):
            new_list[col][row] -= min_col_num
    
    return (new_list, cur_bound)

def expand(arr: list, prev_bound: int, cur_lyst: list):
    expansion = []
    row_num = cur_lyst[-1] - 1
    for col in range(len(arr[row_num])):
        if arr[row_num][col] != float('inf'):
            new_matrix, bound = get_bound(arr, row_num, col)
            if (prev_bound + arr[row_num][col] + bound) < bssf:
                expansion.append([new_matrix, (prev_bound + arr[row_num][col] + bound), cur_lyst[:] + [col + 1]])
    
    return expansion

# TODO: How do I test the current subproblem to see if it is a complete tour?
# ANSWER: keep a data data structure for the current subproblem that shows which
# nodes you've already visited. Then, if the size of that data structure = n + 1 and the
# first and last elements are the same then return the bound, otherwise, infinity.


def test(visited: list, arr_length: int):
    if len(visited) == arr_length + 1 and visited[0] == visited[-1]:
        return True
    return False

def process(arr: list):
    global bssf

    lyst = [1]
    new_list, new_bound = get_bound(arr)

    q = [(new_list, new_bound, lyst)]

    while len(q) != 0:
        cur_element = q.pop(0)
        if cur_element[1] < bssf:
            arr_of_matrices = expand(cur_element[0], cur_element[1], cur_element[2])
            for itm in arr_of_matrices:
                if test(itm[2], len(arr)):
                    bssf = itm[1]
                elif itm[1] < bssf:
                    q.append(itm)

    return bssf
            


arr = \
[
    [float('inf'), 9           , float('inf'), 8           , float('inf')], 
    [float('inf'), float('inf'), 4           , float('inf'), 2           ], 
    [float('inf'), 3           , float('inf'), 4           , float('inf')], 
    [float('inf'), 6           , 7           , float('inf'), 12          ],
    [1           , float('inf'), float('inf'), 10          , float('inf')]
]


process(arr)