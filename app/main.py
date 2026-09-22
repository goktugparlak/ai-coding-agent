from app.agent import CodingAgent


def main() -> None:

    agent = CodingAgent()

    print("AI Coding Agent")
    print(f"Provider: {agent.provider.name}")

    if agent.provider.llm_connected:
        print(f"Model: {agent.provider.model}")

    print("Type 'exit' to quit.")

    while True:

        message = input("\nYou: ").strip()

        if message.lower() in {
            "exit",
            "quit",
        }:
            print("Agent: Goodbye!")
            break

        response = agent.run(message)

        print(
            f"\nAgent:\n{response}"
        )


if __name__ == "__main__":
    main()