import streamlit as st
import json
import random

# Constants
QUIZ_SIZE = 20

# Load questions
with open("chapterOne.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Create quiz sets
quiz_sets = [all_questions[i:i + QUIZ_SIZE] for i in range(0, len(all_questions), QUIZ_SIZE)]
total_quizzes = len(quiz_sets)

# Title
st.title("📘 UGC-NET English MCQ Quiz App")
st.subheader("Indian Literature")

# Select quiz
quiz_index = st.selectbox(f"Choose a Quiz Set (Total: {total_quizzes})", list(range(1, total_quizzes + 1)))
selected_questions = quiz_sets[quiz_index - 1]

# Shuffle options once
if "shuffled_options" not in st.session_state or st.session_state.get("quiz_id") != quiz_index:
    st.session_state.shuffled_options = []
    for q in selected_questions:
        opts = q['options'][:]
        random.shuffle(opts)
        st.session_state.shuffled_options.append(opts)
    st.session_state.quiz_id = quiz_index

# Render quiz
st.subheader(f"Quiz {quiz_index} — {QUIZ_SIZE} Questions")
user_answers = []

with st.form("quiz_form"):
    for idx, q in enumerate(selected_questions):
        st.markdown(f"**Q{idx + 1}. {q['question']}**")
        options = st.session_state.shuffled_options[idx]
        answer = st.radio("Choose one:", options, key=f"q{idx}")
        user_answers.append(answer)
    submitted = st.form_submit_button("Submit")

# Feedback under each question
if submitted:
    st.markdown("### 🧾 Feedback:")

    score = 0
    for idx, (q, user_ans) in enumerate(zip(selected_questions, user_answers)):
        correct = q['answer']
        if user_ans == correct:
            st.success(f"✅ Q{idx + 1}: Correct ({correct})")
            score += 1
        else:
            st.error(f"❌ Q{idx + 1}: Wrong. Your answer: {user_ans} | Correct: {correct}")

    st.markdown(f"### ✅ Final Score: **{score}/{QUIZ_SIZE}**")
