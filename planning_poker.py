
# planning_poker.py
import json
from rules import Rules

class PlanningPoker:
    def __init__(self, tasks, rules):
        self.tasks = tasks
        self.rules = rules
        self.players = []
        self.votes = {}
        self.current_task = None
        self.current_task_index = 0  # Nouvelle variable pour suivre l'indice de la tâche actuelle
        self.evaluated_tasks = []  # Nouvelle liste pour stocker les tâches évaluées

    def record_vote(self, player, value):
        if self.current_task:
            if player not in self.votes:
                self.votes[player] = value
            else:
                self.votes[player] = value

    def load_backlog(self, filename):
        with open(filename, 'r') as file:
            self.tasks = json.load(file)['taches']  # Renommez de backlog à tasks

    def save_backlog(self, filename):
        with open(filename, 'w') as file:
            json.dump({"taches": self.tasks}, file, indent=2)  # Renommez de backlog à tasks

    def get_next_task(self):
        if not self.tasks:
            return None
        return self.tasks.pop(0)

    def get_available_cards(self):
        return [0, 1, 2, 3, 5, 8, 13, 20, 40, 100]

    def reset_votes(self):
        self.votes = {}

    def get_votes(self):
        return list(self.votes.values())

    def is_voting_complete(self):
        return len(self.votes) == len(self.players)

    def complete_current_task(self):
        if self.current_task:
            votes = self.get_votes()
            difficulty = self.rules.calculate_difficulty(votes)
            self.current_task['difficulte'] = difficulty
            self.save_backlog("backlog_state.json")
            self.reset_votes()
            self.evaluated_tasks.append(self.current_task)  # Ajoutez la tâche évaluée à la liste
            self.current_task_index += 1  # Passer à la tâche suivante
            self.current_task = self.get_next_task()



    def get_next_player(self):
        if not self.players:
            return None
        current_index = self.players.index(list(self.votes.keys())[-1]) if self.votes else -1
        next_index = (current_index + 1) % len(self.players)
        return self.players[next_index]