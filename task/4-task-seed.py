from task.app.main import run

"""
Task 4: Demonstrate the `seed` parameter.

`seed` makes the model's output more deterministic for the same parameters.
Combined with `n`, you can see that multiple choices tend to repeat.

Suggested user message:
"Name a random animal"
"""

run(
    deployment_name="gpt-4o",
    print_only_content=False,
    seed=42,   # Any integer works; using 42 as a common example
    n=5,       # Generate multiple choices to see the effect of the seed
)
