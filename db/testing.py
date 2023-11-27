from cs50 import SQL
from flask import Flask, request, jsonify, render_template, url_for

testing = Flask(__name__)
db = SQL("sqlite:///blood_tests.db")

@testing.route("/search/<int:patientID>")
def search(patientID):
    blood_tests = db.execute("SELECT * FROM blood_indicators WHERE ID = ?", patientID)
    return blood_tests

if __name__ == '__main__':
    testing.run(debug=True)
