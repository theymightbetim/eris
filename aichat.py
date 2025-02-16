import ollama

def list_models():
    ollama_list: object = ollama.list()
    models = []
    for model in ollama_list.models:
        models.append((model.model))
    print(models)

def stream_chat(model='deepseek-r1:latest', message="What can I ask you?"):
    messages = [
        {
            'role': 'user',
            'content': message
        }
    ]
    for chunk in ollama.chat(model, messages=messages, stream=True):
        print(chunk['message']['content'], end='', flush=True)
    print()

def send_chat(model='llama3.1:latest', message="What can I ask you?"):
    response = ollama.chat(model, messages=[
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