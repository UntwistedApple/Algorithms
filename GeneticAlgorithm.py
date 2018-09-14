# -*- coding: UTF-8 -*-

from Level import Player
import random
from Level import Button


class GenAI(object):

    def __init__(self, map):
        self.generations = dict()
        self.players = list()
        self.generation = 1
        self.map = map
        self.learning_rate = 5
        self.population = 1000
        self.move_count = 1500
        for count in range(self.population):
            self.players.append(Player.Player(self.map))
        for player in self.players:
            for count in range(self.move_count):
                player.moves.append(random.choice((0, 1, 2, 3)))
        self.map.players = self.players
        self.highest_exploration = int
        self.mutation_rate = 5
        self.mutation_rate = 1 / self.mutation_rate

    def finished(self):
        Button.restart(self.map)
        self.highest_exploration = 0
        for player in self.players:
            if player.new_fields > self.highest_exploration:
                self.highest_exploration = player.new_fields
        for player in self.players:
            player.fitness = self.fitness(player)
        highest = 0
        for player in self.players:
            if player.fitness > highest:
                highest = player.fitness
        highest_players = list()
        for player in self.players:
            if player.fitness == highest:
                highest_players.append(player)
        highest_players.sort(key=lambda x: -x.move_at_last_new)
        for player in highest_players:
            player.fitness += 1 * ((highest_players.index(player)+1)/len(highest_players))
        print(len(highest_players))
        for _ in highest_players:
            print(_.fitness, _.move_at_last_new)
        self.evolve()

    def fitness(self, player):
        fit = 0
        if not player.goal_reached:
            fit += (player.new_fields/self.highest_exploration)**self.learning_rate * 1.5
            #fit *= 1 + 100/player.move_at_last_new
        else:
            fit += 4 + 15 * (1/player.time_in_seconds)
        return fit

    def evolve(self):
        new_players = list()
        highest_fitness = self.players[0]
        for player in self.players:
            if player.fitness >= highest_fitness.fitness:
                highest_fitness = player
        best_player = Player.Player(self.map)
        best_player.visible = True
        print(highest_fitness.visited)
        best_player.moves = highest_fitness.moves
        new_players.append(best_player)
        all_score = 0
        for player in self.players:
            all_score += player.fitness
        for i in range(self.population - 1):
            a = random.random() * all_score
            b = random.random() * all_score
            player_a = self.search(a)
            player_b = self.search(b)
            new_players.append(self.breed(player_a, player_b))
        self.generations[str(self.generation)] = self.players
        self.generation += 1
        self.players = new_players
        self.map.players = self.players

    def search(self, score):
        for player in self.players:
            if score < player.fitness:
                return player
            else:
                score -= player.fitness

    def breed(self, player_1, player_2):
        new_player = Player.Player(self.map)
        for i in range(self.move_count):
            if random.random() > self.mutation_rate:
                new_player.moves.append(random.choice((player_1.moves[i], player_2.moves[i])))
            else:
                new_player.moves.append(random.choice((0, 1, 2, 3)))
        return new_player

