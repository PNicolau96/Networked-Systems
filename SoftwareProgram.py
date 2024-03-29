import math
import matplotlib.pyplot as plt
import sys
import timeit

start = timeit.timeit()
print("hello")


###################################
#PART1

# Defining the calculation of the block probability:

def BlockingProb(lamb=15/60,beta=4,N=5):
    
    numerator = (lamb*beta)**N / math.factorial(N)

    denominator = 1

    for i in range(1,N+1):
        denominator = denominator + (lamb*beta)**i / math.factorial(i)

    BP = numerator/denominator 

    return BP 


# Plotting Blocking Probability for increasing number of video cards:

def Plot_Ncards(lamb=15/60, beta=4, N=5, Nmax=5):

    BPlist=[]

    for n in range(1,Nmax+1):
        BP = BlockingProb(lamb,beta,n*N)
        BPlist.append(BP)
    print([element * 100 for element in BPlist])
    plt.plot(range(1,Nmax+1),[element * 100 for element in BPlist])
    plt.ylabel('Blocking Probability (%)')
    plt.xlabel('# of Video Cards')
    plt.title('Blocking Probability for increasing # of Video Cards (5 cores each)')
    plt.grid(which='major', axis='both')
    plt.xticks(range(1, 6))
    plt.show()


# Plotting Blocking Probability for increasing number of individual CPUs:

def Plot_Ncores(lamb=15/60, beta=4, Nmax=8):

    BPlist=[]

    for N in range(1,Nmax+1):
        BP = BlockingProb(lamb,beta,N)
        BPlist.append(BP)
    
    print([element * 100 for element in BPlist])
    plt.plot(range(1,Nmax+1),[element * 100 for element in BPlist])
    plt.ylabel('Blocking Probability (%)')
    plt.xlabel('# of CPUs')
    plt.title('Blocking Probability for increasing # of CPUs')
    plt.grid(which='major', axis='both')
    plt.show()


#Plot_Ncards()
#Plot_Ncores()
#BlockingProb()

#At 7 cores we're at a BP of 0.0073%

###################################
#PART2


    
def KaufmanRoberts(C,K,b,rho):
    '''
    C : number of available channels
    K : number of job types
    b : list of required capacities for each k
    rho : list of loads for each k
    '''
    g = [0]*(C+1) #List of each g(c)
    
    for c in range(C+1):

        if c==0:
            g[c]=1
            print(f"g({c}) is {g[c]}")

        else:

            for k in range(K):

                if c-b[k]==0:
                    d = 1
                elif c-b[k]<-1:
                    d = 0
                else:
                    d = g[c-b[k]]
            
                g[c] += b[k]*rho[k]*d
            g[c] = (1/c)*g[c]
            print(f"g({c}) is {g[c]}")

    G = sum(g)
    print(f"G is {G}")


    q = []
    for c in range(C+1):
        q.append(g[c]/G)
        print(f"q({c}) is {q[c]}")

    B = [0]*K
    for k in range(K):
        c = C - b[k] + 1
        for i in range(c, C+1):
            B[k] += q[i]
        print(f"B({k}) is {round(B[k]*100,2)}%")

    return g,q,B


lamb = [0.25, 0.007, 0.002, 0.001]
mu = [1/4, 1/20, 1/20, 1/20]
b=[1,3,4,5]
rho = []
for i in range(len(lamb)):
    rho.append(lamb[i]/mu[i])


#g,q,B = KaufmanRoberts(5,4,b,rho)


###################################
#PART3

#file_path = 'out.txt'
#sys.stdout = open(file_path, "w") #for printing to a .txt file

lambs = [1,3,7,11,16]
betas = [1.5]*5
Cells=5
Channels=60
OverallBPlist = []
BPperBestCell = []
ChannelDistribution = []
CombinationTracker = []

cond1 = 1/38
cond2 = 3/38
cond3 = 7/38
cond4 = 11/38
cond5 = 16/38

