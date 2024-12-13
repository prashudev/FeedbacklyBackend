# Feedbackly

A FastAPI application for collecting and analyzing feedback using Google's Gemini AI. This application provides endpoints for submitting feedback and retrieving feedback responses, with AI-powered sentiment analysis.

## Requirements

- Python 3.12 or higher
- Dependencies listed in `requirements.txt`

## Setup Instructions

1. Install Python 3.12 if not already installed:
   - Download from [Python Official Website](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### API Endpoints

#### 1. Submit Feedback
- **URL**: `/api/v1/submitfeedback`
- **Method**: POST
- **Request Body Example**:
  ```json
  {
    "userName": "John Doe",
    "feedback": [
      {
        "question": "How satisfied are you with the presentation?",
        "rating": 4
      }
    ]
  }
  ```

#### 2. Get Feedback Responses
- **URL**: `/api/v1/getfeedbackresponse`
- **Method**: GET
- **Returns**: List of all feedback responses with AI analysis

## Data Storage

Feedback data is stored in a CSV file (`feedback.csv`) with the following columns:
- username
- question
- rating
- geminiSentimentScore
- geminiResponse

## Features

1. **AI-Powered Analysis**: Uses Google's Gemini AI to:
   - Analyze feedback content
   - Generate sentiment scores
   - Provide detailed response analysis

2. **Data Persistence**: All feedback is stored in a CSV file for easy access and analysis

3. **OpenAPI Documentation**: Full API documentation with interactive testing capability

## Error Handling

The application includes comprehensive error handling for:
- Invalid input data
- AI service failures
- File system operations
- Data parsing issues
