# rules.py (complété)
class Rules:
    """
    @class Rules
    @brief Class defining the rules for calculating task difficulty based on votes.

    @details
    The Rules class provides different methods for validating votes and calculating task difficulty.
    The available modes include "strict," "moyenne," "médiane," and "majorité."

    @note
    This class is intended for use with the PlanningPoker class.

    @section author Author:
    TOUZAIN Romane
    VACHER Mathias

    @section date Date:
    Specify the creation or last modification date.
    """

    def __init__(self, mode):
        """
        @fn __init__
        @brief Constructor for Rules.

        @param mode The mode for voting rules ("strict," "moyenne," "médiane," or "majorité").
        """
        self.mode = mode

    def validate_vote(self, votes):
        """
        @fn validate_vote
        @brief Validate the votes based on the selected mode.

        @param votes List of votes from players.

        @return True if the votes are valid according to the selected mode, False otherwise.
        """
        if self.mode == "strict":
            return len(set(votes)) == 1
        elif self.mode == "moyenne":
            # Ajoutez ici la logique pour la moyenne
            return sum(votes) / len(votes)
        elif self.mode == "médiane":
            # Ajoutez ici la logique pour la médiane
            sorted_votes = sorted(votes)
            mid = len(sorted_votes) // 2
            return (sorted_votes[mid] + sorted_votes[~mid]) / 2
        elif self.mode == "majorité":
            # Ajoutez ici la logique pour la majorité
            majority = max(set(votes), key=votes.count)
            return majority
        return False

    def calculate_difficulty(self, votes):
        """
        @fn calculate_difficulty
        @brief Calculate the task difficulty based on votes.

        @param votes List of votes from players.

        @return Calculated difficulty based on the selected mode.
        """
        if self.mode == "strict":
            return votes[0]
        elif self.mode in ["moyenne", "médiane", "majorité"]:
            return sum(votes) / len(votes)
        return None