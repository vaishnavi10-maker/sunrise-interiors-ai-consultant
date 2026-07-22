import os
import re
import httpx

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


load_dotenv()

app = FastAPI(
    title="Sunrise Interiors AI Voice Agent"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CallRequest(BaseModel):
    phone_number: str


@app.get("/")
def root():
    return {
        "message": "Sunrise AI Voice Agent API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/calls")
async def initiate_call(request: CallRequest):

    api_key = os.getenv("BOLNA_API_KEY")
    agent_id = os.getenv("BOLNA_AGENT_ID")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="BOLNA_API_KEY is missing"
        )

    if not agent_id:
        raise HTTPException(
            status_code=500,
            detail="BOLNA_AGENT_ID is missing"
        )

    phone_number = request.phone_number.strip()

    # Normalize phone number
    phone_number = re.sub(
        r"[\s\-()]",
        "",
        phone_number
    )

    if len(phone_number) == 10 and phone_number.isdigit():
        phone_number = "+91" + phone_number

    elif (
        len(phone_number) == 11
        and phone_number.startswith("0")
    ):
        phone_number = "+91" + phone_number[1:]

    elif (
        len(phone_number) == 12
        and phone_number.startswith("91")
    ):
        phone_number = "+" + phone_number

    if not re.fullmatch(
        r"\+91[6-9]\d{9}",
        phone_number
    ):
        raise HTTPException(
            status_code=400,
            detail="Enter a valid Indian mobile number"
        )

    payload = {
        "agent_id": agent_id,
        "recipient_phone_number": phone_number
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "https://api.bolna.ai/call",
            json=payload,
            headers=headers,
            timeout=30
        )

    print("Final phone number:", phone_number)
    print("Bolna status:", response.status_code)
    print("Bolna response:", response.text)

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {
        "success": True,
        "message": "AI call initiated successfully",
        "phone_number": phone_number,
        "data": response.json()
    }