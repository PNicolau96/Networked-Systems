import math
import matplotlib.pyplot as plt


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


Plot_Ncards()
Plot_Ncores()

#At 7 cores we're at a BP of 0.0073%


