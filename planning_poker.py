
# planning_poker.py
import json
from rules import Rules

class PlanningPoker:
    """
    @class PlanningPoker
    @brief Main class for the Planning Poker application.

    @details
    Manages the Planning Poker session, including loading tasks, recording votes, calculating difficulty,
    and keeping track of evaluated tasks.

    @note
    This class relies on the Rules class for calculating difficulty based on votes.

    @section author Author:
    Your Name

    @section license License:
    Specify the license information.

    @section version Version:
    Specify the version of the class.

    @section date Date:
    Specify the creation or last modification date.
    """

    def __init__(self, tasks, rules):
        """
        @fn __init__
        @brief Constructor for PlanningPoker.

        @param tasks List of tasks for the Planning Poker session.
        @param rules An instance of the Rules class defining the voting rules.
        """
        self.tasks = tasks
        self.rules = rules
        self.players = []
        self.votes = {}
        self.current_task = None
        self.current_task_index = 0  # Nouvelle variable pour suivre l'indice de la tâche actuelle
        self.evaluated_tasks = []  # Nouvelle liste pour stocker les tâches évaluées

    def record_vote(self, player, value):
        """
        @fn record_vote
        @brief Record a vote for a player.

        @param player The name of the player.
        @param value The value of the vote.
        """
        if self.current_task:
            if player not in self.votes:
                self.votes[player] = value
            else:
                self.votes[player] = value

    def load_backlog(self, filename):
        """
        @fn load_backlog
        @brief Load tasks from a JSON file.

        @param filename The name of the JSON file containing tasks.
        """
        with open(filename, 'r') as file:
            self.tasks = json.load(file)['taches']  # Renommez de backlog à tasks

    def save_backlog(self, filename):
        """
        @fn save_backlog
        @brief Save tasks to a JSON file.

        @param filename The name of the JSON file to save tasks.
        """
        with open(filename, 'w') as file:
            json.dump({"taches": self.tasks}, file, indent=2)  # Renommez de backlog à tasks

    def get_next_task(self):
        """
        @fn get_next_task
        @brief Get the next task from the task list.

        @return The next task or None if there are no more tasks.
        """
        if not self.tasks:
            return None
        return self.tasks.pop(0)

    def get_available_cards(self):
        """
        @fn get_available_cards
        @brief Get a list of available voting cards.

        @return List of available voting cards.
        """
        return [0, 1, 2, 3, 5, 8, 13, 20, 40, 100]

    def reset_votes(self):
        """
        @fn reset_votes
        @brief Reset all recorded votes.
        """
        self.votes = {}

    def get_votes(self):
        """
        @fn get_votes
        @brief Get a list of recorded votes.

        @return List of recorded votes.
        """
        return list(self.votes.values())

    def is_voting_complete(self):
        """
        @fn is_voting_complete
        @brief Check if the voting is complete for all players.

        @return True if the voting is complete, False otherwise.
        """
        return len(self.votes) == len(self.players)

    def complete_current_task(self):
        """
        @fn complete_current_task
        @brief Complete the current task and update evaluated tasks.

        @details
        - Calculates the difficulty based on votes using rules.
        - Updates the current task with the calculated difficulty.
        - Saves the updated task list to a file.
        - Resets votes and adds the evaluated task to the list.
        - Moves to the next task.
        """
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
        """
        @fn get_next_player
        @brief Get the name of the next player in the voting sequence.

        @return The name of the next player or None if there are no more players.
        """
        if not self.players:
            return None
        current_index = self.players.index(list(self.votes.keys())[-1]) if self.votes else -1
        next_index = (current_index + 1) % len(self.players)
        return self.players[next_index]