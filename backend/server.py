from flask import Flask, request, jsonify
import regression
import scraping
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/salary")
def salary():
    desired_player = request.args.get("desired_player")
    desired_player_year = request.args.get("desired_player_year")
    desired_year = request.args.get("desired_year")
    
    salary = regression.calculate_salary(desired_player, desired_player_year, desired_year)
    
    return str(salary)

@app.route("/names", methods=['GET'])
def names():
    year = request.args.get("desired_player_year")
    return scraping.get_player_names(year)

if __name__ == "__main__":
    app.run(port=5100)