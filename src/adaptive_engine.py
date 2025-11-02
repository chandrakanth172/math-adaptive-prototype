from sklearn.tree import DecisionTreeClassifier
import numpy as np

class AdaptiveEngine:
    def __init__(self, method='rule_based'):
        """
        method: 'rule_based' or 'ml_based'
        """
        self.method = method
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']
        self.ml_model = None
        
        if method == 'ml_based':
            self._initialize_ml_model()
    
    def _initialize_ml_model(self):
        """Initialize a simple decision tree for ML-based adaptation"""
        # Pre-train with sample data
        # Features: [accuracy_rate, avg_response_time_normalized, consecutive_correct]
        # Labels: 0=Easy, 1=Medium, 2=Hard
        
        X_train = np.array([
            [0.3, 0.8, 0],  # Low accuracy, slow -> Easy
            [0.5, 0.6, 1],  # Medium accuracy -> Easy
            [0.7, 0.5, 2],  # Good accuracy -> Medium
            [0.8, 0.4, 3],  # High accuracy -> Medium
            [0.9, 0.3, 3],  # Very high accuracy -> Hard
            [0.4, 0.7, 0],  # Struggling -> Easy
            [0.95, 0.2, 4], # Excellent -> Hard
        ])
        
        y_train = np.array([0, 0, 1, 1, 2, 0, 2])
        
        self.ml_model = DecisionTreeClassifier(max_depth=3, random_state=42)
        self.ml_model.fit(X_train, y_train)
    
    def adapt_difficulty(self, current_difficulty, tracker):
        """Determine next difficulty level based on performance"""
        if self.method == 'rule_based':
            return self._rule_based_adapt(current_difficulty, tracker)
        else:
            return self._ml_based_adapt(current_difficulty, tracker)
    
    def _rule_based_adapt(self, current_difficulty, tracker):
        """Rule-based adaptation logic"""
        recent_streak = tracker.get_recent_streak(3)
        
        # Not enough data yet
        if len(recent_streak) < 3:
            return current_difficulty
        
        # Check for 3 consecutive correct answers
        if all(recent_streak):
            if current_difficulty == 'Easy':
                return 'Medium'
            elif current_difficulty == 'Medium':
                return 'Hard'
        
        # Check for 2 consecutive incorrect answers
        if len([x for x in recent_streak[-2:] if not x]) >= 2:
            if current_difficulty == 'Hard':
                return 'Medium'
            elif current_difficulty == 'Medium':
                return 'Easy'
        
        return current_difficulty
    
    def _ml_based_adapt(self, current_difficulty, tracker):
        """ML-based adaptation using decision tree"""
        summary = tracker.get_summary()
        
        if not summary or summary['total_questions'] < 3:
            return current_difficulty
        
        # Prepare features
        accuracy_rate = summary['accuracy'] / 100
        avg_time_normalized = min(summary['avg_response_time'] / 30, 1)  # Normalize to 0-1
        consecutive_correct = sum(tracker.get_recent_streak(5))
        
        features = np.array([[accuracy_rate, avg_time_normalized, consecutive_correct]])
        
        # Predict difficulty level
        predicted_level_idx = self.ml_model.predict(features)[0]
        predicted_difficulty = self.difficulty_levels[predicted_level_idx]
        
        return predicted_difficulty
    
    def recommend_next_level(self, tracker):
        """Recommend difficulty for next session"""
        summary = tracker.get_summary()
        
        if not summary:
            return 'Easy'
        
        accuracy = summary['accuracy']
        
        if accuracy >= 80:
            return 'Hard'
        elif accuracy >= 60:
            return 'Medium'
        else:
            return 'Easy'
