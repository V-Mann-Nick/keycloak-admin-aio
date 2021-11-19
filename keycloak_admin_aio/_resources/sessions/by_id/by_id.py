from ... import KeycloakResourceWithIdentifier


class SessionsById(KeycloakResourceWithIdentifier):
    """Realm sessions by id.

    .. code:: python

        from keycloak_admin_aio import KeycloakAdmin

        kc: KeycloakAdmin  # needs to be instantiated
        sesson_id: str  # uuid
    """

    def get_url(self) -> str:
        return f"{self._get_parent_url()}/{self.identifier}"

    async def delete(self):
        """Terminate a session by id.

        .. code:: python

            await kc.sessions.by_id(sesson_id).delete()
        """
        connection = await self._get_connection()
        await connection.delete(self.get_url())
