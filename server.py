"""
ntfy MCP Server - 让AI能给你的手机发推送通知
部署后添加到橘瓣的自定义MCP，我就能随时弹窗叫你了
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("ntfy-mcp")

from mcp.server.fastmcp import FastMCP
import httpx

# 你的 ntfy topic —— 可以改，但改了的话手机端的 topic 也得对应
DEFAULT_TOPIC = os.environ.get("NTFY_TOPIC", "aozihdek")
# ntfy 服务器地址 —— 默认用公共服务器，也可以改成你自建的
NTFY_SERVER = os.environ.get("NTFY_SERVER", "https://ntfy.sh")

mcp = FastMCP("ntfy-notifier")


@mcp.tool()
async def send_notification(
    message: str,
    title: str = None,
    topic: str = DEFAULT_TOPIC,
    priority: str = "default",
) -> str:
    """给你的手机发送一条推送通知。
    
    用法：
        - message: 通知正文（必填）
        - title: 通知标题（可选，不填就用默认）
        - topic: ntfy topic 名（默认是你的专属 topic）
        - priority: 优先级，可选 'min', 'low', 'default', 'high', 'max'
          'high' 和 'max' 在安卓上会强弹窗，即使开了免打扰也会响
    
    示例：
        send_notification(message="起床了台风来了", title="AI提醒", priority="high")
    """
    url = f"{NTFY_SERVER}/{topic}"
    headers = {"Content-Type": "text/plain; charset=utf-8"}
    
    if title:
        headers["Title"] = title.encode("utf-8").decode("latin-1", errors="ignore")
    if priority and priority != "default":
        headers["Priority"] = priority
    
    logger.info(f"Sending notification to {topic}: {message[:50]}...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, content=message.encode("utf-8"), headers=headers)
            if 200 <= resp.status_code < 300:
                logger.info(f"Notification sent OK: {resp.status_code}")
                return f"✅ 推送成功！消息已发送到你的手机。"
            else:
                logger.error(f"ntfy returned {resp.status_code}: {resp.text[:200]}")
                return f"❌ 推送失败：HTTP {resp.status_code}"
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return f"❌ 推送失败：{e}"


@mcp.tool()
async def send_wakeup_call(message: str = "醒了吗？该起床了") -> str:
    """专门用来叫你起床的快捷工具。会用最高优先级，确保手机响。"""
    return await send_notification(
        message=message,
        title="🌅 起床时间",
        topic=DEFAULT_TOPIC,
        priority="high",
    )


def main():
    port = int(os.environ.get("PORT", "8000"))
    logger.info(f"Starting ntfy MCP Server on port {port}...")
    logger.info(f"Default topic: {DEFAULT_TOPIC}")
    logger.info(f"ntfy server: {NTFY_SERVER}")
    
    # SSE 模式 —— 橘瓣会通过 SSE 连接这个服务
    mcp.run(transport="sse", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
