import os

from abc import ABC
from chatlas import ChatOpenAI, ChatAnthropic, ChatGoogle, ChatOllama
from dotenv import load_dotenv

SYSTEM_PROMPT = "Provide code-only responses, unless you are acting as a judge."

load_dotenv()

class LLMClient(ABC):
    def ask(self, question: str):
        pass

    def get_name(self):
        pass


class ClaudeClient(LLMClient):
    def __init__(self):
        claude_agent = ChatAnthropic(
            model="claude-3-5-sonnet-latest",
            system_prompt="Respond with code only unless you are told you're a judge."
        )
        self.agent = claude_agent
        self.name = "Claude Sonnet"

    def ask(self, question: str):
        response = self.agent.chat(question)
        return response.get_content()

    def get_name(self):
        return self.name


class OllamaClient(LLMClient):
    def __init__(self):
        github_agent = ChatOllama(
            model="llama3.2",
            system_prompt=SYSTEM_PROMPT
        )
        self.agent = github_agent
        self.name = "Ollama"

    def ask(self, question: str):
        response = self.agent.chat(question)
        return response.get_content()

    def get_name(self):
        return self.name


class ChatGPTClient(LLMClient):
    def __init__(self):
        openai_agent = ChatOpenAI(
            model="gpt-4o",
            system_prompt=SYSTEM_PROMPT
        )
        self.agent = openai_agent
        self.name = "ChatGPT"

    def ask(self, question: str):
        response = self.agent.chat(question)
        return response.get_content()

    def get_name(self):
        return self.name


class GeminiAgent(LLMClient):
    def __init__(self):
        google_agent = ChatGoogle(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini-2.0-flash",
            system_prompt=SYSTEM_PROMPT
        )
        self.agent = google_agent
        self.name = "Google Gemini"

    def ask(self, question: str):
        response = self.agent.chat(question)
        return response.get_content()

    def get_name(self):
        return self.name


def main():
    agents = {
        "claude": ClaudeClient(),
        "chatgpt": ChatGPTClient(),
        "gemini": GeminiAgent(),
        "ollama": OllamaClient(),
    }

    print("Available LLMs: claude, chatgpt, gemini, ollama")
    player_one_name = input("Select player 1: ").strip().lower()
    player_two_name = input("Select player 2: ").strip().lower()
    judge_name = input("Select your judge: ").strip().lower()

    player_one = agents[player_one_name]
    player_two = agents[player_two_name]
    judge = agents[judge_name]

    problem_statement = input("Enter the problem statement: ").strip()

    round_number = 1
    player_one_response = ""
    player_two_response = ""

    while True:
        print(f"\n✽ Round {round_number} ✽")

        if round_number > 1:
            player_one_prompt = f"Here's your previous solution: {player_one_response}\nYour opponent's solution: {player_two_response}\nCan you provide an improved solution that addresses any limitations in both approaches?"
            player_two_prompt = f"Here's your previous solution: {player_two_response}\nYour opponent's solution: {player_one_response}\nCan you provide an improved solution that addresses any limitations in both approaches?"
        else:
            player_one_prompt = problem_statement
            player_two_prompt = problem_statement

        print(f"\n🤖 {player_one.get_name()}'s Answer")
        player_one_response = player_one.ask(player_one_prompt)

        print(f"\n🤖 {player_two.get_name()}'s Answer")
        player_two_response = player_two.ask(player_two_prompt)

        print(f"\n✽ {judge.get_name()}'s Judgement ✽")

        judge_prompt = f"As a judge, evaluate the following solutions to this problem: {problem_statement}. " \
                 f"{player_one.get_name()}'s solution: {player_one_response}. " \
                 f"{player_two.get_name()}'s solution: {player_two_response}. " \
                 "Choose the winner based on code quality, efficiency, and correctness. Begin your response with '{winner_name} is the winner of this round!' " \
                 "followed by a detailed explanation of your decision."
        judge.ask(judge_prompt)

        continue_prompt = input("\nDo you want to continue to the next round? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            break

        round_number += 1

if __name__ == "__main__":
    main()
