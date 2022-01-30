import openai


class ChatBot:

    def __init__(self, api_key, session):
        openai.api_key = api_key
        self.session = session
        
    def api_request(self, prompt, temp=1, max_tokens=64, freq_penalty=1.21, pres_penalty=1.74):
        response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt,
        temperature=temp,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=freq_penalty,
        presence_penalty=pres_penalty,
        stop=["You:", "Friend_q:", "Friend_a:"]
        )
        return response.choices[0].text.strip()

    def ask_question(self, question):
        self.session["prompt"] += f"\nYou: {question}\nFriend_a:"
        response = self.api_request(self.session["prompt"])
        self.session["prompt"] += response
        return response

    def get_question(self, answer):
        self.session["prompt"] += f"\nYou: {answer}\nFriend_q:"
        response = self.api_request(self.session["prompt"])
        self.session["prompt"] += response
        i = 0
        while response[-1] != "?" and i < 5:
            self.session["prompt"] += f"\nFriend_q:"
            response += ' ' + self.api_request(self.session["prompt"])
            i += 1
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
    bot = ChatBot(api_key, "food", "English")
    while True:
        user_input = input()
        if user_input[-1] == '?':
            print()
        else:
            print(bot.chat(user_input))
