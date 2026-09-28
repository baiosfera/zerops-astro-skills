import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
import nats
from nats.aio.client import Client as NATSClient

class NatsService:
    def __init__(self):
        self.nc: NATSClient | None = None

    async def connect(self, server_url: str = "nats://127.0.0.1:4222"):
        self.nc = await nats.connect(servers=[server_url], name="gentle-fastapi-service")

    async def request_rpc(self, subject: str, payload: Dict[str, Any], timeout: float = 2.0) -> Dict[str, Any]:
        if not self.nc:
            raise RuntimeError("NATS client not connected")
        data = json.dumps(payload).encode("utf-8")
        msg = await self.nc.request(subject, data, timeout=timeout)
        return json.loads(msg.data.decode("utf-8"))

    async def register_worker(self, subject: str, queue_group: str, handler):
        if not self.nc:
            raise RuntimeError("NATS client not connected")

        async def msg_handler(msg):
            try:
                req = json.loads(msg.data.decode("utf-8"))
                res = await handler(req)
                if msg.reply:
                    await self.nc.publish(msg.reply, json.dumps(res).encode("utf-8"))
            except Exception as e:
                if msg.reply:
                    await self.nc.publish(msg.reply, json.dumps({"error": str(e)}).encode("utf-8"))

        await self.nc.subscribe(subject, queue=queue_group, cb=msg_handler)

    async def close(self):
        if self.nc:
            await self.nc.drain()
