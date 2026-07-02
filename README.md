# 🚀 Sanic Telegram Bot Pusher

一个基于 **Sanic** 框架构建的高性能 Telegram 消息推送服务。集成了现代化的 **Web UI** 界面和标准 **RESTful API**，支持 Docker 容器化部署与数据持久化。

https://hub.docker.com/r/dangerwolf/sanic_send_tg_bot

https://github.com/dangerwolf/sanic-webui-tgbot


![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Sanic](https://img.shields.io/badge/Sanic-23.x-ff69b4.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)

## ✨ 功能特性

* **⚡ 高性能异步框架**：基于 Sanic + HTTPX，轻松处理高并发请求。
* **🐳 Docker 容器化**：内置依赖，无需配置环境，开箱即用。
* **🖥️ 美观的 Web UI**：
    * 集成 Bootstrap 5，界面简洁大方，适配移动端。
    * 提供可视化消息发送面板（支持 Markdown）。
    * 提供发送历史记录查看面板。
* **💾 数据持久化**：使用 SQLite 记录所有发送日志，支持通过 Docker 卷（Volume）挂载到宿主机。
* **🔌 标准 API 接口**：支持通过 HTTP 请求调用，方便集成到其他脚本或 CI/CD 流程中。

## 📂 项目结构

```text
.
├── Dockerfile          # 构建镜像的配置文件
├── app.py              # 核心业务逻辑 (Sanic App)
└── templates/          # Web UI 模板文件
    ├── base.html
    ├── index.html
    └── history.html

```
## 🛠️ 快速开始 (Docker)
### 1. 构建镜像

在项目根目录下执行：


```Bash
docker build -t sanic-tg-bot .
```
### 2. 启动容器

使用以下命令启动服务。请务必替换 <YOUR_BOT_TOKEN> 和 <YOUR_CHAT_ID>。

Linux/macOS:

```Bash
# 创建数据目录
mkdir -p $(pwd)/bot_data

# 启动容器
docker run -d \
  --name tg-pusher \
  --restart always \
  -p 9010:8000 \
  -v $(pwd)/bot_data:/app/data \
  -e BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz" \
  -e CHAT_ID="123456789" \
  sanic-tg-bot
```
Windows (PowerShell):

```PowerShell
docker run -d `
  --name tg-pusher `
  --restart always `
  -p 9010:8000 `
  -v ${PWD}/bot_data:/app/data `
  -e BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz" `
  -e CHAT_ID="123456789" `
  sanic-tg-bot
```
### 3. 访问服务

启动成功后，访问宿主机端口：
```
Web UI: http://localhost:9010
```


<img width="969" height="570" alt="image" src="https://github.com/user-attachments/assets/f02a9368-d9c5-4adb-88db-95d252846735" />
<img width="1024" height="342" alt="image" src="https://github.com/user-attachments/assets/1b72c82a-dc27-452e-b5bc-a969a6c95242" />


## ⚙️ 配置说明 (环境变量)
|变量名|必填|说明|示例|
| ---- | ---- | ---- | ---- |
|BOT_TOKEN|✅|Telegram Bot 的 Token|12345:AbCdEf...|
|CHAT_ID|❌|默认接收消息的 Chat ID (可在请求中覆盖)|-10012345678|
|TZ|❌|时区设置 (Dockerfile 中已默认为 Asia/Shanghai)|Asia/Shanghai|
## 🔗 API 文档
如果你不想使用 Web UI，可以通过 API 直接调用。

### 1. 发送消息

URL: /send

Method: POST

Content-Type: application/json

参数:

|字段|类型|必填|说明|
| ---- | ---- | ---- | ---- |
|text|string|✅|消息内容 (支持 Markdown)|
|chat_id|string|❌|指定接收者 ID，不填则使用环境变量默认值|

示例 (Curl):

```Bash
curl -X POST http://localhost:9010/send \
     -H "Content-Type: application/json" \
     -d '{
           "text": "*Server Alert*: \nCPU usage is high!", 
           "chat_id": "123456789"
         }'
```
### 2. 获取历史记录

URL: /history

Method: GET

参数:
|字段|说明|
| ---- | ---- 
|limit|返回记录条数 (默认 50)|

示例:

```Bash
curl http://localhost:9010/history?limit=10
```
## 📝 数据存储
容器内的数据库路径为 /app/data/history.db。 通过 -v 参数映射后，数据库文件将保存在宿主机的 bot_data 目录下。

注意：即使删除了容器，只要保留了宿主机的 bot_data 目录，你的发送历史记录就不会丢失。

## 🤝 贡献
欢迎提交 Issue 或 Pull Request 来改进本项目！

## 友情赞助商

1. [![Powered by DartNode](https://dartnode.com/branding/DN-Open-Source-sm.png)](https://dartnode.com "Powered by DartNode - Free VPS for Open Source")

2. 开发者需要免费服务的，推荐使用每个月免费$5额度的云服务。
[https://console.run.claw.cloud/signin?link=XHJEEP7HEVIR](https://console.run.claw.cloud/signin?link=XHJEEP7HEVIR)

3. [Cloudcone VPS](https://app.cloudcone.com/?ref=12850)

4. [![This Website is Powered by DigitalPlat FreeDomain Get a free domain from DigitalPlat.](https://img.shields.io/badge/DigitalPlat-Get%20a%20free%20domain%20from%20DigitalPlat.-2563eb?style=flat-square&logo=databricks&logoColor=ffffff)](https://dash.domain.digitalplat.org/signup?ref=3lT6CU6HGe)

5. [DMIT](https://www.dmit.io/aff.php?aff=23825)



