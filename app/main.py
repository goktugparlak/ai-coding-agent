from app.agent import CodingAgent


def main() -> None:
    agent = CodingAgent()

    print("AI Coding Agent Prototype")
    print("Mock provider mode — no paid AI API is connected.")
    print("Type 'help' for commands or 'exit' to quit.")

    while True:
        message = input("\nYou: ").strip()

        if message.lower() in {"exit", "quit"}:
            print("Agent: Goodbye!")
            break

        response = agent.run(message)
        print(f"\nAgent:\n{response}")


if __name__ == "__main__":
    main()
