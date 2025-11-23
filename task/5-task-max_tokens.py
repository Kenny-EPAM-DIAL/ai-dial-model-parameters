from task.app.main import run

"""
Task 5: Demonstrate the `max_tokens` parameter.

`max_tokens` sets the maximum length of the AI's response. When the model
hits this limit, `finish_reason` becomes "length" and the answer is
truncated.

Suggested user message:
"What is a token when we are working with LLM?"
"""

run(
    deployment_name="gpt-4o",
    print_only_content=False,
    max_tokens=10,  # Intentionally very small to clearly see truncation
)
