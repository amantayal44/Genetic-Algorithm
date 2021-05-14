import random
random.seed(10)
with open("wiki-100k.txt") as f:
    wordlist = []
    for line in f:
        wordlist.append(line.strip().lower())
wordlist = list(wordlist)
text = 'the mishap of two drug dealer trying to survive in the complicated and corrupted world of crime, \nleading them from the point of working for money to working to survive, \nall starting with an honest high school teacher trying to make money for his family after finding \nout cancer had not left him much time'
key = 'hector'

def encrypt(text,key):
    k = len(key)
    i = 0
    cipher = ''
    for alpha in text:
        if alpha not in ['',' ','\n','.',',']:
            c = (ord(alpha) + ord(key[i]) - 2*ord('a'))%26
            cipher += chr(c+ord('a'))
            i = (i+1)%k
        else:
            cipher += alpha
    return cipher

def decrypt(cipher,key):
    k = len(key)
    i = 0
    text = ''
    for alpha in cipher:
        if alpha not in ['',' ','\n','.',',']:
            c = (ord(alpha) - ord(key[i]) + 26)%26
            text += chr(c+ord('a'))
            i = (i+1)%k
        else:
            text += alpha
    return text


# print(encrypt(text,key))
cipher = encrypt(text,key)
b = True
def textprocess(text):
    new = ''
    for i in text:
        if i not in ['\n','.',',']:
            new += i
    return new

def check_in_dict(text):
    words = textprocess(text).split(' ')
    for word in words:
        if word not in wordlist:
            print(word)
            return False
    return True

letters = [chr(i+ord('a')) for i in range(26)]
def init_population(size,k):
    population = []
    for i in range(size):
        key = ''.join([random.choice(letters) for j in range(k)])
        population.append(key)
    return population

def calc_score(key):
    text = decrypt(cipher,key)
    words = textprocess(text).split(' ')
    score = 0
    for word in words:
        if word in wordlist:
            score += 1
    return score
    

score = {}
def fitness(population):
    global score
    for child in population:
        if child not in score:
            score[child] = calc_score(child)


def new_generation(population,score,best,mutaion_rate):
    size = len(population)
    k = len(population[0])
    population.sort(key= lambda x: -1*score[x])
    new_population = population[:best]
    left = int((size - best)/2)
    total_score = sum([score[i] for i in population])
    for i in range(left):
        #selection
        p1 = random.randint(1,total_score-1)
        p2 = random.randint(p1,total_score)
        index = 0
        while p1 or p2:
            if p1 == 0:
                pass
            elif score[population[index]] >= p1:
                parent1 = population[index]
                p1 = 0
            else:
                p1 -= score[population[index]]
            if p2 == 0:
                pass
            elif score[population[index]] >= p2:
                parent2 = population[index]
                p2 = 0
            else:
                p2 -= score[population[index]]
        #crossover
        # s = random.randint(0,k-1)
        s = random.randint(1,k-2)
        child1 = parent1[:s] + parent2[s:]
        child2 = parent2[:s] + parent1[s:]
        #mutation 
        for i in range(k):
            if random.uniform(0,1) < mutaion_rate:
                child1 = child1[:i] + random.choice(letters) + child1[i+1:]
            if random.uniform(0,1) < mutaion_rate:
                child2 = child2[:i] + random.choice(letters) + child2[i+1:]
        new_population.append(child1)
        new_population.append(child2)
    return new_population

def log(gen):
    high = max(score.values())
    keys = [key  for (key, value) in score.items() if value == high]
    print("gen:",gen,"keys:",keys,"score:",high)
    return [high,keys[0]]

#max 55
size = 30
new = 0
population = init_population(size,6)
fitness(population)
new = len(score)
high,key = log(0)
i = 1
while i < 100 and high != 55:
    mutation = 0.4 - 0.3*(i/100)
    if mutation < 0.1: mutation = 0.1
    population = new_generation(population,score,4,mutation)
    fitness(population)
    high,key = log(i)
    i += 1
plaintext = decrypt(cipher,key)
print(plaintext)
# print(calc_score('hector'))