import logging
import httpx
from typing import Optional
from bot.repository.chats_repository import get_outdated_chats, set_chat_deleted

from settings import config

# api_token = config.TOKEN
api_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJyUDRNaDZ3TGhJTm9HbWpwTG1ONU15UzItMGM4OXpPQ2VNMV9aVUVlN0NZIn0.eyJleHAiOjE3NDk4NzIxMjYsImlhdCI6MTc0OTgxODEyNiwiYXV0aF90aW1lIjoxNzQ5ODE4MTI2LCJqdGkiOiJvbnJ0YWM6ZTg3ZjY0NWQtYzI4Yi00ODEwLTkyZDgtYTIxMzY5ODIzMWIzIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5lci1ncHQucnUvcmVhbG1zL2VyZ3B0IiwiYXVkIjpbImJhY2tlbmQiLCJhY2NvdW50Il0sInN1YiI6ImZiOWVjMDRkLWIyMWQtNDllNC04ZTViLWM5MDg0MmExMTBjZCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZyb250ZW5kIiwic2lkIjoiZGI5ZDdmMzYtZjNmYS00NzQwLTkwYTgtZTI1NTkwNDZhYzA2IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2VyLWdwdC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lcmdwdCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJ1c2VyIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYmFja2VuZCI6eyJyb2xlcyI6WyJ1c2VyIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwgb3BlbmlkIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiLQmtC40YDQuNC70LsgRGl2YW5jaGluIiwicHJlZmVycmVkX3VzZXJuYW1lIjoia2RpdmFuY2hpbiIsImdpdmVuX25hbWUiOiLQmtC40YDQuNC70LsiLCJmYW1pbHlfbmFtZSI6IkRpdmFuY2hpbiIsImVtYWlsIjoia2RpdmFuY2hpbkBlZHUuaHNlLnJ1In0.VYTRNgvq0HAEgbW1tFG-Uky67FG6c-6aFfyuvJGb9B_d4hrgUtXV8azqh_1cLyxTSIBvK0Q09pHM4C7VnNXQXEiPje7kk4Un8kIFqtsV8eDCrjABbVgz9feJsgfHOr6pXUA3HzDDct9P512xrxMBlidIX4rTp5rW1XbQWSdV-Sk7L3a6dKL1QPQFE29u4dqY7VM8VcCjzw5K_sY3g6Gl-5O7xwL3noyFiwFQw9QL2zWljlLd_mYPzNbjEF6jDfB9isWSp0xFwkjOpyUQZVeSClvSZjQDX8TUpOj5NKhbGeX63xcqDDIwbIDlz5smlpkA6nQfVGHQt7TK3YPZTO0XeQ"

async def get_assistants(limit = 10) -> Optional[str]:
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


async def create_ergpt_chat(assistant_id: int) -> Optional[str]:
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
            return response.json().get('message')
    except Exception as e:
        logging.error(f"Error: {e}")
    return None

async def get_ergpt_message(chat_id: int) -> Optional[str]:
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

async def update_ergpt_chat_name(chat_id: int, new_name: str) -> Optional[bool]:
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

async def regenerate_ergpt_response(chat_id: int) -> Optional[str]:
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

async def delete_ergpt_chat(chat_id: int) -> Optional[bool]:
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

async def daily_chats_delete():
    """
    Удаляем неактивные чаты
    """
    outdated_chats = await get_outdated_chats()
    for chat in outdated_chats:
        result = await delete_ergpt_chat(chat['chat_id'])
        if result is not None:
            await set_chat_deleted(chat['user_id'])
            logging.info(f"Чат ({chat['chat_id']}) был автоматически удалён.")
        else:
            logging.error(f"Ошибка при автоматическом удалении чата ({chat['chat_id']}).")