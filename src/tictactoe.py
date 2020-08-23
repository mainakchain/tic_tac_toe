import numpy as np

LENGTH = 3


class Environment:
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))  # 0 showing an empty board
        self.X = -1  # number sign for X player
        self.O = 1  # number sign for O player
        self.winner = None  # variable to keep track of if there is a winner
        self.game_over = False  # variable to track if the game is over or not
        self.total_states = 3 ** (LENGTH * LENGTH)  # total number of possible states in the game

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, symbol):
        if self.game_over:
            return 0

        return 1 if self.winner == symbol else 0  # symbol is self.X or self.O

    def get_state(self):
        """
        Return the hash int for the board state
        Hash int is generated as Ternary number system (using 0,1,2)
        """
        k = 0  # Number representing the cell
        h = 0  # Hash Number
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j] == 0:
                    v = 0
                elif self.board[i, j] == self.X:
                    v = 1
                else:
                    v = 2
                h += v * (3 ** k)
                k + +
        return h

    def game_over(self):
        """
        Check for winner:
            along row
            along column
            along diagonals
        check if draw
        else return false
        """
        # checking across rows
        for i in range(LENGTH):
            for player in (self.X, self.O):
                if self.board[i].sum() == player * LENGTH:
                    self.game_over = True
                    self.winner = player
                    return True

        # checking across columns
        for j in range(LENGTH):
            for player in (self.X, self.O):
                if self.board[j].sum() == player * LENGTH:
                    self.game_over = True
                    self.winner = player
                    return True

        # checking along both diagonals
        for player in (self.X, self.O):
            # principal diagonal
            if self.board.trace() == player * LENGTH:
                self.winner = player
                self.game_over = True
                return True

            # secondary diagonal
            if np.fliplr(self.board).trace() == player * LENGTH:
                self.winner = player
                self.game_over = True
                return True

        # check for draw
        if np.all((self.board == 0) == False):  # There are still cells to fill
            self.winner = None
            self.game_over = True
            return False

        # else return false
        self.winner = None  # reset for multiple calls of function
        return False

    def draw_board(self):
        """
        Member function to draw the board to play
        """
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j] == self.X:
                    print('X')
                elif self.board[i, j] == self.O:
                    print('O')
                else:
                    print('_')
                print(" ")
            print("\n")
        print("--------")


class Agent:
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps  # the threshold to guide explore exploit decision
        self.alpha = alpha  # learning rate
        self.verbose = False  # True to show agent's decision making process
        self.state_history = []  # To keep track of state history for an episode

    def setV(self, V):
        """
        To set the value function for the agent
        :param V: Value function
        """
        self.V = V

    def set_symbol(self, symbol):
        """
        To give the agent a symbol to play
        :param symbol: self.X or self.O
        """
        self.symbol = symbol

    def set_verbose(self, v):
        """
        prints more info if b is true
        :param b: True or false for verbosity
        """
        self.verbose = v

    def reset_history(self):
        """
        To reset the history when episode is finished
        """
        self.state_history = []

    def take_action(self, env):
        """
        The agent to take action given the current environment
        Action is taken as per epsilon greedy method
        :param env: Environment class object
        :return:
        """
        r = np.random.rand()
        best_state = None
        if r <= self.eps:
            # explore by taking a random action
            if self.verbose:
                print("Taking a random action...")

            possible_moves = []
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        possible_moves.append((i, j))
            # select a random possible move
            id = np.random.choice(len(possible_moves))
            next_move = possible_moves[id]
        else:
            # exploit by selecting the best action
            pos2value = {}
            next_move = None
            best_value = -1
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        env.board[i.j] = self.symbol
                        state = env.get_state()
                        env.board[i, j] = 0  # changing it back
                        pos2value[(i, j)] =
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i, j)

            if

    def update_state_history(self, state):
        """
        Updating state history for a given episode
        :param state:
        :return:
        """

    def update(self, env):
        """
        Queries the environment for the latest reward. Learning epicentre
        :return:
        """
