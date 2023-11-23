


bssf = float('inf')
lower_bound = 0

def get_bound(arr: list, avoid_row: int = None, avoid_col: int = None) -> tuple:
    cur_bound = 0
    
    #returns new reduced matrix and bound corresponding to it
    new_list = []

    for row in range(len(arr)):
        if row == avoid_row:
            continue
        tmp_lyst = []
        min_val = min(arr[row])
        cur_bound += min_val
        for col in range(len(arr[0])):
            tmp_lyst.append(arr[row][col] - min_val)
        new_list.append(tmp_lyst)
    
    for row in range(len(new_list)):
        if row == avoid_col:
            continue
        min_col_num = min([new_list[col][row] for col in range(len(new_list[0]))])
        cur_bound += min_col_num
        for col in range(len(new_list[0])):
            new_list[col][row] -= min_col_num
    
    return (new_list, cur_bound)

def expand(arr: list, state: int = None):
    for row in range(len(arr)):
        for col in range(len(arr[0])):
            get_bound(arr, row, col)



def process(arr: list):
    get_bound(arr)

    q = [arr]

    while len(q) != 0:
        cur_arr = arr.pop(0)
        if get_bound(cur_arr)[1] < bssf:
            pass


arr = \
[
    [float('inf'), 5, 4, 3], 
    [3, float('inf'), 8, 2], 
    [5, 3, float('inf'), 9], 
    [6, 4, 3, float('inf')]
]


get_bound(arr)