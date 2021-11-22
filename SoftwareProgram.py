import math
import matplotlib.pyplot as plt

###################################
#PART1

# Defining the calculation of the block probability:

def BlockingProb(lamb=15/60,beta=4,N=5):
    
    numerator = (lamb*beta)**N / math.factorial(N)

    denominator = 1

    for i in range(1,N+1):
        denominator = denominator + (lamb*beta)**i / math.factorial(i)

    BP = numerator/denominator 

    print('The blocking probability of the', N, 'core system, with a rate of', lamb*60, 'jobs per hour and an average job duration of', beta, 'minutes is', round(BP*100, 5), '%')
    return BP 


# Plotting Blocking Probability for increasing number of video cards:

def Plot_Ncards(lamb=15/60, beta=4, N=5, Nmax=10):

    BPlist=[]

    for n in range(1,Nmax+1):
        BP = BlockingProb(lamb,beta,n*N)
        BPlist.append(BP)
    
    plt.plot(range(1,Nmax+1),[element * 100 for element in BPlist])
    plt.ylabel('Blocking Probability (%)')
    plt.xlabel('# of Video Cards')
    plt.title('Blocking Probability for increasing # of Video Cards (5 cores each)')
    plt.show()


# Plotting Blocking Probability for increasing number of individual CPUs:

def Plot_Ncores(lamb=15/60, beta=4, Nmax=10):

    BPlist=[]

    for N in range(1,Nmax+1):
        BP = BlockingProb(lamb,beta,N)
        BPlist.append(BP)
    
    plt.plot(range(1,Nmax+1),[element * 100 for element in BPlist])
    plt.ylabel('Blocking Probability (%)')
    plt.xlabel('# of CPUs')
    plt.title('Blocking Probability for increasing # of CPUs')
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
            #print(f"g({c}) is {g[c]}")

    G = sum(g)
    #print(f"G is {G}")


    q = []
    for c in range(C+1):
        q.append(g[c]/G)
        #print(f"q({c}) is {q[c]}")


    B = [0]*K
    for k in range(K):
        for g in range(K):
            if C-b[k]+g > 4:
                continue 
            B[k] += q[(C-b[k]+g)]
        print(f"B({k}) is {round(B[k]*100,2)}%")

    return g,q,B


lamb = [0.25, 0.007*0.7, 0.002*0.2, 0.001*0.1]
mu = [1/4, 1/20, 1/20, 1/20]
b=[1,3,4,5]
rho = []
for i in range(len(lamb)):
    rho.append(lamb[i]/mu[i])


g,q,B = KaufmanRoberts(5,4,b,rho)

#print(rho,g,q,B)