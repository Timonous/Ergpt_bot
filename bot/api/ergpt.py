import logging
import httpx
from typing import Optional

from settings import config

# api_token = config.TOKEN

async def get_assistants(api_token, limit = 10) -> Optional[str]:
    api_url = "https://er-gpt.ru/api/v2/assistant"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "limit": limit
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logging.error(f"Error: {e}")
    return None


async def create_ergpt_chat(assistant_id: int, api_token: str) -> Optional[str]:
    api_url = "https://er-gpt.ru/api/v2/chat"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {"assistant_id": assistant_id}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get('id')
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

async def send_ergpt_message(chat_id: int, msg: str, api_token: str) -> Optional[str]:
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
            return response.json().get('message')
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

async def get_ergpt_message(chat_id: int, api_token: str) -> Optional[str]:
    api_url = f"https://er-gpt.ru/api/v2/chat/{chat_id}/messages"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, headers=headers)
            response.raise_for_status()
            # получаем историю запросов
            return response.json().get('messages')

    except Exception as e:
        logging.error(f"Error: {e}")
    return None

async def update_ergpt_chat_name(chat_id: int, new_name: str, api_token: str) -> Optional[bool]:
    api_url = f"https://er-gpt.ru/api/v2/chat/{chat_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": new_name,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.patch(api_url, json=payload, headers=headers)
            response.raise_for_status()
            return True
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

async def regenerate_ergpt_response(chat_id: int, api_token: str) -> Optional[str]:
    api_url = f"https://er-gpt.ru/api/v2/chat/{chat_id}/regenerate"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(api_url, headers=headers)
            response.raise_for_status()
            # получаем новый ответ нейронки
            return response.json().get('message')
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

async def delete_ergpt_chat(chat_id: int, api_token: str) -> Optional[bool]:
    api_url = f"https://er-gpt.ru/api/v2/chat/{chat_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(api_url, headers=headers)
            response.raise_for_status()
            return True
    except Exception as e:
        logging.error(f"Error: {e}")
    return None