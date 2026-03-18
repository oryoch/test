from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>初期費用計算ツール</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<div class="container mt-5">
    <div class="card p-4 shadow">
        <h2 class="mb-4 text-center">初期費用計算ツール</h2>

        <form method="post">
            <div class="mb-3">
                <label class="form-label">家賃</label>
                <input name="yachin" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">敷金(月)</label>
                <input name="shikikin" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">礼金(月)</label>
                <input name="reikin" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">保証料(%)</label>
                <input name="hoshou" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">前家賃</label>
                <select name="mae" class="form-select">
                    <option value="1">1ヶ月</option>
                    <option value="2">2ヶ月</option>
                </select>
            </div>

            <div class="mb-3">
                <label class="form-label">仲介手数料</label>
                <select name="chukai" class="form-select">
                    <option value="1">通常</option>
                    <option value="2">20%オフ</option>
                    <option value="3">50%オフ</option>
                    <option value="4">22000円</option>
                </select>
            </div>

            <div class="mb-3">
                <label class="form-label">鍵交換</label>
                <input name="kagi" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">消毒</label>
                <input name="shoudoku" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">クリーニング</label>
                <input name="cleaning" class="form-control">
            </div>

            <div class="mb-3">
                <label class="form-label">保険</label>
                <input name="hoken" class="form-control">
            </div>

            <button type="submit" class="btn btn-primary w-100">計算する</button>
        </form>

        {% if total %}
        <div class="alert alert-success mt-4 text-center">
            <h4>合計: {{ total }}円</h4>
            <h5>約 {{ man }} 万円</h5>
        </div>
        {% endif %}

    </div>
</div>

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