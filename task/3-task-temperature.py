from task.app.main import run

"""
Task 3: Demonstrate the `temperature` parameter.

`temperature` controls the randomness / creativity of the output.
Range: 0.0–2.0 (default 1.0).

Suggested user message:
"Describe the sound that the color purple makes when it's angry"
"""

run(
    deployment_name="gpt-4o",
    print_only_content=True,
    temperature=0.3,  # Lower value -> more deterministic, higher -> more creative
    # You can experiment manually by changing to e.g. 0.9 or even 2.1
)
