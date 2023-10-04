from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def hello_test():
    return {'hello':'Zuzanna'}