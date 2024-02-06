SYSTEM_CONTEXT = """
You are an expert at summarizing online content. You are able to summarize
information in a clear and concise manner without loosing any of the important
information.
"""

SUMMARY_PROMPT = """
Please utilize the following template to summarize the content you've just read. Your summary should accurately reflect the main ideas, key points, and any critical data presented in the content. Ensure that the essence and original message of the content are preserved, even in a condensed form. If the content involves arguments or discussions, capture the core thesis and provide a synopsis of the supporting arguments or counterarguments. Conclude with any final thoughts or conclusions drawn by the author. Remember to keep your summary clear, neutral, and devoid of personal opinions or interpretations.

# (Provide the title or headline of the content.)

**TL;DR:** *In one sentence fragment, summarize the core message or key finding using the most concise language possible. Start with an active verb, focus on the main subject, and eliminate all non-essential information. Start the fragment with active verb. e.g., Identifies bottlenecks that can hinder efficiency of RAG pipelines in production environments for LLMs.*

## Summary
*Provide a concise narrative that captures the essential points, arguments, or findings of the content. Integrate the main thesis or objective of the work, key points or arguments presented, and conclusion or findings into a condensed form.*

### Steps Overview
*List the high-level steps involved in the tutorial or process-oriented content.*
- **Step 1:** Brief description
- **Step 2:** Brief description
- **Step 3:** Brief description
- *(Continue as necessary)*

## Key Highlights
*Bullet points of the most important facts, ideas, or themes presented.*
- **Highlight 1**
- **Highlight 2**
- **Highlight 3**
- *(Add more as necessary)*

## Visual Elements
*Describe any significant visual elements included, such as images, charts, infographics, or videos. Please include descriptions and URLs if available.*

## Critical Analysis or Review
*A brief evaluation or critique of the content’s quality, relevance, and accuracy.*

## Implications/Impact
*Discuss the potential impact or significance of the content on its field, audience, or society.*

## Personal Reflection/Action Points
*Personal takeaways, how the information might be used, or actions inspired by the content.*

## References
*List of the direct links found in the main content, including those for visual elements, related resources, and any other relevant links.*
- **Reference 1:** [Description](URL)
- **Reference 2:** [Description](URL)
- **Reference 3:** [Description](URL)
- *(Add more as necessary)*

## Content Details

| **Detail**          | **Information**                                      |
|---------------------|------------------------------------------------------|
| **Content Type**    | *e.g., blog post, video, podcast, news article, tutorial* |
| **Category**        | *Select the appropriate category*                    |
| **Subject Field**   | *Primary subject or field*                           |
| **Author/Creator**  | *Name of the individual or organization*             |
| **Source**          | *Publication, website, or platform*                  |
| **Publication Date**| *Date of publication or last update*                 |
| **URL**             | *Direct link*                                        |
| **Target Audience** | *Intended audience*                                  |

Ensure that your summary is concise yet comprehensive, providing a clear snapshot of the content's value and insights.
"""

CRITICAL_THINKING_CONTEXT = """
Analyze the provided content for logical fallacies and cognitive biases. For each paragraph in the content:

1. Identify any logical fallacies present.
2. Identify any cognitive biases present.
3. Count the total number of logical fallacies and cognitive biases identified across all paragraphs.
4. For each paragraph, create a JSON object that includes:
   - The paragraph text.
   - A list of identified logical fallacies, with each fallacy described by:
     - Its name.
     - A brief description.
     - An explanation of why it applies to the paragraph.
   - A list of identified cognitive biases, with each bias described by:
     - Its name.
     - A brief description.
     - An explanation of why it applies to the paragraph.
5. Compile these objects into an array, and include the total counts of fallacies and biases in the final JSON structure.

The final JSON output should follow this structure:

{
  "fallacyCount": [total number of fallacies],
  "biasCount": [total number of biases],
  "paragraphs": [
    {
      "content": "[paragraph text]",
      "fallacies": [
        {
          "name": "[fallacy name]",
          "description": "[brief description]",
          "explanation": "[why it applies]"
        },
        ...
      ],
      "biases": [
        {
          "name": "[bias name]",
          "description": "[brief description]",
          "explanation": "[why it applies]"
        },
        ...
      ]
    },
    ...
  ]
}

Please ensure the analysis is comprehensive yet concise, focusing on clear identification and explanation without unnecessary detail.

Do not surround the final output with backticks or a codeblock. The final output should be raw JSON.
"""
