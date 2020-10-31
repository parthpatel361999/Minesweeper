

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon

from common import Agent, Board


class Visualizer():

    covered_color = '#DDDDDD'
    uncovered_color = '#AAAAAA'
    edge_color = '#888888'
    count_colors = ['grey', 'turquoise', 'blue', 'purple', 'darkblue',
                    'darkred', 'darkgreen', 'maroon', 'black']
    flag_vertices = np.array([[0.25, 0.2], [0.25, 0.8],
                              [0.75, 0.65], [0.25, 0.5]])

    RANDOM_STEP = 'random'
    RANDOM_STEP_COLOR = 'yellow'
    INFERRED_SAFE_STEP = 'inferred_safe'
    INFERRED_SAFE_STEP_COLOR = 'limegreen'
    INFERRED_MINE_STEP = 'inferred_mine'
    INFERRED_MINE_STEP_COLOR = 'lightcoral'
    PROBABILITY_SAFE_STEP = 'probability_safe'
    PROBABILITY_SAFE_STEP_COLOR = 'lime'
    PROBABILITY_MINE_STEP = 'probability_mine'
    PROBABILITY_MINE_STEP_COLOR = 'brown'
    SAFEST_STEP = 'safest'
    SAFEST_STEP_COLOR = 'cyan'

    def __init__(self, agent, strategy):
        self.agent = agent
        self.strategy = strategy
        self.iteration = 0
        self.createVisualization()

    def createVisualization(self):
        figure = plt.figure(
            figsize=((self.agent.dim + 2) / 3., (self.agent.dim + 2) / 3.))
        ax = figure.add_axes((0.05, 0.05, 0.9, 0.9),
                             aspect='equal', frameon=False,
                             xlim=(-0.05, self.agent.dim + 0.05),
                             ylim=(-0.05, self.agent.dim + 0.05))
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_formatter(plt.NullFormatter())
            axis.set_major_locator(plt.NullLocator())
        squares = np.array([[RegularPolygon((i + 0.5, j + 0.5),
                                            numVertices=4,
                                            radius=0.5 * np.sqrt(2),
                                            orientation=np.pi / 4.0,
                                            ec=self.edge_color,
                                            fc=self.covered_color)
                             for j in range(self.agent.dim)]
                            for i in range(self.agent.dim)])
        [ax.add_patch(sq) for sq in squares.flat]

        for r in range(0, self.agent.dim):
            for c in range(0, self.agent.dim):
                _c = abs(c - (self.agent.dim - 1))
                if (r, c) in self.agent.trippedMineCoords:
                    self.drawTrippedMine(ax, squares, r, _c)
                elif (r, c) in self.agent.identifiedMineCoords:
                    self.drawFlaggedMine(ax, r, _c)
                elif (r, c) in self.agent.revealedCoords:
                    self.drawRevealedSafeCell(ax, squares, r, _c,
                                              self.agent.board[r][c].type)

        figure.canvas.draw()
        plt.savefig(
            "strat{0}Vis/{1}b.png".format(self.strategy, self.iteration))
        plt.close(figure)
        self.iteration += 1

    def showNextStep(self, row, col, stepType):
        figure = plt.figure(
            figsize=((self.agent.dim + 2) / 3., (self.agent.dim + 2) / 3.))
        ax = figure.add_axes((0.05, 0.05, 0.9, 0.9),
                             aspect='equal', frameon=False,
                             xlim=(-0.05, self.agent.dim + 0.05),
                             ylim=(-0.05, self.agent.dim + 0.05))
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_formatter(plt.NullFormatter())
            axis.set_major_locator(plt.NullLocator())
        squares = np.array([[RegularPolygon((i + 0.5, j + 0.5),
                                            numVertices=4,
                                            radius=0.5 * np.sqrt(2),
                                            orientation=np.pi / 4.0,
                                            ec=self.edge_color,
                                            fc=self.covered_color)
                             for j in range(self.agent.dim)]
                            for i in range(self.agent.dim)])
        [ax.add_patch(sq) for sq in squares.flat]

        for r in range(0, self.agent.dim):
            for c in range(0, self.agent.dim):
                _c = abs(c - (self.agent.dim - 1))
                if r == row and c == col:
                    self.drawNextStepCell(squares, r, _c, stepType)
                elif (r, c) in self.agent.trippedMineCoords:
                    self.drawTrippedMine(ax, squares, r, _c)
                elif (r, c) in self.agent.identifiedMineCoords:
                    self.drawFlaggedMine(ax, r, _c)
                elif (r, c) in self.agent.revealedCoords:
                    self.drawRevealedSafeCell(ax, squares, r, _c,
                                              self.agent.board[r][c].type)

        figure.canvas.draw()
        plt.savefig(
            "strat{0}Vis/{1}a.png".format(self.strategy, self.iteration))
        plt.close(figure)

    def drawTrippedMine(self, ax, squares, r, c):
        squares[r, c].set_facecolor(self.uncovered_color)
        ax.text(r + 0.5, c + 0.5, 'X', color='r', fontsize=20,
                ha='center', va='center')

    def drawFlaggedMine(self, ax, r, c):
        ax.add_patch(plt.Polygon(self.flag_vertices + [r, c],
                                 fc='red', ec='black', lw=2))

    def drawRevealedSafeCell(self, ax, squares, r, c, clue):
        squares[r, c].set_facecolor(self.uncovered_color)
        ax.text(r + 0.5, c + 0.5, str(clue),
                color=self.count_colors[clue],
                ha='center', va='center', fontsize=18
                )

    def drawNextStepCell(self, squares, r, c, stepType):
        color = self.uncovered_color
        if stepType == self.RANDOM_STEP:
            color = self.RANDOM_STEP_COLOR
        elif stepType == self.INFERRED_SAFE_STEP:
            color = self.INFERRED_SAFE_STEP_COLOR
        elif stepType == self.INFERRED_MINE_STEP:
            color = self.INFERRED_MINE_STEP_COLOR
        elif stepType == self.PROBABILITY_SAFE_STEP:
            color = self.PROBABILITY_SAFE_STEP_COLOR
        elif stepType == self.PROBABILITY_MINE_STEP:
            color = self.PROBABILITY_MINE_STEP_COLOR
        elif stepType == self.SAFEST_STEP:
            color = self.SAFEST_STEP_COLOR
        squares[r, c].set_facecolor(color)
