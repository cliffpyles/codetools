import streamlit as st
import json
import yaml
import os
import re
from pathlib import Path
from random import shuffle

CONSECUTIVE_PASS_THRESHOLD = 5
CONSECUTIVE_FAIL_THRESHOLD = 3
DIFFICULTY_LEVEL_NAMES = [
    "",
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert",
    "Master",
]


def to_snake_case(s):
    """Convert a string to snake case, replacing spaces and dashes."""
    s = s.replace(" ", "_").replace("-", "_")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def load_questions(excluded_topics=None, included_topics=None):
    """Load questions from JSON files, filtering by excluded or included topics."""
    if excluded_topics is not None and included_topics is not None:
        raise ValueError("Specify either excluded_topics or included_topics, not both.")

    files = Path("./data").glob("*.json")
    topics = []
    for file in files:
        with open(file, "r") as f:
            topic_data = json.load(f)
            topic = to_snake_case(topic_data.get("topic", ""))
            if included_topics and topic in included_topics:
                topics.append(topic_data)
            elif excluded_topics and topic not in excluded_topics:
                topics.append(topic_data)
            elif not included_topics and not excluded_topics:
                topics.append(topic_data)
    return topics


def save_state(state, state_file):
    """Save the current state of the test to a file."""
    with open(state_file, "w") as file:
        yaml.dump(state, file)


def load_state(state_file):
    """Load test state from file, or initialize state if file does not exist."""
    if os.path.exists(state_file):
        with open(state_file, "r") as file:
            return yaml.safe_load(file)
    else:
        return None


def app_state_reset():
    """Reset the app state."""
    st.session_state.current_topic_index = 0
    st.session_state.current_question_index = 0
    st.session_state.current_difficulty_level = 1
    st.session_state.consecutive_correct = 0
    st.session_state.consecutive_incorrect = 0


def main():
    """Main function for the Streamlit app."""
    st.title("Knowledge Test")

    if "load_test" not in st.session_state:
        st.session_state["load_test"] = False

    if st.session_state["load_test"] == False:
        test_name_input = st.text_input(
            "Enter a test name to load or start a new test", ""
        )
        if test_name_input:
            st.session_state["test_name"] = f"{test_name_input}_state.yaml"
            state = load_state(st.session_state["test_name"])
            if state:
                st.session_state["topics_data"] = load_questions()
                st.session_state["results"] = state.get("results", {})
                st.session_state["current_topic_index"] = state.get(
                    "current_topic_index", 0
                )
                st.session_state["current_question_index"] = state.get(
                    "current_question_index", 0
                )
                st.session_state["current_difficulty_level"] = state.get(
                    "current_difficulty_level", 1
                )
                st.session_state["consecutive_correct"] = state.get(
                    "consecutive_correct", 0
                )
                st.session_state["consecutive_incorrect"] = state.get(
                    "consecutive_incorrect", 0
                )
            else:
                st.session_state["topics_data"] = load_questions()
                app_state_reset()
                st.session_state["results"] = {
                    topic["topic"]: {
                        "passed_levels": [],
                        "correct_answers": {i: 0 for i in range(1, 6)},
                    }
                    for topic in st.session_state["topics_data"]
                }
            st.session_state["load_test"] = True

    if "topics_data" in st.session_state and st.session_state["load_test"]:
        topic_list = [topic["topic"] for topic in st.session_state["topics_data"]]
        topic_index = st.session_state.get("current_topic_index", 0)

        if topic_index < len(topic_list):
            current_topic = st.session_state["topics_data"][topic_index]
            st.header(f"Topic: {current_topic['topic']}")

            difficulty_level = st.session_state.get("current_difficulty_level", 1)
            st.subheader(
                f"Difficulty Level: {DIFFICULTY_LEVEL_NAMES[difficulty_level]}"
            )

            questions = [
                q
                for q in current_topic["questions"]
                if q["difficulty"] == difficulty_level
            ]
            question_index = st.session_state.get("current_question_index", 0)

            topic_progress = topic_index / len(topic_list)
            st.progress(topic_progress)

            if questions:
                difficulty_progress = question_index / len(questions)
            else:
                difficulty_progress = 0
            st.progress(difficulty_progress)

            if question_index < len(questions):
                question = questions[question_index]
                st.write(f"{question['question']}")

                choice_info = next(
                    item
                    for item in current_topic["choices"]
                    if item["question_id"] == question["id"]
                )
                options = [choice for choice in choice_info["choices"]]
                selected_answer = st.radio(
                    "Choose an answer:",
                    options,
                    index=None,
                    key=f"question_{question_index}",
                )

                cols = st.columns(3)
                if cols[0].button("Previous") and question_index > 0:
                    st.session_state["current_question_index"] -= 1

                if cols[1].button("Skip"):
                    question_index += 1
                    st.session_state["current_question_index"] = question_index

                if cols[2].button("Quit"):
                    st.session_state["load_test"] = False
                    save_state(
                        {
                            "results": st.session_state["results"],
                            "current_topic_index": st.session_state[
                                "current_topic_index"
                            ],
                            "current_question_index": st.session_state[
                                "current_question_index"
                            ],
                            "current_difficulty_level": st.session_state[
                                "current_difficulty_level"
                            ],
                            "consecutive_correct": st.session_state.consecutive_correct,
                            "consecutive_incorrect": st.session_state.consecutive_incorrect,
                        },
                        st.session_state["test_name"],
                    )

                if selected_answer is not None:

                    if options.index(selected_answer) - 1 == choice_info["answer"]:
                        st.session_state.consecutive_correct += 1
                        st.session_state.consecutive_incorrect = 0
                        st.session_state["results"][current_topic["topic"]][
                            "correct_answers"
                        ][difficulty_level] += 1

                    else:
                        st.session_state.consecutive_incorrect += 1
                        st.session_state.consecutive_correct = 0

                    question_index += 1
                    st.session_state["current_question_index"] = question_index
                    st.experimental_rerun()

            else:
                st.write("No more questions in this difficulty level.")
                st.session_state["current_difficulty_level"] += 1
                st.session_state["current_question_index"] = 0
                if st.session_state["current_difficulty_level"] > 5:
                    st.session_state["current_topic_index"] += 1
                    st.session_state["current_difficulty_level"] = 1

        else:
            st.write("Test completed.")
            st.session_state["load_test"] = False


if __name__ == "__main__":
    main()
