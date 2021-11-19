from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional

from ._data_class import DataClass


@dataclass
class RoleRepresentationComposites(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_rolerepresentation-composites"""

    realm: Optional[list[str]] = None
    client: Optional[dict[str, list[str]]] = None


@dataclass
class RoleRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_rolerepresentation"""

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
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_clientmappingsrepresentation"""

    id: Optional[str] = None
    client: Optional[str] = None
    mappings: Optional[list[RoleRepresentation]] = None


@dataclass
class MappingsRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_mappingsrepresentation"""

    clientMappings: Optional[dict[str, ClientMappingsRepresentation]] = None
    realmMappings: Optional[list[RoleRepresentation]] = None


@dataclass
class ProtocolMapperRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_protocolmapperrepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    protocol: Optional[str] = None
    protocolMapper: Optional[str] = None


@dataclass
class ClientScopeRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_clientscoperepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    protocol: Optional[str] = None
    protocolMappers: Optional[list[ProtocolMapperRepresentation]] = None
    attributes: Optional[dict[str, str]] = None


@dataclass
class FederatedIdentityRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_federatedidentityrepresentation"""

    userId: Optional[str] = None
    userName: Optional[str] = None
    identityProvider: Optional[str] = None


@dataclass
class CredentialRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_credentialrepresentation"""

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
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_userconsentrepresentation"""

    clientId: Optional[str] = None
    createdDate: Optional[int] = None
    grantedClientScopes: Optional[list[str]] = None
    lastUpdatedDate: Optional[int] = None


@dataclass
class UserRepresentation(DataClass):  # type: ignore
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_userrepresentation"""

    id: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    emailVerified: Optional[bool] = None
    username: Optional[str] = None
    requiredActions: Optional[list[str]] = None
    createdTimestamp: Optional[int] = None
    federationLink: Optional[str] = None
    federatedIdentities: Optional[list[FederatedIdentityRepresentation]] = None
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
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_grouprepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    realmRoles: Optional[list[str]] = None
    path: Optional[str] = None
    subGroups: Optional[list[GroupRepresentation]] = None
    clientRoles: Optional[dict[str, Any]] = None
    attributes: Optional[dict[str, list[str]]] = None
    access: Optional[dict[str, bool]] = None


@dataclass
class ScopeRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_scoperepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    displayName: Optional[str] = None
    iconUri: Optional[str] = None
    policies: Optional[list[PolicyRepresentation]] = None
    resources: Optional[list[ResourceRepresentation]] = None


@dataclass
class ResourceRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_resourcerepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    displayName: Optional[str] = None
    icon_uri: Optional[str] = None
    attributes: Optional[dict[str, str]] = None
    ownerManagedAccess: Optional[bool] = None
    scopes: Optional[list[ScopeRepresentation]] = None
    type: Optional[str] = None
    uris: Optional[list[str]] = None


@dataclass
class PolicyRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_policyrepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[dict[str, str]] = None
    owner: Optional[str] = None
    logic: Optional[str] = None
    policies: Optional[list[str]] = None
    resources: Optional[list[str]] = None
    resourcesData: Optional[list[ResourceRepresentation]] = None
    scopes: Optional[list[str]] = None
    scopesData: Optional[list[ScopeRepresentation]] = None
    type: Optional[str] = None


@dataclass
class ResourceServerRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_resourceserverrepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    allowRemoteResourceManagement: Optional[bool] = None
    clientId: Optional[str] = None
    decisionStrategy: Optional[Literal["AFFIRMATIVE", "UNANIMOUS", "CONSENSUS"]] = None
    policyEnforcementMode: Optional[
        Literal["ENFORCING", "PERMISSIVE", "DISABLED"]
    ] = None
    resources: Optional[list[ResourceRepresentation]] = None
    scopes: Optional[list[ScopeRepresentation]] = None
    policies: Optional[list[PolicyRepresentation]] = None


@dataclass
class ClientRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_clientrepresentation"""

    id: Optional[str] = None
    name: Optional[str] = None
    access: Optional[dict[str, bool]] = None
    adminUrl: Optional[str] = None
    alwaysDisplayInConsole: Optional[bool] = None
    attributes: Optional[dict[str, str]] = None
    authenticationFlowBindingOverrides: Optional[dict[str, str]] = None
    authorizationServicesEnabled: Optional[bool] = None
    authorizationSettings: Optional[ResourceServerRepresentation] = None
    baseUrl: Optional[str] = None
    bearerOnly: Optional[bool] = None
    clientAuthenticatorType: Optional[str] = None
    clientId: Optional[str] = None
    consentRequired: Optional[bool] = None
    defaultClientScopes: Optional[list[str]] = None
    description: Optional[str] = None
    directAccessGrantsEnabled: Optional[bool] = None
    enabled: Optional[bool] = None
    frontchannelLogout: Optional[bool] = None
    fullScopeAllowed: Optional[bool] = None
    implicitFlowEnabled: Optional[bool] = None
    nodeReRegistrationTimeout: Optional[int] = None
    notBefore: Optional[int] = None
    oauth2DeviceAuthorizationGrantEnabled: Optional[bool] = None
    optionalClientScopes: Optional[list[str]] = None
    origin: Optional[str] = None
    protocol: Optional[str] = None
    protocolMappers: Optional[list[ProtocolMapperRepresentation]] = None
    publicClient: Optional[bool] = None
    redirectUris: Optional[list[str]] = None
    registeredNodes: Optional[dict[str, str]] = None
    registrationAccessToken: Optional[str] = None
    rootUrl: Optional[str] = None
    secret: Optional[str] = None
    serviceAccountsEnabled: Optional[bool] = None
    standardFlowEnabled: Optional[bool] = None
    surrogateAuthRequired: Optional[bool] = None
    webOrigins: Optional[list[str]] = None


@dataclass
class RequiredActionProviderRepresentation(DataClass):
    """https://www.keycloak.org/docs-api/15.0/rest-api/index.html#_requiredactionproviderrepresentation"""

    alias: Optional[str] = None
    config: Optional[dict[str, Any]] = None
    defaultAction: Optional[bool] = None
    enabled: Optional[bool] = None
    name: Optional[str] = None
    priority: Optional[int] = None
    providerId: Optional[str] = None


@dataclass
class UserSession(DataClass):
    """This is no default Keycloak representation."""

    clients: Optional[dict[str, str]] = None
    id: Optional[str] = None
    ipAddress: Optional[str] = None
    lastAccess: Optional[int] = None
    start: Optional[int] = None
    userId: Optional[str] = None
    username: Optional[str] = None


ResourceType = Literal[
    "REALM",
    "REALM_ROLE",
    "REALM_ROLE_MAPPING",
    "REALM_SCOPE_MAPPING",
    "AUTH_FLOW",
    "AUTH_EXECUTION_FLOW",
    "AUTH_EXECUTION",
    "AUTHENTICATOR_CONFIG",
    "REQUIRED_ACTION",
    "IDENTITY_PROVIDER",
    "IDENTITY_PROVIDER_MAPPER",
    "PROTOCOL_MAPPER",
    "USER",
    "USER_LOGIN_FAILURE",
    "USER_SESSION",
    "USER_FEDERATION_PROVIDER",
    "USER_FEDERATION_MAPPER",
    "GROUP",
    "GROUP_MEMBERSHIP",
    "CLIENT",
    "CLIENT_INITIAL_ACCESS_MODEL",
    "CLIENT_ROLE",
    "CLIENT_ROLE_MAPPING",
    "CLIENT_SCOPE",
    "CLIENT_SCOPE_MAPPING",
    "CLIENT_SCOPE_CLIENT_MAPPING",
    "CLUSTER_NODE",
    "COMPONENT",
    "AUTHORIZATION_RESOURCE_SERVER",
    "AUTHORIZATION_RESOURCE",
    "AUTHORIZATION_SCOPE",
    "AUTHORIZATION_POLICY",
    "CUSTOM",
]

OperationType = Literal["CREATE", "DELETE", "ACTION", "UPDATE"]
