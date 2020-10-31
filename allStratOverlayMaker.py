from common import Agent, Board, display
from strategy4 import strategy4
from strategy3 import strategy3
from strategy2 import strategy2
from strategy1 import strategy1
import numpy as np
import matplotlib.pyplot as plt

def testStrategy():
    mineDensity = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # start value for mineDensity, up to 0.7
    plotDict = {}

    biglist1 = []
    biglist2 = []
    biglist3 = []
    biglist4 = []
    dim = 10 # start value for dim, up to 50 hopefully
    while dim <= 50: #change to 50
        print('dim= ', dim)
        averages = []
        for m in mineDensity:
            successRate = []
            for i in range(30): #change to 30
                gb = Board(dim)
                gb.set_mines((dim**2)*m)
                corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
                ag = Agent(dim=dim, preferredCoords=corners)
                strategy1(gb, dim, ag)
                result = display(dim, ag)
                #print('result:', result)
                successRate.append(result)
            successRate = np.asarray(successRate)
            averages.append(np.average(successRate))
        print(averages)
        biglist1.append(averages)
        dim += 10
    dim = 10
    while dim <= 50: #change to 50
        print('dim= ', dim)
        averages = []
        for m in mineDensity:
            successRate = []
            for i in range(30): #change to 30
                gb = Board(dim)
                gb.set_mines((dim**2)*m)
                corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
                ag = Agent(dim=dim, preferredCoords=corners)
                strategy2(gb, dim, ag)
                result = display(dim, ag)
                #print('result:', result)
                successRate.append(result)
            successRate = np.asarray(successRate)
            averages.append(np.average(successRate))
        print(averages)
        biglist2.append(averages)
        dim += 10
    dim = 10
    while dim <= 50: #change to 50
        print('dim= ', dim)
        averages = []
        for m in mineDensity:
            successRate = []
            for i in range(30): #change to 30
                gb = Board(dim)
                gb.set_mines((dim**2)*m)
                corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
                ag = Agent(dim=dim, preferredCoords=corners)
                strategy3(gb, dim, ag)
                result = display(dim, ag)
                #print('result:', result)
                successRate.append(result)
            successRate = np.asarray(successRate)
            averages.append(np.average(successRate))
        print(averages)
        biglist3.append(averages)
        dim += 10
    dim = 10
    while dim <= 50: #change to 50
        print('dim= ', dim)
        averages = []
        for m in mineDensity:
            successRate = []
            for i in range(30): #change to 30
                gb = Board(dim)
                gb.set_mines((dim**2)*m)
                corners = [(0, 0), (0, dim - 1), (dim - 1, 0), (dim - 1, dim - 1)]
                ag = Agent(dim=dim, preferredCoords=corners)
                strategy4(gb, dim, ag)
                result = display(dim, ag)
                #print('result:', result)
                successRate.append(result)
            successRate = np.asarray(successRate)
            averages.append(np.average(successRate))
        print(averages)
        biglist4.append(averages)
        dim += 10

    plt.figure(figsize=(10,10))
    plt.ylim(0,1)
    plt.plot(mineDensity, biglist1[0], label='Strategy 1')
    plt.plot(mineDensity, biglist2[0], label='Strategy 2')
    plt.plot(mineDensity, biglist3[0], label='Strategy 3')
    plt.plot(mineDensity, biglist4[0], label='Strategy 4')
    plt.legend(loc='best')
    plt.title('Comparison of All Strategies for Dimension {}'.format(10))
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.savefig('AllStrat_Overlaid_Graphs_Dim10.png')

    plt.figure(figsize=(10,10))
    plt.ylim(0,1)
    plt.plot(mineDensity, biglist1[1], label='Strategy 1')
    plt.plot(mineDensity, biglist2[1], label='Strategy 2')
    plt.plot(mineDensity, biglist3[1], label='Strategy 3')
    plt.plot(mineDensity, biglist4[1], label='Strategy 4')
    plt.legend(loc='best')
    plt.title('Comparison of All Strategies for Dimension {}'.format(20))
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.savefig('AllStrat_Overlaid_Graphs_Dim20.png')

    plt.figure(figsize=(10,10))
    plt.ylim(0,1)
    plt.plot(mineDensity, biglist1[2], label='Strategy 1')
    plt.plot(mineDensity, biglist2[2], label='Strategy 2')
    plt.plot(mineDensity, biglist3[2], label='Strategy 3')
    plt.plot(mineDensity, biglist4[2], label='Strategy 4')
    plt.legend(loc='best')
    plt.title('Comparison of All Strategies for Dimension {}'.format(30))
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.savefig('AllStrat_Overlaid_Graphs_Dim30.png')

    plt.figure(figsize=(10,10))
    plt.ylim(0,1)
    plt.plot(mineDensity, biglist1[3], label='Strategy 1')
    plt.plot(mineDensity, biglist2[3], label='Strategy 2')
    plt.plot(mineDensity, biglist3[3], label='Strategy 3')
    plt.plot(mineDensity, biglist4[3], label='Strategy 4')
    plt.legend(loc='best')
    plt.title('Comparison of All Strategies for Dimension {}'.format(40))
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.savefig('AllStrat_Overlaid_Graphs_Dim40.png')

    plt.figure(figsize=(10,10))
    plt.ylim(0,1)
    plt.plot(mineDensity, biglist1[4], label='Strategy 1')
    plt.plot(mineDensity, biglist2[4], label='Strategy 2')
    plt.plot(mineDensity, biglist3[4], label='Strategy 3')
    plt.plot(mineDensity, biglist4[4], label='Strategy 4')
    plt.legend(loc='best')
    plt.title('Comparison of All Strategies for Dimension {}'.format(50))
    plt.xlabel('Mine Density')
    plt.ylabel('Average Final Score')
    plt.savefig('AllStrat_Overlaid_Graphs_Dim50.png')

    # f, ax = plt.subplots(5,1, figsize=(15,15))
    # dim = 10
    # for i in range(0, 5):
    #     ax[i].plot(mineDensity, biglist[i])
    #     ax[i].set_title('Board with Dimension {}'.format(dim))
    #     ax[i].set_xlabel('Mine Density')
    #     ax[i].set_ylabel('Average Final Score')
    #     dim += 10
    # f.savefig('test.png', bbox_inches="tight")
    # f.show()
    #print(biglist)
testStrategy()
    