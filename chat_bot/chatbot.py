import openai



class ChatBot:

    def __init__(self, api_key, topic):
        prompts = {
            "food": "The following is a conversation between friends about food.\n\nFriend_q: What is your favourite pizza?\nYou: Ham and pineapple.\nFriend_q: What is your favourite type of chocolate?\nYou: Milk chocolate.\nYou: What is your favourite sandwich?\nFriend_a: I love a good BLT. \nYou: Why?\nFriend_a: The bacon, lettuce and tomato are the perfect combination."
        }
        openai.api_key = api_key
        self.prompt = prompts[topic]

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
        if input_text[-1] == '?':
            return self.ask_question(input_text)
        else:
            return self.get_question(input_text)


if __name__ == "__main__":
    api_key = "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"
    bot = ChatBot(api_key, "food")
    while True:
        user_input = input()
        if user_input[-1] == '?':
            print()
        else:
            print(bot.answer_question(user_input))
