from flask import Flask, request, render_template_string
import os
from pathlib import Path

app = Flask(__name__)

# Path to store data in separate /data directory
DATA_DIR = "/data"
DATA_FILE = os.path.join(DATA_DIR, "entries.txt")

# Ensure data directory exists
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get and validate form data
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()

        if not name or not age:
            return "Please provide both name and age", 400

        if not age.isdigit():
            return "Age must be a number", 400

        # Store the data
        try:
            with open(DATA_FILE, 'a') as f:
                f.write(f"Name: {name}, Age: {age}\n")
            return f"Thank you, {name}. Your data has been saved!"
        except IOError as e:
            return f"Error saving data: {str(e)}", 500

    # Show form for GET requests
    return render_template_string('''
        <!doctype html>
        <title>Data Entry Form</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 20px; }
            h1 { color: #333; }
            form { margin-top: 20px; }
            input[type="text"], input[type="number"] { padding: 8px; margin: 5px 0; width: 100%; }
            input[type="submit"] { background: #4CAF50; color: white; padding: 10px; border: none; cursor: pointer; }
            input[type="submit"]:hover { background: #45a049; }
        </style>
        <body>
            <h1>Data Entry Form</h1>
            <form method="POST">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name" required><br><br>
                
                <label for="age">Age:</label><br>
                <input type="number" id="age" name="age" required><br><br>
                
                <input type="submit" value="Submit">
            </form>
        </body>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
