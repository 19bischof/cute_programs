from fastapi import FastAPI, Request
import utils
app = FastAPI()
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