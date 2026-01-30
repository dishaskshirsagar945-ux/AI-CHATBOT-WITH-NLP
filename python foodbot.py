import nltk
import string
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("punkt")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

menu = {
    "pizza": 250,
    "burger": 120,
    "pasta": 180,
    "sandwich": 100,
    "coffee": 80,
    "tea": 50
}

order = {}

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

def extract_quantity(text):
    match = re.search(r'\b\d+\b', text)
    if match:
        return int(match.group())
    return 1

def chatbot_response(user_input):
    tokens = preprocess(user_input)

    
    if "menu" in tokens:
        menu_text = "🍽 Our Menu:\n"
        for item, price in menu.items():
            menu_text += f"{item.title()} - Rs {price}\n"
        return menu_text

    for item in menu:
        if item in tokens:
            qty = extract_quantity(user_input)
            order[item] = order.get(item, 0) + qty
            return f"✅ {qty} {item}(s) added to your order."

    if "order" in tokens or "bill" in tokens:
        if not order:
            return "🛒 Your order is empty."

        total = 0
        summary = "🧾 Order Summary:\n"
        for item, qty in order.items():
            price = menu[item] * qty
            total += price
            summary += f"{item.title()} x {qty} = Rs {price}\n"

        summary += f"\n💰 Total Bill: Rs {total}"
        return summary

    
    if "checkout" in tokens or "pay" in tokens:
        if not order:
            return "You have not ordered anything."
        return "🎉 Order placed! Thank you for visiting."


    if "bye" in tokens or "exit" in tokens or "quit" in tokens:
        return "👋 Goodbye! Have a nice day."

    return "❓ I didn't understand. Type 'menu' to see items."


print("🍽 Welcome to FoodBot!")
print("Type 'menu' to see available items.")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        print("Bot: Goodbye!")
        break

    response = chatbot_response(user_input)
    print("Bot:", response)
