import streamlit as st
import yaml
import glob
import json
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


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
        3: "advanced",
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


def filter_questions(
    questions, questions_per_level=50, included_topics=[], randomize_questions=False
):
    # Filter questions by included topics if any are specified
    if included_topics:
        questions = [q for q in questions if q["topic"] in included_topics]

    filtered_questions = []

    if randomize_questions:
        # Group questions by topic and level
        questions_by_topic_level = {}
        for question in questions:
            key = (question["topic"], question["level"])
            if key not in questions_by_topic_level:
                questions_by_topic_level[key] = []
            questions_by_topic_level[key].append(question)

        for _, qs in questions_by_topic_level.items():
            # If questions_per_level is not specified or higher than the number of available questions, include all questions
            limit = (
                min(questions_per_level, len(qs)) if questions_per_level else len(qs)
            )
            # Randomly select questions
            selected_qs = random.sample(qs, limit)
            filtered_questions.extend(selected_qs)
    else:
        # If randomization is not required, simply limit the questions by questions_per_level
        # This section needs to group questions by topic and level to correctly apply the limit
        questions_by_topic_level = {}
        for question in questions:
            key = (question["topic"], question["level"])
            if key not in questions_by_topic_level:
                questions_by_topic_level[key] = []
            questions_by_topic_level[key].append(question)

        for _, qs in questions_by_topic_level.items():
            limit = (
                min(questions_per_level, len(qs)) if questions_per_level else len(qs)
            )
            filtered_questions.extend(qs[:limit])

    return filtered_questions


def load_data():
    if "data" not in st.session_state:
        load_state()


# Load the app state
def load_state():
    if os.path.exists("current_test.yaml"):
        try:
            with open("current_test.yaml", "r") as file:
                state = yaml.safe_load(file)
                st.session_state.update(state)
        except Exception as e:
            st.error(f"Failed to load state from file: {e}")
    else:
        try:
            questions_raw = load_questions()
            questions = transform_questions(questions_raw)
            # Assuming filter_questions functionality is correctly implemented
            questions = filter_questions(questions, questions_per_level=5)
            st.session_state.data = questions
            st.session_state.current_index = 0
            # Save the initial state now that questions are loaded and filtered
            save_state()
        except Exception as e:
            st.error(f"Error processing questions: {e}")


# Convert the session state to a serializable format
def state_to_serializable(state_proxy):
    serializable_state = {}
    keys_to_serialize = [
        "data",
        "current_index",
    ]
    for key in keys_to_serialize:
        if key in state_proxy:
            serializable_state[key] = state_proxy[key]
    return serializable_state


# Save the current state of the app to a YAML file with serialization
def save_state():
    try:
        serializable_state = state_to_serializable(st.session_state)
        with open("current_test.yaml", "w") as file:
            yaml.safe_dump(serializable_state, file)
    except Exception as e:
        st.error(f"Failed to save state to file: {e}")


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
        save_state()
        st.rerun()
    elif name == "GOTO_PREVIOUS_QUESTION":
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
        save_state()
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

    return topic_progress, level_progress, topic, level


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
    level_order = ["beginner", "intermediate", "advanced", "expert", "master"]
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


def has_passed_current_level(topic, level):
    scores_by_topic_and_level = calculate_scores_by_topic_and_level()
    key = (topic, level)
    if key in scores_by_topic_and_level:
        score_info = scores_by_topic_and_level[key]
        passed = score_info["correct"] / score_info["total"] > 0.5
        return passed
    return False  # Assume failure if no data available


def find_first_question_of_next_topic(current_topic):
    current_found = False
    for index, question in enumerate(st.session_state.data):
        if question["topic"] == current_topic:
            current_found = True
        elif current_found:
            return index  # Return the index of the first question of the next topic
    return None  # Return None if no next topic is found


def calculate_highest_level_per_topic():
    scores = calculate_scores_by_topic_and_level()
    # Initialize with all topics at level 0 (not started)
    highest_levels = {
        topic: 0 for topic in set(q["topic"] for q in st.session_state.data)
    }

    # Update with the highest level passed for each topic
    for (topic, level), score in scores.items():
        level_value = [
            "beginner",
            "intermediate",
            "advanced",
            "expert",
            "master",
        ].index(level) + 1
        if score["correct"] / score["total"] > 0.5:  # Considered passing
            highest_levels[topic] = max(highest_levels[topic], level_value)

    return highest_levels


def insert_line_breaks(text, char_limit=10):
    """
    Insert line breaks into text at space positions to ensure
    that each line does not exceed the character limit.
    """
    words = text.split()
    broken_text = ""
    current_line = ""
    for word in words:
        if len(current_line) + len(word) <= char_limit:
            current_line += word + " "
        else:
            broken_text += current_line.strip() + "\n"
            current_line = word + " "
    broken_text += current_line.strip()  # Add the last line
    return broken_text


