import streamlit as st
import time
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

# Page configuration
st.set_page_config(
    page_title="Adaptive Math Learning",
    page_icon="🧮",
    layout="centered"
)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.user_name = ''
    st.session_state.difficulty = 'Easy'
    st.session_state.question_count = 0
    st.session_state.max_questions = 10
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.puzzle_gen = PuzzleGenerator()
    st.session_state.tracker = PerformanceTracker()
    st.session_state.adaptive_engine = None
    st.session_state.adaptation_method = 'rule_based'  # Default to rule-based

def welcome_screen():
    # Sidebar for teacher/parent settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings (For Teachers/Parents)")
        st.markdown("Choose how the app adjusts difficulty:")
        method = st.radio(
            "Adaptation Method:",
            ['🎯 Simple Rules (Transparent Logic)', '🤖 Smart AI (Machine Learning)'],
            key='method_choice',
            help="Simple Rules: Clear if-then logic. Smart AI: Uses decision tree model."
        )
        st.session_state.adaptation_method = 'rule_based' if 'Simple' in method else 'ml_based'
        
        st.markdown("---")
        st.markdown("**About Adaptation Methods:**")
        if 'Simple' in method:
            st.info("📋 **Simple Rules**: If child gets 3 correct in a row → harder level. If 2 wrong in a row → easier level.")
        else:
            st.info("🧠 **Smart AI**: Uses accuracy, speed, and recent performance to predict the best difficulty level.")
    
    st.title("🧮 Adaptive Math Learning")
    st.markdown("### Welcome! Let's practice math together!")
    st.markdown("*Fun math puzzles that adjust to your skill level!*")
    
    st.session_state.user_name = st.text_input("What's your name?", key='name_input', placeholder="Enter your name here...")
    
    st.markdown("#### Choose your starting difficulty:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Easy", use_container_width=True, help="Simple addition and subtraction (1-10)"):
            st.session_state.difficulty = 'Easy'
    with col2:
        if st.button("🟡 Medium", use_container_width=True, help="Bigger numbers and multiplication"):
            st.session_state.difficulty = 'Medium'
    with col3:
        if st.button("🔴 Hard", use_container_width=True, help="Challenging multiplication and division"):
            st.session_state.difficulty = 'Hard'
    
    st.info(f"Selected Difficulty: **{st.session_state.difficulty}**")
    
    if st.button("🚀 Start Learning!", use_container_width=True, type="primary"):
        if st.session_state.user_name:
            st.session_state.adaptive_engine = AdaptiveEngine(method=st.session_state.adaptation_method)
            st.session_state.stage = 'quiz'
            st.rerun()
        else:
            st.error("Please enter your name!")

def generate_new_question():
    question, answer = st.session_state.puzzle_gen.generate_puzzle(st.session_state.difficulty)
    st.session_state.current_question = question
    st.session_state.current_answer = answer
    st.session_state.tracker.start_question()

