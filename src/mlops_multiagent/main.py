"""CLI entrypoint for the project."""

from __future__ import annotations

from pathlib import Path

from mlops_multiagent.graph import build_graph


def _ask_bool(question: str) -> bool:
    """Asks a simple yes/no question."""
    answer = input(question).strip().lower()
    return answer == "yes"


def _collect_user_input() -> dict[str, object]:
    """Collects user input via the terminal."""
    print("=" * 80)
    print("CV Match Flow")
    print("=" * 80)

    cv_path = input("Enter path to CV (.pdf or .docx): ").strip()
    location = input("Preferred work location: ").strip()
    employment_type = input("Preferred employment type (full-time/part-time): ").strip().lower()
    languages = input("Languages (optional, separate with commas): ").strip()
    drivers_license = _ask_bool("Do you have a driver's license? (yes/no): ")
    commute_willingness = input("Commute willingness (optional, e.g. 'yes, 30 min'): ").strip()

    return {
        "cv_path": cv_path,
        "location": location,
        "employment_type": employment_type,
        "languages": languages,
        "drivers_license": drivers_license,
        "commute_willingness": commute_willingness,
    }


def main() -> None:
    """Runs the entire LangGraph workflow from the terminal."""
    try:
        user_input = _collect_user_input()
        cv_path = Path(str(user_input["cv_path"]))

        if not cv_path.exists():
            print(f"\nError: File does not exist: {cv_path}")
            return

        graph = build_graph()

        initial_state = {
            "user_input": user_input,
        }

        final_state = graph.invoke(initial_state)

        hitl = final_state.get("hitl", {})
        if hitl.get("wants_contact"):
            print("\nThank you! Contact details registered:")
            print(f"Name: {hitl.get('name', '')}")
            print(f"Email: {hitl.get('email', '')}")
        else:
            print("\nNo personal contact selected. The workflow is now complete.")

    except KeyboardInterrupt:
        print("\nInterrupted by the user.")
    except Exception as exc:
        print(f"\nAn unexpected error occurred: {exc}")


if __name__ == "__main__":
    main()