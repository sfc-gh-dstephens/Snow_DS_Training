"""
Access SPCS services using Snowflake keypair authentication.

This module provides functionality to authenticate with Snowflake using JWT tokens
and connect to SPCS (Snowflake Container Services) endpoints.
"""

import argparse
import json
import logging
import sys
import os
import time
from datetime import timedelta
from typing import Dict, Any, Optional

import requests

from generateJWT import JWTGenerator

# Constants
DEFAULT_JWT_LIFETIME_MINUTES = 59
DEFAULT_JWT_RENEWAL_DELAY_MINUTES = 54
DEFAULT_ENDPOINT_PATH = "/"
OAUTH_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"
HTTP_SUCCESS = 200
TOKEN_CACHE_FILE = os.path.expanduser("~/.snowflake_token_cache.json")
TOKEN_EXPIRY_BUFFER_SECONDS = 60

logger = logging.getLogger(__name__)


def main() -> None:
    args = _parse_args()

    try:
        token = _get_token(args)
        snowflake_jwt = _token_exchange(
            token,
            endpoint=args.endpoint,
            role=args.role,
            snowflake_account_url=args.snowflake_account_url,
            snowflake_account=args.account,
        )
        spcs_url = f"https://{args.endpoint}{args.endpoint_path}"
        _connect_to_spcs(snowflake_jwt, spcs_url, args.payload)
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)


def _get_token(args: argparse.Namespace) -> str:
    cache_key = f"{args.account}_{args.user}_{args.role or 'norole'}"
    cached_token = _get_cached_token(cache_key)

    if cached_token:
        logger.info("Using cached JWT token")
        return cached_token

    try:
        token_generator = JWTGenerator(
            args.account,
            args.user,
            args.private_key_file_path,
            timedelta(minutes=args.lifetime),
            timedelta(minutes=args.renewal_delay),
        )
        token = token_generator.get_token()

        # Estimate expiry time: now + lifetime in seconds
        expiry = int(time.time()) + args.lifetime * 60
        _cache_token(cache_key, token, expiry)

        return token
    except Exception as e:
        logger.error(f"Failed to generate JWT token: {e}")
        raise



def _token_exchange(
    token: str,
    role: Optional[str],
    endpoint: str,
    snowflake_account_url: Optional[str],
    snowflake_account: str,
) -> str:
    """
    Exchange JWT token for Snowflake OAuth token.

    Args:
        token: JWT token to exchange
        role: Optional role to assume
        endpoint: Target endpoint for scope
        snowflake_account_url: Optional custom Snowflake account URL
        snowflake_account: Snowflake account identifier

    Returns:
        str: Raw Snowflake OAuth access token
    """
    scope_role = f"session:role:{role}" if role else None
    scope = f"{scope_role} {endpoint}" if scope_role else endpoint

    data = {
        "grant_type": OAUTH_GRANT_TYPE,
        "scope": scope,
        "assertion": token,
    }

    oauth_url = (
        f"{snowflake_account_url}/oauth/token"
        if snowflake_account_url
        else f"https://{snowflake_account}.snowflakecomputing.com/oauth/token"
    )

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    logger.info(f"OAuth URL: {oauth_url}")

    try:
        response = requests.post(oauth_url, data=data, headers=headers, timeout=30)
        response.raise_for_status()
        logger.info("Successfully obtained Snowflake OAuth token")
        return response.text.strip()  # This is the raw token string
    except requests.RequestException as e:
        logger.error(f"Failed to exchange token: {e}")
        raise



def _get_cached_token(cache_key: str) -> Optional[str]:
    if not os.path.exists(TOKEN_CACHE_FILE):
        return None

    try:
        with open(TOKEN_CACHE_FILE, "r") as f:
            cache = json.load(f)

        entry = cache.get(cache_key)
        if not entry:
            return None

        if entry["expiry"] - TOKEN_EXPIRY_BUFFER_SECONDS > time.time():
            return entry["token"]

        logger.info("Cached token expired")
        return None

    except Exception as e:
        logger.warning(f"Failed to read token cache: {e}")
        return None


def _cache_token(cache_key: str, token: str, expiry: int) -> None:
    cache = {}

    try:
        if os.path.exists(TOKEN_CACHE_FILE):
            with open(TOKEN_CACHE_FILE, "r") as f:
                cache = json.load(f)
    except Exception as e:
        logger.warning(f"Failed to read existing cache (continuing): {e}")

    cache[cache_key] = {"token": token, "expiry": expiry}

    try:
        with open(TOKEN_CACHE_FILE, "w") as f:
            json.dump(cache, f)
    except Exception as e:
        logger.warning(f"Failed to write token cache: {e}")


def _connect_to_spcs(token: str, url: str, payload: Optional[str] = None) -> None:
    headers = {
        "Authorization": f'Snowflake Token="{token}"',
        "Content-Type": "application/json",
    }

    request_payload = _parse_payload(payload)

    try:
        if request_payload is not None:
            response = requests.post(
                url, headers=headers, json=request_payload, timeout=30
            )
        else:
            response = requests.post(url, headers=headers, timeout=30)

        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response: {response.text}")

        if response.status_code != HTTP_SUCCESS:
            logger.warning(f"Non-success status code: {response.status_code}")

    except requests.RequestException as e:
        logger.error(f"Failed to connect to SPCS: {e}")
        raise


def _parse_payload(payload: Optional[str]) -> Optional[Dict[str, Any]]:
    if payload is None:
        logger.info("No payload provided")
        return None

    try:
        parsed_payload = json.loads(payload)
        logger.info("Successfully parsed custom payload")
        return parsed_payload
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON payload: {e}")
        raise ValueError(f"Invalid JSON payload: {e}")


def _parse_args() -> argparse.Namespace:
    _setup_logging()

    parser = argparse.ArgumentParser(
        description="Access SPCS services using Snowflake keypair authentication"
    )

    parser.add_argument("--account", required=True, help="Snowflake account identifier")
    parser.add_argument("--user", required=True, help="User name for authentication")
    parser.add_argument("--private_key_file_path", required=True, help="Private key file path")
    parser.add_argument("--endpoint", required=True, help="SPCS ingress endpoint")

    parser.add_argument("--lifetime", type=int, default=DEFAULT_JWT_LIFETIME_MINUTES)
    parser.add_argument("--renewal_delay", type=int, default=DEFAULT_JWT_RENEWAL_DELAY_MINUTES)
    parser.add_argument("--role", help="Role to use (optional)")
    parser.add_argument("--endpoint-path", default=DEFAULT_ENDPOINT_PATH)
    parser.add_argument("--snowflake_account_url", help="Custom Snowflake URL (optional)")
    parser.add_argument("--payload", help="Optional JSON payload")

    return parser.parse_args()


def _setup_logging() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


if __name__ == "__main__":
    main()
