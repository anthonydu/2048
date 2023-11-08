import torch
import random
import numpy as np
from collections import deque
from ai import GameOf2048AI
from model import Linear_QNet, QTrainer
from plot import plot

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0.1  # randomness
        self.gamma = 0.99  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(256, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game: GameOf2048AI):
        state = []
        for num in game.game.board.flatten():
            state.append(list(map(lambda s: int(s), list(bin(num)[2:].zfill(16)))))
        return np.array(state).flatten()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        self.epsilon *= 99 / 100
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        final_move = [0, 0, 0, 0]
        if random.random() < self.epsilon:
            final_move[random.randrange(4)] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move[torch.argmax(prediction).item()] = 1
        return final_move


def train():
    record = 0
    agent = Agent()
    game = GameOf2048AI()
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset_game()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()

            print("Game", agent.n_games, "Score", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
