import ollama


class OllamaClient():
    def __init__(self, model):
        self.model = model
        self.models = self.list_models()

    def set_model(self, model):
        if model in self.models:
            self.model = model
            return True
        return False

    def list_models(self):
        ollama_list: object = ollama.list()
        models = []
        for model in ollama_list.models:
            models.append((model.model))
        return models

    def pull_model(self, model):
        try:
            ollama.pull(model)
            self.set_model(model)
            return ""
        except Exception as e:
            print(e)

    def stream_chat(self, message="What can I ask you?"):
        messages = [
            {
                'role': 'user',
                'content': message
            }
        ]
        for chunk in ollama.chat(self.model, messages=messages, stream=True):
            print(chunk['message']['content'], end='', flush=True)
        print()

    def send_chat(self, message="What can I ask you?"):
        response = ollama.chat(self.model, messages=[
            {
                'role': 'user',
                'content': message
            }
        ])
        return response['message']['content']

    if __name__ == "__main__":
        list_models()
        stream_chat()
        send_chat()