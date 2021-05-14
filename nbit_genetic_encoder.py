import random
import statistics
random.seed(2)
n = 10

no = int(input("Enter "+str(n)+" bit integer "))

population = []
score = []
max_score = 1024
def initial_population(size):
    global n
    global population
    for i in range(size):
        gene = []
        for j in range(n):
            gene.append(random.choice([0,1]))
        population.append(gene)

def fitness(no):
    global population
    global score
    global n
    # mod = int(pow(2,int(n/2)))
    # l_no = int(no/mod)
    # r_no = no%mod
    score = []
    for gene in population:
        gene_no = ""
        for i in range(n):
            gene_no += str(gene[i])
        gene_no = int(gene_no,base=2)
        score.append(int(pow(2,n))-abs(gene_no - no))
    # for gene in population:
    #     gene_no = int("".join([str(i) for i in gene]),base=2)
    #     l = int(gene_no/mod)
    #     r = gene_no%mod
    #     score.append(2*mod - abs(l - l_no) - abs(r - r_no))



def next_population(size,k):
    global population
    global score
    new_population = []
    for i in range(int(size/2)):
        parent = random.choices(population,weights=score,k=2) 
        new_population.append(parent[0][:k]+parent[1][k:])
        new_population.append(parent[1][:k]+parent[0][k:])
    return new_population 

def mutation(percentage):
    global population
    for j in range(len(population)):
        for i in range(len(population[j])):
            if(random.uniform(0,1) < percentage):
                population[j][i] = 1 - population[j][i]

def evolve(size,no):
    global population
    global score
    global n
    initial_population(size)
    fitness(no)
    i = 1
    binary = "".join([str(i) for i in population[score.index(max(score))]])
    # print("gen: 0 best:",binary,"max score:",max(score))
    while True:
        if max(score) == max_score:
            # binary = "".join([str(i) for i in population[score.index(32)]])
            # print("binary form is",binary)
            return i - 1
        population = next_population(size,int(n/2))
        mutation(0.1)
        fitness(no)
        binary = "".join([str(i) for i in population[score.index(max(score))]])
        print("gen:",i,"best:",binary,"max score:",max(score))
        i += 1
    
evolve(32,no)
# gen = []
# for i in range(1024):
#     gen.append(evolve(32,i))
# avg = sum(gen)/1024
# # std = (sum([(avg - i)**2 for i in gen])/1024)**0.5
# std = statistics.stdev(gen)
# print(sum(gen)/1024)
# print(sum([1 for i in gen if i > 50]))

# print(std)
# print(statistics.median(gen))
# print(statistics.mode(gen))
