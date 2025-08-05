import together


client = together.Together(api_key="")

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=[
        {
            "role": "user",
            "content": "What are some fun things to do in New York?"
        }
    ]
)

print(response.choices[0].message.content)
