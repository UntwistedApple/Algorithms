# -*- coding: UTF-8 -*-

from Level import Player
import random
from Level import Button


class GenAI(object):

    def __init__(self, map):
        self.generations = dict()
        self.constant_moves = list()
        self.players = list()
        self.generation = 1
        self.map = map
        self.done = False
        self.learning_rate = 7
        self.population = 1000
        self.move_count = 1500
        self.player_addition = self.move_count
        for count in range(self.population):
            self.players.append(Player.Player(self.map))
        if type(self) == GenAI:
            for player in self.players:
                for count in range(self.move_count):
                    player.moves.append(random.choice((0, 1, 2, 3)))
        self.map.players = self.players
        self.highest_exploration = int
        self.mutation_rate = 6
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
            player.fitness += 2 * ((highest_players.index(player)+1)/len(highest_players))**5
        print(len(highest_players))
        for _ in highest_players[-10:]:
            print(_.fitness, _.move_at_last_new)
        self.evolve()

    def fitness(self, player):
        fit = 0
        if not player.goal_reached:
            fit += (player.new_fields/self.highest_exploration)**self.learning_rate * 2.5
            #fit *= 1 + 100/player.move_at_last_new
        else:
            if not self.done:
                self.done = True
                self.constant_moves = list()
                self.moves_to_make = self.move_count
            fit += 5 + 15 * (1/player.time_in_seconds)
        if player.failed:
            fit *= 0.5
        return fit

    def evolve(self):
        highest_fitness_player = self.players[0]
        for player in self.players:
            if player.fitness >= highest_fitness_player.fitness:
                highest_fitness_player = player
        print(highest_fitness_player.visited)
        new_players = list()
        best_player = Player.Player(self.map)
        best_player.visible = True
        best_player.moves = highest_fitness_player.moves
        new_players.append(best_player)
        all_score = 0
        for player in self.players:
            all_score += player.fitness
        for i in range(self.population - 1):
            a = random.random() * all_score
            b = random.random() * all_score
            player_a = self.search(a)
            player_b = self.search(b)
            new_players.append(self.breed(player_a, player_b, self.move_count))
        self.generations[str(self.generation)] = self.players
        self.generation += 1
        self.players = new_players
        self.map.players = self.players

    def add(self, new_players):
        pass

    def search(self, score):
        for player in self.players:
            if score < player.fitness:
                return player
            else:
                score -= player.fitness

    def breed(self, player_1, player_2, new_genes, rand=False):
        new_player = Player.Player(self.map)
        new_player.moves = list()
        for move in self.constant_moves:
            new_player.moves.append(move)
        for i in range(new_genes):
            if random.random() > self.mutation_rate and not rand:
                if random.random() < 1/(1+player_1.fitness/player_2.fitness):
                    new_player.moves.append(player_2.moves[i])
                else:
                    new_player.moves.append(player_1.moves[i])
            else:
                new_player.moves.append(random.choice((0, 1, 2, 3)))
        return new_player


class GenAI_2(GenAI):

    def __init__(self, map):

        GenAI.__init__(self, map)
        self.moves_per_change = 50
        self.moves_to_make = self.moves_per_change
        self.player_addition = self.moves_per_change
        self.generations_per_change = 70
        self.move_count = self.moves_per_change
        for player in self.players:
            player.moves = list()
            for count in range(self.move_count):
                player.moves.append(random.choice((0, 1, 2, 3)))

    def evolve(self):
        new_chance = False
        for player in self.players:
            if not player.failed:
                highest_fitness_player = player
                break
        for player in self.players:
            if player.fitness >= highest_fitness_player.fitness:
                highest_fitness_player = player
        print(str(highest_fitness_player.visited)+'\n')
        new_players = list()
        best_player = Player.Player(self.map)
        best_player.visible = True
        for move in highest_fitness_player.moves:
            best_player.moves.append(move)
        if (self.generation % self.generations_per_change) == 0 and not self.done:
            self.constant_moves = highest_fitness_player.moves
            self.move_count += self.moves_per_change
            for i in range(self.moves_per_change):
                best_player.moves.append(random.choice((0, 1, 2, 3)))
            new_chance = True
        new_players.append(best_player)
        all_score = 0
        for player in self.players:
            all_score += player.fitness
        for i in range(self.population - 1):
            a = random.random() * all_score
            b = random.random() * all_score
            player_a = self.search(a)
            player_b = self.search(b)
            new_players.append(self.breed(player_a, player_b, self.moves_to_make, new_chance))
        self.generations[str(self.generation)] = self.players
        self.generation += 1
        self.players = new_players
        self.map.players = self.players


class GenAI_3(GenAI):

    def __init__(self, map):
        GenAI.__init__(self, map)
        self.moves_per_change = 100
        self.move_count = self.moves_per_change
        self.generations_per_change = 30

    def add(self, new_players):
        self.move_count += self.moves_per_change
        for player in new_players:
            for move in range(self.moves_per_change):
                player.moves.append(random.choice((0, 1, 2, 3)))
