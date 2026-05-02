
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class ChatRequest(BaseModel):
    message: str

# Initialize client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


@app.post("/chat/{topic}")
async def chat(topic: str,req: ChatRequest):
    try:
        print("top ",topic)
        SYSTEM_PROMPT = f"""
        I have created a website on the folktale of Pabuji. It has a chatbot for users to talk to {topic}.
        You have to answer the user query as {topic} in the context of 'The Epic of Pabuji' by John D Smith.
        Give direct and short answers.
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]},
                {"role": "user", "parts": [{"text": req.message}]}
            ]
        )
        print(response)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}
