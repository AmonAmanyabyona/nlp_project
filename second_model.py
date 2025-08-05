import together

# 🔐 Authenticate with Together AI
client = together.Together(api_key="")

def chat_with_rag(query, quotes):
    # 🧠 Format quotes as context
    context_text = "\n".join(f"{q['author']}: \"{q['quote']}\"" for q in quotes)

    # 🗨️ Build full prompt in [INST] format
    full_prompt = f"""[INST] 
You are a friendly assistant who uses quotes from Wikiquote to enrich answers.

Here are the quotes:
{context_text}
If No matching quotes are found say this is outside my expertise
Answer this user query in a conversational tone, referencing relevant quotes when appropriate:
{query}
General note: Reply with the quote in question and let the user know the author of the quote.Ensure the response is relevant to **quotes** and does not explore external philosophical, societal, or abstract concepts.
Do not ask a question at the end of the response.
[/INST]"""

    # 🛠️ Generate response via Together API
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    return response.choices[0].message.content

# 🧪 Test case
if __name__ == "__main__":
    prompt = "What are the two biggest football clubs in English football?"
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": f"[INST] {prompt} [/INST]"}]
    )

    print("🧠 Response from Together AI LLaMA-3.3:")
    print(response.choices[0].message.content)
