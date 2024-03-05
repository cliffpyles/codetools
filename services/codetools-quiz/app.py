import streamlit as st
import glob
import json


# Load questions from JSON files with error handling
def load_questions():
    question_files = glob.glob("data/*.json")
    all_data = []
    for file in question_files:
        try:
            with open(file, "r") as f:
                data = json.load(f)
                all_data.append(data)
        except Exception as e:
            st.error(f"Error loading questions from {file}: {e}")
    return all_data


# Transform questions into a structured format
def transform_questions(input_data):
    # Define a mapping from numeric difficulty to named difficulty levels
    difficulty_mapping = {
        1: "beginner",
        2: "intermediate",
        3: "advance",
        4: "expert",
        5: "master",
    }

    transformed_data = []

    for topic_info in input_data:
        topic = topic_info["topic"]
        questions = topic_info["questions"]
        choices_info = topic_info["choices"]

        for question in questions:
            # Find the choices and correct answer for this question
            for choice in choices_info:
                if choice["question_id"] == question["id"]:
                    # Map the numeric difficulty to a named level
                    level = difficulty_mapping.get(question["difficulty"], "beginner")
                    correct_answer = choice["choices"][choice["answer"]]
                    transformed_question = {
                        "topic": topic,
                        "level": level,
                        "question": question["question"],
                        "choices": choice["choices"],
                        "correct_answer": correct_answer,
                        "selected_answer": None,
                    }
                    transformed_data.append(transformed_question)

    return transformed_data


def load_data():
    questions_raw = load_questions()
    questions = transform_questions(questions_raw)
    if "data" not in st.session_state:
        st.session_state.data = questions
        st.session_state.current_index = 0


def dispatch(action):
    name = action.get("name").upper()
    payload = action.get("payload", None)

    if name == "SELECT_ANSWER":
        st.session_state.data[st.session_state.current_index][
            "selected_answer"
        ] = payload
    elif name == "GOTO_NEXT_QUESTION":
        if st.session_state.current_index < len(st.session_state.data) - 1:
            st.session_state.current_index += 1
        else:
            # New: Mark the quiz as complete if this was the last question
            st.session_state.quiz_complete = True
        st.rerun()
    elif name == "GOTO_PREVIOUS_QUESTION":
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
        st.rerun()
    else:
        st.error(f"Unknown action: {name}")


def calculate_progress():
    current_question = st.session_state.data[st.session_state.current_index]
    topic = current_question["topic"]
    level = current_question["level"]

    topic_questions = [q for q in st.session_state.data if q["topic"] == topic]
    level_questions = [q for q in topic_questions if q["level"] == level]

    topic_progress = sum(
        1 for q in topic_questions if q["selected_answer"] is not None
    ) / len(topic_questions)
    level_progress = sum(
        1 for q in level_questions if q["selected_answer"] is not None
    ) / len(level_questions)

    return topic_progress, level_progress


def calculate_scores_by_topic_and_level():
    # Initialize a dictionary to store scores
    scores = {}

    for question in st.session_state.data:
        topic = question["topic"]
        level = question["level"]
        key = (topic, level)  # Create a unique key for each topic and level combination

        # Initialize the score entry if not present
        if key not in scores:
            scores[key] = {"correct": 0, "total": 0}

        # Increment total questions
        scores[key]["total"] += 1

        # Increment correct answers
        if question["selected_answer"] == question["correct_answer"]:
            scores[key]["correct"] += 1

    return scores


def calculate_highest_passing_level(scores):
    # Define the order of levels from lowest to highest
    level_order = ["beginner", "intermediate", "advance", "expert", "master"]
    # Initialize a dictionary to keep the highest passing level for each topic
    highest_passing_levels = {}

    for (topic, level), score in scores.items():
        correct = score["correct"]
        total = score["total"]

        # Calculate the passing rate
        passing_rate = correct / total

        # Check if passing (more than 50% correct)
        if passing_rate > 0.5:
            # Check if this topic is already in the highest passing levels
            if topic in highest_passing_levels:
                # Check if the current level is higher than the one already stored
                if level_order.index(level) > level_order.index(
                    highest_passing_levels[topic]["level"]
                ):
                    highest_passing_levels[topic] = {"level": level, "score": score}
            else:
                highest_passing_levels[topic] = {"level": level, "score": score}

    return highest_passing_levels


def render_sidebar():
    topic_progress, level_progress = calculate_progress()

    with st.sidebar:
        st.header("Knowledge Test")
        st.subheader("Topic Progress")
        st.progress(topic_progress)
        st.subheader("Level Progress")
        st.progress(level_progress)


def render_results():
    scores = calculate_scores_by_topic_and_level()
    highest_passing_levels = calculate_highest_passing_level(scores)

    st.write("### Quiz Complete!")

    # Display the highest passing level for each topic
    for topic, info in highest_passing_levels.items():
        level = info["level"]
        st.write(f"**{topic}:** {level}")


def render_navigation():
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    if st.session_state.current_index > 0:
        with col1:
            if st.button("Previous"):
                dispatch({"name": "GOTO_PREVIOUS_QUESTION"})

    if st.session_state.current_index < len(st.session_state.data) - 1:
        with col5:
            if st.button("Next"):
                dispatch({"name": "GOTO_NEXT_QUESTION"})


def render_main():
    # Modification: Only display questions if quiz is not complete
    if not st.session_state.get("quiz_complete", False):
        current_question = st.session_state.data[st.session_state.current_index]

        st.markdown(f"##### Q: {current_question.get('question')}")
        choices = current_question.get("choices")
        selected_answer = st.radio(label="Choices", options=choices, index=None)

        if selected_answer is not None:
            dispatch({"name": "SELECT_ANSWER", "payload": selected_answer})
            dispatch({"name": "GOTO_NEXT_QUESTION"})
    else:
        render_results()  # Display results if quiz is complete


def main():
    if "quiz_complete" not in st.session_state:
        st.session_state.quiz_complete = False
    load_data()
    render_sidebar()
    render_main()
    if not st.session_state.quiz_complete:
        render_navigation()


if __name__ == "__main__":
    main()