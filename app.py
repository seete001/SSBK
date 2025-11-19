from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "1234"

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    # Save to SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO contacts (name, email, phone, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone, message))
    conn.commit()
    conn.close()
    
    #flashing the success message
    flash("Your message has been sent successfully!", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)