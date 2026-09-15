"""Minimal Chrome DevTools Protocol client for Suno automation."""

import json
import time
import urllib.request

import websocket

from config import CDP_URL


def http_json(path: str, method: str = "GET", payload=None):
    request = urllib.request.Request(CDP_URL + path, method=method)
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, data=data, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def list_tabs():
    return http_json("/json/list")


def find_suno_tab():
    pages = [t for t in list_tabs() if t.get("type") == "page" and "suno.com" in (t.get("url") or "")]
    for tab in pages:
        if "/create" in (tab.get("url") or ""):
            return tab
    return pages[0] if pages else None


class Tab:
    def __init__(self, info):
        self.info = info
        self.ws = websocket.create_connection(info["webSocketDebuggerUrl"], timeout=30)
        self._id = 0

    def cmd(self, method, params=None):
        self._id += 1
        message_id = self._id
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(f"{method} error: {message['error']}")
                return message.get("result", {})

    def eval_js(self, expression):
        result = self.cmd("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        })
        value = result.get("result", {})
        if value.get("type") == "undefined" and "value" not in value:
            return None
        if "value" in value:
            return value["value"]
        raise RuntimeError(f"JS error: {value.get('description')}")

    def navigate(self, url):
        self.cmd("Page.navigate", {"url": url})
        time.sleep(0.5)

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def get_tab():
    info = find_suno_tab()
    if info is None:
        raise RuntimeError("没有找到 Suno 标签页，请确认自动化浏览器已打开 suno.com")
    return Tab(info)
