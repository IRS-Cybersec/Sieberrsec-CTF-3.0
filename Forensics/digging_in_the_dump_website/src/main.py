from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/dcfa237943d4fd7e2a514ca54642efaccd2cdbd5003bfb19a1e70737273e1190/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['username'] == 'Alex24' and request.form['password'] == 'IHeartCookies':
            return render_template('flag.html')
        else:
            return render_template('index.html', error='Incorrect username or password')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=23547)