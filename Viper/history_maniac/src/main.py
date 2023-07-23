from fastapi import FastAPI, Request
import utils as utils
from fastapi.staticfiles import StaticFiles
import os

try:
    os.mkdir('data')
except FileExistsError:
    pass
with open("pid.txt","w") as f:
    f.write(str(os.getpid()))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

utils.get_file()

@app.post("/append_history/")
async def append_history(request: Request):
    data = await request.json()
    url = data.get("url", "No message received.")  # Get the "message" field from the JSON data
    print('url:',url)
    utils.append_to_file(url)
    utils.upload_new_file()
    
    # Your action logic here (you can use the "message" variable)
    # For demonstration purposes, let's just return the message back to the client
    
    return {"result": True}