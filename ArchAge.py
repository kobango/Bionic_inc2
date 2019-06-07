import numpy
import matplotlib.pyplot as plt


def foodarray():
    N = numpy.zeros([20, 20])
    pos = numpy.random.randint(1, 13, [9, 2])

    for i in pos:
        for j in i:
            N[i, j] = 1

    pos = numpy.random.randint(1, 20, [2, 2])

    for i in pos:
        for j in i:
            N[i, j] = 1
    return N


def evr():
    N = numpy.zeros([20, 20])
    i = 0
    while i < 20:
        j = 0

        while j < 20:
            if (i == 0 or j == 0 or i == 19 or j == 19):
                N[i, j] = 1
            j = j + 1
        i = i + 1
    return N


class Population:
    def __init__(self, protocels):
        self.celss = protocels
        self.enw = evr()

    def killweak(self):
        for i in self.celss:
            if (i.food < 0):
                poz = i.position
                self.enw[poz[0], poz[1]] = 0
                self.celss.remove(i)

    def killmass(self):
        for i in self.celss:

            if (i.food > 400):
                poz = i.position
                self.enw[poz[0], poz[1]] = 0
                self.celss.remove(i)
            if(i.genotype[2]==1):
                if(i.food > 300):
                    poz = i.position
                    for c in self.celss:
                        if ((abs(c.position[0]-poz[0])< 2) and (abs(c.position[1]-poz[1])<2)):
                            i.food - 2
                            c.food + 2

    def reproduction(self):
        for i in self.celss:
            if (i.food > 100):
                ran = numpy.random.randint(-1, 1, [2])
                babpos = i.position + ran
                if (self.enw[babpos[0], babpos[1]] == 0):
                    babycell = ProtoCell(i.position + ran)
                    babycell.genotype = i.genotype
                    self.celss.append(babycell)
                    i.food = 40
                    if(babycell.genotype[3]==1):
                        self.enw[babpos[0], babpos[1]] = 3
                    else:
                        self.enw[babpos[0], babpos[1]] = 2

            if (i.food > 100):
                ran = numpy.random.randint(-1, 1, [2])
                babpos = i.position + ran
                if (self.enw[babpos[0], babpos[1]] == 0):
                    babycell = ProtoCell(i.position + ran)
                    babycell.genotype = i.genotype
                    self.celss.append(babycell)
                    i.food = 40
                    if (babycell.genotype[3] == 1):
                        self.enw[babpos[0], babpos[1]] = 3
                    else:
                        self.enw[babpos[0], babpos[1]] = 2


    def live(self, foodaray):
        self.predators()
        for i in self.celss:
            i.feed(foodaray)

            i.hungry()

    def mutation(self):
        for z in self.celss:
            r = numpy.random.randint(0, 15501)
            if(r>15499):
                z.genotype = [1,1,0,1]
                poz = z.position
                self.enw[poz[0],poz[1]]=3
                print('Mutation done')

    def predatornumber(self):
        mutanty = 0
        for i in self.celss:
            if i.genotype[3]==1:
                mutanty = mutanty +1
        return mutanty

    def predators(self):
        targetpos = self.enw.copy
        for i in self.celss:
            if i.genotype[3] == 1:
                poz = i.position
                for c in self.celss:
                    if ((abs(c.position[0]-poz[0])< 2) and (abs(c.position[1]-poz[1])<2)):
                        if (c.genotype[3]==0):
                            i.food = i.food + c.food
                            c.food = 0


    def popstatus(self):
        c = 0
        for k in self.celss:
            c = c + 1

        return c

    def popposition(self):
        for g in self.celss:
            g.posprint()

    def arrayofpos(self):
        A = []
        for g in self.celss:
            A = [A, g.position]
        return A

    def popfood(self):
        G = 0
        c = 0
        for g in self.celss:
            f = g.foodlvl()
            G =G + f
            c = c +1
        if(c==0):
            return 0
        return G/c

    def popfoodarray(self):
        A = self.enw.copy()

        for cel in self.celss:
            poz = cel.position
            A[poz[0],[poz[1]]] = cel.food

        return A



class ProtoCell:
    def __init__(self, position):
        self.position = position
        self.food = 40
        self.genotype = [1,1,1,0]

    def feed(self, foodarray):
        if (foodarray[self.position[0], self.position[1]] == 1 and self.genotype[1]==1):
            self.food = self.food + 25

    def hungry(self):
        self.food = self.food - 1

    def foodlvl(self):
        return (self.food)

    def posprint(self):
        print(self.position)


pos = numpy.array([10, 12])
pos2 = numpy.array([5, 8])
protocel = ProtoCell(pos)
protocel2 = ProtoCell(pos2)
pop = Population([protocel, protocel2])

srodowisko = evr()
i = 0
A = [2]
F = []
K = []
Q = []
z=500
while (i < 4000):
    if (divmod(i, 1000) == 0):
        numpy.random.seed(1234)
    Food = foodarray()
    
    pop.live(Food)
    pop.killweak()
    pop.reproduction()
    pop.killmass()
    pop.mutation()

    popul = pop.popstatus()
    if(i==z):
        B = pop.popfoodarray()
        plt.pcolormesh(B)

        plt.show()
        z =z +20
        plt.pcolormesh(pop.enw)
        plt.show()


    i = i + 1
    K.append(pop.predatornumber())
    A.append(popul)
    F.append(pop.popfood())
    Q.append(popul-pop.predatornumber())

A
plt.subplot(3,1,1)

plt.plot(A)
plt.title("Liczebnośc populacji w czasie")
plt.xlabel("Czas")
plt.ylabel("Liczebność populacji")
plt.grid()
plt.subplot(3,1,2)
plt.plot(F)
plt.title("Średnia liczba pożywienia w populacji w czasie")
plt.xlabel("Czas")
plt.ylabel("Liczba pożywienia")
plt.grid()
plt.subplot(3,1,3)
plt.plot(K)
plt.title("Liczba drapieżników w czasie")
plt.xlabel("Czas")
plt.ylabel("Liczba drapieżników")
plt.grid()
plt.show()


plt.subplot(2,1,1)
plt.plot(Q)
plt.title("Liczba ofiar w czasie")
plt.xlabel("Czas")
plt.ylabel("Liczba ofiar")
plt.grid()
plt.subplot(2,1,2)
plt.plot(K)
plt.title("Liczba drapieżników w czasie")
plt.xlabel("Czas")
plt.ylabel("Liczba drapieżników")
plt.grid()
plt.show()