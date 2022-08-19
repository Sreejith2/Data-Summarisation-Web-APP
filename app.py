import requests
from flask import Flask,render_template,url_for,request
import os
app=Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route('/Summerize',methods=["GET","POST"])
def Summarize():
    if request.method=="POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}

        data = request.form["data"]
        maxL = int(request.form["maxL"])
        minL = maxL//4

        def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })
        return render_template("index.html", result=output[0]["summary_text"])
    else:
        return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
