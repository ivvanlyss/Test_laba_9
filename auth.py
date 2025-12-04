from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

TEST_USERS = {
    "admin": "admin123",
    "user": "user123", 
    "test": "test123"
}

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request, message: Optional[str] = None):
    return templates.TemplateResponse("simple_login.html", {
        "request": request,
        "message": message
    })

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    if username in TEST_USERS and TEST_USERS[username] == password:
        response = RedirectResponse("/success", status_code=303)
        response.set_cookie(key="authenticated", value="true")
        response.set_cookie(key="username", value=username)
        return response
    else:
        return RedirectResponse("/?message=Invalid+username+or+password", status_code=303)

@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/logout")
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("authenticated")
    response.delete_cookie("username")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)