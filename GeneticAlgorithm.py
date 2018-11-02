# -*- coding: UTF-8 -*-

from Level import Player, Button
import random
import copy
import config as cnf

config = cnf.read()


class GenAI(object):

    def __init__(self, map):
        self.map = map
        old_or_new = ((self.old_fitness, Player.PlayerOld),
                      (self.new_fitness, Player.PlayerNew))
        self.fitness, self.PlayerClass, = old_or_new[self.map.new_fitness]
        self.constant_moves = list()
        self.players = list()
        self.generation = 1
        self.done = False
        self.learning_rate = config['learning_rate']
        self.learning_rate_2 = config['learning_rate2']
        self.learning_rate_finished = self.learning_rate * 2
        self.population = config['population']
        self.move_count = config['move_count']
        for count in range(self.population):
            self.players.append(self.PlayerClass(self.map))
        if type(self) == GenAI:
            for player in self.players:
                for count in range(self.move_count):
                    player.moves.append(random.choice((0, 1, 2, 3)))
        self.map.players = self.players
        self.highest_exploration = int
        self.mutation_rate = config['mutation_rate']
        self.mutation_rate = 1 / self.mutation_rate
        self.stop = False
        self.max_moves = 0

    def finished(self):
        Button.restart(self.map)
        self.highest_exploration = 0
        for player in self.players:
            if self.map.new_fitness:
                player_progresses = player.progress
            else:
                player_progresses = player.new_fields
            if player_progresses > self.highest_exploration:
                self.highest_exploration = player_progresses
        highest = 0
        for player in self.players:
            if player.progress > highest:
                highest = player.progress
        for player in self.players:
            player.fitness = self.fitness(player, highest)
        highest = 0
        for player in self.players:
            if player.fitness > highest:
                highest = player.fitness
        highest_players = list()
        for player in self.players:
            if player.fitness == highest:
                highest_players.append(player)
        highest_players.sort(key=lambda x: -x.move_at_last_new)
        if not self.map.new_fitness:
            for player in highest_players:
                player.fitness += 2 * ((highest_players.index(player)+1)/len(highest_players))**self.learning_rate_2
        print(len(highest_players))
        for _ in highest_players[-10:]:
            print(_.fitness, _.move_at_last_new)
        self.evolve()

    def old_fitness(self, player, x):
        fit = 0
        if not player.goal_reached:
            fit += (player.new_fields/self.highest_exploration)**self.learning_rate * 2.5
        else:
            if not self.done:
                self.done = True
                self.max_moves = len(player.moves)
                self.constant_moves = list()
                self.moves_to_make = self.move_count
            fit += 5 + 15 * (1/player.time_in_seconds)
            # TODO: Nicht alle tiles werden erkannt? Oder ist der Weiteste nicht immer der Beste?
            # TODO: Scheint allerdings erst nach einem Neuladen eines Algorithmus der Fall zu sein...
        if player.failed:
            fit *= 0.5
        return fit

    def new_fitness(self, player, highest):
        fit = 0
        if not player.goal_reached:
            fit += (player.progress/highest) ** (self.learning_rate) * 5
        else:
            if not self.done:
                print(player)
                self.done = True
                self.max_moves = len(player.moves)
                print('\nMax moves: %s\n' % self.max_moves)
                self.constant_moves = list()
                self.moves_to_make = self.move_count
                self.success(player.time)
            fit += 10 + 15 * (1 / player.time_in_seconds)
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
        best_player = self.PlayerClass(self.map)
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
        self.generation += 1
        self.players = new_players
        self.map.players = self.players

    def search(self, score):
        for player in self.players:
            if score < player.fitness:
                return player
            else:
                score -= player.fitness

    def breed(self, player_1, player_2, new_genes, rand=False):
        new_player = self.PlayerClass(self.map)
        new_player.moves = copy.copy(self.constant_moves)
        for i in range(new_genes):
            if random.random() > self.mutation_rate and not rand:
                if random.random() > 0.5:
                    new_player.moves.append(player_2.moves[len(self.constant_moves)+i])
                else:
                    new_player.moves.append(player_1.moves[len(self.constant_moves)+i])
            else:
                new_player.moves.append(random.choice((0, 1, 2, 3)))
        return new_player

    def success(self, time):
        self.map.goal_reached = True
        text1 = 'Solved in %d days and ' % time[0]
        text1 += '%d:%d:%d:%d' % (time[1], time[2], time[3], time[4])
        text2 = 'Interrupt trough a restart or continue running to improve results'
        self.map.done_text = (text1, 225, 150)
        self.map.help_text = (text2, 1, 800)
        self.learning_rate = self.learning_rate_finished


