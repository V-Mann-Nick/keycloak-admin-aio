import httpx


async def raise_for_status_hook(response: httpx.Response):
    if response.status_code >= 400:
        await response.aread()
    response.raise_for_status()


httpx_default_args = {"event_hooks": {"response": [raise_for_status_hook]}}


def merge_with_default_httpx_args(user_args: dict) -> dict:
    return {**httpx_default_args, **user_args}
