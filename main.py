import numpy as np
import sys, random
args = sys.argv[1:]

faceColors = ["W","Y","G","B","R","O"]
faceNames = ["U", "D", "F", "B", "L", "R"]
movetype = ["", "'", "2"]

def print_color(d, c=None):
	colors = {
		"W": "\033[47m", 
		"Y": "\033[43m", 
		"G": "\033[42m",
		"B": "\033[44m",
		"R": "\033[41m",
		"O": "\033[45m"
	}
	if c in faceColors:
		print(f"{colors[c]}{d}\033[49m", end="")
	else:
		print(d, end="")

def reset():
	cube = np.array([[x for y in range(8)] for x in range(6)])
	return cube

def viewer(data:np.ndarray):
	cube = [[faceColors[data[x][y]] for y in range(8)] for x in range(6)]
	cube = [viewerFace(cube[x], faceColors[x]) for x in range(6)]
	view = "\n".join([f"    {x}" for x in cube[0]])+"\n"+"\n".join([" ".join([x[z] for x in [cube[y] for y in [5,2,4,3]]]) for z in range(3)])+"\n"+"\n".join([f"    {x}" for x in cube[1]])+"\n"
	return view

def viewerFace(face:list, center):
	d = ["".join(face[0:3]),f"{face[7]}{center}{face[3]}","".join(reversed(face[4:7]))]
	return d

def viewprint(data:np.ndarray):
	d = data.copy()
	view = viewer(d)
	for i in view:
		print_color(i,i)

def mov(cube:np.ndarray, face, prime=False):
	f = faceNames.index(face)
	cube[f] = np.roll(cube[f], 2*(2*int(not(prime))-1))
	if f==0:
		data = [list(cube[x][0:3]) for x in [2,5,3,4]]
		if prime:
			pop = data.pop(0)
			data.append(pop)
		else:
			pop = data.pop()
			data.insert(0, pop)
		for i,j in enumerate([2,5,3,4]):
			cube[j][0:3] = data[i]
	elif f==1:
		data = [list(cube[x][4:7]) for x in [2,4,3,5]]
		if prime:
			pop = data.pop(0)
			data.append(pop)
		else:
			pop = data.pop()
			data.insert(0, pop)
		for i,j in enumerate([2,4,3,5]):
			cube[j][4:7] = data[i]
	elif f==2:
		data = [list(np.roll(cube[x], -i*2)[4:7]) for i,x in enumerate([0,4,1,5])]
		if prime:
			pop = data.pop(0)
			data.append(pop)
		else:
			pop = data.pop()
			data.insert(0, pop)
		for i,j in enumerate([0,4,1,5]):
			temp = np.roll(cube[j], -i*2)
			temp[4:7] = data[i]
			cube[j] = np.roll(temp, i*2)
	elif f==3:
		data = [list(np.roll(cube[x], i*2)[0:3]) for i,x in enumerate([0,5,1,4])]
		if prime:
			pop = data.pop(0)
			data.append(pop)
		else:
			pop = data.pop()
			data.insert(0, pop)
		for i,j in enumerate([0,5,1,4]):
			temp = np.roll(cube[j], i*2)
			temp[0:3] = data[i]
			cube[j] = np.roll(temp, -i*2)
	elif f==4:
		data = [list(np.roll(cube[x], 2)[0:3]) for x in [0,2,1]] + [list(cube[3])[2:5]]
		if prime:
			pop = data.pop(0)
			data.append(pop)
		else:
			pop = data.pop()
			data.insert(0, pop)
		for i,j in enumerate([0,2,1]):
			temp = np.roll(cube[j], 2)
			temp[0:3] = data[i]
			cube[j] = np.roll(temp, -2)
		cube[3][2:5] = data[3]
	else:
		data = [list(cube[0])[2:5], list(np.roll(cube[3], 2))[0:3]] + [list(cube[x])[2:5] for x in [1,2]]
		if prime:
			pop = data.pop(0)
			data.append(pop)
		else:
			pop = data.pop()
			data.insert(0, pop)
		cube[0][2:5] = data[0]
		temp = np.roll(cube[3], 2)
		temp[0:3] = data[1]
		cube[3] = np.roll(temp, -2)
		cube[1][2:5] = data[2]
		cube[2][2:5] = data[3]
	return cube

def move(cube:np.ndarray=reset(), string:str=None):
	now = cube
	if string:
		for i in string.split():
			if "2" in i:
				now = mov(mov(now, i.replace("2", "")), i.replace("2", ""))
			elif "'" in i:
				now = mov(now, i.replace("'", ""), True)
			else:
				now = mov(now, i)
	return now

def scramble(length:int=18):
	direction = 0
	adjust = 0
	temp = 0
	moves = []
	for i in range(length):
		while direction==temp and adjust==0:
			temp = random.randint(0,5)
			adjust = int(adjust==(temp+1)//2)*((temp+1)//2)
		direction = temp
		type = random.randint(0,2)
		moves.append(f"{faceNames[temp]}{movetype[type]}")
	return moves



if "--scramble" in args:
	moves = " ".join(scramble())
	print(moves)
	viewprint(move(string=moves))
	exit()