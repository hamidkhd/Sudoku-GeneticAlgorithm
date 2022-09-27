from typing import Counter
import numpy as np 
import random
import time


map_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


class Chromosome:
    def __init__(self):
        self.map = list()
        self.fitness = int(0)


    def fitness_calculation(self, Solution):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == Solution[i][j]:
                    self.fitness += 1


def population_building(Question, Solution):
    population = list()
    value = 2 ** (len(map_values))
    for i in range(value):
        temp_values = list()
        for j in range(len(map_values)):
            x = np.random.choice(map_values, size=len(map_values), replace=True)
            temp_values.append(x.tolist())

        for x in range(len(Question)):
            for y in range(len(Question[x])):
                if Question[x][y] != '-':
                    temp_values[x][y] = Question[x][y]

        new_chromosome = Chromosome()
        new_chromosome.map = temp_values.copy()
        new_chromosome.fitness_calculation(Solution)
        population.append(new_chromosome)

    return population 


def selection(population):
    population = sorted(population, key=lambda x: x.fitness) 
    fitness_rank = [i ** 2 for i in range(len(population))]
    population = random.choices(population, weights= fitness_rank, k=len(population))
    return population


def crossover(population, Question, Solution, weight):
    new_population = list()
    if weight == 1:
        p_c = (sum([i.fitness for i in population]) / len(population)) / (len(map_values) ** 2) 
    else:
        p_c = weight

    for x in range(len(population)//2):
        # rand_people = np.random.choice(population, size=2, replace=False)
        population = sorted(population, key=lambda x: x.fitness) 
        fitness_rank = [i ** 2 for i in range(len(population))]
        rand_people = random.choices(population, weights= fitness_rank, k=2)
        parent_a, parent_b = rand_people

        p_rand = random.random()

        if p_rand < p_c:
            child1, child2 = crossover_helper(parent_a, parent_b, Question, Solution)
            new_population.append(child1)
            new_population.append(child2)
        else:
            new_population.append(parent_a)
            new_population.append(parent_b)

    return new_population


def crossover_helper(parent_a, parent_b, Question, Solution):
    a = parent_a.map
    b = parent_b.map

    new_a = Chromosome()
    new_b = Chromosome()

    for i in range(len(map_values)):
        point = random.randint(0, len(map_values)-1)
        new_a.map.append(a[i][:point] + b[i][point:])
        new_b.map.append(b[i][:point] + a[i][point:])

    # for x in range(len(Question)):
    #     for y in range(len(Question[x])):
    #         if Question[x][y] != '-':
    #             new_a.map[x][y] = Question[x][y]
    #             new_b.map[x][y] = Question[x][y]

    new_a.fitness_calculation(Solution)
    new_b.fitness_calculation(Solution)

    return new_a, new_b


def mutation(population, Question, Solution, weight):
    p_c = (sum([i.fitness for i in population]) / len(population)) / (len(map_values) ** 2) 
    p_m = min(((1 - p_c) / 3), (1 / len(map_values)))
    if weight != 1:
        p_m *= weight

    for i in population:
        new_map = list()
        p_rand = random.random()

        if p_rand < p_m:
            for j in i.map:
                temp = list()
                for x in j:
                    p_rand = random.random()

                    if p_rand < p_m:
                        temp.append(np.random.choice(map_values, size=1, replace=True)[0]) 
                    else:
                        temp.append(x)

                new_map.append(temp)

            i.map = new_map
            i.fitness = int(0)
            i.fitness_calculation(Solution)

            # for x in range(len(Question)):
            #     for y in range(len(Question[x])):
            #         if Question[x][y] != '-':
            #             i.map[x][y] = Question[x][y]

    return population


def get_file_data(file_name):
    map_info = list()
    file = open(file_name,"r")
    file_content = file.readlines()
    for i in file_content:
        line_info = list()
        for j in i:
            if j != '\n':
                line_info.append(j)
        map_info.append(line_info)
    file.close()
    return map_info


def main():
    input_Question = get_file_data("Test.txt")
    input_Solution = get_file_data("Test-Solution.txt")
    population = population_building(input_Question, input_Solution)   

    counter = int(0)

    repeat = int(0)
    pre_result = int(0)
    crossover_weight = int(1)
    mutation_weight = int(1)

    start = time.process_time()
    while True:
        population = selection(population)
        population = crossover(population, input_Question, input_Solution, crossover_weight)
        population = mutation(population, input_Question, input_Solution, mutation_weight)

        result = max([i.fitness for i in population])
        counter += 1          
        end = time.process_time()

        repeat += 1 if pre_result == result else 0

        if repeat >= 3:
            crossover_weight = 0.95
            mutation_weight = 5
            repeat = 0
        else:
            crossover_weight = 1
            mutation_weight = 1

        pre_result = result
        counter += 1        
        
        end = time.process_time()
        print(counter, result, end-start, "s")
        
        if result == len(map_values) ** 2:
            for i in population:
                if i.fitness == len(map_values) ** 2:
                    print(i.map)
            break


if __name__ == "__main__":
    main()
