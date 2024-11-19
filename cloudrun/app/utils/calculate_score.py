class OralHealthScoreCalculator:
    weight_mapping = {
        "calculus": {0: 3, 1: 2, 2: 1, 3: 0},
        "caries": {0: 3, 1: 2, 2: 1, 3: 0},
        "discoloration": {0: 3, 1: 2, 2: 1, 3: 0},
        "gingivitis": {0: 3, 1: 1, 2: 1, 3: 0},
        "mouthUlcer": {0: 3, 1: 2, 2: 1, 3: 0},
    }
    score_mapping = {
        "pain_never": 0,
        "pain_rarely": -0.25,
        "pain_often": -0.5,
        "pain_always": -1,
        "bleeding_never": 0,
        "only_when_brushing": -0.25,
        "bleeding_often": -1,
        "bleeding_always": -2,
        "moving_no": 0,
        "moving_one_tooth": -2,
        "moving_multiple_teeth": -3,
        "twice_a_day": 0.5,
        "more_than_twice_a_day": 0.5,
        "once_a_day": 0,
        "less_than_once_a_day": -1,
        "frequently_never": 0.5,
        "frequently_occasionally": 0,
        "frequently_often": -0.5,
        "frequently_always": -0.5,
        "smoke_no": 0,
        "yes_occasionally": -1,
        "yes_daily": -2,
        "dentist_always": 0.5,
        "dentist_often": 0.5,
        "dentist_rarely": -1.5,
        "dentist_never": -2,
    }
    
    def get_score_by_quest_id(self, quest_id: str):
        """
               Retrieves the score associated with a specific question ID.

               Args:
                   quest_id (str): The ID of the question response for which the score is to be retrieved.

               Returns:
                   float: The score associated with the provided question ID. If the quest_id is not found,
                          it returns 0 by default.

               Usage:
                   score = calculator.get_score_by_quest_id("pain_never")
               """
        
        return self.score_mapping.get(quest_id, 0)
    
    def calculate_score_by_severity_and_condition(self, severity: int, condition: str) -> float:
        """
        Calculates the score based on severity and condition.

        Parameters:
        - severity (int): The severity level (0, 1, 2, or 3)
        - condition (str): The condition (e.g., "calculus", "caries")

        Returns:
        - float: The calculated score
        """
        if condition not in self.weight_mapping:
            raise ValueError(f"Invalid condition: {condition}")
        
        weight = self.weight_mapping[condition].get(severity, 0)
        return (10 / 15) * weight
    
    def calculate_total_score(self, conditions: dict) -> float:
        """
        Calculates the total score by summing the scores for each condition.

        Parameters:
        - conditions (dict): A dictionary with condition names as keys and severity as values.

        Returns:
        - float: The total calculated score
        """
        total_score = 0.0
        for condition, severity in conditions.items():
            score = self.calculate_score_by_severity_and_condition(severity, condition)
            total_score += score
        return total_score
