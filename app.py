import os
import aiosqlite
import httpx
from datetime import datetime
from sanic import Sanic, response, Request
from sanic.log import logger
from jinja2 import Environment, FileSystemLoader

app = Sanic("TelegramBotService")

# --- 0. 配置区域 ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DEFAULT_CHAT_ID = os.getenv("CHAT_ID", "")
DB_PATH = "/app/data/history.db"

# 初始化 Jinja2 模板引擎
# 告诉程序，HTML 文件放在当前目录下的 templates 文件夹里
jinja_env = Environment(loader=FileSystemLoader("./templates"), autoescape=True)

def render_template(template_name, **context):
    """辅助函数：渲染 HTML 模板"""
    template = jinja_env.get_template(template_name)
    html_content = template.render(**context)
    return response.html(html_content)

# --- 1. 数据库初始化 (保持不变) ---
@app.before_server_start
async def setup_db(app, loop):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_ip TEXT,
                send_time TEXT,
                content TEXT,
                success BOOLEAN,
                api_response TEXT
            )
        """)
        await db.commit()

# --- 2. 页面路由 (新增 UI 部分) ---

@app.get("/")
async def page_index(request):
    """ 首页：发送消息界面 """
    # 将默认的 chat_id 传给前端，方便显示
    return render_template("index.html", default_chat_id=DEFAULT_CHAT_ID)

@app.get("/ui/history")
async def page_history(request):
    """ 历史页：查看记录界面 """
    return render_template("history.html")

# --- 3. API 接口 (保持原有逻辑，微调) ---

@app.post("/send")
async def send_message(request: Request):
    data = request.json or {}
    text = data.get("text", "")
    chat_id = data.get("chat_id", DEFAULT_CHAT_ID)

    if not text:
        return response.json({"error": "内容不能为空"}, status=400)
    
    sender_ip = request.ip
    send_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = False
    api_res_text = ""

    # API 请求
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = { "chat_id": chat_id, "text": text, "parse_mode": "Markdown" }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(tg_url, json=payload, timeout=10.0)
            api_res_text = resp.text
            if resp.status_code == 200:
                success = True
            else:
                logger.error(f"Telegram API Error: {resp.text}")
    except Exception as e:
        api_res_text = str(e)

    # 存库
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (sender_ip, send_time, content, success, api_response) VALUES (?, ?, ?, ?, ?)",
            (sender_ip, send_time, text, success, api_res_text)
        )
        await db.commit()

    return response.json({
        "status": "success" if success else "failed",
        "telegram_response": api_res_text
    }, status=200 if success else 500)

@app.get("/history")
async def get_history_api(request: Request):
    # 增加 limit 参数处理
    try:
        limit = int(request.args.get("limit", 50))
    except:
        limit = 50

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = await cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "ip": row["sender_ip"],
                "time": row["send_time"],
                "content": row["content"],
                "success": bool(row["success"]),
                "response": row["api_response"]
            })
            
    return response.json(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
