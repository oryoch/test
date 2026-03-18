from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>初期費用計算</title>
</head>
<body>
    <h2>初期費用計算ツール</h2>
    <form method="post">
        家賃：<input name="yachin"><br>
        敷金（月）：<input name="shikikin"><br>
        礼金（月）：<input name="reikin"><br>
        保証料（%）：<input name="hoshou"><br>

        前家賃：
        <select name="mae">
            <option value="1">1ヶ月</option>
            <option value="2">2ヶ月</option>
        </select><br>

        仲介手数料：
        <select name="chukai">
            <option value="1">通常</option>
            <option value="2">20%オフ</option>
            <option value="3">50%オフ</option>
            <option value="4">22000円</option>
        </select><br>

        鍵交換：<input name="kagi"><br>
        消毒：<input name="shoudoku"><br>
        クリーニング：<input name="cleaning"><br>
        保険：<input name="hoken"><br>

        <button type="submit">計算</button>
    </form>

    {% if total %}
        <h3>合計：{{ total }}円（約{{ man }}万円）</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    total = None
    man = None

    if request.method == "POST":
        yachin = int(request.form["yachin"])
        shikikin = int(request.form["shikikin"])
        reikin = int(request.form["reikin"])
        hoshou = float(request.form["hoshou"])
        mae = int(request.form["mae"])

        chukai_choice = request.form["chukai"]

        if chukai_choice == "1":
            chukai = yachin * 1.1
        elif chukai_choice == "2":
            chukai = yachin * 1.1 * 0.8
        elif chukai_choice == "3":
            chukai = yachin * 1.1 * 0.5
        else:
            chukai = 22000

        kagi = int(request.form["kagi"])
        shoudoku = int(request.form["shoudoku"])
        cleaning = int(request.form["cleaning"])
        hoken = int(request.form["hoken"])

        total = (
            yachin * mae +
            yachin * shikikin +
            yachin * reikin +
            yachin * (hoshou / 100) +
            chukai + kagi + shoudoku + cleaning + hoken
        )

        man = round(total / 10000, 1)

    return render_template_string(HTML, total=int(total) if total else None, man=man)

import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)