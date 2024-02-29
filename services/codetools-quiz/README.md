# Codetools Quiz README

## Why - The Purpose

Codetools Quiz is designed for personal evaluation, helping test takers pinpoint their strengths and weaknesses in software and IT knowledge. It acts as a roadmap, guiding users in understanding their position within the technical landscape. It's aimed at fostering a culture of self-awareness and directed learning in the technology field.

## How - The Process

The quiz employs a multiple-choice format for easy self-assessment, accessible through a CLI interface. Future updates will introduce a web-based application and a public API for broader access. To prepare for testing, users need to generate test data with the `GenerateTestData.ipynb` notebook, which requires an `OPENAI_API_KEY`. The `SimulateTests.ipynb` notebook offers test simulations and visual feedback on performance.

### Getting Started

1. **Install Dependencies**: Use the Pipfile in the project root to install necessary dependencies.
2. **Generate Test Data**: Execute the `GenerateTestData.ipynb` notebook to create questions and answers.
3. **Simulate and Visualize Tests**: The `SimulateTests.ipynb` provides simulations and visual analytics of test results.

### Using the CLI

- **List Topics**: `cli.py list-topics` shows all topics available for testing.
- **Start a Test**: `cli.py start [--include <topics>] [--exclude <topics>] [--name <test name>]` initiates a new test.
- **Resume a Test**: `cli.py resume --name <test name>` continues a previously started test.

Add `--help` for more details on command usage, e.g., `cli.py start --help`.

## What - The Features

- **Customizable Tests**: Select specific topics to assess.
- **Progress Tracking**: Pick up tests at your convenience.
- **Feedback for Improvement**: Gain insights from performance analytics.

## Appropriate Uses

- **Self-Evaluation**: To understand your knowledge level and identify areas for improvement.
- **Learning Path Guidance**: To map out areas in the tech landscape where you need further study or practice.
- **Skill Development**: To track progress over time as you learn and grow in specific technical areas.

## Inappropriate Uses

- **Certification or Credentialing**: This quiz is not designed to certify expertise or knowledge for professional purposes.
- **Evaluating Others**: It is not suitable for assessing the knowledge or competence of other individuals.
- **True Comprehension Testing**: The quiz focuses on breadth and familiarity rather than in-depth understanding of subjects.

By keeping these appropriate and inappropriate uses in mind, users can effectively leverage the Codetools Quiz to support their learning journey in the field of technology.