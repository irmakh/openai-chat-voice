from helpers.memory_helper import run_garbage_collection

def generate(user_prompt: str, content: str, client, config) -> str:
    """
    Run the chat model based on the user's prompt and generate a response.

    Args:
        user_prompt (str): The user's prompt to generate a response from

    Returns:
        str: The generated response
    """
    

    run_garbage_collection()
    completion = client.chat.completions.create(
        model=config["chat_model_name"],
        messages=[
            {
                "role": "system", 
                "content": content
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ],
        temperature=0.7
    )

    answer = completion.choices[0].message.content
    run_garbage_collection()

    return answer