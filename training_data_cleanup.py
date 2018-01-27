import pickle

flatten = lambda l: [item for sublist in l for item in sublist]

x_wins = pickle.load(open("x_wins.p", "rb"))
y_wins = pickle.load(open("y_wins.p", "rb"))

dx = [tuple([tuple([tuple(z) for z in l]) for l in x]) for x in flatten(x_wins)]
dy = [tuple([tuple([tuple(z) for z in l]) for l in x]) for x in flatten(y_wins)]

print(len(dx))
dx = list(set(dx))
print(len(dx))

print(len(dy))
dy = list(set(dy))
print(len(dy))

print(len(dx)+len(dy))

pickle.dump(x_wins,open("x_wins_clean.p", "wb"))
pickle.dump(y_wins,open("y_wins_clean.p", "wb"))