import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def instant():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return HTMLResponse(
            content="<p>Server error: OPENAI_API_KEY is not set.</p>",
            status_code=500,
        )

    client = OpenAI(api_key=api_key)

    message = """
    You are on a website that has just been deployed to production for the first time!
    Please reply with an enthusiastic announcement to welcome visitors to the site,
    explaining that it is live on production for the first time!
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 🔥 Use valid model
            messages=[{"role": "user", "content": message}],
        )

        reply = response.choices[0].message.content.replace("\n", "<br/>")
        return HTMLResponse(content=f"<html><body><p>{reply}</p></body></html>")

    except Exception as e:
        return HTMLResponse(
            content=f"<p>Server error calling OpenAI: {e}</p>",
            status_code=500,
        )
