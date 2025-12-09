from abc import ABC


class ModuleAccess(ABC):
    ALLOWED_ROLES = []

    @classmethod
    def get_allowed_roles(cls):
        """
        Lazy enough to not want to rewrite this method 20 times.
        Returns the allowed roles to access a certain module.
        Allowed roles are defined at a controller level.
        """
        return cls.ALLOWED_ROLES
