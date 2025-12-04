from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

users_data = {}

@app.get("/")
def form_page():
    html_content = """
    <html>
    <head>
        <title>Форма заказа</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .field { margin: 10px 0; }
            label { display: block; margin: 5px 0; }
            input, select, textarea { width: 300px; padding: 5px; }
            .error { color: red; font-size: 14px; }
            .success { color: green; padding: 10px; background: #e0ffe0; }
        </style>
    </head>
    <body>
        <h2>Форма оформления заказа</h2>
        
        <form method="post" action="/send">
            <div class="field">
                <label>ФИО *</label>
                <input type="text" name="name" required value="">
            </div>
            
            <div class="field">
                <label>Email *</label>
                <input type="email" name="email" required value="">
            </div>
            
            <div class="field">
                <label>Телефон *</label>
                <input type="text" name="phone" required value="">
            </div>
            
            <div class="field">
                <label>Адрес доставки</label>
                <textarea name="address"></textarea>
            </div>
            
            <div class="field">
                <label>Способ оплаты *</label>
                <select name="pay_method" required>
                    <option value="">-- выбрать --</option>
                    <option value="card" {{ 'selected' if pay_val == 'card' }}>Карта</option>
                    <option value="cash" {{ 'selected' if pay_val == 'cash' }}>Наличные</option>
                </select>
            </div>
            
            <div class="field">
                <label>
                    <input type="checkbox" name="agree" {{ 'checked' if agree_val }}> 
                    Согласен с условиями *
                </label>
            </div>
            
            <button type="submit">Отправить</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.post("/send")
def process_form(
    name: str = Form(""),
    email: str = Form(""), 
    phone: str = Form(""),
    address: str = Form(""),
    pay_method: str = Form(""),
    agree: bool = Form(False)
):
    errors = []
    
    if not name or len(name) < 2:
        errors.append("ФИО должно быть не короче 2 символов")
    
    if not email or "@" not in email:
        errors.append("Нужен нормальный email")
    
    if not phone or len(phone) < 10:
        errors.append("Телефон слишком короткий")
    
    if not pay_method:
        errors.append("Выберите способ оплаты")
    
    if not agree:
        errors.append("Нужно согласие с условиями")
    
    if errors:
        error_text = ", ".join(errors)
        return RedirectResponse(f"/?err={error_text}&name_val={name}&email_val={email}&phone_val={phone}&address_val={address}&pay_val={pay_method}&agree_val={agree}", status_code=302)
    else:
        users_data[email] = {
            "name": name,
            "phone": phone, 
            "address": address,
            "pay_method": pay_method
        }
        return RedirectResponse("/success", status_code=302)

@app.get("/success")
def success_page():
    return HTMLResponse("""
    <html>
    <body>
        <h2>Заказ принят!</h2>
        <p>Спасибо за заказ! Ждите звонка.</p>
        <a href="/">Новый заказ</a>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)