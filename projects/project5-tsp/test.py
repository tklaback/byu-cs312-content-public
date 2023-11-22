


bssf = float('inf')
lower_bound = 0

def get_bound(arr: list) -> tuple:
    cur_bound = 0
        
    def increment_and_return(arr: list):
        nonlocal cur_bound
        min_val = min(arr)
        cur_bound += min_val

        return [x - min_val for x in arr]

    
    #returns new reduced matrix and bound corresponding to it
    new_list = [increment_and_return(arr[row]) for row in range(len(arr))] # list(map(lambda x: x - min(arr[row]) if x != float('inf') else float('inf'), arr[row]))

    for row in range(len(new_list)):
        min_col_num = min([new_list[col][row] for col in range(len(new_list[0]))])
        cur_bound += min_col_num
        for col in range(len(new_list[0])):
            new_list[col][row] -= min_col_num
    
    return (new_list, cur_bound)

def process(arr: list):
    pass

arr = \
[
    [float('inf'), 5, 4, 3], 
    [3, float('inf'), 8, 2], 
    [5, 3, float('inf'), 9], 
    [6, 4, 3, float('inf')]
]


get_bound(arr)