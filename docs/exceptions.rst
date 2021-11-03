Exceptions
==========

This packages does not have its own exceptions. The exceptions raised by `httpx
<https://github.com/encode/httpx/>`_ bubble up so it's your responsibility to
handle these. ``Httpx`` is configured in a way that it will it will run
``response.raise_for_status()`` for every response.

For example:

.. code:: python

    import asyncio
    import httpx
    from typing import Optional
    from keycloak_admin_aio import KeycloakAdmin, RoleRepresentation

    async def get_role(kc: KeycloakAdmin, role_name: str) -> Optional[RoleRepresentation]:
        try:
            return await kc.roles.by_name(role_name).get()
        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == httpx.codes.NOT_FOUND:
                print(f"Role '{role_name}' could not be found: {ex}")
            else:
                raise ex

    async def main():
        async with KeycloakAdmin.with_password() as kc:  # provide credentials
            role = await get_role(kc, "no-exist")

    asyncio.run(main())

For help on how to handle ``httpx`` exceptions please refer to the `httpx docs <https://www.python-httpx.org/exceptions/>`_.
