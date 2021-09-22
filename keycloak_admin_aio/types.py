from dataclasses import dataclass
from keycloak_admin_aio.lib.data_class import DataClass
from typing import Any, Optional


@dataclass
class RoleRepresentationComposites(DataClass):
    realm: Optional[list[str]] = None
    client: Optional[dict[str, list[str]]] = None


@dataclass
class RoleRepresentation(DataClass):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    containerId: Optional[str] = None
    composites: Optional[RoleRepresentationComposites] = None
    composite: Optional[bool] = None
    clientRole: Optional[bool] = None
    attributes: Optional[dict[str, list[str]]] = None


@dataclass
class ClientMappingsRepresentation(DataClass):
    id: Optional[str] = None
    client: Optional[str] = None
    mappings: Optional[list[RoleRepresentation]] = None


@dataclass
class MappingsRepresentation(DataClass):
    clientMappings: Optional[dict[str, ClientMappingsRepresentation]] = None
    realmMappings: Optional[RoleRepresentation] = None


@dataclass
class ProtocolMapperRepresentation(DataClass):
    id: Optional[str] = None
    name: Optional[str] = None
    protocol: Optional[str] = None
    protocolMapper: Optional[str] = None


@dataclass
class ClientScopeRepresentation(DataClass):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    protocol: Optional[str] = None
    protocolMappers: Optional[list[ProtocolMapperRepresentation]] = None
    attributes: Optional[dict[str, str]] = None


@dataclass
class FederatedIdentitiyRepresentation(DataClass):
    userId: Optional[str] = None
    userName: Optional[str] = None
    identityProvider: Optional[str] = None


@dataclass
class CredentialRepresentation(DataClass):
    id: Optional[str] = None
    createdDate: Optional[int] = None
    credentialData: Optional[str] = None
    priority: Optional[int] = None
    secretData: Optional[str] = None
    temporary: Optional[bool] = None
    type: Optional[str] = None
    userLabel: Optional[str] = None
    value: Optional[str] = None


@dataclass
class UserConsentRepresentation(DataClass):
    clientId: Optional[str] = None
    createdDate: Optional[int] = None
    grantedClientScopes: Optional[list[str]] = None
    lastUpdatedDate: Optional[int] = None



@dataclass
class UserRepresentation(DataClass):
    id: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    emailVerified: Optional[bool] = None
    username: Optional[str] = None
    requiredActions: Optional[list[str]] = None
    createdTimestamp: Optional[int] = None
    federationLink: Optional[str] = None
    federatedIdentities: Optional[list[FederatedIdentitiyRepresentation]] = None
    enabled: Optional[bool] = None
    disableableCredentialTypes: Optional[list[str]] = None
    credentials: Optional[list[CredentialRepresentation]] = None
    notBefore: Optional[int] = None
    access: Optional[dict[str, bool]] = None
    attributes: Optional[dict[str, list[str]]] = None
    clientConsents: Optional[list[UserConsentRepresentation]] = None
    totp: Optional[bool] = None
    self: Optional[str] = None
    origin: Optional[str] = None
    realmRoles: Optional[list[str]] = None
    groups: Optional[list[str]] = None
    serviceAccountClientId: Optional[str] = None
    clientRoles: Optional[dict[str, Any]] = None


@dataclass
class GroupRepresentation(DataClass):
    id: Optional[str] = None
    name: Optional[str] = None
    realmRoles: Optional[list[str]] = None
    path: Optional[str] = None
    subGroups: Optional[list[dict]] = None
    clientRoles: Optional[dict[str, Any]] = None
    attributes: Optional[dict[str, list[str]]] = None
    access: Optional[dict[str, bool]] = None
