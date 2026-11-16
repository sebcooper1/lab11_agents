# ollama_model.py
# Author: Sebastian Cooper

from ollama import ResponseError, chat

class OllamaModel:
    """A real AI model that runs on this computer through Ollama."""

    def __init__(self, model_name):
        """Remember which model to ask."""
        self.model_name = model_name

    def reply(self, instructions, history):
        """Send the conversation to the model. Return its reply."""
        messages = [{"role": "system", "content": instructions}]
        messages = messages + history

        try:
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            return None
        except ResponseError:
            return None

        return response.message.content

    def decide(self, instructions, history, tools):
        """Ask Ollama for either a text response or a tool request."""
        messages = [{"role": "system", "content": instructions}]
        messages.extend(self.tool_messages(history))

        try:
            response = chat(
                model=self.model_name,
                messages=messages,
                tools=tools,
            )
        except ConnectionError:
            return None
        except ResponseError:
            return None

        message = response.message

        if message.tool_calls:
            call = message.tool_calls[0]
            return {
                "tool": call.function.name,
                "arguments": call.function.arguments,
            }

        return {"text": message.content or ""}

    def tool_messages(self, history):
        """Convert chatbot history into messages Ollama understands."""
        messages = []

        for message in history:
            if message["role"] == "tool":
                messages.append({
                    "role": "tool",
                    "content": message["content"],
                })
            else:
                messages.append({
                    "role": message["role"],
                    "content": message["content"],
                })

        return messages
