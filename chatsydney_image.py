from rich.console import Console
from rich.markdown import Markdown

def print_markdown(md_text):
    console = Console()
   
    console.print(Markdown(md_text))



import asyncio

from sydney import SydneyClient

import tkinter as tk
from tkinter import filedialog

def pick_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        initialdir="Pictures",
        #remove the above, if needed
        title="Select a local graphics file, as no URI provided as argument in the !image prompt",
        filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
    )
    return file_path

async def main() -> None:
    async with SydneyClient() as sydney:
        while True:
            prompt = input("User: ")

            if prompt == "!reset":
                await sydney.reset_conversation()
                continue
            elif prompt == "!exit":
                break


            # Check if the prompt starts with "!image"
            if prompt.startswith("!image"):
                # Split the prompt into three parts: the "!image" keyword, the URI, the prompt
                _, uri, prompt = prompt.split(maxsplit=2)

                # Check if the URI starts with "http"
                if not uri.startswith("http"):
                    # If not, assume it's a local file and show the file picker
                    uri = pick_file()
                    print ("\033[2mSelected:\033[1m", uri, "\033[5m Wait for image upload...\033[0m \n")

                
                print("Sydney: ", end="", flush=True)
                # Pass the URI and the prompt as the parameters
                response=await sydney.ask(prompt, attachment=uri)
                print_markdown(response)
                #Or:
                '''
                async for response in sydney.ask_stream(prompt, attachment=uri):
                    
                    print(response, end="", flush=True)
                    '''
                    


            else:
                # Use the ask_stream method as before
                print("Sydney: ", end="", flush=True)
                
                response=await sydney.ask(prompt)
                print_markdown(response)
                 #Or:
                '''               
                async for response in sydney.ask_stream(prompt):
                    print(response, end="", flush=True)
                    '''
                    
            
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
