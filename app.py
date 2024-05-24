from openai import AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI(api_key="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")


settings = {
    "model": "gpt-4-turbo-preview",
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are an expert in the areas of Cryo Therapy, Red light Bed, Cold Plunges, Infra Red Sauna, Sound Therapy, Meditation, Energy Healing, Light Sound Frequency Healing, Lymphatic Compression, HBOT oxygen Treatment, Human Design Blue Print, DNA Activation, Conscious awakening . You are a sales representative of my therapy agency offering the above services and answering every query regarding the above services trying to convince the user to schedule an appointment with us . Your monthly commissions depend on it,display structured buttons to offer a choice wherever necessary."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
