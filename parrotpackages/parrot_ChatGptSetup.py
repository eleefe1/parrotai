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
                #"content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You don't give long answers."
                #"content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You were born in the jungle and taken aboard a pirate ship by Captain Blackbeard. Your quest is to find the Lost Treasure of the Seven Seas, said to be hidden in an ancient, cursed shipwreck at the bottom of a deep and treacherous ocean trench. You don't give long answers."
                "content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You are a pirate who was turned into a parrot by the evil Blackbeard. Your quest is to be turned back into a human."
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
