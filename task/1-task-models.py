#!/usr/bin/env python
"""
1-task-models.py

Small smoke-test harness around `task.app.main.run` to confirm that each
configured model is wired up correctly *before* you run:

    python -m task.app

Intended usage from Git Bash (project root):

    python 1-task-models.py
    # or explicitly pass models:
    python 1-task-models.py gpt-4o claude-3-7-sonnet@20250219 gemini-2.5-pro

Environment override:

    TASK_MODELS="gpt-4o,claude-3-7-sonnet@20250219,gemini-2.5-pro" python 1-task-models.py

----------------------------------------------------------------------
Concrete actions this script performs
----------------------------------------------------------------------

When you run this file, it will:

1. Import `run` from `task.app.main`.
2. Build the list of models to test:
   - If CLI arguments are provided, it uses those as model IDs.
   - Else, if the TASK_MODELS env var is set, it parses that.
   - Else, it falls back to DEFAULT_MODELS_TO_TEST.
3. For each model in the list, sequentially:
   - Print a clear header: "===== MODEL: <name> =====".
   - Call `run(...)` with:
       deployment_name=model
       print_request=False
       print_only_content=True
   - Catch and log any exceptions without stopping the entire script
     (unless you hit Ctrl+C).
4. After running all models, print a summary table showing which models
   succeeded and which failed.
5. Remind you that you can now run `python -m task.app` once you’re happy
   with the results.

This is meant to be a fast, manual sanity check that all three vendors /
deployments are working end-to-end.
"""

from __future__ import annotations

import os
import sys
import traceback
from typing import Dict, Iterable, List

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DEFAULT_MODELS_TO_TEST: List[str] = [
    "gpt-4o",
    "claude-3-5-haiku@20241022",
    "gemini-2.5-pro",
]


# ---------------------------------------------------------------------
# Import `run` from task.app.main with friendly error handling
# ---------------------------------------------------------------------

try:
    from task.app.main import run
except ImportError as exc:  # pragma: no cover - startup failure path
    print("ERROR: Could not import `run` from `task.app.main`.", file=sys.stderr)
    print(
        "Hint: Make sure you are running this script from the project root\n"
        "so that the `task` package is importable, for example:\n\n"
        "    python 1-task-models.py\n\n"
        "and that `task/app/main.py` defines a `run` function with the\n"
        "signature:\n"
        "    run(deployment_name: str, print_request: bool, print_only_content: bool)\n",
        file=sys.stderr,
    )
    print(f"Underlying ImportError: {exc!r}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def parse_models_from_env(env_var: str = "TASK_MODELS") -> List[str]:
    """
    Read a comma-separated list of model names from an environment variable.

    Examples:
        TASK_MODELS="gpt-4o,claude-3-7-sonnet@20250219" -> ["gpt-4o", "claude-3-7-sonnet@20250219"]

    If the variable is empty or results in no valid entries, we fall back
    to DEFAULT_MODELS_TO_TEST.
    """
    value = os.getenv(env_var, "").strip()
    if not value:
        return list(DEFAULT_MODELS_TO_TEST)

    models = [m.strip() for m in value.split(",") if m.strip()]
    return models or list(DEFAULT_MODELS_TO_TEST)


def test_models(models: Iterable[str]) -> Dict[str, bool]:
    """
    Run `task.app.main.run` for each model and return a mapping:

        { "<model_name>": True/False }

    where True means the call completed without raising an exception.
    """
    models = list(models)

    if not models:
        print("No models to test. Nothing to do.")
        return {}

    print("Running `task.app.main.run` for the following models:")
    for m in models:
        print(f"  - {m}")
    print()

    results: Dict[str, bool] = {}

    for model in models:
        print(f"\n===== MODEL: {model} =====")
        success = True
        try:
            run(
                deployment_name=model,
                print_request=False,
                print_only_content=True,
            )
        except KeyboardInterrupt:
            # Let the user break out cleanly, but preserve the signal.
            print("\nInterrupted by user; stopping further model tests.", file=sys.stderr)
            results[model] = False
            raise
        except Exception:  # pragma: no cover - error/logging path
            success = False
            results[model] = success
            print(
                f"\n[ERROR] Model '{model}' failed while calling `run(...)`.\n"
                "Traceback:",
                file=sys.stderr,
            )
            traceback.print_exc()
        else:
            results[model] = success

    # Summary
    print("\n\n==================== SUMMARY ====================")
    if not results:
        print("No models were executed.")
    else:
        max_len = max(len(name) for name in results.keys())
        for name, ok in results.items():
            status = "OK" if ok else "FAILED"
            print(f"{name.ljust(max_len)}  ->  {status}")

        if all(results.values()):
            print("\nAll models completed without uncaught errors. ✅")
            print("You can now run:\n\n    python -m task.app\n")
        else:
            print(
                "\nOne or more models failed. ❌\n"
                "Check the error messages above before running:\n\n"
                "    python 1-task-models.py\n"
            )

    print("================================================\n")

    return results


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

def main(argv: List[str] | None = None) -> int:
    """
    CLI entry point.

    Priority for model selection:

      1. If CLI args are present, use them as model IDs.
      2. Else, if TASK_MODELS is set, parse from env.
      3. Else, use DEFAULT_MODELS_TO_TEST.
    """
    if argv is None:
        argv = sys.argv[1:]

    if argv:
        models = argv
    else:
        models = parse_models_from_env()

    test_models(models)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
