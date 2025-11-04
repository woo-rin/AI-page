from fastapi import FastAPI
from starlette.responses import RedirectResponse
from crawling import Crawling_selenium, Crawling_requests

app = FastAPI()
@app.get("/request_list")
def read_kbo_list_request():
    try:
        data = Crawling_requests()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.get("/selenium_list")
def read_kbo_list_selenium():
    try:
        data = Crawling_selenium()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# Swagger 리다이렉트
@app.get("/")
def redirect():
    return RedirectResponse(url="/docs", status_code=301)