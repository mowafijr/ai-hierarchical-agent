from groq import Groq

class LLMClient:
    def __init__(self, config):
        self.client = Groq(api_key=config["groq_api_key"])
        self.model = config["groq_model"]

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content