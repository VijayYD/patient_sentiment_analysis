import os
import google.genai as genai
from google.genai import Client, types # Import GenerativeModel directly
import json

# --- Configuration ---
# Ensure your API key is set as an environment variable: GEMINI_API_KEY
try:
    # We still keep the Client for potential future use or other API calls,
    # but for direct GenerativeModel instantiation, it might not be strictly needed for this specific use case.
    # However, it's good practice to initialize it to ensure API key setup is handled.
    client = Client()

    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable not set.")

except (KeyError, ValueError) as e:
    print(f"Error initializing Google GenAI client: {e}")
    print("Please ensure your Gemini API key is set as an environment variable (GEMINI_API_KEY).")
    print("Refer to the documentation or previous instructions on how to set environment variables.")
    exit()

# Choose the Gemini Flash model
MODEL_NAME = "gemini-1.5-flash" # Or "gemini-pro" for potentially higher quality but slower/pricier

# --- Sentiment Analysis Function ---
def analyze_patient_feedback_sentiment(feedback_text: str) -> dict:
    """
    Analyzes the sentiment of patient feedback using the Gemini Flash SDK.
    """

    if not feedback_text or not isinstance(feedback_text, str):
        return {"sentiment": "N/A", "reason": "Invalid feedback text provided."}

    prompt = f"""
    You are an AI assistant specialized in analyzing patient feedback from outbound calls.
    Your task is to determine the sentiment of the provided patient feedback and provide a brief reason for that sentiment.
    Classify the sentiment as 'positive', 'negative', or 'neutral'.
    Provide the output in a JSON format with two keys: "sentiment" and "reason".

    Patient Feedback: "{feedback_text}"

    JSON Output:
    """

    try:
        # FIX: Directly instantiate GenerativeModel with the model name
        #model = client.models.g(MODEL_NAME)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    parts=[
                        types.Part(text=prompt)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )

        try:
            sentiment_data = json.loads(response.text)
            return sentiment_data
        except json.JSONDecodeError:
            return {"sentiment": "error", "reason": f"Could not parse JSON: {response.text}"}

    except Exception as e:
        return {"sentiment": "error", "reason": f"An error occurred: {e}"}

# --- Example Usage ---

if __name__ == "__main__":
    patient_feedbacks = [
        "The nurse was incredibly helpful and understanding. I felt much better after the call.",
        "I waited on hold for almost 20 minutes just to schedule an appointment. This is unacceptable.",
        "The doctor explained the procedure clearly, and I appreciate the follow-up.",
        "They just called to remind me about my upcoming appointment. No specific feedback on the call itself.",
        "I'm really frustrated with the billing department. My last bill was incorrect, and it's taking forever to resolve.",
        "Everything was fine, thank you for checking in."
    ]

    print("--- Analyzing Patient Feedback ---")
    for i, feedback in enumerate(patient_feedbacks):
        print(f"\nFeedback {i+1}: \"{feedback}\"")
        sentiment_result = analyze_patient_feedback_sentiment(feedback)
        print(f"Sentiment: {sentiment_result.get('sentiment', 'N/A')}")
        print(f"Reason: {sentiment_result.get('reason', 'N/A')}")
        print("-" * 30)

    short_feedback = "Okay."
    print(f"\nFeedback: \"{short_feedback}\"")
    sentiment_result = analyze_patient_feedback_sentiment(short_feedback)
    print(f"Sentiment: {sentiment_result.get('sentiment', 'N/A')}")
    print(f"Reason: {sentiment_result.get('reason', 'N/A')}")
    print("-" * 30)