"""
This module provides a typed schema of the Keycloak input and outputs.

There's a few ways in which you can instantiate a dataclass including some not
provided by the standard libarary:

Instantiate a dataclass with keyword arguments
----------------------------------------------

.. code:: python

    from keycloak_admin_aio import RoleRepresentation

    role_representation = RoleRepresentation(
        name="role-name", description="role-description"
    )

    ## or from a dict

    role_representation = RoleRepresentation(
        **{"name": "role-name", "description": "role-description"}
    )


Instantiate a dataclass with the from_dict class method
-------------------------------------------------------

The above works well if you have a flat data model. If you have a dataclass
which uses other dataclasses using ``**`` with a dict will not work as
expected.  If you have a nested data structure you should use the ``from_dict``
function.

.. code:: python

    from keycloak_admin_aio import ClientMappingsRepresentation

    client_mapping_representation = ClientMappingsRepresentation(
        client="some-client", mappings=[RoleRepresentation(name="some-role")]
    )

    # can also be done like this

    client_mapping_representation = ClientMappingsRepresentation.from_dict(
        {"client": "some-client", "mappings": [{"name": "some-role"}]}
    )

    assert client_mapping_representation.mappings[0].name == "some-role"

Instantiate a list of dataclasses with the from_list class method
-----------------------------------------------------------------

If you have a list of dictionaries you want to parse into a list of dataclasses
you use the ``from_list`` method.

.. code:: python

    from keycloak_admin_aio import RoleRepresentation

    roles = [{"name": "A"}, {"name": "B"}, {"name": "C"}]
    roles = RoleRepresentation.from_list(roles)
"""

# Needed for sphinx autodoc
__all__ = [
    "RoleRepresentation",
    "RoleRepresentationComposites",
    "ClientMappingsRepresentation",
    "MappingsRepresentation",
    "ProtocolMapperRepresentation",
    "ClientScopeRepresentation",
    "FederatedIdentityRepresentation",
    "CredentialRepresentation",
    "UserConsentRepresentation",
    "UserRepresentation",
    "GroupRepresentation",
    "ScopeRepresentation",
    "ResourceRepresentation",
    "PolicyRepresentation",
    "ResourceServerRepresentation",
    "ClientRepresentation",
    "RequiredActionProviderRepresentation",
    "UserSession",
]

from .types import *
