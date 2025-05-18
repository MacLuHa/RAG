import tiktoken
import random

encoding = tiktoken.get_encoding("cl100k_base")

tokens = encoding.encode("Тестовое разбиение на токены")

print(tokens)

print(len(tokens))

print(encoding.decode(tokens))

random_tokens = []

for i in range(16):
    random_tokens.append(random.randrange(0,10000))

print(encoding.decode(random_tokens))