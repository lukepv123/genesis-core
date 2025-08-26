from typing import Optional, Dict, Any

try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

class HttpClient:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def get(self, url: str, **kwargs) -> Dict[str, Any]:
        if not httpx:
            return {"error": "httpx not installed"}
        with httpx.Client(timeout=self.timeout) as client:
            r = client.get(url, **kwargs)
            return {"status_code": r.status_code, "body": r.text}

    def post(self, url: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        if not httpx:
            return {"error": "httpx not installed"}
        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, json=json, **kwargs)
            return {"status_code": r.status_code, "body": r.text}
