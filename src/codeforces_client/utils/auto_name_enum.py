from enum import Enum, EnumMeta


class CaseInsensitiveEnumMeta(EnumMeta):

    def __call__(cls, value, *args, **kwargs):
        return super().__call__(value.upper(), *args, **kwargs)


class AutoNameEnum(Enum, metaclass=CaseInsensitiveEnumMeta):

    def _generate_next_value_(name, start, count, last_values):
        return name
