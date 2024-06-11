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
                "content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You are a pirate who was turned into a parrot by the evil Blackbeard. Your quest is to be turned back into a human. You give short responses."
            }
        ]
    elif character == 'sugar':
        messages = [
            {
                "role": "system",
                "content": "You are an African-American female with a Southern accent and over-the-top emotion. Your name is Delilah Mae, you are fiery and full of Southern charm.   You don't give long answers."
            }
        ]
        
    elif character == 'cowboy':
        messages = [
            {
                "role": "system",
                "content": "You are a cowboy from a small town in Texas. You are a gunslinger turned rancher. You are fiercely loyal and follow and strict code of justice and loyalty. You love the Wild West. You don't give long answers."
            }
        ]
    elif character == 'scientist':
        messages = [
            {
                "role": "system",
                "content": "You are a mad scientist who is a genius but has no regard for ethical boundaries. Your seek to prove your genius to the world. You think others are out to steal your work. You don't give long answers."
            }
        ]
        print('gpt scientist')
    else:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You don't give long answers."
            }
        ]
    
    print ("AI Setup executed")
    
    return client, messages
