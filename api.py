import json
import os
from flask import Flask, request, render_template

app = Flask(__name__)

TEMPS = {
    'January':  {'01-28-2009': '32', '01-27-2010': '35', '01-26-2011': '40', '01-25-2012': '55', '01-23-2013': '0', '01-29-2014': '15', '01-25-2015': '22', '01-26-2016': '40'},
    'February': {'02-28-2009': '32', '02-27-2010': '35', '02-26-2011': '40', '02-25-2012': '55', '02-23-2013': '0', '02-29-2014': '15', '02-25-2015': '22', '02-26-2016': '40'},
    'March':    {'03-28-2009': '32', '03-27-2010': '35', '03-26-2011': '40', '03-25-2012': '55', '03-23-2013': '0', '03-29-2014': '15', '03-25-2015': '22', '03-26-2016': '40'},
}

@app.route('/')
def Temps():
    json_data = json.dumps(TEMPS)
    return render_template('index.html', data=json_data)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
