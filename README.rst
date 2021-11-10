What is keycloak_admin_aio?
---------------------------

This package provides an asynchronous api wrapper for the `keycloak admin api
<https://www.keycloak.org/docs-api/15.0/rest-api>`_.

The main dependencies are:

- `httpx <https://github.com/encode/httpx/>`_: asynchronous http client
- `dacite <https://github.com/konradhalas/dacite>`_: parse nested dictionaries into nested dataclasses

Links:

- `Source code <https://github.com/delphai/keycloak-admin-aio>`_
- `Documentation <https://delphai.github.io/keycloak-admin-aio/>`_
- `Pypi <https://pypi.org/project/keycloak-admin-aio/>`_

How to install?
---------------

.. code:: shell

   poetry add keycloak-admin-aio

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
            users = await kc.users.get(email="@google")
            await asyncio.gather(
                *[
                    kc.users.by_id(user.id).execute_actions_email.send_email(
                        ["UPDATE_PASSWORD"]
                    )
                    for user in users
                ]
            )

    asyncio.run(main())

With client credentials:

.. code:: python

    keycloak_admin_args = {
        "realm": realm,
        "server_url": server_url,
        "client_id": client_id,
        "client_secret": "the_secret",
    }

    async def main():
        async with KeycloakAdmin.with_client_credentials(**keycloak_admin_args) as kc:
            ...

    asyncio.run(main())

License
-------

`Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_


© Copyright 2021, delphai by AtomLeap GmbH
