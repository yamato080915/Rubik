import numpy as np
from collections import deque
from main import *

MAXDEPTH = 6

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

def solve_bfs(input:np.ndarray):
	queue = deque()
	history = {}

	byte = input.tobytes()
	queue.append( (input, [], 0) )
	history[byte] = 0

	while queue:
		cube, moves, depth = queue.popleft()

		if is_solved(cube):
			print(" ".join([f"{faceNames[x[0]]}{movetype[x[1]]}" for x in moves]))
			return
		if depth>=MAXDEPTH:
			continue
		for i in range(18):
			if depth==0 or moves[-1][0] != i//3:
				moved = cube.copy()
				mov(moved, faceNames[i//3], i%3==1)
				if i%3==2:
					mov(moved, faceNames[i//3])
				byte = moved.tobytes()
				if byte in history and history[byte] <= depth + 1:
					continue
				history[byte] = depth + 1
				queue.append( (moved, moves + [[i//3, i%3]], depth + 1) )

string = " ".join(scramble(6))
print("scramble =", string)
cube = move(string=string)
solve_bfs(cube)