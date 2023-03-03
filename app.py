import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": generate_prompt(animal)}],
            temperature=0.8,
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """請使用正體中文(台灣) 產生關於某超級英雄動物的名稱，格式為： 超級英雄：「產生的名稱！！！」
    英雄名字例如： 
    美国队长（Captain America） ...
    钢铁侠（Iron Man） ...
    雷神（Thor） ...
    绿巨人（Hulk） ...
    黑寡妇（Black Widow） ...
    鹰眼（Hawkeye） ...
    死侍（Deadpool） ...
    毒液（Venom）

    題目是：
        動物: {}
        名字:""".format(
                animal.capitalize()
    )
