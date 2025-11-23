from task.app.main import run

"""
Task 8: Demonstrate the `stop` parameter.

`stop` tells the model to stop generating when it hits certain substrings.
This can be a single string or a list of strings.

Suggested user message:
"Explain the key components of a Large Language Model architecture"

Below, we stop on:
- a double newline (paragraph break)
- specific section titles that might appear in a structured answer
"""

run(
    deployment_name="gpt-4o",
    print_only_content=True,
    stop=[
        "\n\n",
        "**Embedding Layer**",
        "**Transformer Blocks**",
        "**Training**",
    ],
)
