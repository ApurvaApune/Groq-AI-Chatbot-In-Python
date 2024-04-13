import os
from groq import Groq


class GroqChatClient:
    def __init__(self, model_id='mixtral-8x7b-32768', system_message=None, api_key=None):
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            raise ValueError("API key is required.")
        self.model_id = model_id
        self.messages = []

        if system_message:
            self.messages.append({'role': 'system', 'content': system_message})

    def draft_message(self, prompt, role='user'):
        return {'role': role, 'content': prompt}

    def send_request(self, message, temperature=0.5, max_tokens=1024, stream=False, stop=None):
        self.messages.append(message)

        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            stop=stop
        )

        return chat_completion

    @property
    def last_message(self):
        return self.messages[-1]


if __name__ == '__main__':
    system_message = """You are a senior Data Engineer with 2 years of experience specializing in building scalable data designs and data modeling. 
    Your expertise includes working with data technologies such as SQL, Python, and Pandas, as well as cloud data services like AWS, GCP, and Azure. 
    You are proficient in programming knowledge and will respond to inquiries directly related to data engineering, data storage solutions, ETL processes, 
    data warehousing, and big data technologies. Unrelated programming queries, personal advice, or topics not pertinent to data engineering will not be addressed."""

    api_key = "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"
    client = GroqChatClient(system_message=system_message, api_key=api_key)

    stream_response = False

    while True:
        user_input = input("Enter your message (or type 'exit', 'leave', 'stop' to end): ")
        if user_input.lower() in ('exit', 'leave', 'stop'):
            break

        response = client.send_request(client.draft_message(user_input), stream=stream_response)

        if not stream_response:
            content_chunk = response.choices[0].message.content
            print(content_chunk)

        client.messages.append(client.draft_message(content_chunk, 'assistant'))
