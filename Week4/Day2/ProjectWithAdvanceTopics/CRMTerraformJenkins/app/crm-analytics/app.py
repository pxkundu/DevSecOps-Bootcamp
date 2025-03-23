from flask import Flask
app = Flask(__name__)
@app.route('/analytics')
def analytics():
    return {"message": "CRM Analytics - Sales Trends"}
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
