from openai import AsyncOpenAI

from settings import config

client = AsyncOpenAI(api_key=config.DEEPSEEK_API_KEY, base_url=config.DEEPSEEK_ENDPOINT)


async def call_deepseek_api(message: str) -> str:

    response = await client.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "user", "content": message}
        ],
        temperature=float(config.TEMPERATURE),
        max_tokens=int(config.MAX_TOKENS),
    )

    return response.choices[0].message.content
