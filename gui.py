# gui.py (mise à jour)
import tkinter as tk
from tkinter import simpledialog, messagebox
from rules import Rules
import json

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, options):
        self.options = options
        self.result = None
        self.prompt = prompt  # Ajout de la variable prompt
        super().__init__(parent, title=title)

    def body(self, parent):
        self.geometry("300x100")
        self.title(self.title)
        tk.Label(parent, text=self.prompt, anchor="w").pack(side="top", fill="x")  # Utilisation de self.prompt
        self.entry = tk.Entry(parent)
        self.entry.pack(side="top", fill="x")
        return self.entry

    def apply(self):
        self.result = self.entry.get()

def start_gui(planning_poker):
    root = tk.Tk()
    root.title("Planning Poker")

    def get_num_players():
        return simpledialog.askinteger("Nombre de joueurs", "Entrez le nombre de joueurs :", minvalue=1)

    def get_player_names(num_players):
        names = []
        for i in range(num_players):
            name = simpledialog.askstring("Nom du joueur", f"Nom du joueur {i + 1} :")
            names.append(name)
        return names

    def get_rules():
        rules_options = ["strict", "moyenne", "médiane", "majorité"]
        rules = CustomDialog(root, "Règles", "Choisissez les règles (strict, moyenne, médiane, majorité) :", rules_options).result
        return rules

    num_players = get_num_players()
    player_names = get_player_names(num_players)

    planning_poker.players = player_names
    rules = Rules(get_rules())
    planning_poker.rules = rules
    planning_poker.current_task = planning_poker.get_next_task()

    task_label = tk.Label(root, text="")
    task_label.pack()

    player_name_label = tk.Label(root, text="")
    player_name_label.pack()

    next_task_button_text = tk.StringVar()
    next_task_button_text.set("Récapitulatif")  

    def on_card_selected(value, player):
        planning_poker.record_vote(player, value)
        show_player_name(planning_poker.get_next_player())
        if planning_poker.is_voting_complete():
            validate_and_next_task()

    def validate_and_next_task():
        if planning_poker.rules.validate_vote(planning_poker.get_votes()):
            planning_poker.complete_current_task()
            show_current_task()
            show_player_name(planning_poker.get_next_player())
            show_cards(planning_poker.players)
        else:
            messagebox.showinfo("Vote invalide", "Le vote n'est pas valide. Recommencez le vote.")
            planning_poker.reset_votes()
            show_current_task()

    def save_result_to_backlog():
        with open('backlog.json', 'r') as f:
            backlog = json.load(f)

        # Mettre à jour la difficulté de la tâche avec la moyenne des votes
        task_id = planning_poker.current_task['id']
        votes = planning_poker.get_votes()
        average_difficulty = sum(votes) / len(votes)
        backlog['taches'][task_id - 1]['difficulte'] = average_difficulty

        with open('backlog.json', 'w') as f:
            json.dump(backlog, f, indent=2)

    def on_next_task_button_click():
        planning_poker.reset_votes()
        planning_poker.complete_current_task()  # Mettez à jour la tâche actuelle avant de passer à la suivante
        next_task = planning_poker.get_next_task()
        if next_task:
            planning_poker.current_task = next_task
            show_current_task()
            show_player_name(planning_poker.get_next_player())
            show_cards(planning_poker.players)
            if not next_task:  # Si c'est la dernière tâche
                next_task_button_text.set("Récapitulatif")  # Changer le texte du bouton
                root.update_idletasks()  # Forcer la mise à jour immédiate de l'interface utilisateur
        else:
            show_summary()

    def show_summary():
        summary = "\nRécapitulatif des tâches évaluées :\n"
        for task in planning_poker.evaluated_tasks:  # Utilisez evaluated_tasks au lieu de tasks
            summary += f"Tâche : {task['nom']}\n"
            summary += f"Description : {task['description']}\n"
            summary += f"Difficulté : {task['difficulte']}\n\n"

        messagebox.showinfo("Récapitulatif des tâches évaluées", summary)
        root.destroy()  # Fermez l'application après avoir affiché le récapitulatif

    def show_current_task():
        task_label.config(text=f"Tâche actuelle : {planning_poker.current_task['nom']} - {planning_poker.current_task['description']}")

    def show_cards(players):
        # Créer un cadre pour afficher les cartes
        cards_frame = tk.Frame(root)
        cards_frame.pack()

        for player in players:
            card_label = tk.Label(cards_frame, text=f"Carte de {player} :")
            card_label.pack(side="left", padx=5)

            # Afficher les cartes (à compléter avec votre propre logique)
            for card_value in planning_poker.get_available_cards():
                card_button = tk.Button(cards_frame, text=str(card_value), command=lambda value=card_value, player=player: on_card_selected(value, player))
                card_button.pack(side="left", padx=5)

    def show_player_name(player_name):
        player_name_label.config(text=f"Au tour de : {player_name}")

    next_task_button = tk.Button(root, textvariable=next_task_button_text, command=on_next_task_button_click)
    next_task_button.pack()

    show_current_task()
    show_player_name(planning_poker.get_next_player())
    show_cards(planning_poker.players)

    root.mainloop()
