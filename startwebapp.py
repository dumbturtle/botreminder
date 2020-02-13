from webapp import creat_app

if __name__ == "__main__":
    app = creat_app()
    app.run(host='0.0.0.0', debug=True)
