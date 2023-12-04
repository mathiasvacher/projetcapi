# rules.py (complété)
class Rules:
    def __init__(self, mode):
        self.mode = mode

    def validate_vote(self, votes):
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
        if self.mode == "strict":
            return votes[0]
        elif self.mode in ["moyenne", "médiane", "majorité"]:
            return sum(votes) / len(votes)
        return None