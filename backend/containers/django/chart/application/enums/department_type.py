from enum import Enum

from django.utils.translation import gettext

"""
部署のEnum
"""

class DepartmentType(Enum):
    SALES = ('100', 'Sales', '営業')
    MARKETING = ('200', 'Marketing', 'マーケティング')
    PRODUCTION = ('300', 'Production', '商品開発')

    def __new__(cls, value, en_name, jp_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.en_name = en_name
        obj.jp_name = jp_name
        return obj

    @classmethod
    def get_condition_value(cls, value):
        for department_type in DepartmentType:
            if department_type.value == value:
                return department_type
        raise ValueError(gettext("E902") % value)
