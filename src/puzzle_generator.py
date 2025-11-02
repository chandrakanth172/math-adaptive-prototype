import random

class PuzzleGenerator:
    def __init__(self):
        self.operations = ['+', '-', '*', '/']
        
        # Emoji themes for visual appeal
        self.emoji_sets = {
            'fruits': ['🍎', '🍊', '🍌', '🍇', '🍓', '🍉', '🍒'],
            'animals': ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻'],
            'sports': ['⚽', '🏀', '🏈', '⚾', '🎾', '🏐', '🏓'],
            'toys': ['🎮', '🧸', '🎲', '🪀', '🎯', '🎪', '🎨'],
            'nature': ['⭐', '🌟', '💫', '🌈', '🌸', '🌺', '🌻'],
            'food': ['🍕', '🍔', '🍟', '🌭', '🍿', '🧁', '🍩'],
            'vehicles': ['🚗', '🚕', '🚙', '🚌', '🚎', '🏎️', '🚓']
        }
    
    def generate_puzzle(self, difficulty):
        """Generate a math puzzle based on difficulty level"""
        if difficulty == "Easy":
            return self._generate_easy()
        elif difficulty == "Medium":
            return self._generate_medium()
        else:  # Hard
            return self._generate_hard()
    
    def _generate_easy(self):
        """Easy: Single digit addition/subtraction with emojis"""
        use_emoji = random.choice([True, False])  # 50% chance of emoji
        
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(['+', '-'])
        
        if operation == '-' and num1 < num2:
            num1, num2 = num2, num1
        
        if use_emoji and operation == '+':
            # Visual addition with emojis
            theme = random.choice(list(self.emoji_sets.keys()))
            emoji = random.choice(self.emoji_sets[theme])
            question = f"{emoji * num1} + {emoji * num2} = ?"
            answer = num1 + num2
            return question, answer
        elif use_emoji and operation == '-':
            # Visual subtraction with emojis
            theme = random.choice(list(self.emoji_sets.keys()))
            emoji = random.choice(self.emoji_sets[theme])
            question = f"{emoji * num1} - {emoji * num2} = ?"
            answer = num1 - num2
            return question, answer
        else:
            # Regular number problem with emoji decoration
            emoji_decoration = random.choice(['🧮', '🔢', '✏️', '📝'])
            question = f"{emoji_decoration} {num1} {operation} {num2}"
            answer = eval(f"{num1} {operation} {num2}")
            return question, answer
    
    def _generate_medium(self):
        """Medium: Two digit addition/subtraction or single digit multiplication with context"""
        choice = random.choice(['add_sub', 'multiply'])
        
        if choice == 'add_sub':
            num1 = random.randint(10, 50)
            num2 = random.randint(1, 20)
            operation = random.choice(['+', '-'])
            
            if operation == '-' and num1 < num2:
                num1, num2 = num2, num1
            
            # Add contextual emoji
            context_emojis = {
                '+': ['📚', '🎁', '⭐', '🍬', '🎈'],
                '-': ['🍪', '🎮', '🏆', '💰', '🎯']
            }
            emoji = random.choice(context_emojis[operation])
            question = f"{emoji} {num1} {operation} {num2}"
            answer = eval(f"{num1} {operation} {num2}")
            
        else:  # Multiplication
            num1 = random.randint(2, 10)
            num2 = random.randint(2, 10)
            operation = '*'
            
            # Add multiplication context
            mult_emojis = ['🎁', '📦', '🧺', '🎒', '🛍️']
            emoji = random.choice(mult_emojis)
            question = f"{emoji} {num1} × {num2}"
            answer = num1 * num2
        
        return question, answer
    
    def _generate_hard(self):
        """Hard: Large numbers or division with visual context"""
        choice = random.choice(['multiply', 'divide'])
        
        if choice == 'multiply':
            num1 = random.randint(10, 25)
            num2 = random.randint(10, 25)
            operation = '×'
            
            # Power/achievement theme for hard problems
            hard_emojis = ['🚀', '💪', '🏆', '🎯', '⚡']
            emoji = random.choice(hard_emojis)
            question = f"{emoji} {num1} {operation} {num2}"
            answer = num1 * num2
            
        else:  # Division
            # Division with whole number answers
            num2 = random.randint(2, 12)
            answer = random.randint(5, 20)
            num1 = num2 * answer
            
            # Sharing/distribution theme
            div_emojis = ['🍕', '🍰', '🎂', '🍪', '🧁']
            emoji = random.choice(div_emojis)
            question = f"{emoji} {num1} ÷ {num2}"
        
        return question, int(answer)
    
    def get_emoji_explanation(self, question):
        """Optional: Provide context for emoji-based questions"""
        # This can be used to show kids what the emoji represents
        explanations = {
            '🍎': 'apples',
            '🐶': 'puppies',
            '⭐': 'stars',
            '🎮': 'game controllers',
            '🍕': 'pizza slices',
            '🚗': 'cars'
        }
        # You can extend this to show contextual help if needed
        pass
