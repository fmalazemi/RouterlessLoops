#!/usr/bin/python
'''
In this python script, you can:
	1. Create loops for NxN ----> genNxN(N)
	2. calculate average hop count ----> calcHopCount(L, N)
	3. Test if two loops can be fused ---> canFuse(x, L1, L2)
	4. Fuse two loops into one ----> fuse(x, L1, L2)
	5. Count number of pairs sharing a loop ---> countPairsShareOneLoop(L, N) 
	6. Check if hop count can be lowered than avg hop count 
		if a loop is reversed -----> reverseOne(L, N)
	7. Rotate a loop 90 degree ----> Rotate90(L)
	8. Shift a loop -----> 
	9. Test if two loops are equal ----> equalLoops(L1, L2)
	10. calculate average of all hop count averages for
		each link fault ---->  CalcAvgOfAvg(N, L)
	11. convert a node coordiante from [x,y] 
		to x*N+y ----> convertCordinates(N, L)
'''







def calcHopCount(N, loopSet):
	#given a loop set, calculate average hop count
	D = [[ N*N*N for x in range(N*N)] for x in range(N*N)]
	for l in loopSet: 
		for i in xrange(len(l)):
			d = 0
			for j in xrange( len(l)):  
				j = (i+j)%len(l)
				D[l[i]][l[j]] = min(d, D[l[i]][l[j]])
				d += 1

	s = 0.0
	for i in D:
		s += sum(i)
		#print i, sum(i)
	for i in D:
		for j in i:
			if j == N*N*N: ## my infinity
				print "\nERROR: Not Complete interconnection."
				assert False 
	return s/(N**4-N**2)





def canFuse(x, L1, L2):
	#Can loops L1 & L2 be fused at node x? 
	#In this function, we check if there is x->y in L1 and y->x in L2
	#otherwise return false
	
	#Sanitary check :) 
	if x not in L1 or  x not in L2:
		return False
		
	#test if links are opposites 
	p = (L1.index(x) + 1) % len(L1)
	q = L2.index(x) - 1
	if L1[p] != L2[q]: 
		return False 
	return True  


	

def fuse(x, L1, L2):
	
	#join the two loops L1 & L2 assume canFuse(x, L1, L2) == True
	
	#Sanitary check	
	if not canFuse(x, L1, L2):
		print "\nERROR: Can not fuse.", L1, "with", L2, "at", x
		assert False 

	p = L1.index(x)
	q = L2.index(x)
	L = L1[:p+1] + L2[q:] + L2[:q] + L1[p+1:]
	#split L1 and to add L2[q:]+L2[:q] in the middle 
	#REMEMBER: some nodes may appear more than once in fused L
	return L


def generateLoop(a, b, n, m):
	
	#a,b are upper left corner, n,m are lower right corner
	L = []
	i = a
	j = b
	while j < m:
		L.append([i,j])
		j += 1	
	while i < n:
		L.append([i, j])
		i += 1
	while j > b:
		L.append([i,j])
		j -= 1
	while i > a:
		L.append([i,j])
		i -= 1
	return L
	
	
def reverseLoop(L):
	#Why do you need a function for this ?
	L.reverse() 
	return L
		
	
def convertCordinates(L, N):
	# converts every node in every loop from [a,b] to a*N+b
	# L must be the outer layer for NxN network. 
		
	A = []
	for l in L:
		newL = []
		for node in l:
			newL.append(node[0] * N + node[1])
		A.append(newL)
	return A
	
	
def shiftLoop(L, rowShift, colShift):
	
	
	A = [] 
	for node in L:
		A.append([node[0]+rowShift, node[1]+colShift])
	return A
	
	
def shiftAllLoops(L, rowShift, colShift):
	A = []
	for l in L:
		a = shiftLoop(l, rowShift, colShift)
		A.append(a)
	return A

def rotate90(L):
	#Rotate the loop 90 where L is a loop 
	#for outer layer for some NxN network.  
	#That is, L coordiantes lay on row/column 0 and N-1
	A = []
	for l in L:
		a = []
		for node in l:
			a.append([node[1], node[0]])
		#a.reverse()
		A.append(a)
	return A
		


