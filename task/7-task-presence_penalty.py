from task.app.main import run

"""
Task 7: Demonstrate the `presence_penalty` parameter.

Positive values encourage the model to introduce new topics rather than
sticking only to what was already mentioned; higher values -> more topic
diversity.

Range: -2.0 to 2.0 (default 0.0)

Suggested user message:
"What is an entropy in LLM's responses?"
"""

run(
    deployment_name="gpt-4o",
    print_only_content=True,
    presence_penalty=1.5,  # Experiment with 0.0, 1.5, and 2.0 to see differences
)
