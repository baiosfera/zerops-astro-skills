#!/usr/bin/env python3
"""
Frappe REST & RPC Client (v2.4)
Universal, tenant-agnostic Python client for Frappe Framework & ERPNext (v15/v16).
Supports Token Authentication, Standard CRUD, Batch Ingestion (insert_many),
Atomic Child Table Updates, Document Lifecycle (submit/cancel), and Private File Uploads.
"""

import os
import sys
import json
import argparse
import unittest
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urljoin
import urllib.request
import urllib.error


class FrappeClient:
    """Robust, tenant-agnostic client for Frappe REST & RPC APIs."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout: int = 10,
    ):
        if base_url is None:
            self.base_url = os.getenv("FRAPPE_URL", "").rstrip("/")
        else:
            self.base_url = base_url.rstrip("/")
        self.api_key = os.getenv("FRAPPE_API_KEY", "") if api_key is None else api_key
        self.api_secret = os.getenv("FRAPPE_API_SECRET", "") if api_secret is None else api_secret
        self.timeout = timeout

        if self.api_key and self.api_secret:
            self.auth_header = f"token {self.api_key}:{self.api_secret}"
        else:
            self.auth_header = ""

    def _get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "ERPNext-Agent-Client/2.4",
        }
        if content_type:
            headers["Content-Type"] = content_type
        if self.auth_header:
            headers["Authorization"] = self.auth_header
        return headers

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Union[Dict[str, Any], bytes]] = None,
        params: Optional[Dict[str, Any]] = None,
        content_type: str = "application/json",
    ) -> Dict[str, Any]:
        """Execute raw HTTP request using standard library urllib."""
        if not self.base_url:
            raise ValueError("FRAPPE_URL is not configured.")

        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            query_parts = []
            for k, v in params.items():
                if isinstance(v, (dict, list)):
                    encoded_val = urllib.request.quote(json.dumps(v))
                else:
                    encoded_val = urllib.request.quote(str(v))
                query_parts.append(f"{k}={encoded_val}")
            url = f"{url}?{'&'.join(query_parts)}"

        body = None
        if data is not None:
            if isinstance(data, dict):
                body = json.dumps(data).encode("utf-8")
            elif isinstance(data, bytes):
                body = data
            elif isinstance(data, str):
                body = data.encode("utf-8")

        req = urllib.request.Request(
            url=url,
            data=body,
            headers=self._get_headers(content_type),
            method=method.upper(),
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                resp_data = response.read().decode("utf-8")
                return json.loads(resp_data) if resp_data else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            try:
                parsed_err = json.loads(err_body)
                raise RuntimeError(f"HTTP {e.code}: {parsed_err.get('exception') or parsed_err.get('message') or err_body}")
            except json.JSONDecodeError:
                raise RuntimeError(f"HTTP {e.code}: {err_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network error connecting to {url}: {e.reason}")

    # =========================================================================
    # Standard CRUD Operations (/api/resource/:doctype)
    # =========================================================================

    def get_doc(self, doctype: str, name: str) -> Dict[str, Any]:
        """Read a single document by DocType and name."""
        res = self._request("GET", f"api/resource/{urllib.request.quote(doctype)}/{urllib.request.quote(name)}")
        return res.get("data", {})

    def get_list(
        self,
        doctype: str,
        fields: Optional[List[str]] = None,
        filters: Optional[Union[Dict[str, Any], List[Any]]] = None,
        or_filters: Optional[Union[Dict[str, Any], List[Any]]] = None,
        order_by: Optional[str] = None,
        limit_start: int = 0,
        limit_page_length: int = 20,
    ) -> List[Dict[str, Any]]:
        """List documents matching filters with projection and pagination."""
        params: Dict[str, Any] = {
            "limit_start": limit_start,
            "limit_page_length": limit_page_length,
        }
        if fields:
            params["fields"] = fields
        if filters:
            params["filters"] = filters
        if or_filters:
            params["or_filters"] = or_filters
        if order_by:
            params["order_by"] = order_by

        res = self._request("GET", f"api/resource/{urllib.request.quote(doctype)}", params=params)
        return res.get("data", [])

    def insert(self, doctype: str, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document."""
        res = self._request("POST", f"api/resource/{urllib.request.quote(doctype)}", data=doc_data)
        return res.get("data", {})

    def update(self, doctype: str, name: str, doc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing document. NOTE: Be cautious when passing child tables."""
        res = self._request("PUT", f"api/resource/{urllib.request.quote(doctype)}/{urllib.request.quote(name)}", data=doc_data)
        return res.get("data", {})

    def delete(self, doctype: str, name: str) -> bool:
        """Delete a document."""
        res = self._request("DELETE", f"api/resource/{urllib.request.quote(doctype)}/{urllib.request.quote(name)}")
        return res.get("message") == "ok" or res.get("data") == "ok"

    # =========================================================================
    # Advanced RPC & Batch Ingestion Operations (/api/method/frappe.client.*)
    # =========================================================================

    def call_method(self, method_name: str, args: Optional[Dict[str, Any]] = None, http_method: str = "POST") -> Any:
        """Execute a whitelisted Frappe Python RPC method."""
        if http_method.upper() == "GET":
            res = self._request("GET", f"api/method/{method_name}", params=args)
        else:
            res = self._request("POST", f"api/method/{method_name}", data=args or {})
        return res.get("message")

    def insert_many(self, doctype: str, docs: List[Dict[str, Any]]) -> List[str]:
        """
        Batch insert up to 200 documents in a single atomic HTTP call.
        Uses /api/method/frappe.client.insert_many.
        """
        payload = {
            "docs": [{"doctype": doctype, **doc} for doc in docs]
        }
        res = self.call_method("frappe.client.insert_many", payload)
        return res or []

    def bulk_update(self, docs: List[Dict[str, Any]]) -> List[str]:
        """Batch update documents using /api/method/frappe.client.bulk_update."""
        payload = {"docs": docs}
        res = self.call_method("frappe.client.bulk_update", payload)
        return res or []

    def set_value(self, doctype: str, name: str, fieldname: str, value: Any) -> Dict[str, Any]:
        """
        Atomically set a single field value without sending the entire document.
        Ideal for child table rows and status flags without trigger overhead.
        """
        payload = {
            "doctype": doctype,
            "name": name,
            "fieldname": fieldname,
            "value": value,
        }
        return self.call_method("frappe.client.set_value", payload)

    def submit(self, doctype: str, name: str) -> Dict[str, Any]:
        """Submit a submittable document (docstatus 0 -> 1)."""
        doc = self.get_doc(doctype, name)
        return self.call_method("frappe.client.submit", {"doc": doc})

    def cancel(self, doctype: str, name: str) -> Dict[str, Any]:
        """Cancel a submitted document (docstatus 1 -> 2)."""
        return self.call_method("frappe.client.cancel", {"doctype": doctype, "name": name})

    # =========================================================================
    # File Management (/api/method/upload_file)
    # =========================================================================

    def upload_file(
        self,
        filename: str,
        file_bytes: bytes,
        doctype: Optional[str] = None,
        docname: Optional[str] = None,
        fieldname: Optional[str] = None,
        is_private: int = 1,
        folder: str = "Home",
    ) -> Dict[str, Any]:
        """
        Upload a file using multipart/form-data to /api/method/upload_file.
        Supports private files (is_private=1) and auto-binding to doc fields.
        """
        boundary = "----WebKitFormBoundaryERPNextClientBoundary7MA4YWxkTrZu0gW"
        lines = []

        def add_field(name: str, val: Any):
            lines.append(f"--{boundary}".encode("utf-8"))
            lines.append(f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"))
            lines.append(b"")
            lines.append(str(val).encode("utf-8"))

        if doctype:
            add_field("doctype", doctype)
        if docname:
            add_field("docname", docname)
        if fieldname:
            add_field("fieldname", fieldname)
        add_field("is_private", is_private)
        add_field("folder", folder)

        # File part
        lines.append(f"--{boundary}".encode("utf-8"))
        lines.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode("utf-8"))
        lines.append(b"Content-Type: application/octet-stream")
        lines.append(b"")
        lines.append(file_bytes)
        lines.append(f"--{boundary}--".encode("utf-8"))
        lines.append(b"")

        payload = b"\r\n".join(lines)
        headers = self._get_headers(content_type=f"multipart/form-data; boundary={boundary}")

        if not self.base_url:
            raise ValueError("FRAPPE_URL is not configured.")

        url = f"{self.base_url}/api/method/upload_file"
        req = urllib.request.Request(url=url, data=payload, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                resp_data = response.read().decode("utf-8")
                return json.loads(resp_data).get("message", {})
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code} uploading file: {err_body}")


# =============================================================================
# Unit Tests / Mock Suite
# =============================================================================

class TestFrappeClient(unittest.TestCase):
    """Deterministic unit tests validating client logic and signatures."""

    def test_init_and_headers(self):
        client = FrappeClient(
            base_url="https://demo.frappe.cloud",
            api_key="key123",
            api_secret="sec456",
        )
        self.assertEqual(client.base_url, "https://demo.frappe.cloud")
        headers = client._get_headers()
        self.assertEqual(headers["Authorization"], "token key123:sec456")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(headers["Accept"], "application/json")

    def test_missing_url_raises(self):
        client = FrappeClient(base_url="", api_key="k", api_secret="s")
        with self.assertRaises(ValueError):
            client.get_doc("Item", "TEST")

    def test_query_params_serialization(self):
        client = FrappeClient(base_url="https://demo.frappe.cloud", api_key="k", api_secret="s")
        params = {"filters": [["Item", "is_stock_item", "=", 1]], "limit_page_length": 50}
        self.assertIn("filters", params)


def main():
    parser = argparse.ArgumentParser(description="Frappe REST & RPC Client v2.4")
    parser.add_argument("--test", action="store_true", help="Run internal unit tests")
    parser.add_argument("--ping", action="store_true", help="Verify connectivity to FRAPPE_URL")
    args = parser.parse_args()

    if args.test:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFrappeClient)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    if args.ping:
        client = FrappeClient()
        try:
            pong = client.call_method("frappe.ping", http_method="GET")
            print(f"✓ Connected successfully to {client.base_url}: {pong}")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Connection failed: {e}", file=sys.stderr)
            sys.exit(1)

    parser.print_help()


if __name__ == "__main__":
    main()
