import streamlit as st
import json
import random

# Constants
QUIZ_SIZE = 20

# Title
st.title("📘 UGC-NET English Literature Quiz")
st.subheader("Choose Quiz Type:")

# Updated quiz type selector
quiz_type = st.selectbox("Quiz Type", ["Indian Literature", "Cultural Studies", "Chronology"])

# Load the appropriate JSON file
if quiz_type == "Indian Literature":
    json_file = "chapterOne.json"
elif quiz_type == "Cultural Studies":
    json_file = "chapterTwo.json"
else:
    json_file = "chronology.json"

# Load questions
with open(json_file, "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Create quiz sets
quiz_sets = [all_questions[i:i + QUIZ_SIZE] for i in range(0, len(all_questions), QUIZ_SIZE)]
total_quizzes = len(quiz_sets)

# Quiz Set selector
quiz_index = st.selectbox(f"Choose a Quiz Set (Total: {total_quizzes})", list(range(1, total_quizzes + 1)))
selected_questions = quiz_sets[quiz_index - 1]

# Shuffle options once
quiz_key = f"{quiz_type}_quiz{quiz_index}"
if "shuffled_options" not in st.session_state or st.session_state.get("quiz_id") != quiz_key:
    st.session_state.shuffled_options = []
    for q in selected_questions:
        opts = q['options'][:]
        random.shuffle(opts)
        st.session_state.shuffled_options.append(opts)
    st.session_state.quiz_id = quiz_key

# Render quiz
st.subheader(f"{quiz_type} — Quiz {quiz_index}")
user_answers = []

# Chronology-based rendering
if quiz_type == "Chronology":
    for idx, q in enumerate(selected_questions):
        st.markdown(f"---\n### Q{idx + 1}: {q['question']}")
        st.markdown(f"A. {q['works'][0]}")
        st.markdown(f"B. {q['works'][1]}")
        st.markdown(f"C. {q['works'][2]}")
        st.markdown(f"D. {q['works'][3]}")
        st.markdown("")

        options = st.session_state.shuffled_options[idx]
        user_ans = st.radio("Choose the correct order:", options, key=f"chrono_q{idx}")

        if st.button(f"Submit Q{idx + 1}", key=f"submit_{idx}"):
            correct = q["answer"]
            if user_ans == correct:
                st.success(f"✅ Correct! ({correct})")
            else:
                st.error(f"❌ Incorrect. Your answer: {user_ans} | Correct: {correct}")

# MCQ-based rendering (Indian Lit / Cultural Studies)
else:
    with st.form("quiz_form"):
        for idx, q in enumerate(selected_questions):
            st.markdown(f"---\n### Q{idx + 1}. {q['question']}")
            options = st.session_state.shuffled_options[idx]
            answer = st.radio("Choose one:", options, key=f"q{idx}")
            user_answers.append(answer)
        submitted = st.form_submit_button("Submit")

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
        st.markdown(f"### ✅ Final Score: **{score}/{len(selected_questions)}**")
