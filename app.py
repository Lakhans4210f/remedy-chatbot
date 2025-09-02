from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# -------------------------
# Load and prepare CSV data
# -------------------------
df = pd.read_csv('cep.csv')
df.columns = df.columns.str.strip()
df['condition'] = df['condition'].str.lower()
df = df.drop_duplicates(subset=['condition', 'remedy_name', 'ingredients', 'steps'])

# -------------------------
# Chatbot logic
# -------------------------
def get_remedies(user_input):
    user_input = user_input.lower()
    for condition in df['condition'].unique():
        if condition in user_input:
            results = df[df['condition'] == condition]
            response = ""
            for _, row in results.iterrows():
                response += f"Remedy: {row['remedy_name']}<br>"
                if pd.notna(row['ingredients']):
                    response += f"Ingredients: {row['ingredients']}<br>"
                if pd.notna(row['steps']):
                    response += f"Steps: {row['steps']}<br>"
                response += "<br>"
            return response
    return "Sorry, I don't have a remedy for that condition."

# -------------------------
# Flask routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    reply = ""
    user_message = ""
    if request.method == "POST":
        user_message = request.form["message"]
        reply = get_remedies(user_message)
    return render_template("index.html", reply=reply, user_message=user_message)

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
