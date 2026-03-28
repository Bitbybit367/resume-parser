from flask import Flask, request, render_template
import r_parser
import psycopg2

app = Flask(__name__)

# 🔗 PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="resume_db",
    user="postgres",
    password="#@TB2007#"   # 👈 replace with your password
)

cur = conn.cursor()


# 🏠 HOME ROUTE (Upload + Store)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("📂 File received")

        file = request.files['resume']

        # 🧠 Extract text
        text = r_parser.extract_text(file)

        # 📊 Extract data
        data = {
            "Name": r_parser.extract_name(text),
            "Email": r_parser.extract_email(text),
            "Phone": r_parser.extract_phone(text),
            "Skills": r_parser.extract_skills(text),
            "Education": r_parser.extract_education(text)
        }

        print("📊 Data:", data)

        # 💾 Store in DB
        cur.execute(
            "INSERT INTO candidates (name, email, phone, skills, education) VALUES (%s, %s, %s, %s, %s)",
            (
                data["Name"],
                str(data["Email"]),
                str(data["Phone"]),
                str(data["Skills"]),
                str(data["Education"])
            )
        )

        conn.commit()

        return render_template('index.html', data=data)

    return render_template('index.html')


# 🔍 SEARCH ROUTE
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print("🔍 Search triggered")

        skill = request.form['skill']

        # 🔎 Search without duplicates
        cur.execute(
            """
            SELECT DISTINCT name, email, phone, skills, education
            FROM candidates
            WHERE skills ILIKE %s
            """,
            ('%' + skill + '%',)
        )

        results = cur.fetchall()

        print("📊 Search Results:", results)

        return render_template('search.html', results=results)

    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)