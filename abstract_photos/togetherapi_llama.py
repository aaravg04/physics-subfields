from gradio_client import Client
TOKEN = "<insert_token_here>"
client = Client("togethercomputer/Llama-3.2-Vision-Free")
result = client.predict(
		message={"text":"","files":[]},
		history=[],
		together_api_key=TOKEN,
		max_new_tokens=300,
		temperature=0.7,
		api_name="/bot_streaming"
)
print(result)