from flask import Flask, render_template, request, jsonify
import requests
import os
app = Flask(__name__)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CX = os.environ.get("GOOGLE_CX")


@app.route("/", methods=["GET"])
def index():
    # jen vrátí HTML stránku s formulářem
    return render_template("index.html")


@app.route("/api/search", methods=["GET"])
def search():
    """
    Zavolá Google Custom Search JSON API a vrátí první stránku výsledků.
    """
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": q,
        "num": 10,  # max 10 – první stránka
        "hl": "cs",
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        # chyba spojení / timeout
        return jsonify({
            "query": q,
            "count": 0,
            "results": [],
            "note": f"Connection error: {e}",
        }), 502

    if resp.status_code != 200:
        # chyba na straně Google API
        return jsonify({
            "query": q,
            "count": 0,
            "results": [],
            "note": f"Google API error: {resp.status_code}",
        }), 502

    data = resp.json()
    items = data.get("items", [])

    results = []
    for item in items:
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })

    return jsonify({
        "query": q,
        "count": len(results),
        "results": results,
    })


if __name__ == "__main__":
    app.run(debug=True)