import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

testdata = [
    {
        "date_of_news": "February 23, 2018",
        "title": "nGen_LUX is here",
        "hyperlink": "https://learn.colorfabb.com/ngen_lux-is-here/",
        "organizations_entity": [
            [2, "Kristaps Politis"],
        ],
    }
]


@app.route("/", methods=["GET"])
def home():
    return """<h1>News_Content_Named_Entity_Recognition</h1>
<p>A prototype API testing for LEONARD.</p>"""


@app.route("/api/v1/resources/testdata/all", methods=["GET"])
def api_all():
    return jsonify(testdata)


app.run()