from recompensas_app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Running on port 5001 as per requirement
    app.run(host='0.0.0.0', port=5001, debug=True)
