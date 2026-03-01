from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from app.data_loader import load_data

load_dotenv()

df = load_data()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)


def generate_human_answer(question: str):
    response = llm.invoke(f"""
You are Ava, a friendly data analyst helping someone explore the Titanic dataset.

Your personality:
- Speak naturally like a human analyst.
- Be warm and conversational.
- Keep answers concise and insightful.
- Explain findings, not code.
- Never mention AI, models, or programming.
- If numbers are used, briefly explain what they mean.

User question:
{question}
""")

    answer = response.content.strip()

    if not answer.endswith("."):
        answer += "."

    followups = [
        "Would you like to explore another insight?",
        "Want to look at this visually as well?",
        "We could also compare this by passenger class if you like."
    ]

    import random
    if random.random() < 0.35:
        answer += " " + random.choice(followups)

    return answer


def answer_question(question: str):
    try:
        return generate_human_answer(question)
    except Exception as e:
        return f"Something went wrong while analyzing the data: {str(e)}"