from flask import Flask,jsonify,request
import os

app = Flask(__name__)
COUNTER_FILE = "/data/counter.txt"

def read_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE,"r") as f:
            return int(f.read().strip())
    else:
        return 0
    
def update_counter(counter):
    with open(COUNTER_FILE,"w") as f:
        f.write(str(counter))

@app.route("/",methods = ["GET","POST"])
def handle_request():
    counter = read_counter()
    if request.method == "POST":
        counter += 1
        update_counter(counter)
        return f"POST requests counter updated. Current count: {counter}"
    else:
        return f"Current POST requests count: {counter}"
    
@app.route("/health",methods = ["GET"])
def health_check():
    try:
        read_counter()
        return jsonify({"status":"healthy"}),200
    except Exception as e:
        return jsonify({"status":"unhealthy","reason":str(e)}),500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=False)
