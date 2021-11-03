What is keycloak_admin_aio?
---------------------------

This package provides an asynchronous api wrapper for the `keycloak admin api
<https://www.keycloak.org/docs-api/15.0/rest-api>`_.  It uses `httpx
<https://github.com/encode/httpx/>`_ as an asynchronous http client.

How to use it?
--------------

.. code:: python

    import asyncio
    from keycloak_admin_aio import KeycloakAdmin

    server_url = "http://localhost:8080/auth"
    client_id = "admin-cli"  # used by default
    realm = "master"  # used by default

With administrator username and password:

.. code:: python

    keycloak_admin_args = {
        "server_url": server_url,
        "client_id": client_id,
        "realm": realm,
        "username": "admin",
        "password": "password123",
    }

    async def main():
        async with KeycloakAdmin.with_password(**keycloak_admin_args) as kc:
            ...

    asyncio.run(main())

With client credentials:

.. code:: python

    keycloak_admin_args = {
        "server_url": server_url,
        "client_id": client_id,
        "client_secret": "the_secret",
    }

    async def main():
        async with KeycloakAdmin.with_client_credentials(**keycloak_admin_args) as kc:
            ...

    asyncio.run(main())
