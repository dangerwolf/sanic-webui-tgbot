# 🚀 Sanic Telegram Bot Pusher

一个基于 **Sanic** 框架构建的高性能 Telegram 消息推送服务。集成了现代化的 **Web UI** 界面和标准 **RESTful API**，支持 Docker 容器化部署与数据持久化。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Sanic](https://img.shields.io/badge/Sanic-23.x-ff69b4.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

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
