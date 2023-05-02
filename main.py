from fastapi import FastAPI
from routers.ram_usage import router
import uvicorn


TAGS_META = [
    {
        "name": "Ram_Usage",
        "description": "Get a number and return record",
    }]
app = FastAPI(title="Ram Usage",
              description="Get a number and return record",
              version="0.1.0",
              openapi_tags=TAGS_META,
              docs_url="/api/v1/docs")
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
