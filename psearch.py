import sollya
import random
import itertools

period = 2 + 10.0 * random.random()
print("period={}".format(float(2 * sollya.pi(100) / period)))

f = lambda x: sollya.cos(period * x)

def diff(func, x0, u=0.00001):
    return (func(x0 + u) - func(x0)) / u

def search_equality(func, x0, xstart, epsilon=0.001, step=0.0001):
    f_x0 = func(x0)
    h = func(xstart) - f_x0
    while abs(h) > epsilon:
        dxs = diff(func, xstart)
        if dxs > 0 and h > 0:
            xstart -= step
        elif dxs > 0 and h < 0:
            xstart += step
        elif dxs < 0 and h > 0:
            xstart += step
        else:
            xstart -= step
        h = func(xstart) - f_x0
    return x0, xstart

print("looking for deltas")
delta = []
for x0 in range(100):
    x0, x1 = search_equality(f, 1.0, x0 + 10.0)
    delta.append(x1 - x0)

print("computing subtraction of delta product")
sorted(delta)
new_delta = [abs(x1 - x0) for x0, x1 in itertools.product(delta, delta)]

print("reviewing candidates")
epsilon = 0.0001
num_test = 10
solution = None

def validate_period(func, candidate, epsilon=0.0001):
    f_values = list(map(f, [candidate * i for i in range(num_test)]))
    return  max(f_values) - min(f_values) < epsilon

for candidate in new_delta:
    if abs(candidate) < epsilon:
        # discard small values
        continue
    else:
        f_values = list(map(f, [candidate * i for i in range(num_test)]))
        if validate_period(f, candidate, epsilon=epsilon):
            solution = candidate
            print("found unrefined period is {}".format(candidate))
            break

# refine candidate
for divider in range(2, 100):
    if validate_period(f, solution / divider):
        solution = solution / divider
        print("refined solution is {}".format(solution))

            
        

