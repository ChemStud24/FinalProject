def C(n):
	d = {0:0, 1:6, 2:21, 3:56, 4:126, 5:252}
	return d.get(n)

def T(n):
	return sum(range(n,0,-1))

def states(N):
	return sum(C(n)*((6*T(N+n) - 6*T(n)) + N) for n in range(N+1))