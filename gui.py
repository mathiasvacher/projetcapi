# gui.py (mise à jour)
import tkinter as tk
from tkinter import simpledialog, messagebox, IntVar
from rules import Rules
import json

class CustomDialog(simpledialog.Dialog):
    """
    @class CustomDialog
    @brief Custom dialog box for user input.

    This class defines a custom dialog box that inherits from tkinter's simpledialog.Dialog.
    It is designed for capturing user input with a prompt.

    @details
    The dialog includes a title, prompt, and an entry widget for user input.

    @note
    This class is intended for use with the tkinter library.

    @section author Author:
    TOUZAIN Romane
    VACHER Mathias

    @section date Date:
    04/12/2023
    """
        
    def __init__(self, parent, title, prompt, options):
        """
        @fn __init__
        @brief Constructor for CustomDialog.

        @param parent The parent widget.
        @param title The title of the dialog box.
        @param prompt The prompt displayed to the user.
        @param options Additional options for customization.
        """

        self.options = options
        self.result = None
        self.prompt = prompt  # Ajout de la variable prompt
        super().__init__(parent, title=title)

    def body(self, parent):
        """
        @fn body
        @brief Create the dialog body.

        @param parent The parent widget.

        @details
        - Set the geometry of the dialog.
        - Set the title of the dialog.
        - Display the prompt with a label.
        - Create an entry widget for user input.

        @return The entry widget.
        """
        self.geometry("300x150")
        self.title(self.title)
        tk.Label(parent, text=self.prompt, anchor="w").pack(side="top", fill="x")  # Utilisation de self.prompt

        # Utilisez des boutons radio pour choisir les règles
        self.var = IntVar()
        for i, option in enumerate(self.options):
            tk.Radiobutton(parent, text=option, variable=self.var, value=i).pack(anchor="w")

    def apply(self):
        """
        @fn apply
        @brief Apply the user's input.

        @details
        Set the result attribute to the user's input.
        """
        self.result = self.options[self.var.get()]

