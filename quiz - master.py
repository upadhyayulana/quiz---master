from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    message = None

    if request.method == "POST":

        student_id = request.form.get("student_id", "").strip()

        if not student_id:
            message = "Please enter your Student ID."
            return render_template(
                "index.html",
                result=result,
                message=message
            )

        data = load_data()

        # Check whether this student already attempted
        if student_id in data:
            message = "This Student ID has already submitted the exam."
            return render_template(
                "index.html",
                result=result,
                message=message
            )

        # Correct answers
        correct_answers = {
            "q1": "Delhi",
            "q2": "Python",
            "q3": "CPU",
            "q4": "HTML",
            "q5": "RAM"
        }

        score = 0

        for question, correct_answer in correct_answers.items():
            answer = request.form.get(question)

            if answer == correct_answer:
                score += 1

        # Save attempt
        data[student_id] = {
            "score": score,
            "total": len(correct_answers)
        }

        save_data(data)

        result = {
            "score": score,
            "total": len(correct_answers)
        }

    return render_template(
        "index.html",
        result=result,
        message=message
    )


if __name__ == "__main__":
    app.run()
