"""
Asynchronous stdio and remote MCP client adapter for Oráculo (v4.0).
Coordinates: lunar, bazi_reader, zmanim, and kundali.
Serializes stdio calls via asyncio.Lock per server to prevent JSON-RPC pipe corruption.
Caches outputs locally under raw/json/cache/ to avoid repeated process execution.
"""

import asyncio
import json
import os
import shutil
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None

from pipeline.config import config
from pipeline.cache_manager import CacheManager


def _xml_elem_to_dict(elem: ET.Element) -> Any:
    """Recursively converts an XML ElementTree element into a python dict/list/str."""
    d: Dict[str, Any] = {}
    if elem.attrib:
        d["@attributes"] = elem.attrib
    text = (elem.text or "").strip()
    children = list(elem)
    if not children:
        if elem.attrib:
            if text:
                d["#text"] = text
            return d
        return text

    for child in children:
        child_val = _xml_elem_to_dict(child)
        if child.tag in d:
            if isinstance(d[child.tag], list):
                d[child.tag].append(child_val)
            else:
                d[child.tag] = [d[child.tag], child_val]
        else:
            d[child.tag] = child_val
    if text:
        d["#text"] = text
    return d


class UnifiedMcpClient:
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self._locks: Dict[str, asyncio.Lock] = {
            "lunar": asyncio.Lock(),
            "bazi_reader": asyncio.Lock(),
            "zmanim": asyncio.Lock(),
            "kundali": asyncio.Lock(),
        }

    def _get_server_params(self, server_name: str) -> Optional[StdioServerParameters]:
        env = os.environ.copy()
        
        if server_name == "lunar":
            binary = shutil.which("lunar-mcp-server") or "/home/zerops/.local/bin/lunar-mcp-server"
            if not os.path.exists(binary):
                binary = "lunar-mcp-server"
            return StdioServerParameters(command=binary, args=[], env=env)

        elif server_name == "bazi_reader":
            return StdioServerParameters(command="npx", args=["-y", "bazi-mcp"], env=env)

        elif server_name == "zmanim":
            env["UV_LINK_MODE"] = "copy"
            return StdioServerParameters(command="uvx", args=["zmanim-mcp-server"], env=env)

        elif server_name == "kundali":
            kundali_key = config.kundali_mcp_key or os.getenv("KUNDALI_MCP_KEY", "")
            return StdioServerParameters(
                command="npx",
                args=[
                    "-y", "mcp-remote", "https://mcp.kundalimcp.com/mcp",
                    "--header", f"Authorization: Bearer {kundali_key}"
                ],
                env=env
            )

        return None

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> dict:
        # Check cache first: check dedicated engine directory, then legacy mcp directory
        cached = self.cache.get(server_name, tool_name, arguments)
        if cached is None:
            cached = self.cache.get("mcp", f"{server_name}_{tool_name}", arguments)
        if cached is not None:
            return cached

        server_params = self._get_server_params(server_name)
        if not server_params:
            return {"error": f"Unknown MCP server: {server_name}"}

        # Stdio pipes must be serialized to avoid JSON-RPC frame corruption
        lock = self._locks.get(server_name)
        if not lock:
            lock = asyncio.Lock()
            self._locks[server_name] = lock

        async with lock:
            try:
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool(tool_name, arguments=arguments)

                        # Parse MCP Tool result
                        payload = {}
                        if hasattr(result, 'content') and result.content:
                            for item in result.content:
                                if hasattr(item, 'text'):
                                    text_raw = (item.text or "").strip()
                                    try:
                                        payload = json.loads(text_raw)
                                        break
                                    except Exception:
                                        if text_raw.startswith("<"):
                                            try:
                                                root = ET.fromstring(text_raw)
                                                payload = {
                                                    "xml_parsed": {root.tag: _xml_elem_to_dict(root)},
                                                    "_raw_xml": text_raw
                                                }
                                                break
                                            except Exception:
                                                payload = {"text": item.text}
                                        else:
                                            payload = {"text": item.text}
                        
                        if not payload:
                            payload = {"result": str(result)}

                        # Cache output in dedicated provider folder
                        self.cache.set(server_name, tool_name, arguments, payload, http_status=200)
                        return payload

            except Exception as e:
                return {"error": f"MCP {server_name} execution error: {str(e)}"}
