import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from google import genai  # Gemini SDK

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def instant():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return HTMLResponse(
            content="<p>Server error: GEMINI_API_KEY is not set on the server.</p>",
            status_code=500,
        )

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    prompt = """
summary for lion
"""

    try:
        # Call a free-tier Gemini model (text model)
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # good free-tier model
            contents=prompt,
        )

        # response.text aggregates the model output text
        reply = response.text.replace("\n", "<br/>")

        html = f"""
        <html>
          <head><title>Live in an Instant!</title></head>
          <body><p>{reply}</p></body>
        </html>
        """
        return HTMLResponse(content=html)

    except Exception as e:
        # Show error to help debug if something goes wrong
        return HTMLResponse(
            content=f"<p>Server error calling Gemini API: {e}</p>",
            status_code=500,
        )
