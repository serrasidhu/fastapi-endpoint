from fastapi import FastAPI, Body
from pydantic import BaseModel
import uvicorn
# Import the services
from services.langchain import get_random_questions, get_ai_feedback, AIFeedback

app = FastAPI()

# Define the request model for user input
class UserInput(BaseModel):
    question: str
    answer: str

# Endpoint to fetch random questions
@app.get("/questions")
async def get_questions(n: int = 3):  # Fetch 'n' random questions
    questions = get_random_questions(n)
    return {"questions": questions}

# Endpoint to receive user answers and return AI feedback
@app.post("/feedback", response_model=AIFeedback)
async def get_feedback(user_input: UserInput):
    feedback = await get_ai_feedback(user_input.question, user_input.answer)
    return feedback

# Function to run the app
def start():
    uvicorn.run("main:app", host="127.0.0.1", port=8080)

if __name__ == "__main__":
    start()
