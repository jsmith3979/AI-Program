import matplotlib.pyplot as plt
import random
import copy
import math
# my parameters for the code to use
N = 20
P = 100
MIN = -10
MAX = 10
MUTSTEP = 0.4
MUTRATE = 0.3
population = []
Generations = 100
mean_fitness = []

# my genes for each population stored below in an array with it being *N,
# N being the amount of genes i want per population and then fitness where
# the fitness is calculated for each population
class Individual:
    def __init__(self):
        self.gene = [0] * N  # stores the genes of each individual
        self.fitness = 0  # where the fitness value is displayed

# function 1

def test_function(ind):
    utility = 0

    for i in range(1, N):
        utility = utility + (i * (((2 * (ind.gene[i] ** 2)) - ind.gene[i - 1]) ** 2))

    return (utility + ((ind.gene[0] - 1) ** 2))

# function 2

# def test_function(ind):
#     utility1=0
#
#     utility2=0
#
#     for i in range(N):
#
#          utility1 = utility1 + (ind.gene[i]**2)
#
#          utility2 = utility2 + ( 0.5 * (i+1) * ind.gene[i] )
#
#     return (utility1 + (utility2**2) + (utility2**4))

# Rosenbrock function/ function 3

# def test_function(ind):
#     utility = 0
#     for i in range(len(ind.gene) - 1):
#         xnext = ind.gene[i + 1]
#         new = 100 * (xnext - ind.gene[i] ** 2) ** 2 + (ind.gene[i] - 1) ** 2
#         utility += new
#     return utility

# tournament where two members of the population are selected and then essentially fight and whoever is the lowest
# individual will go on to produce offspring
def new_tourny_selection(population):
    offspring = []
    for i in range(len(population)):
        offspring_one = population[random.randint(0, len(population) - 1)]
        offspring_two = population[random.randint(0, len(population) - 1)]

        if test_function(offspring_one) < test_function(offspring_two):
            offspring.append(offspring_one)
        else:
            offspring.append(offspring_two)
    return offspring

# get min utility is used to find the lowest individual in the population
def getMinUtitlity(population):
    max_utility = float('inf')
    for i in population:
        utility = test_function(i)
        if utility < max_utility:
            max_utility = utility
    return max_utility

# get max utility is used to find the highest individual in the population
def getMaxUtitlity(population):
    min_utility = float('-inf')
    for ind in population:
        utility = test_function(ind)
        if utility > min_utility:
            min_utility = utility
    return min_utility


if __name__ == '__main__':
    # more values and arrays being stored mostly for the graphs and for storage of highest and lowest individuals
    lowest_sum = 0
    lowest_individual = 0
    lowest_individual_sums = []
    highest_sum = 0
    highest_individual = 0
    highest_individual_sums = []

# this is to initialise the first generation of population
    for k in range(0, P):
        tempGene = []
        for y in range(0, N):
            tempGene.append(random.uniform(MIN, MAX))
        newInd = Individual()
        newInd.gene = tempGene.copy()
        population.append(newInd)
    for x in range(0, Generations):
        # this is to store total fitness for both population and offspring
        # as well as also to get the offsrping we made from the tournament and set it as
        # the variable offspring
        population_total_fitness = 0
        offspring = new_tourny_selection(population)
        offspring_fit_sum = 0
        # this is used to find the sum total of the population
        for ind in population:
            ind.fitness = test_function(ind)
            population_total_fitness += ind.fitness
        # this is my crossover it will set 3 variables named toff1 and toff2 and temp
        # toff1 and toff2 will then copy the offspring individual then the crosspoint variable
        # will be set with a random gene from 1 to however many genes you have set it to
        # we then do a loop going between crosspoint value and N we then put the toff1.gene and make it toff2.gene
        # and then set toff2.gene to temp.gene and then we make the new offspring[i] toff1 and then we make
        # offspring[i+1] toff2
        toff1 = Individual()
        toff2 = Individual()
        temp = Individual()
        for i in range(0, P - 1, 2):
            toff1 = copy.deepcopy(offspring[i])
            toff2 = copy.deepcopy(offspring[i + 1])
            temp = copy.deepcopy(offspring[i])
            crosspoint = random.randint(1, N)
            for j in range(crosspoint, N):
                toff1.gene[j] = toff2.gene[j]
                toff2.gene[j] = temp.gene[j]
            offspring[i] = copy.deepcopy(toff1)
            offspring[i + 1] = copy.deepcopy(toff2)
        # here we have the mutation code which sets new ind as individual()
        # and make new.ind as an array
        # we then go through 0 to N in a loop, we get a offspring[i].gene and also
        # we get the mutprob by setting a random number
        # then we do an if statement if mutprob is lower than our mutrate then we set the number
        # between -mutstep or mutstep then we change the gene to that number by doing gene = gene + alter
        # we then do if gene is bigger than max than gene = max, if it isn't bigger than gene = min
        # we then add this to newind.gene and then set offspring[i] to newind
        for i in range(0, P):
            newind = Individual()
            newind.gene = []
            for j in range(0, N):
                gene = offspring[i].gene[j]
                mutprob = random.random()
                if mutprob < MUTRATE:
                    alter = random.uniform(-MUTSTEP, MUTSTEP)
                    gene = gene + alter
                    if gene > MAX:
                        gene = MAX
                    if gene < MIN:
                        gene = MIN
                newind.gene.append(gene)
            offspring[i] = copy.deepcopy(newind)
        # this is used to find the total fitness of offspring
        for off in offspring:
            off.fitness = test_function(off)
            offspring_fit_sum += off.fitness
        # this is used to stop the offspring being higher than the population
        # if the offspring is higher than the population we set the offspring for that generation
        # as the population
        for i in range(0, P):
            if offspring[i].fitness > population[i].fitness:
                offspring[i] = copy.deepcopy(population[i])
        # this is used to calculate the mean fitness of the offspring
        # and also to put the information in an array to be displayed by the graph
        mean_fitness_generation = offspring_fit_sum / P
        mean_fitness.append(mean_fitness_generation)
        # this is used to get the lowest individual and then add it to the array to then be displayed by the graph
        lowest_individual = getMinUtitlity(offspring)
        lowest_individual_sums.append(lowest_individual)
        # this is used to get the highest individual and then add it to the array to be displayed by the graph
        highest_individual = getMaxUtitlity(offspring)
        highest_individual_sums.append(highest_individual)
        # we do this so that the next run of this code will have the population set to the offspring values
        population = copy.deepcopy(offspring)

        print(f"lowest individual in gen: {x + 1}, {lowest_individual}")

# this is how im plotting my values into the graph using range and len of the arrays to display each individual
plt.plot(range(len(lowest_individual_sums)),lowest_individual_sums, label="Lowest fitness")
plt.plot(range(len(mean_fitness)), mean_fitness, label="Mean fitness")
plt.plot(range(len(highest_individual_sums)),highest_individual_sums, label="Highest fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.show()

