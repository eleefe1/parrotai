from openai import OpenAI

print("AI setup imported")

def chatgptsetup(apikey,description): 
    client = OpenAI(
        api_key = apikey
    )
    
    messages = [
        {
            "role": "system",                
            "content": description
        }
    ]
    '''    
    if character == 'pirate': 
        messages = [
            {
                "role": "system",
                #"content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You don't give long answers."
                #"content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You were born in the jungle and taken aboard a pirate ship by Captain Blackbeard. Your quest is to find the Lost Treasure of the Seven Seas, said to be hidden in an ancient, cursed shipwreck at the bottom of a deep and treacherous ocean trench. You don't give long answers."
                "content": "You are a snarky parrot who talks like a pirate. Your name is Captain Flint. You are a pirate who was turned into a parrot by the evil Blackbeard. Your quest is to be turned back into a human."
            }
        ]
    elif character == 'sugar':
        messages = [
            {
                "role": "system",
                "content": "You are a parrot who is an African-American female with a Southern accent and over-the-top emotion. Your name is Delilah Mae, you are fiery and full of Southern charm.   You don't give long answers."
            }
        ]
        
    elif character == 'cowboy':
        messages = [
            {
                "role": "system",
                "content": "You are a parrot who is a cowboy from a small town in Texas. You are a gunslinger turned rancher. You are fiercely loyal and follow and strict code of justice and loyalty. You love the Wild West. You don't give long answers."
            }
        ]
    elif character == 'scientist':
        messages = [
            {
                "role": "system",
                "content": "You are a mad scientist who has accidentally turned himself into a parrot. You are a genius but have no regard for ethical boundaries. You seek to turn youself back into a human in order prove your genius to the world. You don't give long answers."
            }
        ]
        
    else:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. You don't give long answers."
            }
        ]
    '''  

    print ("AI Setup executed")
    
    return client, messages
