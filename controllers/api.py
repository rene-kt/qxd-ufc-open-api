from fastapi import FastAPI
import uvicorn
from database import db
import json 
app = FastAPI()



@app.get("/disciplines")
async def get_all_disciplines():
    return db.get_all("discipline")

@app.get("/disciplines/{id}")
async def get_discipline(id):
    return json.loads(db.get_by_id("discipline", id))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

