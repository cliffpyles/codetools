import click
import json
import os
import re
import yaml
from pathlib import Path
from random import randint, choice, shuffle

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


def generate_test_name():
    """Generate a unique, human-friendly name for the test."""
    adjectives = ["mighty", "curious", "speedy", "brave", "smart"]
    nouns = ["eagle", "panda", "rabbit", "lion", "fox"]
    number = randint(1, 99)
    return f"{choice(adjectives)}-{choice(nouns)}-{number}"


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
        """Load test state from file, or initialize state if file does not exist."""
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
        print(f"\nTest Name: {self.test_name}\n")
        for topic in self.loaded_questions[self.current_topic_index :]:
            self.process_topic(topic)
        self.show_results()

    def process_topic(self, topic):
        """Process a single topic within the test."""
        self.current_topic_index = self.loaded_questions.index(topic)
        current_topic_results = self.results[topic["topic"]]
        print(f"Topic: {topic['topic']}\n")

        for difficulty_level in range(1, 6):
            if difficulty_level in current_topic_results["passed_levels"]:
                continue  # Skip difficulty level if already passed

            difficulty_level_name = DIFFICULTY_LEVEL_NAMES[difficulty_level]
            print(f"Difficulty Level: {difficulty_level_name}\n")
            self.process_difficulty_level(
                topic, difficulty_level, current_topic_results
            )

        self.current_question_index = 0  # Reset for the next topic
        self.reset_consecutive_counters()

    def process_difficulty_level(self, topic, difficulty_level, current_topic_results):
        """Process questions for a specific difficulty level within a topic."""
        questions = [
            q for q in topic["questions"] if q["difficulty"] == difficulty_level
        ]
        shuffle(questions)  # Shuffle questions for randomness

        for question in questions[self.current_question_index :]:
            self.current_question_index = questions.index(question)
            self.process_question(
                topic, question, difficulty_level, current_topic_results
            )

            if self.check_thresholds():
                break

        self.update_state_after_level_or_topic(current_topic_results, difficulty_level)

    def process_question(
        self, topic, question, difficulty_level, current_topic_results
    ):
        """Process a single question, prompting the user and updating counters."""
        choice_info = next(
            item for item in topic["choices"] if item["question_id"] == question["id"]
        )
        print(
            f"{topic['topic']} ({DIFFICULTY_LEVEL_NAMES[difficulty_level]}): {question['question']}\n"
        )
        for k, choice in enumerate(choice_info["choices"], start=1):
            print(f"{k}. {choice}")
        print("5. I don't know\n6. Proceed to next topic")

        answer = click.prompt("\nYour answer", type=int, show_choices=False)
        print("")
        self.update_counters(
            answer, choice_info, difficulty_level, current_topic_results
        )

    def update_counters(
        self, answer, choice_info, difficulty_level, current_topic_results
    ):
        """Update consecutive counters based on the user's answer."""
        if answer == 5:
            self.consecutive_incorrect += 1
        elif answer == 6:
            self.reset_consecutive_counters()
        elif answer - 1 == choice_info["answer"]:
            self.consecutive_correct += 1
            self.consecutive_incorrect = 0
            current_topic_results["correct_answers"][difficulty_level] += 1
        else:
            self.consecutive_incorrect += 1
            self.consecutive_correct = 0
        self.update_state()

    def check_thresholds(self):
        """Check if consecutive correct or incorrect answers have reached their thresholds."""
        if self.consecutive_incorrect >= CONSECUTIVE_FAIL_THRESHOLD:
            self.reset_consecutive_counters()
            print("(failed)\n")
            return True
        elif self.consecutive_correct == CONSECUTIVE_PASS_THRESHOLD:
            self.reset_consecutive_counters()
            print("(passed)\n")
            return True
        return False

    def update_state_after_level_or_topic(
        self, current_topic_results, difficulty_level
    ):
        """Update the state when advancing levels or finishing a topic."""
        if self.consecutive_correct >= CONSECUTIVE_PASS_THRESHOLD:
            current_topic_results["passed_levels"].append(difficulty_level)
        self.reset_consecutive_counters()
        self.update_state()

    def reset_consecutive_counters(self):
        """Reset consecutive correct and incorrect counters."""
        self.consecutive_correct, self.consecutive_incorrect = 0, 0

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
        """Display the test results."""
        print("\nTest Completed. Here are your results:\n")
        for topic, data in self.results.items():
            print(f"Topic: {topic}")
            levels_passed = ", ".join(map(str, data["passed_levels"])) or "None"
            print(f"Levels Passed: {levels_passed}")
            for level, correct in data["correct_answers"].items():
                print(f"Level {level} Correct Answers: {correct}")
            print("\n")


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
@click.option("--name", help="Specify the name for a test")
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

    test_name = name if name else generate_test_name()
    test = KnowledgeTest(topics_data, test_name)
    test.run_test()


@cli.command(help="Resume a test by test name.")
@click.option("--name", help="Specify the name for a test", required=True)
def resume(name):
    if os.path.exists(f"{name}_state.yaml"):
        topics_data = load_questions()  # Load all topics to ensure correct resumption
        test = KnowledgeTest(topics_data, name)
        test.run_test()
    else:
        print(f"No saved test with the name '{name}' found.")


if __name__ == "__main__":
    cli()
