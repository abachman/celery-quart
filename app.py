from dotenv import load_dotenv
from quart import render_template

from src.create_app import create_app

load_dotenv()
app = create_app()


@app.route("/", methods=["GET"])
async def home():
    return await render_template("home.html")


@app.get("/chat")
@app.get("/chat/<conversation_id>")
async def chat(conversation_id: str = None):
    return await render_template("chat.html", conversation_id=conversation_id)


if __name__ == "__main__":
    app.run()
