import numpy as np
from tqdm import tqdm
import time
import random
import sys

LENGTH = 3


class Environment:
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))  # 0 showing an empty board
        self.X = -1  # number sign for X player
        self.O = 1  # number sign for O player
        self.winner = None  # variable to keep track of if there is a winner
        self.ended = False  # variable to track if the game is over or not
        self.total_states = 3 ** (LENGTH * LENGTH)  # total number of possible states in the game

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, symbol):
        if not self.game_over():
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
                elif self.board[i, j] == self.O:
                    v = 2
                h += v*(3 ** k)
                k += 1
        return h

    def game_over(self, force_recalculate=False):
        """
        Check for winner:
            along row
            along column
            along diagonals
        check if draw
        else return false
        """
        if not force_recalculate and self.ended:
            return self.ended

        # checking across rows
        for i in range(LENGTH):
            for player in (self.X, self.O):
                if self.board[i].sum() == player * LENGTH:
                    self.ended = True
                    self.winner = player
                    return True

        # checking across columns
        for j in range(LENGTH):
            for player in (self.X, self.O):
                if self.board[:, j].sum() == player * LENGTH:
                    self.ended = True
                    self.winner = player
                    return True

        # checking along both diagonals
        for player in (self.X, self.O):
            # principal diagonal
            if self.board.trace() == player * LENGTH:
                self.winner = player
                self.ended = True
                return True

            # secondary diagonal
            if np.fliplr(self.board).trace() == player * LENGTH:
                self.winner = player
                self.ended = True
                return True

        # check for draw condition
        if np.all((self.board == 0) == False):  # There are still cells to fill
            self.winner = None
            self.ended = True
            return True

        # else return false
        self.winner = None  # reset for multiple calls of function
        return False

    def draw_board(self):
        """
        Member function to draw the board to play
        """
        print("-------------")
        for i in range(LENGTH):
            print("|", end='')
            for j in range(LENGTH):
                if self.board[i, j] == self.X:
                    print(' X |', end='')
                elif self.board[i, j] == self.O:
                    print(' O |', end='')
                else:
                    print('   |', end='')
            print("")
        print("-------------")


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
            pos2value = {} # To store all the position to value dict for verbose
            best_value = -99
            next_move = None
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        env.board[i, j] = self.symbol
                        state = env.get_state()
                        env.board[i, j] = 0  # changing it back
                        pos2value[(i, j)] = self.V[state]
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i, j)

            if self.verbose:
                print("Taking a greedy action")

                # printing value of the position wherever empty
                print("-------------")
                for i in range(LENGTH):
                    print("|", end='')
                    for j in range(LENGTH):
                        if env.board[i, j] == env.X:
                            print(' X |', end='')
                        elif env.board[i, j] == env.O:
                            print(' O |', end='')
                        else:
                            num = round(pos2value[(i, j)], 2)
                            print('.%d|' % (num*1e2), end='')
                    print("")
                print("-------------")

        # making the move
        env.board[next_move[0], next_move[1]] = self.symbol

    def update_state_history(self, state):
        """
        Updating state history for a given episode
        :param state: state value
        """
        self.state_history.append(state)

    def update(self, env):
        """
        Queries the environment for the latest reward. Learning epicentre
        """
        reward = env.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target - self.V[prev])
            self.V[prev] = value  # This value estimate converges to it's 'actual value' in the episode
            target = value
        self.reset_history()


class Hooman:
    def __init__(self):
        pass

    def set_symbol(self, symbol):
        self.symbol = symbol

    def take_action(self, env):
        while True:
            move = input("Enter the position as i,j you want to place your move (i,j ∈ {0,1,2): ")
            # break if we make a valid move
            i, j = move.split(',')
            i = int(i.strip())
            j = int(j.strip())
            if env.is_empty(i,j):
                env.board[i,j] = self.symbol
                break
            else:
                print("Invalid move! Try again...")

    def update_state_history(self, state):
        pass

    def update(self, env):
        pass


def play_game(p1, p2, env, draw=0):
    """
    Main function that is called to play the game
    :param p1: player 1 object
    :param p2: player 2 object
    :param env: Environment object
    :param draw: draw the board for which player (1 or 2)
    """
    # iterates until the game is over
    current_player = None
    while not env.game_over():
        # alternate chances in between players p1 starts first
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        # draw before the hooman makes a move.
        if draw:
            if draw == 1 and current_player == p1:
                env.draw_board()
            if draw == 2 and current_player == p2:
                env.draw_board()

        # The current player makes a move
        current_player.take_action(env)

        # updating state histories
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    # Draws the board at the end of the game
    if draw:
        env.draw_board()
        if draw == 2:
            if env.winner == env.X:
                print("KitKat won! Better luck next time :P")
            else:
                print("Congrats! You won!!")
        else:
            if env.winner == env.O:
                print("KitKat won! Better luck next time :P")
            else:
                print("Congrats! You won!!")

    # doing value function updates
    p1.update(env)
    p2.update(env)


def get_state_hash_winner(env, i=0, j=0):
    """
    Returns the tuple for (state_hash, ended, winner)
    """
    results = []

    for v in (0, env.X, env.O):
        env.board[i, j] = v
        if j == LENGTH-1:
            if i == LENGTH-1:
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                results.append((state, ended, winner))
            else:
                results += get_state_hash_winner(env, i+1, 0)  # next row first column
        else:
            results += get_state_hash_winner(env, i, j+1)  # next column same row

    return results


def initialize_vx(env, state_winner_tuples):
    V = np.zeros(env.total_states)
    for state, ended, winner in state_winner_tuples:
        if ended:
            if winner == env.X:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V


def initialize_vo(env, state_winner_tuples):
    V = np.zeros(env.total_states)
    for state, ended, winner in state_winner_tuples:
        if ended:
            if winner == env.O:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


if __name__ == '__main__':
    # training agents by creating two Agent object (AIs)
    p1 = Agent()
    p2 = Agent()

    # set value functions for both the agents
    env = Environment()
    state_winner_tuples = get_state_hash_winner(env, 0, 0)

    # initializing value functions
    VX = initialize_vx(env, state_winner_tuples)
    p1.setV(VX)
    VO = initialize_vo(env, state_winner_tuples)
    p2.setV(VO)

    # Assigning symbols to each player
    p1.set_symbol(env.X)
    p2.set_symbol(env.O)

    # TRAINING
    print("Training KitKat.....")
    T = 1000 # Play T games to train
    for t in tqdm(range(T)):
        play_game(p1, p2, Environment()) # Creating new environment for every episode

    hooman = Hooman()

    # Toss to decide who should go first
    print("Tossing ", end='')

    spinner = spinning_cursor()
    for _ in range(30):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')

    print("")
    toss = random.choice(["KitKat", "Player"])

    if toss == "Player":
        print("You won the toss. You go first.")
        hooman.set_symbol(env.X)
        while True:
            p2.set_verbose(True)
            play_game(hooman, p2, Environment(), draw=1)

            ans = input("Play again? [Y/N]: ")
            if ans and ans.lower() == 'n':
                break
    else:
        print("KitKat won the toss. Dare you to win ( •̀ᴗ•́ )و ̑̑.")
        hooman.set_symbol(env.O)
        while True:
            p1.set_verbose(True)
            play_game(p1, hooman, Environment(), draw=2)

            ans = input("Play again? [Y/N]: ")
            if ans and ans.lower() == 'n':
                break
