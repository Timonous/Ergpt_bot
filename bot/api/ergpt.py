import httpx
from typing import Optional

from settings import config

api_token = config.TOKEN

async def create_ergpt_chat(assistant_id: int) -> Optional[str]:
    api_url = "https://er-gpt.ru/api/v2/chat"


    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "assistant_id": assistant_id,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            print(result)

            # получаем id чата
            return result.get('id')

    except Exception as e:
        print(f"failed to crate chat: {e}")

        return None

async def send_ergpt_message(chat_id: int, msg: str) -> Optional[str]:
    api_url = f"https://er-gpt.ru/api/v2/chat/{chat_id}/messages"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "content": msg,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            # получаем msg ответа нейронки
            result = response.json()
            print(result)

            return result.get('message')

    except Exception as e:
        print(f"failed to send msg: {e}")

        return None