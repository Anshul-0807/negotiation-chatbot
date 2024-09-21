from flask import Flask, request, jsonify
import openai
from transformers import pipeline
import torch
import os
from dotenv import load_dotenv
import openai



app = Flask(__name__)


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is missing.")

# Sentiment Analysis Pipeline using transformers
sentiment_analyzer = pipeline("sentiment-analysis")

# Pricing Logic
initial_price = 100
min_price = 75

def adjust_price(user_price, sentiment):
    if sentiment == "POSITIVE":
        discount_factor = 0.2
    else:
        discount_factor = 0.1

    max_discount = initial_price * discount_factor
    adjusted_price = initial_price - max_discount

    if user_price < adjusted_price:
        return adjusted_price, f"That's the best deal I can offer at ${adjusted_price}."
    else:
        return user_price, f"Great! I can accept your offer of ${user_price}."

@app.route("/negotiate", methods=["POST"])
def negotiate():
    try:
        user_input = request.json.get("message")

        # Try to extract user-proposed price
        try:
            user_price = float(user_input.split()[-1])  # Assumes the price is mentioned at the end
        except ValueError:
            user_price = None

        # Analyze sentiment of the user's message
        sentiment_result = sentiment_analyzer(user_input)
        sentiment = sentiment_result[0]['label']

        # Handle price negotiation if the user mentions a price
        if user_price:
            adjusted_price, message = adjust_price(user_price, sentiment)
            chatbot_reply = f"{message} (Sentiment: {sentiment})"
        else:
            # Use OpenAI API to generate a response if no price is mentioned
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a supplier negotiating prices."},
                    {"role": "user", "content": user_input},
                ]
            )
            chatbot_reply = response["choices"][0]["message"]["content"]

        return jsonify({"reply": chatbot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


# print(torch.__version__)
# print(torch.cuda.is_available())