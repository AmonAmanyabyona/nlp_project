#chat_completion.py
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from config import GITHUB_TOKEN, AZURE_ENDPOINT, AZURE_MODEL

client = ChatCompletionsClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(GITHUB_TOKEN),
)

def chat_with_model(prompt):
    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage(prompt),
        ],
        temperature=1,
        top_p=1,
        model=AZURE_MODEL
    )
    return response.choices[0].message.content


def chat_with_rag(query, quotes):
    # Format retrieved quotes into context
    context_text = "\n".join(f"{q['author']}: \"{q['quote']}\"" for q in quotes)

    # Combine query and context into one prompt
    full_prompt = f"""User Query: {query}
Here are some relevant quotes from Wikiquote:\n{context_text}
Respond conversationally, referencing quotes where useful.
If No matching quotes are found say this is outside my expertise
General note: Reply with the quote in question and let the user know the author of the quote.Ensure the response is relevant to **quotes** and does not explore external philosophical, societal, or abstract concepts.
Do not ask a question at the end of the response.
"""

    response = client.complete(
        messages=[
            SystemMessage("You are a thoughtful assistant that uses quotes to enrich conversations."),
            UserMessage(full_prompt),
        ],
        temperature=1,
        top_p=1,
        model=AZURE_MODEL
    )
    return response.choices[0].message.content


# Run this only if script is executed directly
if __name__ == "__main__":
    prompt = f"What is Machine Translation?"
    response = chat_with_model(prompt)

    print("\n\n")
    print(response)