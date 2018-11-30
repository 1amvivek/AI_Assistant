from flask import Flask, render_template

app = Flask(__name__)

@app.route('/chart')
def chart():
    chart = {"Technology": 560}
    return render_template('chart.html', chart = chart)

if __name__ == '__main__':
    app.run(debug=True)
