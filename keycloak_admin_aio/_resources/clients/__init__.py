"""https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_clients_resource

One should not be confused between ``client_id`` and the UUID a ``client`` has.
Therefor this section will refer to variable names containing the UUID of a
client as ``client_uuid``.
"""

from .clients import Clients
