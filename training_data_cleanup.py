import pickle

flatten = lambda l: [item for sublist in l for item in sublist]

x_wins = pickle.load(open("x_wins.p", "rb"))
y_wins = pickle.load(open("y_wins.p", "rb"))

dx = [tuple([tuple([tuple(z) for z in l]) for l in x]) for x in flatten(x_wins)]
dy = [tuple([tuple([tuple(z) for z in l]) for l in x]) for x in flatten(y_wins)]

print(len(dx))
dx = set(dx)
print(len(dx))

print(len(dy))
dy = set(dy)
print(len(dy))

print(len(dx)+len(dy))

dx = [flatten(flatten(x)) for x in dx]
dy = [flatten(flatten(x)) for x in dy]

pickle.dump(dx,open("x_wins_clean.p", "wb"))
pickle.dump(dy,open("y_wins_clean.p", "wb"))