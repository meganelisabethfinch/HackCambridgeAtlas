import openai
from chat_bot import prompts


class ChatBot:

    def __init__(self, api_key, topic):
        openai.api_key = api_key
        self.prompt = prompts.get_prompt(topic)

    def api_request(self, prompt, temp=1, max_tokens=1024, freq_penalty=1.21, pres_penalty=1.74):
        response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt,
        temperature=temp,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=freq_penalty,
        presence_penalty=pres_penalty,
        stop=["You:", "Friend_a:", "Friend_q:"]
        )
        return response.choices[0].text.strip()

    def ask_question(self, question):
        self.prompt += f"\nYou: {question}\nFriend_a:"
        response = self.api_request(self.prompt)
        self.prompt += response
        return response

    def get_question(self, answer):
        self.prompt += f"\nYou: {answer}\nFriend_q:"
        response = self.api_request(self.prompt)
        self.prompt += response
        while response[-1] != "?":
            self.prompt += "\nFriend_q:"
            response += ' ' + self.api_request(self.prompt)
        return response

    def translate(self, text, source_language, target_language):
        translate_prompt = f"Translate this from {source_language} to {target_language}:\n{text}"
        response = self.api_request(translate_prompt, temp=0.3, freq_penalty=0, pres_penalty=0)
        return response

    def chat(self, input_text):
        if not input_text:
            return "Sorry, could you repeat that?"
        elif input_text[-1] == '?':
            return self.ask_question(input_text)
        else:
            return self.get_question(input_text)

if __name__ == "__main__":
    api_key = "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"
    bot = ChatBot(api_key, "lifestyle")
    while True:
        user_input = input()
        if user_input[-1] == '?':
            print()
        else:
            print(bot.chat(user_input))
