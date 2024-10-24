import random
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAI
import os
load_dotenv()
google_gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

if google_gemini_api_key is None:
    raise ValueError("GOOGLE_GEMINI_API_KEY is not set in the environment variables.")

# Define a list of example questions
QUESTIONS = [
    "What are your strengths?",
    "Describe a challenge you faced and how you handled it.",
    "Where do you see yourself in 5 years?",
    "Why do you want to work here?",
    "Tell me about a time you worked in a team."
]

# AI feedback class (for returning feedback)
class AIFeedback(BaseModel):
    strengths: str
    weaknesses: str
    improvement_tips: str

# Function to fetch random questions
def get_random_questions(n: int):
    return random.sample(QUESTIONS, min(n, len(QUESTIONS)))

async def get_ai_feedback(question: str, answer: str) -> AIFeedback:
    prompt = f"""
        You are an AI interview coach. Based on the following question and answer, provide feedback by highlighting strengths, weaknesses, and tips for improvement.

        Question: {question}
        Answer: {answer}

        Your response should follow this format:
        Strengths: 
        Weaknesses: 
        Improvement tips:
    """

    google_gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if google_gemini_api_key is None:
        raise ValueError("GOOGLE_GEMINI_API_KEY is not set in the environment variables.")

    os.environ["GOOGLE_API_KEY"] = google_gemini_api_key
    chat = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.6)

    try:
        response = chat.invoke(prompt)  # Call without await if it's synchronous
        print("Raw Response:", response)  # Log the raw response
    except Exception as e:
        raise RuntimeError("Failed to get a response from the AI model.") from e

    lines = response.strip().split("\n")
    
    strengths = lines[1].replace("Strengths: ", "") if len(lines) > 1 else "Not provided"
    weaknesses = lines[2].replace("Weaknesses: ", "") if len(lines) > 2 else "Not provided"
    improvement_tips = lines[3].replace("Improvement tips: ", "") if len(lines) > 3 else "Not provided"

    return AIFeedback(
        strengths=strengths,
        weaknesses=weaknesses,
        improvement_tips=improvement_tips
    )