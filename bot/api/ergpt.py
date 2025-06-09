import logging
import httpx
from typing import Optional

from settings import config

# api_token = config.TOKEN
api_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJyUDRNaDZ3TGhJTm9HbWpwTG1ONU15UzItMGM4OXpPQ2VNMV9aVUVlN0NZIn0.eyJleHAiOjE3NDk1Mjc2MTgsImlhdCI6MTc0OTQ3MzYxOCwiYXV0aF90aW1lIjoxNzQ5NDczNjE2LCJqdGkiOiJvbnJ0YWM6ZGNhOWQ3NmYtNzhjNi00MGViLWI1MDQtMDUxODdhM2MwMGU4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5lci1ncHQucnUvcmVhbG1zL2VyZ3B0IiwiYXVkIjpbImJhY2tlbmQiLCJhY2NvdW50Il0sInN1YiI6IjRmNzQ0MWZjLTE3OGEtNGQ1Mi1hY2E4LWM1ZDBjNWZmMmMwYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZyb250ZW5kIiwic2lkIjoiNmZkZTAxZmUtM2IxZS00YTFhLThlYTQtMTUxMzg3YjA2MWRhIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2VyLWdwdC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lcmdwdCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJ1c2VyIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYmFja2VuZCI6eyJyb2xlcyI6WyJ1c2VyIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwgb3BlbmlkIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiLQlNCw0L3QuNC7IEt1bmFrYmFldiIsInByZWZlcnJlZF91c2VybmFtZSI6ImRla3VuYWtiYWV2IiwiZ2l2ZW5fbmFtZSI6ItCU0LDQvdC40LsiLCJmYW1pbHlfbmFtZSI6Ikt1bmFrYmFldiIsImVtYWlsIjoiZGVrdW5ha2JhZXZAZWR1LmhzZS5ydSJ9.SAlvPJe8J8D11YlDCnAoXnspf7VGQu_67n7TuXceg4KYwg3vyzqldihu2WU3RWdLR-j1EPIDfOdbEFiJDa1lmOPIsghVbd_CiYFy59fWjpZh0Ac7leNcQ_wXHiyAlfKy8R1Sm2cyDhmnIjjRfnU8dIaBqbZCtPbEr8KR1jzyQTUG0aNafDKh7T6zus9o6oGO-SXRDVeKKV7fRK8zxdp4paG586khsCQNP2r5G2RotgcL0nRIzpk3l8fqnu2vnkm_zfvmnnqAnWcCqZ81rZTV5gamSSHTD5NBbSdNVKVfFzg9YQIPF2mkrVXOJyZ0OV-LObySKg6WEFkwcEtnmaYTPg"

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

async def send_ergpt_message(chat_id: int, msg: str) -> Optional[str]: #, api_token: str
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