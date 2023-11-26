


bssf = float('inf')
lower_bound = 0

def get_bound(arr: list, avoid_row: int = None, avoid_col: int = None) -> tuple:
    cur_bound = 0
    
    #returns new reduced matrix and bound corresponding to it
    if avoid_row and avoid_col:
        arr[avoid_col][avoid_row] = float('inf')
    
    new_list = []

    for row in range(len(arr)):
        if row == avoid_row:
            for col in range(len(arr[0])):
                tmp_lyst.append(float('inf'))
            new_list.append(tmp_lyst)
            continue
        tmp_lyst = []
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

def expand(arr: list, row_num: int, prev_bound: int, remaining_path_cost: int):
    expansion = []
    for col in range(len(arr[row_num])):
        if arr[row_num][col] != float('inf'):
            new_matrix, bound = get_bound(arr, row_num, col)
            if (prev_bound + remaining_path_cost + bound) < bssf:
                expansion.append([(row_num, col), (prev_bound + remaining_path_cost + bound)])
    
    return expansion

# TODO: How do I test the current subproblem to see if it is a complete tour?



def process(arr: list):
    get_bound(arr)

    q = [arr]

    while len(q) != 0:
        cur_arr = q.pop(0)
        new_matrix, bound = get_bound(cur_arr)
        if bound < bssf:
            pass


arr = \
[
    [float('inf'), 9           , float('inf'), 8           , float('inf')], 
    [float('inf'), float('inf'), 4           , float('inf'), 2           ], 
    [float('inf'), 3           , float('inf'), 4           , float('inf')], 
    [float('inf'), 6           , 7           , float('inf'), 12          ]
    [1           , float('inf'), float('inf'), 10          , float('inf')]
]


get_bound(arr)