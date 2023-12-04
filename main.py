# main.py
from gui import start_gui
from planning_poker import PlanningPoker
import json

def main():
    """
    @file
    @brief main.py

    @mainpage Planning Poker Application
    Application for conducting Planning Poker sessions.

    This script initializes the Planning Poker application, loads tasks from the 'backlog.json' file,
    creates an instance of the PlanningPoker class, and starts the graphical user interface.

    Usage:
    - Ensure 'backlog.json' contains the list of tasks.
    - Choose the rules for the Planning Poker session (e.g., 'moyenne').

    @section dependencies Dependencies:
    - gui.py
    - planning_poker.py
    - json

    @section author Author:
    TOUZAIN Romane
    VACHER Mathais

    @section date Date:
    04/12/2023

    @fn main
    @brief Main function to start the Planning Poker application.

    @details
    - Loads tasks from 'backlog.json'.
    - Initializes the PlanningPoker instance with tasks and rules.
    - Starts the graphical user interface.

    @note
    This script should be executed to run the Planning Poker application.

    @return None
    """
    
    # Charger les tâches depuis le fichier backlog.json
    with open('backlog.json', 'r') as f:
        tasks = json.load(f)['taches']

    # Créer une instance de PlanningPoker avec les tâches et les règles
    rules = "moyenne"  # Vous pouvez choisir les règles ici
    planning_poker = PlanningPoker(tasks, rules)

    # Démarrer l'interface graphique
    start_gui(planning_poker)

if __name__ == "__main__":
    main()

