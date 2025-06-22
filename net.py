import streamlit as st
import json
import random

# Constants
QUIZ_SIZE = 20

# Title
st.title("📘 UGC-NET English Quiz App")
st.subheader("Choose Section:")

# Step 1: Section Selector
section_choice = st.radio("Select Quiz Type:", ["Paper 1", "Paper 2", "Important Authors"])

# Step 2: Logic Based on Section
if section_choice == "Paper 1":
    st.subheader("Paper 1 – General Aptitude")
    chapter = st.selectbox("Choose Chapter", ["Research Aptitude"])  # Add more later
    json_file = "ResearchAptitude.json"

elif section_choice == "Paper 2":
    st.subheader("Paper 2 – English Literature")
    quiz_type = st.selectbox("Quiz Type", ["Indian Literature", "Cultural Studies", "Chronology", "Literary Theory", "Linguistics", "African Literature", "European Literature", "British Part 1", "British Part 2", "British Part 3", "British Part 4", "Australian Literature"])
    
    if quiz_type == "Indian Literature":
        json_file = "chapterOne.json"
    elif quiz_type == "Cultural Studies":
        json_file = "chapterTwo.json"
    elif quiz_type == "Literary Theory":
        json_file = "chapterThree.json"
    elif quiz_type == "Linguistics":
        json_file = "linguistics.json"
    elif quiz_type == "African Literature":
        json_file = "african.json"
    elif quiz_type == "European Literature":
        json_file = "europe.json"
    elif quiz_type == "British Part 1":
        json_file = "EnglishpartOne.json"
    elif quiz_type == "British Part 2":
        json_file = "EnglishpartTwo.json"
    elif quiz_type == "British Part 3":
        json_file = "EnglishpartThree.json"
    elif quiz_type == "British Part 4":
        json_file = "EnglishpartFour.json"
    elif quiz_type == "Australian Literature":
        json_file = "aus.json"
    else:
        json_file = "chronology.json"

else:
    st.subheader("Important Authors – Focused Practice")
    author_choice = st.selectbox("Choose Author", ["T.S. Eliot", "Coleridge", "William Wordsworth", "Dryden", "Johnson", "John Keats", "John Milton", "Alexander Pope", "Charles Dickens"])
    if author_choice == "T.S. Eliot":
        json_file = "ts_eliot.json"
    elif author_choice == "Coleridge":
        json_file = "coleridge.json"
    elif author_choice == "William Wordsworth":
        json_file = "wordsworth.json"
    elif author_choice == "Dryden":
        json_file = "dryden.json"
    elif author_choice == "Johnson":
        json_file = "johnson.json"
    elif author_choice == "John Keats":
        json_file = "keats.json"
    elif author_choice == "John Milton":
        json_file = "milton.json"
    elif author_choice == "Alexander Pope":
        json_file = "pope.json"
    elif author_choice == "Charles Dickens":
        json_file = "dickens.json"
    else:
        json_file = "default_author.json"

# Load questions
with open(json_file, "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Create quiz sets
quiz_sets = [all_questions[i:i + QUIZ_SIZE] for i in range(0, len(all_questions), QUIZ_SIZE)]
total_quizzes = len(quiz_sets)

# Quiz Set selector
quiz_index = st.selectbox(f"Choose a Quiz Set (Total: {total_quizzes})", list(range(1, total_quizzes + 1)))
selected_questions = quiz_sets[quiz_index - 1]

# Shuffle options once per session and quiz
quiz_key = f"{json_file}_quiz{quiz_index}"
if "shuffled_options" not in st.session_state or st.session_state.get("quiz_id") != quiz_key:
    st.session_state.shuffled_options = []
    for q in selected_questions:
        opts = q['options'][:] if 'options' in q else q['works'][:]
        random.shuffle(opts)
        st.session_state.shuffled_options.append(opts)
    st.session_state.quiz_id = quiz_key

# Render quiz
st.subheader(f"📝 Quiz {quiz_index}")

# Chronology-style rendering
if section_choice == "Paper 2" and quiz_type == "Chronology":
    for idx, q in enumerate(selected_questions):
        st.markdown(f"---\n### Q{idx + 1}: {q['question']}")
        st.markdown(f"A. {q['works'][0]}")
        st.markdown(f"B. {q['works'][1]}")
        st.markdown(f"C. {q['works'][2]}")
        st.markdown(f"D. {q['works'][3]}")
        options = st.session_state.shuffled_options[idx]
        user_ans = st.radio("Choose the correct order:", options, key=f"chrono_q{idx}")

        if st.button(f"Submit Q{idx + 1}", key=f"submit_{idx}"):
            correct = q["answer"]
            if user_ans == correct:
                st.success(f"✅ Correct! ({correct})")
            else:
                st.error(f"❌ Incorrect. Your answer: {user_ans} | Correct: {correct}")

# Regular MCQ rendering
else:
    half = len(selected_questions) // 2
    first_half = selected_questions[:half]
    second_half = selected_questions[half:]

    if "user_answers" not in st.session_state or st.session_state.quiz_id != quiz_key:
        st.session_state.user_answers = [None] * len(selected_questions)

    # Part 1
    with st.form("quiz_form_part1"):
        st.markdown("### 🧾 Part 1: Questions 1 to 10")
        for idx, q in enumerate(first_half):
            st.markdown(f"---\n### Q{idx + 1}. {q['question']}")
            options = st.session_state.shuffled_options[idx]
            st.session_state.user_answers[idx] = st.radio("Choose one:", options, key=f"q{idx}")
        submitted1 = st.form_submit_button("Submit Part 1")

    if submitted1:
        st.markdown("### 📋 Feedback for Part 1:")
        score1 = 0
        for idx, q in enumerate(first_half):
            user_ans = st.session_state.user_answers[idx]
            correct = q['answer']
            if user_ans == correct:
                st.success(f"✅ Q{idx + 1}: Correct ({correct})")
                score1 += 1
            else:
                st.error(f"❌ Q{idx + 1}: Wrong. Your answer: {user_ans} | Correct: {correct}")
        st.session_state.score1 = score1
        st.markdown(f"#### 🧮 Score for Part 1: **{score1}/{half}**")

    # Part 2
    with st.form("quiz_form_part2"):
        st.markdown("### 🧾 Part 2: Questions 11 to 20")
        for idx, q in enumerate(second_half, start=half):
            st.markdown(f"---\n### Q{idx + 1}. {q['question']}")
            options = st.session_state.shuffled_options[idx]
            st.session_state.user_answers[idx] = st.radio("Choose one:", options, key=f"q{idx}")
        submitted2 = st.form_submit_button("Submit Part 2")

    if submitted2:
        st.markdown("### 📋 Feedback for Part 2:")
        score2 = 0
        for idx, q in enumerate(second_half, start=half):
            user_ans = st.session_state.user_answers[idx]
            correct = q['answer']
            if user_ans == correct:
                st.success(f"✅ Q{idx + 1}: Correct ({correct})")
                score2 += 1
            else:
                st.error(f"❌ Q{idx + 1}: Wrong. Your answer: {user_ans} | Correct: {correct}")
        st.session_state.score2 = score2
        st.markdown(f"#### 🧮 Score for Part 2: **{score2}/{len(second_half)}**")

        total_score = st.session_state.get("score1", 0) + score2
        st.markdown(f"### ✅ Final Combined Score: **{total_score}/{len(selected_questions)}**")
