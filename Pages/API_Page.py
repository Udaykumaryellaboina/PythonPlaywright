# api_page.py
from playwright.async_api import async_playwright, APIRequestContext, APIResponse
from typing import Dict, Any, Optional
import time
import json


class APIPage:
    def __init__(self):
        self.api_context: Optional[APIRequestContext] = None
        self.last_response: Optional[APIResponse] = None

    async def run_get_tests(
        self,
        api_name: str,
        api_test_point: str,
        api_request: APIRequestContext,
        request_url: str
    ) -> Dict[str, Any]:
        start_time = int(time.time() * 1000)

        # Hit API
        api_body: APIResponse = await api_request.get(request_url, ignore_https_errors=True)

        api_json: Optional[Dict[str, Any]] = None
        if api_body.status != 204:
            try:
                api_json = await api_body.json()
            except Exception:
                api_json = None  # fallback if not JSON

        end_time = int(time.time() * 1000)
        test_time = end_time - start_time
        status_code = api_body.status

        added_data = {
            "APIAppID": "APIID:4314",
            "APICategory": api_name,
            "APIEndPointName": api_test_point,
            "TestTime": test_time,
            "StatusCode": status_code,
        }

        combined_data = {**added_data, **(api_json if isinstance(api_json, dict) else {})}
        return combined_data

    # ✅ Init context with optional headers
    async def init(self, playwright, headers: Dict[str, str] = {}):
        self.api_context = await playwright.request.new_context(extra_http_headers=headers)

    # ✅ Basic Authentication
    async def authenticate_with_basic_auth(self, playwright, username: str, password: str):
        self.api_context = await playwright.request.new_context(
            http_credentials={"username": username, "password": password}
        )

    # ✅ Bearer Token
    async def authenticate_with_bearer_token(self, playwright, token: str):
        self.api_context = await playwright.request.new_context(
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )

    # ✅ API Key in Header
    async def authenticate_with_api_key(self, playwright, header_name: str, api_key: str):
        self.api_context = await playwright.request.new_context(
            extra_http_headers={header_name: api_key}
        )

    # ✅ Client Credentials flow
    async def authenticate_with_client_credentials(
        self, playwright, token_url: str, client_id: str, client_secret: str, scope: str = ""
    ):
        temp_context = await playwright.request.new_context()
        token_response = await temp_context.post(
            token_url,
            form={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": scope,
            },
        )

        if token_response.status != 200:
            raise Exception(f"Failed to fetch token: {token_response.status}")

        token_json = await token_response.json()
        access_token = token_json["access_token"]

        self.api_context = await playwright.request.new_context(
            extra_http_headers={"Authorization": f"Bearer {access_token}"}
        )

    # ✅ Generic request handler
    async def hit_request(self, method: str, url: str, body: Any = {}) -> APIResponse:
        if not self.api_context:
            raise Exception("API context not initialized. Call init/authenticate first.")

        method = method.upper()
        if method == "GET":
            response = await self.api_context.get(url)
        elif method == "POST":
            response = await self.api_context.post(url, data=body)
        elif method == "PUT":
            response = await self.api_context.put(url, data=body)
        elif method == "DELETE":
            response = await self.api_context.delete(url)
        else:
            raise Exception(f"Unsupported HTTP method: {method}")

        self.last_response = response
        return response

    # ✅ Get response status
    def get_status(self) -> int:
        if not self.last_response:
            raise Exception("No response available. Call hit_request() first.")
        return self.last_response.status

    # ✅ Get response body
    async def get_response_body(self) -> Any:
        if not self.last_response:
            raise Exception("No response available. Call hit_request() first.")
        try:
            return await self.last_response.json()
        except Exception:
            return await self.last_response.text()
