from openai import OpenAI

with open('our_key.txt', 'r') as file:
    our_key = file.read()

client = OpenAI(
  api_key=our_key
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);



