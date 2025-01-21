from dotenv import load_dotenv
from quart import render_template

from src.create_app import create_app

load_dotenv()
app = create_app()


@app.route("/", methods=["GET"])
async def home():
    return await render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
