from gpt4all import GPT4All
model = GPT4All("mistral-7b-openorca.Q4_0.gguf",) # device='amd', device='intel'
output = model.generate("The capital of France is ", max_tokens=3)
print(output)