def CellsNetwork():

    lambs = [1,3,7,11,16]

    OverallBPlist = []
    BPperBestCell = []
    ChannelDistribution = []
    CombinationTracker = []

    cond1 = 1/38
    cond2 = 3/38
    cond3 = 7/38
    cond4 = 11/38
    cond5 = 16/38

    breakout=False

    for Channels in range(60,151):
        # Mobile Voice Networks Cells
        for CellChansOne in range(1,Channels+1):
            if breakout:
                break
            channels_one = CellChansOne #number of channels in cell 1
            for CellChansTwo in range(1,(Channels+1)-channels_one):
                if breakout:
                    break
                channels_two = CellChansTwo #number of channels in cell 2
                for CellChansThree in range(1,(Channels+1)-channels_one-channels_two):
                    if breakout:
                        break
                    channels_three = CellChansThree # number of channels in cell 3
                    for CellChansFour in range(1,(Channels+1)-channels_one-channels_two-channels_three):
                        channels_four = CellChansFour # number of channels in cell 4
                        channels_five = Channels - channels_one - channels_two - channels_three - channels_four
                        if channels_five ==0:
                            continue

                        ChannelDistribution.append([channels_one,channels_two,channels_three,channels_four,channels_five])

                        #combination 1
                        BPAone = cond1*BlockingProb(lambs[0],1.5,channels_one+channels_four+channels_five)
                        BPAtwo = cond2*BlockingProb(lambs[1],1.5,channels_two)
                        BPAthree = cond3*BlockingProb(lambs[2],1.5,channels_three)
                        BPAfour = cond4*BlockingProb(lambs[3],1.5,channels_four+channels_one)
                        BPAfive = cond5*BlockingProb(lambs[4],1.5,channels_five+channels_two)
                        BPA = 1-((1-BPAone)*(1-BPAtwo)*(1-BPAthree)*(1-BPAfour)*(1-BPAfive))
                        #combination 2
                        BPBone = cond1*BlockingProb(lambs[0],1.5,channels_one+channels_four)
                        BPBtwo = cond2*BlockingProb(lambs[1],1.5,channels_two+channels_five)
                        BPBthree = BPAthree
                        BPBfour = BPAfour
                        BPBfive = BPAfive
                        BPB = 1-((1-BPBone)*(1-BPBtwo)*(1-BPBthree)*(1-BPBfour)*(1-BPBfive))
                        #combination 3
                        BPCone = BPBone
                        BPCtwo = BPBtwo
                        BPCthree = BPAthree
                        BPCfour = cond4*BlockingProb(lambs[3],1.5,channels_four)
                        BPCfive = cond5*BlockingProb(lambs[4],1.5,channels_five+channels_one+channels_two)
                        BPC = 1-((1-BPCone)*(1-BPCtwo)*(1-BPCthree)*(1-BPCfour)*(1-BPCfive))
                        #combination 4
                        BPDone = BPAone
                        BPDtwo = BPAtwo
                        BPDthree = BPAthree
                        BPDfour = BPCfour
                        BPDfive = BPCfive
                        BPD = 1-((1-BPDone)*(1-BPDtwo)*(1-BPDthree)*(1-BPDfour)*(1-BPDfive))

                        BestCombination = min(BPA,BPB,BPC,BPD) #Find which of the combinations yield the lowest overall blocking probability
                        OverallBPlist.append(BestCombination)

                        #Save the blocking probabilities of the best overall combination and that of each of its cells
                        if BPA==BestCombination:
                            CombinationTracker.append(1)
                            BPperBestCell.append([BPAone,BPAtwo,BPAthree,BPAfour,BPAfive])
                        elif BPB==BestCombination:
                            CombinationTracker.append(2)
                            BPperBestCell.append([BPBone,BPBtwo,BPBthree,BPBfour,BPBfive])
                        elif BPC==BestCombination:
                            CombinationTracker.append(3)
                            BPperBestCell.append([BPCone,BPCtwo,BPCthree,BPCfour,BPCfive])
                        elif BPD==BestCombination:
                            CombinationTracker.append(4)
                            BPperBestCell.append([BPDone,BPDtwo,BPDthree,BPDfour,BPDfive])

                        if BestCombination<0.025:
                            breakout = True
                            break

        min_overallBP = min(OverallBPlist)
        BPindex = OverallBPlist.index(min_overallBP)

        Solution = [min_overallBP,ChannelDistribution[BPindex],CombinationTracker[BPindex],BPperBestCell[BPindex]]
        print(Solution)

        end = timeit.timeit()
        print(end - start)

CellsNetwork()

#print(len(OverallBPlist),len(ChannelDistribution),len(CombinationTracker),len(BPperBestCell))