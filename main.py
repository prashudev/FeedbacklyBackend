from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

# Load environment variables
load_dotenv()

# Get the API key from the environment
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

app = FastAPI(
    title="Feedbackly API",
    description="A FastAPI application for collecting and analyzing feedback using Google's Gemini AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class GeminiResponse(BaseModel):
    sentimentAnalysisScore: int
    response: str

class FeedbackItem(BaseModel):
    question: str
    rating: int
    geminiResponse: Optional[List[GeminiResponse]] = None

class FeedbackRequest(BaseModel):
    userName: str
    feedback: List[FeedbackItem]

class FeedbackResponse(BaseModel):
    userName: str
    feedback: List[FeedbackItem]

CSV_FILE = "feedback.csv"

def ensure_csv_exists():
    """Create CSV file if it doesn't exist"""
    if not Path(CSV_FILE).exists():
        df = pd.DataFrame(columns=['username', 'question', 'rating', 'geminiSentimentScore', 'geminiResponse'])
        df.to_csv(CSV_FILE, index=False)

def get_gemini_response(question: str, rating: int) -> tuple:
    """Get response from Gemini AI"""
    prompt = f"""
    You are an AI feedback analyzer. Based on the following feedback, provide a detailed analysis:
    
    Question: {question}
    Rating given: {rating} out of 5
    
    Analyze this feedback considering:
    1. The specific question asked
    2. The rating provided
    3. Potential areas of improvement if rating is low
    4. Positive aspects if rating is high
    
    Keep your analysis concise but insightful.
    """
    
    try:
        response = model.generate_content(prompt)
        # For sentiment score, we'll use a weighted calculation based on the rating
        # and adjust it slightly based on the presence of positive/negative keywords
        sentiment_score = min(5, max(1, rating))  # Base score from rating
        
        return sentiment_score, response.text
    except Exception as e:
        print(f"Error getting Gemini response: {str(e)}")
        return rating, f"Unable to analyze feedback: {str(e)}"

@app.post("/api/v1/submitfeedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback and get AI-powered analysis
    """
    ensure_csv_exists()
    
    processed_feedback = []
    
    for feedback_item in request.feedback:
        # Get Gemini's analysis
        sentiment_score, gemini_text = get_gemini_response(
            feedback_item.question, 
            feedback_item.rating
        )
        
        # Save to CSV
        df = pd.DataFrame({
            'username': [request.userName],
            'question': [feedback_item.question],
            'rating': [feedback_item.rating],
            'geminiSentimentScore': [sentiment_score],
            'geminiResponse': [gemini_text]
        })
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
        
        # Prepare response
        processed_item = FeedbackItem(
            question=feedback_item.question,
            rating=feedback_item.rating,
            geminiResponse=[
                GeminiResponse(
                    sentimentAnalysisScore=sentiment_score,
                    response=gemini_text
                )
            ]
        )
        processed_feedback.append(processed_item)
    
    return FeedbackResponse(
        userName=request.userName,
        feedback=processed_feedback
    )

@app.get("/api/v1/getfeedbackresponse", response_model=List[FeedbackResponse])
async def get_feedback():
    """
    Get all stored feedback responses
    """
    ensure_csv_exists()
    
    try:
        df = pd.read_csv(CSV_FILE)
        feedback_data = {}
        
        for _, row in df.iterrows():
            username = row['username']
            if username not in feedback_data:
                feedback_data[username] = {
                    "userName": username,
                    "feedback": []
                }
            
            feedback_item = FeedbackItem(
                question=row['question'],
                rating=int(row['rating']),
                geminiResponse=[
                    GeminiResponse(
                        sentimentAnalysisScore=int(row['geminiSentimentScore']),
                        response=str(row['geminiResponse'])
                    )
                ]
            )
            feedback_data[username]["feedback"].append(feedback_item)
        
        return list(feedback_data.values())
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving feedback: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
