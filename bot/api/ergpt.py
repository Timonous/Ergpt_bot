import logging
import httpx
from typing import Optional
from bot.repository.chats_repository import get_outdated_chats, set_chat_deleted
from bot.repository.group_chats_repository import get_outdated_group_chats, set_groupt_chat_deleted

from settings import config

# api_token = config.TOKEN
api_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJyUDRNaDZ3TGhJTm9HbWpwTG1ONU15UzItMGM4OXpPQ2VNMV9aVUVlN0NZIn0.eyJleHAiOjE3NDk5NTAyNzAsImlhdCI6MTc0OTg5NjI3MCwiYXV0aF90aW1lIjoxNzQ5ODk2MjcwLCJqdGkiOiJvbnJ0YWM6MzVmNzZmYzUtNWVkYy00NjFkLTgxZDktYTQ1YzQ4NWQ4OTkyIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5lci1ncHQucnUvcmVhbG1zL2VyZ3B0IiwiYXVkIjpbImJhY2tlbmQiLCJhY2NvdW50Il0sInN1YiI6ImZiOWVjMDRkLWIyMWQtNDllNC04ZTViLWM5MDg0MmExMTBjZCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZyb250ZW5kIiwic2lkIjoiNTcwZTYyOGItOWI0OC00ODYyLTk4ZGMtMTY2NDYyOTNmYTdlIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2VyLWdwdC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lcmdwdCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJ1c2VyIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYmFja2VuZCI6eyJyb2xlcyI6WyJ1c2VyIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwgb3BlbmlkIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiLQmtC40YDQuNC70LsgRGl2YW5jaGluIiwicHJlZmVycmVkX3VzZXJuYW1lIjoia2RpdmFuY2hpbiIsImdpdmVuX25hbWUiOiLQmtC40YDQuNC70LsiLCJmYW1pbHlfbmFtZSI6IkRpdmFuY2hpbiIsImVtYWlsIjoia2RpdmFuY2hpbkBlZHUuaHNlLnJ1In0.IMMc25TPyIQutKM60on01QhVXyZnbFkBn1IZEW9cFWmCQl23bzlIMxmN9o24WPa2SJqMEN7D43X2eTFb9CbjGIO3pkA9imdaLbvDWJ8GsIlQ6Fe6n-9eyKyZVnGtTvrM-N4XW7mVFW5BwHXWE4jIsEHEp5gtjc_9M_7l_Zd2rmhvhRsmaKQZgeK91kPvYsq1CiG7K5WvOb7fbvHvuGvz8Q0KuAfNyudD0IrtKTpFYGQ6g-d_IYGGUZ8LmTKkwHkl7SzRtHQiD2Tq7T5Ug11OSUzSRqfotZHSHTIw92JH03kNK0T4dULtCTUVYiQKh5z5tzoP6Xo_YZCvpP-KMbHYkg"

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
    group_outdated_chats = await get_outdated_group_chats()
    if outdated_chats:
        for chat in outdated_chats:
            result = await delete_ergpt_chat(chat['chat_id'])
            if result is not None:
                await set_chat_deleted(chat['user_id'])
                logging.info(f"Чат ({chat['chat_id']}) был автоматически удалён.")
            else:
                logging.error(f"Ошибка при автоматическом удалении чата ({chat['chat_id']}).")
    if group_outdated_chats:
        for group_chat in group_outdated_chats:
            result = await delete_ergpt_chat(group_chat['chat_id'])
            if result is not None:
                await set_groupt_chat_deleted(group_chat['group_id'])
                logging.info(f"Групповой чат ({group_chat['chat_id']}) был автоматически удалён.")
            else:
                logging.error(f"Ошибка при автоматическом удалении группового чата ({group_chat['chat_id']}).")