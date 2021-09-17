from dataclasses import dataclass
from keycloak_admin_aio.lib.data_class import DataClass
from typing import Optional


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
