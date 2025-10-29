from app import create_app
print("App running on http://127.0.0.1:5000")
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
