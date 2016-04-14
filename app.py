import json
import os
import data_handler as dh
from flask import Flask, request, render_template

app = Flask(__name__)

TEMPS = {
  "January": [
    {"date": "01-28-2009", "temp": "0"}, 
    {"date": "01-27-2010", "temp": "35"}, 
    {"date": "01-26-2011", "temp": "-5"},
    {"date": "01-25-2012", "temp": "65"},
    {"date": "01-23-2013", "temp": "0"},
    {"date": "01-29-2014", "temp": "15"},
    {"date": "01-25-2015", "temp": "22"},
    {"date": "01-26-2016", "temp": "40"}
  ],
  "February": [
    {"date": "02-28-2009", "temp": "30"},
    {"date": "02-27-2010", "temp": "35"},
    {"date": "02-26-2011", "temp": "-2"},
    {"date": "02-25-2012", "temp": "60"},
    {"date": "02-23-2013", "temp": "0"},
    {"date": "02-29-2014", "temp": "15"},
    {"date": "02-25-2015", "temp": "22"},
    {"date": "02-26-2016", "temp": "40"}
  ],
  "March": [
    {"date": "03-28-2009", "temp": "30"},
    {"date": "03-27-2010", "temp": "35"},
    {"date": "03-26-2011", "temp": "40"},
    {"date": "03-25-2012", "temp": "55"},
    {"date": "03-23-2013", "temp": "10"},
    {"date": "03-29-2014", "temp": "15"},
    {"date": "03-25-2015", "temp": "22"},
    {"date": "03-26-2016", "temp": "70"}
  ]
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    json_data = json.dumps(TEMPS)
    return json_data


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