class GenAI_2(GenAI):

    def __init__(self, map):

        GenAI.__init__(self, map)
        self.moves_per_change = config['moves_every_change']
        self.moves_to_make = self.moves_per_change
        self.generations_per_change = config['generations_between_changes']
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
        best_player = self.PlayerClass(self.map)
        best_player.visible = True
        best_player.moves = copy.copy(highest_fitness_player.moves)
        if (self.generation % self.generations_per_change) == 0 and not self.done:
            self.constant_moves = highest_fitness_player.moves
            self.move_count += self.moves_per_change
            for i in range(self.moves_per_change):
                best_player.moves.append(random.choice((0, 1, 2, 3)))
            new_chance = True
        new_players.append(copy.copy(best_player))
        all_score = 0
        for player in self.players:
            all_score += player.fitness
        for i in range(self.population - 1):
            a = random.random() * all_score
            b = random.random() * all_score
            player_a = self.search(a)
            player_b = self.search(b)
            new_players.append(self.breed(player_a, player_b, self.moves_to_make, new_chance))
        self.generation += 1
        self.players = new_players
        self.map.players = self.players


class GenAI_3(GenAI):

    def __init__(self, map):
        GenAI.__init__(self, map)
        self.new_constants = config['new_constant_moves']
        self.moves_in_advance = config['moves_in_advance']  # Bewegungen im Voraus die dynamisch sind
        self.move_count = self.moves_in_advance
        self.generations_before_begin = config['generations_before_begin']
        self.generations_per_change = config['generations_between_changes']
        self.new_chance = bool
        for player in self.players:
            for count in range(self.move_count):
                player.moves.append(random.choice((0, 1, 2, 3)))

    def evolve(self):
        self.new_chance = False
        highest_fitness_player = self.players[0]
        for player in self.players:
            if player.fitness >= highest_fitness_player.fitness:
                highest_fitness_player = player
        if self.done:
            print('Goal reached!')
        else:
            if self.map.new_fitness:
                print(str(round(highest_fitness_player.progress*100, 4))+'%')
            else:
                print(highest_fitness_player.visited)
        new_players = list()
        best_player = self.PlayerClass(self.map)
        best_player.visible = True
        best_player.moves = highest_fitness_player.moves
        new_players.append(best_player)
        if not self.done and self.generation >= self.generations_before_begin:
            if ((self.generation-self.generations_before_begin) % self.generations_per_change) == 0:
                self.move_count += self.new_constants
                for ind in range(self.new_constants):
                    best_player.moves.append(random.choice((0, 1, 2, 3)))
                    move = best_player.moves[len(self.constant_moves)]
                    self.constant_moves.append(move)
                self.new_chance = True
        print('%d constant moves' % len(self.constant_moves))
        all_score = 0
        for player in self.players:
            all_score += player.fitness
        for i in range(self.population - 1):
            a = random.random() * all_score
            b = random.random() * all_score
            player_a = self.search(a)
            player_b = self.search(b)
            if not self.done:
                new_player = self.breed(player_a, player_b, self.moves_in_advance, self.new_chance)
            else:
                new_player = self.breed(player_a, player_b, self.max_moves, False)
            if self.new_chance:
                new_player.moves.append(random.choice((0, 1, 2, 3)))
            new_players.append(new_player)
        self.generation += 1
        self.players = new_players
        self.map.players = self.players
