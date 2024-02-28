import click
import json
import re
from pathlib import Path
from random import randint, choice
import yaml
import os
from random import shuffle

CONSECUTIVE_PASS_THRESHOLD = 3
CONSECUTIVE_FAIL_THRESHOLD = 3


class KnowledgeTest:
    def __init__(self, topics, test_name):
        self.topics = topics
        self.test_name = test_name
        self.state_file = f"{self.test_name}_state.yaml"
        (
            self.results,
            self.loaded_questions,
            self.current_topic_index,
            self.current_question_index,
            self.consecutive_correct,
            self.consecutive_incorrect,
        ) = self.load_state()

    def load_state(self):
        """Load or initialize test."""
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as file:
                state = yaml.safe_load(file)
                return (
                    state.get("results", {}),
                    state.get("questions", self.topics),
                    state.get("current_topic_index", 0),
                    state.get("current_question_index", 0),
                    state.get("consecutive_correct", 0),
                    state.get("consecutive_incorrect", 0),
                )
        else:
            results = {
                topic["topic"]: {
                    "passed_levels": [],
                    "correct_answers": {i: 0 for i in range(1, 6)},
                }
                for topic in self.topics
            }
            return results, self.topics, 0, 0, 0, 0

    def run_test(self):
        """Run or resume the knowledge test."""
        difficulty_level_names = [
            "",
            "Beginner",
            "Intermediate",
            "Advanced",
            "Expert",
            "Master",
        ]
        print(f"\nTest Name: {self.test_name}\n")
        for i, topic in enumerate(
            self.loaded_questions[self.current_topic_index :],
            start=self.current_topic_index,
        ):
            self.current_topic_index = i
            current_topic_results = self.results[topic["topic"]]
            print(f"Topic: {topic['topic']}\n")
            for difficulty_level in range(1, 6):
                if difficulty_level in current_topic_results["passed_levels"]:
                    continue  # Skip difficulty level if already passed

                difficulty_level_name = difficulty_level_names[difficulty_level]
                print(f"Difficulty Level: {difficulty_level_name}\n")
                questions = [
                    q for q in topic["questions"] if q["difficulty"] == difficulty_level
                ]
                shuffle(questions)  # Shuffle questions for randomness
                for j, question in enumerate(
                    questions[self.current_question_index :],
                    start=self.current_question_index,
                ):
                    self.current_question_index = j
                    if self.consecutive_incorrect >= CONSECUTIVE_FAIL_THRESHOLD:
                        self.consecutive_correct, self.consecutive_incorrect = 0, 0
                        print("(failed)\n")
                        break
                    elif self.consecutive_correct == CONSECUTIVE_PASS_THRESHOLD:
                        self.consecutive_correct, self.consecutive_incorrect = 0, 0
                        print("(passed)\n")
                        break

                    choice_info = next(
                        item
                        for item in topic["choices"]
                        if item["question_id"] == question["id"]
                    )
                    print(
                        f"{topic['topic']} ({difficulty_level_name}): {question['question']}\n"
                    )
                    for i, choice in enumerate(choice_info["choices"], start=1):
                        print(f"{i}. {choice}")
                    print("5. I don't know\n6. Proceed to next topic")

                    answer = click.prompt("\nYour answer", type=int, show_choices=False)
                    if answer == 5:
                        self.consecutive_incorrect += 1
                    elif answer == 6:
                        self.consecutive_correct, self.consecutive_incorrect = 0, 0
                        break
                    elif answer - 1 == choice_info["answer"]:
                        self.consecutive_correct += 1
                        self.consecutive_incorrect = 0
                        current_topic_results["correct_answers"][difficulty_level] += 1
                    else:
                        self.consecutive_incorrect += 1
                        self.consecutive_correct = 0
                    # Update state after every question
                    self.update_state()

                if self.consecutive_correct >= CONSECUTIVE_PASS_THRESHOLD:
                    current_topic_results["passed_levels"].append(difficulty_level)
                    # Ensure state is updated when advancing levels or finishing a topic
                    self.update_state()
                    self.consecutive_correct, self.consecutive_incorrect = 0, 0
                self.current_question_index = (
                    0  # Reset for the next difficulty level or topic
                )

            self.consecutive_correct, self.consecutive_incorrect = (
                0,
                0,
            )  # Reset counters for the next topic

        self.show_results()

    def update_state(self):
        """Save the current state of the test to a file."""
        state = {
            "results": self.results,
            "questions": self.loaded_questions,
            "current_topic_index": self.current_topic_index,
            "current_question_index": self.current_question_index,
            "consecutive_correct": self.consecutive_correct,
            "consecutive_incorrect": self.consecutive_incorrect,
        }
        with open(self.state_file, "w") as file:
            yaml.dump(state, file)

    def show_results(self):
        """Show test results."""
        print("\nTest Completed. Here are your results:\n")
        for topic, data in self.results.items():
            print(f"Topic: {topic}")
            levels_passed = ", ".join(map(str, data["passed_levels"])) or "None"
            print(f"Levels Passed: {levels_passed}")
            for level, correct in data["correct_answers"].items():
                print(f"Level {level} Correct Answers: {correct}")
            print("\n")


