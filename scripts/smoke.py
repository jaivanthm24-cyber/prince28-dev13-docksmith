"""Smoke test script for live or staging DockSmith deployment.

Usage:
    python scripts/smoke.py [LIVE_URL] [EXPECTED_SHA]
Or set environment variables:
    LIVE_URL=https://docksmith.onrender.com python scripts/smoke.py
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request


def fetch(url: str, timeout: int = 10) -> tuple[int, dict | str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "DockSmith-SmokeTest/1.0", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read().decode("utf-8")
            if "application/json" in content_type:
                return resp.status, json.loads(raw)
            return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw
    except Exception as e:
        return 0, str(e)


def main() -> int:
    base_url = sys.argv[1] if len(sys.argv) > 1 else os.getenv("LIVE_URL", "http://127.0.0.1:8000")
    base_url = base_url.rstrip("/")
    expected_sha = sys.argv[2] if len(sys.argv) > 2 else os.getenv("EXPECTED_SHA")

    print(f"=== DockSmith Smoke Tests: {base_url} ===")
    if expected_sha:
        print(f"Expected Git SHA: {expected_sha}")

    # Allow service to warm up if hosted on cold-start platform (e.g. Render free tier)
    max_retries = 12
    retry_interval = 5

    health_ok = False
    health_data = {}

    for attempt in range(1, max_retries + 1):
        print(f"[{attempt}/{max_retries}] Probing /health ...")
        status, body = fetch(f"{base_url}/health")
        if status == 200 and isinstance(body, dict) and body.get("status") == "ok":
            health_ok = True
            health_data = body
            print(f"  -> OK (200): {body}")
            break
        print(f"  -> Waiting for service (status={status}, body={body})")
        time.sleep(retry_interval)

    if not health_ok:
        print("FAIL: /health did not return 200 OK within timeout.")
        return 1

    # Verify Git SHA if expected_sha is provided
    running_sha = health_data.get("git_sha", "")
    if expected_sha:
        if not running_sha.startswith(expected_sha[:7]):
            print(f"FAIL: Running SHA '{running_sha}' does not match expected '{expected_sha}'.")
            return 1
        print(f"  -> SHA verification passed: {running_sha}")

    # Check /ready (database connectivity)
    print("Probing /ready ...")
    status, body = fetch(f"{base_url}/ready")
    if status != 200 or not isinstance(body, dict) or body.get("status") != "ready":
        print(f"FAIL: /ready returned status={status}, body={body}")
        return 1
    print(f"  -> OK (200): {body}")

    # Check /docs (OpenAPI interactive docs)
    print("Probing /docs ...")
    status, _ = fetch(f"{base_url}/docs")
    if status != 200:
        print(f"FAIL: /docs returned status={status}")
        return 1
    print("  -> OK (200)")

    # Check /v1/documents (data availability)
    print("Probing /v1/documents?limit=2 ...")
    status, body = fetch(f"{base_url}/v1/documents?limit=2")
    if status != 200 or not isinstance(body, dict) or "items" not in body:
        print(f"FAIL: /v1/documents returned status={status}, body={body}")
        return 1
    total = body.get("total", 0)
    items_count = len(body.get("items", []))
    print(f"  -> OK (200): total={total}, items_returned={items_count}")

    print("=== ALL SMOKE TESTS PASSED CLEANLY ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
