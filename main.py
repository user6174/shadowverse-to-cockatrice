from gene import *
import matplotlib.pyplot as plt

population = []
if input('\nDo you wish to initialize the population to a previously saved one? (y/n): ') == 'y':
    with open("population.txt", 'r') as f:
        tmp = f.readlines()
    for i in tmp:
        population.append(Deck(eval(i)))
else:
    population = 2 ** 11

g = Gene(population)
max_rating_hist = []
min_rating_hist = []
avg_rating_hist = []
cycleArgs = ('nat',  # tag to score
             0.1,  # score acceptance threshold for individuals in gen1
             0.005,  # increase of the above threshold over generations
             'SAS',  # selection method to use
             'DSPC',  # crossover method to use
             3,  # number of extra mutations in gen1
             10,  # after how many generations the number above decreases by 1
             'PM')  # mutation method to use

try:
    while g.getMaxRating() < 0.95:
        if g.cycle(*cycleArgs):
            max_rating_hist.append(g.getMaxRating())
            min_rating_hist.append(g.getMinRating())
            avg_rating_hist.append(g.getAvgRating())
        else:
            break
except KeyboardInterrupt:
    pass
if input('\nDo you wish to save this population for resuming the algorithm in the future? (y/n): ') == 'y':
    with open('population.txt', 'w+') as f:
        for i in g.getPopulation():
            f.write(str(i.getCards()) + '\n')
print(g.getBestIndividual())

x_axis = [i for i in range(len(avg_rating_hist))]
plt.xlabel('generations')
plt.ylabel('fitness')
plt.grid(True)
plt.plot(x_axis, min_rating_hist, 'r.', label='minimum fitness')
plt.plot(x_axis, avg_rating_hist, 'g.', label='average fitness')
plt.plot(x_axis, max_rating_hist, 'b.', label='maximum fitness')
plt.legend()
