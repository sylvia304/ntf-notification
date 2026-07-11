# ntfy MCP Server

让 AI 给你的手机发推送通知。

## 原理

```
橘瓣(AI) → MCP Server → ntfy.sh → 你的手机弹窗
```

## 部署到 Render（免费）

1. 把这三个文件上传到你的 GitHub 仓库
2. 打开 [render.com](https://render.com)，用 GitHub 登录
3. 点 "New +" → "Web Service"，选你的仓库
4. Render 会自动读取 `render.yaml`，不需要手动配置
5. 等部署完成，你会得到一个地址类似 `https://ntfy-notifier.onrender.com`
6. 在橘瓣的设置中，添加自定义 MCP Server，填入：
   ```
   https://你的地址.onrender.com/sse
   ```

## 部署到 Railway（免费，需要信用卡验证）

1. 上传到 GitHub
2. 打开 [railway.app](https://railway.app)
3. New Project → Deploy from GitHub → 选仓库
4. 设置 Start Command: `python server.py`
5. 在 Variables 里添加 `PORT=8000`
6. 拿到地址后在橘瓣填入 `https://地址/sse`

## 本地测试

```bash
pip install -r requirements.txt
python server.py
```

然后用 curl 测试：
```bash
curl -X POST http://localhost:8000/sse
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `NTFY_TOPIC` | ntfy topic 名 | `aozihdek` |
| `NTFY_SERVER` | ntfy 服务器地址 | `https://ntfy.sh` |
| `PORT` | 服务端口 | `8000` |

## 手机端

安装 [ntfy](https://ntfy.sh) App，订阅 topic `aozihdek`。

打开 App → 点 + → 填入 `aozihdek` → 订阅。

确保在系统设置里给了 ntfy 通知权限，最好关掉电池优化（不然被杀后台收不到）。
