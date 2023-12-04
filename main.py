# main.py
from gui import start_gui
from planning_poker import PlanningPoker
import json


def main():
    
    """
    @fonction main
    @brief Description of the class.

    Détailler la description
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
