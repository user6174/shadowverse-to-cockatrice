from deck import *
from random import random


class Gene:
    def __init__(self, population=2 ** 11):
        """
        :param population: either an int dictating the size of the starting population or a list of Deck objects
        """
        # the methods and variables used are explained below
        if type(population) == int:
            self.population = []
            for i in range(population):
                self.population.append(Deck())
        else:
            self.population = population
        self.size = len(self)
        
    def __len__(self):
        return len(self.population)

    population = []  # a list of decks

    def getPopulation(self):
        return self.population

    def setPopulation(self, population):
        self.population = population

    size = 0
    '''
    The number of individuals comprising the INITIAL population (this variable isn't meant to be updated after a size
    change; in fact, it indicates what target size should be reached again after a change in the actual size.
    '''

    def getSize(self):
        return self.size

    gen = 1  # an integer keeping track of the current iteration of the population history

    def getGen(self):
        return self.gen

    def setGen(self, gen):
        self.gen = gen

    # integers representing the maximum, minimum and average ratings of the population
    max_rating = 0
    min_rating = 0
    avg_rating = 0

    def getMaxRating(self):
        return self.max_rating

    def setMaxRating(self):
        self.max_rating = max([i.rating for i in self.population])

    def getMinRating(self):
        return self.min_rating

    def setMinRating(self):
        self.min_rating = min([i.rating for i in self.population])

    def getAvgRating(self):
        return self.avg_rating

    def setAvgRating(self):
        self.avg_rating = sum([i.rating for i in self.population]) / self.size

    best_rating = 0  # the highest rating ever appeared in the history of the population
    best_individual = []  # the deck with the highest rating ever appeared in the history of the population
    '''
    Note that while this variable isn't needed if the algorithm stops after a certain rating threshold is surpassed, 
    it's useful to have when one runs the algorithm indefinitely or up to a certain generation.
    '''
    def getBestRating(self):
        return self.best_rating

    def setBestRating(self):
        if self.max_rating > self.best_rating:
            self.best_rating = self.max_rating

    def getBestIndividual(self):
        return self.best_individual

    def setBestIndividual(self):
        if self.max_rating >= self.best_rating:
            best_individual_index = [i.rating for i in self.population].index(self.max_rating)
            self.best_individual = self.population[best_individual_index]

    def updateParams(self):
        """Updates rating statistics and variables relative to the best individual."""
        self.setMinRating()
        self.setAvgRating()
        self.setMaxRating()
        self.setBestRating()
        self.setBestIndividual()

    def cull(self, threshold=0, annealing=0):
        """
        Removes all the individuals with a score less than x, where x = threshold + gen * annealing
        
        :param threshold: it shouldn't be too different from the average gen1 ratings because otherwise too few/too 
        many decks are excluded, with an impact on, respectively, the effectiveness of the culling process and the 
        genetic diversity that one wishes to maintain.
        :param annealing: note that the number of generations that the population can live through caps 
        at n = (1 - threshold)/annealing (for example, with a threshold of .3 an annealing of .01 the algorithm is given
        70 generations worth of time to find an optimal solution. with this in mind, sensible values  lay in the 
        10^-2 ~ 10^-3 range.
        """
        threshold += self.gen * annealing
        self.population = [i for i in self.population if i.rating > threshold]

    def getIndividual(self, method):
        """Picks an individual from the population with an algorithm that correlates the chance of being picked with the
        rating of the individual.

        :param method: it specifies how the selection is carried out - the options are:
            > 'SAS' (stochastic acceptance selection: https://arxiv.org/pdf/1109.3627.pdf )
        """
        if method == 'SAS':
            while True:
                threshold = random()
                individual = choice(self.population)
                if threshold < individual.rating / self.max_rating:
                    return individual

    def cycle(self, rating_tag='', cull_threshold=0, cull_annealing=0,
              selection_method='SAS', crossover_method='SPC',
              mutation_annealing_param=0, mutation_annealing_step=1, mutation_method='PM'):
        """Runs a generation of the population's history: the population is culled and from the remaining individuals
        some are selected for breeding. Offspring is produced until it gets to size of the previous population, at
         which moment it is appointed as the new population, and the population parameters are updated.

        :param rating_tag: refer to Deck.rate
        :param cull_threshold: refer to self.cull
        :param cull_annealing: refer to self.cull
        :param selection_method: refer to self.getIndividual
        :param crossover_method: refer to Deck.mix
        :param mutation_annealing_param: an int stating how many extra mutations (note that one is always carried
        out regardless) the offspring of gen1 is subjected to
        :param mutation_annealing_step: an int representing after how long of an 'era' the number of extra mutations is
        reduced by one
        :param mutation_method: refer to Deck.mutate
        """
        print("generation {}:".format(self.gen))
        for i in self.population:
            i.rate(rating_tag)
        self.updateParams()
        tmp = self.population[:]
        self.cull(cull_threshold, cull_annealing)
        if len(self) == 0:
            print("The program ended prematurely as every individual would be culled.")
            self.population = tmp
            return False
        del tmp
        print("    culled {} individual{} out of {} under threshold {}".format(
            self.size - len(self.population), 's' * ((self.size - len(self.population)) != 1), self.size,
            round(cull_threshold + self.gen * cull_annealing, 8)))
        print("    selecting breeders from a pool of {} ({}% of the starting population)...".format(
            len(self.population), round(100 - (1 - len(self.population) / self.size) * 100, 2)))
        next_gen = []
        extra_mutations = mutation_annealing_param - self.gen // mutation_annealing_step
        print("    {} extra mutation{} will be performed on the offspring".format(
            extra_mutations * (extra_mutations > 0), 's' * (extra_mutations != 1)))
        while len(next_gen) < self.size:
            parent = self.getIndividual(selection_method)
            new_individual = parent.mix(self.getIndividual(selection_method), crossover_method)
            new_individual.mutate(mutation_method)
            for i in range(extra_mutations):
                new_individual.mutate(mutation_method)
            next_gen.append(new_individual)
        self.population = next_gen
        self.gen += 1
        print("    minimum fitness: {}\n    average fitness: {}\n    maximum fitness: {}\n".format(self.min_rating,
                                                                                                   self.avg_rating,
                                                                                                   self.max_rating))
        return True
