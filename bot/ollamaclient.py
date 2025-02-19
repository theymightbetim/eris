import ollama


class OllamaClient:
    def __init__(self, model, system):
        self._model = model
        self._system = system
        self.models = self.list_models()

    def set_model(self, model):
        if model in self.models:
            self._model = model
            return True
        return False

    def set_system(self, system):
        self._system = system

    @staticmethod
    def list_models():
        ollama_list = ollama.list()
        models = []
        for model in ollama_list.models:
            models.append(model.model)
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
        for chunk in ollama.chat(self._model, messages=messages, stream=True):
            print(chunk['message']['content'], end='', flush=True)
        print()

    def send_chat(self, message="What can I ask you?"):
        response = ollama.chat(self._model, messages=[
            {
                'role': 'system',
                'content': self._system,
            },
            {
                'role': 'user',
                'content': message,
            }
        ])
        return response['message']['content']
