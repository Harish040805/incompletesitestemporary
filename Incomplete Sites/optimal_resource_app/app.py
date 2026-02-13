from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    try:
        x, y, l = sp.symbols("x y l")

        f = 5*x + 3*y
        g = 2*x + y - 100

        L = f + l*g

        eq1 = sp.diff(L, x)
        eq2 = sp.diff(L, y)
        eq3 = g

        sol = sp.solve([eq1, eq2, eq3], [x, y, l], dict=True)

        sol = sol[0]

        return jsonify({
            "x": float(sol[x]),
            "y": float(sol[y]),
            "lambda": float(sol[l])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
