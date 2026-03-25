"""CLI-entrypoint för projektet."""

from __future__ import annotations

from pathlib import Path

from mlops_multiagent.graph import build_graph


def _ask_bool(question: str) -> bool:
    """Ställer en enkel ja/nej-fråga."""
    answer = input(question).strip().lower()
    return answer == "ja"


def _collect_user_input() -> dict[str, object]:
    """Samlar in användarens input via terminalen."""
    print("=" * 80)
    print("CV Match Flow")
    print("=" * 80)

    cv_path = input("Ange sökväg till CV (.pdf eller .docx): ").strip()
    location = input("Önskad arbetsort: ").strip()
    employment_type = input("Önskad arbetstid (heltid/deltid): ").strip().lower()
    languages = input("Språk (valfritt, separera med kommatecken): ").strip()
    drivers_license = _ask_bool("Har du körkort? (ja/nej): ")
    commute_willingness = input("Pendlingsvilja (valfritt, t.ex. 'ja, 30 min'): ").strip()

    return {
        "cv_path": cv_path,
        "location": location,
        "employment_type": employment_type,
        "languages": languages,
        "drivers_license": drivers_license,
        "commute_willingness": commute_willingness,
    }


def main() -> None:
    """Kör hela LangGraph-flödet från terminalen."""
    try:
        user_input = _collect_user_input()
        cv_path = Path(str(user_input["cv_path"]))

        if not cv_path.exists():
            print(f"\nFel: Filen finns inte: {cv_path}")
            return

        graph = build_graph()

        initial_state = {
            "user_input": user_input,
        }

        final_state = graph.invoke(initial_state)

        print("\n" + "=" * 80)
        print("SLUTRESULTAT")
        print("=" * 80)
        print(final_state.get("final_recommendation", "Ingen rekommendation genererades."))

        hitl = final_state.get("hitl", {})
        if hitl.get("wants_contact"):
            print("\nTack! Kontaktuppgifter registrerade:")
            print(f"Namn: {hitl.get('name', '')}")
            print(f"E-post: {hitl.get('email', '')}")
        else:
            print("\nIngen personlig kontakt vald. Flödet avslutas.")

    except KeyboardInterrupt:
        print("\nAvbrutet av användaren.")
    except Exception as exc:
        print(f"\nEtt oväntat fel uppstod: {exc}")


if __name__ == "__main__":
    main()