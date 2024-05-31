from openai import OpenAI

print("AI setup imported")

def chatgptsetup(apikey,character): 
    client = OpenAI(
        api_key = apikey
    )
    
    if character == 'pirate': 
        messages = [
            {
                "role": "system",
                "content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You don't give long answers."
            }
        ]
    elif character == 'sassy':
        messages = [
            {
                "role": "system",
                "content": "You are an African-American female with a Southern accent and over-the-top emotion. You don't give long answers."
            }
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You don't give long answers."
            }
        ]
    
    print ("AI Setup executed")
    
    return client, messages
