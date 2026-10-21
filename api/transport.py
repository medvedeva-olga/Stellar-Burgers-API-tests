import json
import os

MASK = "***"
# Максимальная длина тела/заголовков в дампе. Переопределяется LOG_MAX_BODY.
MAX_LENGTH = int(os.getenv("LOG_MAX_BODY", "2000"))
SENSITIVE_KEYS = {
    "password",
    "token",
    "accesstoken",
    "refreshtoken",
    "authorization",
    "cookie",
    "set-cookie",
}


def redact(data):
    """Маскирует значения чувствительных полей, чтобы не светить их в логах."""
    if isinstance(data, dict):
        return {
            key: MASK if str(key).lower() in SENSITIVE_KEYS else redact(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [redact(item) for item in data]
    return data


def _truncate(text):
    if len(text) <= MAX_LENGTH:
        return text
    return f"{text[:MAX_LENGTH]}\n… (обрезано, всего {len(text)} символов)"


def _pretty(data):
    return _truncate(json.dumps(redact(data), indent=2, ensure_ascii=False))


def _format_request_body(body):
    if not body:
        return "None"
    if isinstance(body, bytes):
        body = body.decode("utf-8", errors="replace")
    try:
        return _pretty(json.loads(body))
    except (TypeError, ValueError):
        return _truncate(str(body))


def _format_response_body(response):
    try:
        return _pretty(response.json())
    except ValueError:
        return _truncate(response.text or "None")


class HTTPLogBuffer:
    """Копит HTTP-обмен в памяти в рамках одного теста."""

    def __init__(self):
        self.logs = []

    def record(self, response, *args, **kwargs):
        request = response.request
        self.logs.append(
            "=========================================\n"
            f"REQUEST: {request.method} {request.url}\n"
            f"HEADERS: {_pretty(dict(request.headers))}\n"
            f"BODY:\n{_format_request_body(request.body)}\n"
            "-----------------------------------------\n"
            f"RESPONSE: {response.status_code} "
            f"({response.elapsed.total_seconds() * 1000:.0f} ms)\n"
            f"HEADERS: {_pretty(dict(response.headers))}\n"
            f"BODY:\n{_format_response_body(response)}\n"
            "=========================================\n\n"
        )

    def get_full_log(self):
        return "".join(self.logs)
