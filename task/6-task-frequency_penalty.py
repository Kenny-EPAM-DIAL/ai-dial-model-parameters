from task.app.main import run

"""
Task 6: Demonstrate the `frequency_penalty` parameter.

Positive values penalize tokens that have already appeared, reducing exact
repetitions. Negative values encourage repetition.

Range: -2.0 to 2.0 (default 0.0)

Suggested user message:
"Explain the water cycle in simple terms for children"
"""

run(
    deployment_name="gpt-4o",
    print_only_content=True,
    frequency_penalty=1.2,  # Try 0.0, 1.2, and -1.0 manually to compare behavior
)