def plot_knowledge_level_chart(highest_levels):
    level_names = [
        "beginner",
        "intermediate",
        "advanced",
        "expert",
        "master",
    ]
    topics = list(highest_levels.keys())
    levels = [highest_levels[topic] for topic in topics]

    # Calculate the numeric representation for plotting
    level_numeric = [level for level in levels]

    # Prepare data for the Plotly chart
    data = go.Barpolar(
        r=level_numeric,
        theta=topics,
        marker_color=level_numeric,
        marker_line_color="black",
        marker_line_width=1,
        opacity=0.7,
    )

    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                type="category",
                tickvals=[1, 2, 3, 4],
                ticktext=level_names,
                range=[0, 4],  # Adjust the range based on your levels
            ),
            angularaxis=dict(direction="clockwise", period=len(topics)),
        ),
        title="Knowledge Levels per Topic",
    )

    fig = go.Figure(data=data, layout=layout)

    # Show the figure in the Streamlit app
    st.plotly_chart(fig)


def render_performance_chart():
    highest_levels = calculate_highest_level_per_topic()
    plot_knowledge_level_chart(highest_levels)


def render_sidebar():
    with st.sidebar:
        st.subheader("Progress")
        render_topic_tree()


def render_results():
    # scores = calculate_scores_by_topic_and_level()
    # highest_passing_levels = calculate_highest_passing_level(scores)
    # passed_topics = [
    #     (topic, info["level"]) for topic, info in highest_passing_levels.items()
    # ]
    # st.write("### Quiz Complete!")

    # # Display the highest passing level for each topic
    # for topic, level in passed_topics:
    #     st.write(f"**{topic}:** {level}")

    render_performance_chart()


def render_navigation():

    # if st.session_state.current_index > 0:
    #     with col1:
    #         if st.button("Previous"):
    #             dispatch({"name": "GOTO_PREVIOUS_QUESTION"})

    # if st.session_state.current_index < len(st.session_state.data) - 1:
    #     with col2:
    #         if st.button("Next"):
    #             dispatch({"name": "GOTO_NEXT_QUESTION"})
    st.divider()
    with st.container():
        col1, col2, col3 = st.columns(3, gap="medium")
        if st.session_state.current_index < len(st.session_state.data) - 1:
            with col3:
                if st.button("Skip Question", use_container_width=True):
                    dispatch({"name": "GOTO_NEXT_QUESTION"})


def render_topic_tree():
    scores_by_topic_and_level = calculate_scores_by_topic_and_level()

    levels = [
        "beginner",
        "intermediate",
        "advanced",
        "expert",
        "master",
    ]
    seen = set()
    topics = [
        q["topic"]
        for q in st.session_state.data
        if q["topic"] not in seen and not seen.add(q["topic"])
    ]
    current_question_topic = st.session_state.data[st.session_state.current_index][
        "topic"
    ]
    current_question_level = st.session_state.data[st.session_state.current_index][
        "level"
    ]
    current_question_topic_index = topics.index(current_question_topic)
    completed_icon = ":white_check_mark:"
    incomplete_icon = ":hourglass_flowing_sand:"

    for topic_index, topic in enumerate(topics):
        is_completed = current_question_topic_index > topic_index
        status_icon = completed_icon if is_completed is True else incomplete_icon
        is_current_topic = topic_index == current_question_topic_index

        with st.expander(f"{status_icon} {topic}", expanded=is_current_topic):
            for level in levels:
                key = (topic, level)
                is_active_level = is_current_topic and level == current_question_level

                if key in scores_by_topic_and_level:
                    score = scores_by_topic_and_level[key]
                    correct = score["correct"]
                    total = score["total"]

                    active_status_message = (
                        f"**{level.capitalize()}: {correct}/{total}**"
                    )
                    inactive_status_message = f"{level.capitalize()}: {correct}/{total}"
                    status_message = (
                        active_status_message
                        if is_active_level
                        else inactive_status_message
                    )
                    st.markdown(status_message)
                else:
                    st.markdown(f"{level.capitalize()}: Not Started")


def render_debugger():
    data = st.session_state.data
    current_index = st.session_state.current_index
    quiz_complete = st.session_state.quiz_complete
    questions_count = len(st.session_state.data)
    scores_by_topic_and_level = calculate_scores_by_topic_and_level()
    # choices = [datum["choices"] for datum in data]
    choices = data
    st.markdown(
        f"current_index: **{current_index}** | quiz_complete: **{quiz_complete}** | questions count: **{questions_count}**"
    )
    choices_df = pd.DataFrame.from_records(choices)
    st.subheader("Data")
    st.dataframe(
        choices_df,
        column_order=(
            "topic",
            "level",
            "correct_answer",
            "selected_answer",
            "question",
            "choices",
        ),
    )

    st.subheader("Scores")
    for score in scores_by_topic_and_level:
        # st.write(score)
        st.write(score, scores_by_topic_and_level[score])


def render_questions():
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
    tab_1, tab_2, tab_3 = st.tabs(["Questions", "Results", "Debugger"])

    with tab_1:
        render_questions()
        if not st.session_state.quiz_complete:
            render_navigation()
    with tab_2:
        render_results()
    with tab_3:
        render_debugger()


if __name__ == "__main__":
    main()
