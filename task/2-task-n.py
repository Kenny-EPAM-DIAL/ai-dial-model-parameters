from task.app.main import run

"""
Task 2: Demonstrate the `n` parameter.

The `n` parameter controls how many chat completion choices are generated
for each input message. After starting the script, ask for example:

User message: "Why is the snow white?"

You can then compare the different choices returned in a single response.
"""

run(
    deployment_name="gpt-4o",   # You can also try: "claude-3-7-sonnet@20250219", "gemini-2.5-pro"
    print_only_content=False,   # Set to True if you want only the content printed
    n=3,                        # Number of completion choices (1–5 as per task instructions)
)
