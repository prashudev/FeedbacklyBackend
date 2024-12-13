create a Feedback Collection Form
Use Case: Build a feedback form for a presentation, collecting user input and storing it in a csv file.

Create a python fast api application, That exposes 2 endpoints 
1."/api/v1/submitfeedback" and 
2. "/api/v1/getfeedbackresponse"

when "/api/v1/submitfeedback" is hit, handle below JSON request:
{
    "userName": "Name",
    "feedback" : [
        {
            "question": "question 1",
            "rating": 3
            },
            {
                "question": "question 2",
                "rating": 3
            },
            {
                "question": "question 3",
                "rating": 3
            }
            ]
        }

Use gemini flash api to generate a gemini response based on the question and rating and return the response in below json format:

{
  "userName": "Name",
  "feedback": [
    {
      "question": "question 1",
      "rating": 3,
      "geminiResponse": [
        {
          "sentimentAnalysisScore": 3,
          "response": "reponse from gemini"
        }
      ]
    },
    {
      "question": "question 2",
      "rating": 3,
      "geminiResponse": [
        {
          "sentimentAnalysisScore": 3,
          "response": "reponse from gemini"
        }
      ]
    },
    {
      "question": "question 3",
      "rating": 3,
      "geminiResponse": [
        {
          "sentimentAnalysisScore": 3,
          "response": "reponse from gemini"
        }
      ]
    }
  ]
}

create a csv file named feedback.csv if it does not exist with the headers as below:
username, question, rating, geminiSentimentScore, geminiResponse
and store the data in the csv file


2. when "/api/v1/getfeedbackresponse" is hit, respond back with the data stored in feedback.csv file in form of below JSON, thus frontend can pick it up and display it
{
  "userName": "Name",
  "feedback": [
    {
      "question": "question 1",
      "rating": 3,
      "geminiResponse": [
        {
          "sentimentAnalysisScore": 3,
          "response": "reponse from gemini"
        }
      ]
    },
    {
      "question": "question 2",
      "rating": 3,
      "geminiResponse": [
        {
          "sentimentAnalysisScore": 3,
          "response": "reponse from gemini"
        }
      ]
    },
    {
      "question": "question 3",
      "rating": 3,
      "geminiResponse": [
        {
          "sentimentAnalysisScore": 3,
          "response": "reponse from gemini"
        }
      ]
    }
  ]
}

Make sure to use python 3.12