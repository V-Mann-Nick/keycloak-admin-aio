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
