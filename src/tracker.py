import time
import pandas as pd

class PerformanceTracker:
    def __init__(self):
        self.records = []
        self.start_time = None
    
    def start_question(self):
        """Start timing for a question"""
        self.start_time = time.time()
    
    def record_answer(self, question, user_answer, correct_answer, difficulty):
        """Record the user's answer and performance"""
        response_time = time.time() - self.start_time
        is_correct = (user_answer == correct_answer)
        
        self.records.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'response_time': round(response_time, 2),
            'difficulty': difficulty
        })
        
        return is_correct, response_time
    
    def get_summary(self):
        """Generate session summary statistics"""
        if not self.records:
            return None
        
        df = pd.DataFrame(self.records)
        
        summary = {
            'total_questions': len(self.records),
            'correct_answers': df['is_correct'].sum(),
            'accuracy': round((df['is_correct'].sum() / len(self.records)) * 100, 2),
            'avg_response_time': round(df['response_time'].mean(), 2),
            'recent_performance': df['is_correct'].tail(5).tolist()
        }
        
        return summary
    
    def get_recent_streak(self, n=3):
        """Get the last n answers to determine streaks"""
        if len(self.records) < n:
            return [r['is_correct'] for r in self.records]
        return [r['is_correct'] for r in self.records[-n:]]
