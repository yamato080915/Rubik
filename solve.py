import numpy as np
from main import *

def is_solved(cube:np.ndarray=reset()):
    return np.array_equal(cube, reset())

def solve_func(cube:np.ndarray, depth=0, hand:list=[], history:set=set()):
    #print(depth)
    if depth==3:
        return
    for i in range(18):
        moved = cube.copy()
        moved = mov(moved, faceNames[i//3], i%3==1)
        if i%3==2:moved = mov(moved, faceNames[i//3])
        if is_solved(moved):
            print(" ".join(hand+[f"{faceNames[i//3]}{movetype[i%3]}"]))
        else:
            byte = moved.tobytes()
            if not byte in history:
                history.add(byte)
                solve_func(moved, depth+1, hand+[f"{faceNames[i//3]}{movetype[i%3]}"], history)

def solve(cube:np.ndarray):
    solve_func(cube)

string = " ".join(scramble(2))
print(string)
#viewprint(move(string=string))
cube = move(string=string)
solve(cube)