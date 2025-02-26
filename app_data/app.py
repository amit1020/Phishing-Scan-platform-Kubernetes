from web import Create_App


app = Create_App()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234 ,debug=True)