def quiz_screen():
    st.title(f"Hi {st.session_state.user_name}! 👋")
    
    # Progress bar
    progress = st.session_state.question_count / st.session_state.max_questions
    st.progress(progress)
    st.markdown(f"**Question {st.session_state.question_count + 1} of {st.session_state.max_questions}**")
    
    # Display current difficulty with friendly colors
    difficulty_color = {'Easy': '🟢', 'Medium': '🟡', 'Hard': '🔴'}
    st.markdown(f"### Current Level: {difficulty_color[st.session_state.difficulty]} {st.session_state.difficulty}")
    
    # Generate question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display question in a friendly way
    st.markdown(f"## 🧮 What is: `{st.session_state.current_question}` ?")
    
    # Answer input
    user_answer = st.number_input("Your answer:", step=1, key=f'answer_{st.session_state.question_count}', value=0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
            # Record answer
            is_correct, response_time = st.session_state.tracker.record_answer(
                st.session_state.current_question,
                user_answer,
                st.session_state.current_answer,
                st.session_state.difficulty
            )
            
            # Increment question count
            st.session_state.question_count += 1
            
            # Adapt difficulty BEFORE showing feedback
            new_difficulty = st.session_state.adaptive_engine.adapt_difficulty(
                st.session_state.difficulty,
                st.session_state.tracker
            )
            
            # Show friendly, encouraging feedback
            if is_correct:
                if new_difficulty != st.session_state.difficulty:
                    if new_difficulty == 'Medium':
                        st.success(f"🎉 Great job! You got it in {response_time:.1f}s! You're on a roll! Let's try a harder one next!")
                    elif new_difficulty == 'Hard':
                        st.success(f"🏆 Awesome! You got it in {response_time:.1f}s! Super! Ready for an extra challenge?")
                else:
                    st.success(f"✨ Excellent work! You got it in {response_time:.1f}s! Keep it up!")
            else:
                if new_difficulty != st.session_state.difficulty:
                    if new_difficulty == 'Easy':
                        st.error(f"😊 The answer was **{st.session_state.current_answer}**. No worries! Let's try an easier puzzle to help you out!")
                    elif new_difficulty == 'Medium':
                        st.error(f"💡 The answer was **{st.session_state.current_answer}**. Almost there! Let's try something a bit easier.")
                else:
                    st.error(f"👍 The answer was **{st.session_state.current_answer}**. Keep going! Practice makes perfect!")
            
            time.sleep(2)  # Give kids time to read the message
            
            # Check if session complete
            if st.session_state.question_count >= st.session_state.max_questions:
                st.session_state.stage = 'summary'
                st.rerun()
            
            # Update difficulty
            if new_difficulty != st.session_state.difficulty:
                st.session_state.difficulty = new_difficulty
            
            # Clear current question for next one
            st.session_state.current_question = None
            st.rerun()
    
    with col2:
        if st.button("🛑 End Session", use_container_width=True):
            st.session_state.stage = 'summary'
            st.rerun()

def summary_screen():
    st.title("📊 Session Summary")
    st.markdown(f"### Great work, {st.session_state.user_name}! 🎉")
    
    summary = st.session_state.tracker.get_summary()
    
    if summary:
        # Display key metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Questions", summary['total_questions'])
        with col2:
            st.metric("Correct Answers", summary['correct_answers'])
        with col3:
            st.metric("Accuracy", f"{summary['accuracy']}%")
        
        st.metric("⏱️ Average Response Time", f"{summary['avg_response_time']} seconds")
        
        # Friendly recommendation
        recommended_level = st.session_state.adaptive_engine.recommend_next_level(st.session_state.tracker)
        
        if recommended_level == 'Hard':
            st.success(f"🎯 **Amazing! Try the Hard level next time!**")
        elif recommended_level == 'Medium':
            st.success(f"🎯 **You're doing great! Try the Medium level next time!**")
        else:
            st.success(f"🎯 **Keep practicing! Start with Easy level next time!**")
        
        # Performance visualization
        st.markdown("### 📈 Your Performance")
        st.markdown("*Green = Correct, Red = Try Again*")
        
        if st.session_state.tracker.records:
            import pandas as pd
            df = pd.DataFrame(st.session_state.tracker.records)
            st.bar_chart(df['is_correct'].astype(int))
        
        # Encouragement message based on accuracy
        if summary['accuracy'] >= 80:
            st.balloons()
            st.markdown("### 🌟 Outstanding performance! You're a math star!")
        elif summary['accuracy'] >= 60:
            st.markdown("### 💪 Good job! Keep practicing and you'll be amazing!")
        else:
            st.markdown("### 🎈 Great effort! Every practice makes you better!")
    
    if st.button("🔄 Start New Session", use_container_width=True, type="primary"):
        # Reset session state
        st.session_state.stage = 'welcome'
        st.session_state.question_count = 0
        st.session_state.current_question = None
        st.session_state.tracker = PerformanceTracker()
        st.rerun()

# Main app routing
if st.session_state.stage == 'welcome':
    welcome_screen()
elif st.session_state.stage == 'quiz':
    quiz_screen()
elif st.session_state.stage == 'summary':
    summary_screen()
