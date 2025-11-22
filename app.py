from application.main import app

# for debug
# app.run(host='0.0.0.0', port=9999, debug=True)

# for build
app.run(host='0.0.0.0', port=5000, debug=False)