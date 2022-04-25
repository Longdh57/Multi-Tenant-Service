import enum


class UserRole(enum.Enum):
    ADMIN = 'admin'
    GUEST = 'guest'


class StaffContractType(enum.Enum):
    PART_TIME = 'Thoi vu'
    OFFICIAL = 'Chinh thuc'


class SearchTreeParam(enum.Enum):
    TREE = 'tree'
    LIST = 'list'


class SalesRoleName(enum.Enum):
    SALE_MANAGER = "sale-manager"
    SALE_ADMIN = "sale-admin"
    SALE_LEADER = "team-lead"
    SALE = "sale"
    ADMINISTRATOR = "administrator"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_list_value(cls):
        return [e.value for e in cls]


class AlgorithmsParentNode(enum.Enum):
    SP = "SP"
    HR = "HR"
