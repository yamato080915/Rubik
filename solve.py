import numpy as np
from main import *

MAXDEPTH = 5

def is_solved(cube:np.ndarray=reset()):
	return np.array_equal(cube, reset())

def solve_dfs(cube:np.ndarray, depth=0, moves=[]):
	if depth==0:
		global history
		history = {cube.tobytes(): 0}
	elif depth==MAXDEPTH:
		return
	for i in range(18):
		if depth==0 or moves[-1][0]!=i//3:
			moved = cube.copy()
			mov(moved, faceNames[i//3], i%3==1)
			if i%3==2:
				mov(moved, faceNames[i//3])
			moves_ = moves + [[i//3, i%3]]
			byte = moved.tobytes()
			if byte in history and history[byte]<=depth+1:
				continue
			history[byte] = depth+1
			if is_solved(moved):
				print(" ".join([f"{faceNames[x[0]]}{movetype[x[1]]}" for x in moves_]))
			else:
				solve_dfs(moved, depth+1, moves_)

string = " ".join(scramble(5))
print("scramble =", string)
cube = move(string=string)
solve_dfs(cube)