def start_gui(planning_poker):
    """
    @fn start_gui
    @brief Start the graphical user interface for the Planning Poker application.

    @param planning_poker An instance of the PlanningPoker class.

    @details
    - Creates and configures the main application window.
    - Gathers information about the number of players, player names, and rules.
    - Manages the flow of the Planning Poker session, including voting and task completion.
    - Displays task information, player names, and voting cards.
    - Provides a summary of evaluated tasks at the end of the session.

    @note
    This function uses tkinter for GUI components.

    @section author Author:
    TOUZAIN Romane
    VACHER Mathias

    @section date Date:
    04/12/2023

    @param planning_poker An instance of the PlanningPoker class.
    """
    
    # Ajoutez la déclaration de rules_options ici
    rules_options = ["strict", "moyenne", "médiane", "majorité"]

    root = tk.Tk()
    root.title("Planning Poker")

    def get_num_players():
        """
        @fn get_num_players
        @brief gets and asks how many players should vote 

        @details
        Asks the users to input how many players are playing, with a min value of 1
        """
        return simpledialog.askinteger("Nombre de joueurs", "Entrez le nombre de joueurs :", minvalue=1)


    def get_player_names(num_players):
        """
        @fn get_player_names
        @brief gets and asks player's names

        @details
        Asks the users to input the names of the players 
        """
        names = []
        for i in range(num_players):
            name = simpledialog.askstring("Nom du joueur", f"Nom du joueur {i + 1} :")
            names.append(name)
        return names

    def get_rules():
        """
        @fn get_rules
        @brief gets and asks the rules that want to get played

        @details
        Asks the users to input the rules he wants to play with 
        """
        # Utilisez la nouvelle boîte de dialogue pour choisir les règles
        dialog = CustomDialog(root, "Règles", "Choisissez les règles :", rules_options)
        return dialog.result

    num_players = get_num_players()
    player_names = get_player_names(num_players)

    planning_poker.players = player_names
    # Utilisez la règle sélectionnée dans le jeu
    rules = Rules(get_rules())
    planning_poker.rules = rules
    planning_poker.current_task = planning_poker.get_next_task()

    task_label = tk.Label(root, text="")
    task_label.pack()

    player_name_label = tk.Label(root, text="")
    player_name_label.pack()

    next_task_button_text = tk.StringVar()
    next_task_button_text.set("Récapitulatif accessible en fin de partie")  

    def on_card_selected(value, player):
        """
        @fn on_card_selected
        @brief reacts based on what card the player selected

        @details
        if the vote is ok according to the rule, next player gets to vode, otherwise it asks the players to replay
        """
        planning_poker.record_vote(player, value)
        show_player_name(planning_poker.get_next_player())
        if planning_poker.is_voting_complete():
            validate_and_next_task()

    def validate_and_next_task():
        """
        @fn validate_and_next_task
        @brief validate the player's vote

        @details
        if the vote is ok according to the rule, next player gets to vode, otherwise it asks the players to replay
        """
        if planning_poker.rules.validate_vote(planning_poker.get_votes()):
            planning_poker.complete_current_task()
            show_current_task()
            show_player_name(planning_poker.get_next_player())
            show_cards()  # Correction : Supprimez l'argument planning_poker.players
        else:
            messagebox.showinfo("Vote invalide", "Le vote n'est pas valide. Recommencez le vote.")
            planning_poker.reset_votes()
            show_current_task()

    def save_result_to_backlog():
        """
        @fn save_result_to_backlog
        @brief saves the results of the vote to the backlog.json file

        @details
        saves the results of the vote to the backlog.json file
        """
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
        planning_poker.complete_current_task()
        next_task = planning_poker.get_next_task()
        if next_task:
            planning_poker.current_task = next_task
            show_current_task()
            show_player_name(planning_poker.get_next_player())
            show_cards()  # Correction : Supprimez l'argument planning_poker.players
            if not next_task:
                next_task_button_text.set("Récapitulatif")
                root.update_idletasks()
        else:
            show_summary()

    def show_summary():
        """
        @fn show_summary
        @brief show a page containing all the votes and tasks with their corresponding difficulty after the vote

        @details
        show a page containing all the votes and tasks with their corresponding difficulty after the vote
        """
        summary = "\nRécapitulatif des tâches évaluées :\n"
        for task in planning_poker.evaluated_tasks:  # Utilisez evaluated_tasks au lieu de tasks
            summary += f"Tâche : {task['nom']}\n"
            summary += f"Description : {task['description']}\n"
            summary += f"Difficulté : {task['difficulte']}\n\n"

        messagebox.showinfo("Récapitulatif des tâches évaluées", summary)
        root.destroy()  # Fermez l'application après avoir affiché le récapitulatif

    def show_current_task():
        """
        @fn show_current_task
        @brief Display information about the current task.

        @details
        Updates the label with the name and description of the current task.
        """
        task_label.config(text=f"Tâche actuelle : {planning_poker.current_task['nom']} - {planning_poker.current_task['description']}")

    def show_cards():
        """
        @fn show_cards
        @brief displays the cards on the window

        @details
        display all the xcards on the window as buttons
        """
        # Créer un cadre pour afficher les cartes
        cards_frame = tk.Frame(root)
        cards_frame.pack()

        # Afficher les cartes pour chaque joueur
        card_label = tk.Label(cards_frame, text=f"Cartes uniques pour la tâche {planning_poker.current_task['nom']} :")
        card_label.pack(side="left", padx=5)

        # Afficher les cartes (à compléter avec votre propre logique)
        for card_value in planning_poker.get_available_cards():
            card_button = tk.Button(cards_frame, text=str(card_value), command=lambda value=card_value: on_card_selected(value))
            card_button.pack(side="left", padx=5)

    def on_card_selected(value):
        """
        @fn on_card_selected
        @brief handles all the work after a player votes

        @details
        handles all the work after a player votes (next player that has to vote, updates the current task on the top of the screen)
        """
        # Changer la logique pour gérer la sélection de carte par le joueur actuel
        player = planning_poker.get_next_player()
        planning_poker.record_vote(player, value)
        show_player_name(planning_poker.get_next_player())
        if planning_poker.is_voting_complete():
            validate_and_next_task()

    def show_player_name(player_name):
        """
        @fn show_player_name
        @brief Displays information about the player that has to vote

        @details
        Displays information about the player that has to vote
        """
        player_name_label.config(text=f"Au tour de : {player_name}")

    next_task_button = tk.Button(root, textvariable=next_task_button_text, command=on_next_task_button_click)
    next_task_button.pack()

    show_current_task()
    show_player_name(planning_poker.get_next_player())
    show_cards()

    root.mainloop()
