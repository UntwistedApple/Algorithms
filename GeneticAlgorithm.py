# -*- coding: UTF-8 -*-

from Level import Player
import random
from Level import Button
import copy


class GenAI(object):

    def __init__(self, map):
        self.constant_moves = list()
        self.players = list()
        self.generation = 1
        self.map = map
        self.done = False
        self.learning_rate = 8
        self.learning_rate_2 = 2
        self.population = 1000
        self.move_count = 1500
        #self.player_addition = self.move_count
        for count in range(self.population):
            self.players.append(Player.Player(self.map))
        if type(self) == GenAI:
            for player in self.players:
                for count in range(self.move_count):
                    player.moves.append(random.choice((0, 1, 2, 3)))
        self.map.players = self.players
        self.highest_exploration = int
        self.mutation_rate = 3
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
            player.fitness += 2 * ((highest_players.index(player)+1)/len(highest_players))**self.learning_rate_2
        print(len(highest_players))
        for _ in highest_players[-10:]:
            print(_.fitness, _.move_at_last_new)
        self.evolve()

    def fitness(self, player):
        fit = 0
        if not player.goal_reached:
            fit += (player.new_fields/self.highest_exploration)**self.learning_rate * 2.5
        else:
            if not self.done:
                self.done = True
                self.constant_moves = list()
                self.moves_to_make = self.move_count
            fit += 5 + 15 * (1/player.time_in_seconds)
            # TODO: Nicht alle tiles werden erkannt? Oder ist der Weiteste nicht immer der Beste?
            # TODO: Scheint allerdings erst nach einem Neuladen eines Algorithmus der Fall zu sein...
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
        new_player = Player.Player(self.map)
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


class GenAI_2(GenAI):       # TODO: Alle neuen moves ab der ersten Generation scheinen vererbt/kopiert
                            # TODO: wahrscheinlich von dem besten Player zu sein.. (Nur in V3?)
                            # TODO: Die Spieler verhalten sich zu ähnlich bis auf erkennbare Mutationen. --> DONE
                # TODO: SAME ERROR! --> DONE!
    # TODO: Alle tiles (evtl. bis auf den best_player) scheinen bevorzugt nach unten-rechts zu wandern! --> DONE

    def __init__(self, map):

        GenAI.__init__(self, map)
        self.moves_per_change = 100
        self.moves_to_make = self.moves_per_change
        self.generations_per_change = 30
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
        self.new_constants = 15
        self.moves_in_advance = 50  # Bewegungen im Voraus die dynamisch sind
        self.move_count = self.moves_in_advance
        self.generations_before_begin = 10
        self.generations_per_change = 10
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
        print(highest_fitness_player.visited)
        new_players = list()
        best_player = Player.Player(self.map)
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
            new_player = self.breed(player_a, player_b, self.moves_in_advance, self.new_chance)
            if self.new_chance:
                new_player.moves.append(random.choice((0, 1, 2, 3)))
            new_players.append(new_player)
        self.generation += 1
        self.players = new_players
        self.map.players = self.players
        print(self.players[0].moves)
        print(self.constant_moves)
