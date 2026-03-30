from __future__ import annotations

import argparse

from mlops_multiagent.graph import build_graph
from mlops_multiagent.models import UserInput
from mlops_multiagent.state import FlowState


def parse_bool(value: str | None) -> bool | None:
    if value is None or value == "":
        return None

    lowered = value.strip().lower()
    if lowered in {"ja", "j", "yes", "y", "true", "1"}:
        return True
    if lowered in {"nej", "n", "no", "false", "0"}:
        return False
    return None


def collect_user_input() -> UserInput:
    parser = argparse.ArgumentParser(description="Sekventiellt multi-agent-flöde för CV-matchning")
    parser.add_argument("--cv-path", type=str)
    parser.add_argument("--location", type=str)
    parser.add_argument("--employment-type", type=str, choices=["heltid", "deltid"])
    parser.add_argument("--language", type=str, default=None)
    parser.add_argument("--driving-license", type=str, default=None)
    parser.add_argument("--commute-willingness", type=str, default=None)
    args = parser.parse_args()

    cv_path = args.cv_path or input("Ange sökväg till CV-fil (.pdf eller .docx): ").strip()
    location = args.location or input("Ange önskad arbetsort: ").strip()
    employment_type = args.employment_type or input("Ange önskad arbetstid (heltid eller deltid): ").strip().lower()
    language = args.language if args.language is not None else (input("Ange språk (valfritt, tryck Enter för att hoppa över): ").strip() or None)
    driving_license = parse_bool(args.driving_license) if args.driving_license is not None else parse_bool(input("Har du körkort? (ja/nej, valfritt): ").strip())
    commute_willingness = parse_bool(args.commute_willingness) if args.commute_willingness is not None else parse_bool(input("Kan du tänka dig att pendla? (ja/nej, valfritt): ").strip())

    return UserInput(
        cv_path=cv_path,
        location=location,
        employment_type=employment_type,
        language=language,
        driving_license=driving_license,
        commute_willingness=commute_willingness,
    )


def build_initial_state(user_input: UserInput) -> FlowState:
    return {
        "cv_path": user_input.cv_path,
        "preferences": {
            "location": user_input.location,
            "employment_type": user_input.employment_type,
            "language": user_input.language,
            "driving_license": user_input.driving_license,
            "commute_willingness": user_input.commute_willingness,
        },
        "stop_flow": False,
        "error_message": None,
        "contact_request": None,
        "debug": {},
    }


def run_hitl() -> dict[str, str] | None:
    answer = input("\nVill du bli kontaktad personligen? (ja/nej): ").strip().lower()

    if answer not in {"ja", "j"}:
        print("Flödet avslutas utan kontaktförfrågan.")
        return None

    name = input("Ange ditt namn: ").strip()
    email = input("Ange din e-postadress: ").strip()

    print(f"Tack! Kontaktuppgifter registrerade för {name} ({email}).")
    return {"name": name, "email": email}


def main() -> None:
    try:
        user_input = collect_user_input()
        graph = build_graph()
        final_state = graph.invoke(build_initial_state(user_input))

        if final_state.get("stop_flow"):
            print(final_state.get("error_message") or "Flödet stoppades.")
            return

        print("\n" + final_state["final_response"])
        contact_request = run_hitl()

        if contact_request:
            final_state["contact_request"] = contact_request

    except KeyboardInterrupt:
        print("\nKörningen avbröts av användaren.")
    except Exception as exc:
        print(f"Ett oväntat fel uppstod: {exc}")


if __name__ == "__main__":
    main()