def to_snake_case(s):
    """Convert a string to snake case, also replacing spaces and dashes."""
    s = s.replace(" ", "_").replace("-", "_")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def generate_test_name():
    """Generate a unique, human-friendly name for the test."""
    adjectives = ["mighty", "curious", "speedy", "brave", "smart"]
    nouns = ["eagle", "panda", "rabbit", "lion", "fox"]
    number = randint(1, 99)
    return f"{choice(adjectives)}-{choice(nouns)}-{number}"


def load_questions(excluded_topics=None, included_topics=None):
    """Load questions from JSON files in the data directory."""
    if excluded_topics is not None and included_topics is not None:
        raise ValueError(
            "Either excluded_topics or included_topics should be provided, but not both."
        )

    if excluded_topics is not None:
        excluded_topics = [to_snake_case(topic) for topic in excluded_topics]
    if included_topics is not None:
        included_topics = [to_snake_case(topic) for topic in included_topics]

    topics = []
    files = Path("./data").glob("*.json")
    for file in files:
        with open(file, "r") as f:
            topic_data = json.load(f)
            topic = to_snake_case(topic_data.get("topic", ""))
            if included_topics is not None:
                if topic in included_topics:
                    topics.append(topic_data)
            elif excluded_topics is not None:
                if topic not in excluded_topics:
                    topics.append(topic_data)
            elif included_topics is None and excluded_topics is None:
                topics.append(topic_data)

    return topics


@click.group()
def cli():
    """Knowledge Test CLI"""
    pass


@cli.command(help="List all available topics.")
def list_topics():
    topics = load_questions()
    print("Available Topics:")
    for topic in topics:
        print(f"- {topic['topic']}")


@cli.command(help="Start the knowledge test.")
@click.option(
    "--exclude",
    help="Specify topics to exclude from the test, separated by commas.",
    multiple=True,
)
@click.option(
    "--include",
    help="Specify topics to include on the test, separated by commas.",
    multiple=True,
)
@click.option(
    "--name",
    help="Specify the name for a test",
)
def start(exclude, include, name):
    excluded_topics = (
        {topic.strip() for t in exclude for topic in t.split(",")} if exclude else None
    )
    included_topics = (
        {topic.strip() for t in include for topic in t.split(",")} if include else None
    )
    topics_data = load_questions(excluded_topics, included_topics)
    if not topics_data:
        print("No topics found with the specified criteria.")
        return

    test_name = name if name is not None else generate_test_name()
    test = KnowledgeTest(topics_data, test_name)
    test.run_test()


@cli.command(help="Resume a test by test name.")
@click.option("--name", help="Specify the name for a test", required=True)
def resume(name):
    if os.path.exists(f"{name}_state.yaml"):
        topics_data = (
            load_questions()
        )  # Load all topics to ensure test can resume correctly
        test = KnowledgeTest(topics_data, name)
        test.run_test()
    else:
        print(f"No saved test with the name '{name}' found.")


if __name__ == "__main__":
    cli()