def genOuterLayerLoops(N):
	if N == 1:
		return []
	if N == 2:
		return [generateLoop(0, 0, N-1, N-1), reverseLoop(generateLoop(0, 0, N-1, N-1))]
	L = [] 
	L.append(reverseLoop(generateLoop(0, 0, N-1, N-1)))
	
	j = 1
	while j < N-1:
		L.append(generateLoop(0, 0, N-1, j))
		j += 1
	j = N-2
	while j > 0:
		L.append(generateLoop(0, j, N-1,N-1))
		j -= 1
	i = 0
	while i < N-1:
		L.append(generateLoop(i, 0, i+1, N-1))
		i += 1
	return L
	
		


def genNxN(N):
	L = []
	rowShift = 0
	colShift = 0
	M = N
	while M > 1:
		A = genOuterLayerLoops(M)
		if (M/2) % 2 == 1:
			A = rotate90(A)
				
		A = shiftAllLoops(A, rowShift, colShift)

		L = L + A
		M -= 2
		rowShift += 1
		colShift += 1
	L = convertCordinates(L, N)

	return L


def printLoop(L, N):
	print L, "The loop"
	grid = [[0]*N for i in xrange(N)]
	for i in L:
		row = i/N
		col = i%N
		grid[row][col] = 1
	
	for i in grid:
		print i
	print "     _______________"



def countPairsShareOneLoop(L, N):
	# For relaibility, check how many pairs of nodes sharing a single loop
	
	
	M = N*N
	T = [ [0]*M for i in range(M)]
	for l in L:
		for i in xrange(len(l)):
			for j in range(i+1, len(l)):
				
				T[l[i]][l[j]] += 1
				T[l[j]][l[i]] += 1
	count = 0 # pairs sharing one loop
	count2 = 0 # pairs sharing multiple loops
	for i in xrange(N*N):
		for j in range(i+1, N*N):
			if T[i][j] == 1:
				count += 1 
			if T[i][j] == 0:
				print i, "to", j
				assert False
			if T[i][j] > 1:
				count2 += 1
	return count, count2
	


def equalLoops(L1, L2):
	if len(L1) != len(L2):
		return False
	n = len(L1)
	if L1[0] not in L2:
		return False  
	j = L2.index(L1[0])
	for i in xrange(n):
		if L1[i] != L2[j]:
			return False 
		j = (j+ 1)%n
	return True 
	


def CalcAvgOfAvg(L, N):
	# record the avg hop count after every fault occur
	# return the average of all averages
	count = 0
	avg = 0.0
	max_ = calcHopCount(N, L)
	min_ = max_ * 20 

	for loop1 in xrange(len(L)):
		for loop2 in range(loop1+1, len(L)):
			for i in L[loop1]:
				if not i in L[loop2]:
					continue 
				if not canFuse(i, L[loop1], L[loop2]):
					continue 
				fusedLoop = fuse(i, L[loop1], L[loop2])
				x = min(loop1, loop2)
				y = max(loop1, loop2)
				temp = L[:x]+L[x+1:y] + L[y+1:]
				temp.append(fusedLoop)			
				hops = calcHopCount(N, temp)
				max_ = max(max_, hops)
				min_ = min(min_, hops)
				if max_ == hops:
					max_List = temp
				avg += hops
				count += 1
	return avg/count, min_, max_




def reverseOne(L, N):
	#to test if reversing a loop will results in lower hop count
	minHops = calcHopCount(N, L)
	for i in L:
		i.reverse()
		minHops = min(calcHopCount(N, L), minHops)
		i.reverse()
	
	return minHops 



for i in range(2, 5):
	N = i
	L = genNxN(i)
	oneLoopPairs, multiLoopPairs =  countPairsShareOneLoop(L, N)
	
	
	
	
	avg, min_, max_ = CalcAvgOfAvg(L, N)

	s = str(i)+"x"+str(i)+"\t"+ str(calcHopCount(N, L))+"\t"+ str(oneLoopPairs)+"\t"+str(multiLoopPairs)+"\t"+str(avg)+"\t"+str(min_)+"\t"+str(max_)
	print s


		


