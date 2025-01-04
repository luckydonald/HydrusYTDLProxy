from typing import overload, TypeVar

VALUE = TypeVar('VALUE', bound=object)  # can be any type, but not None
DEFAULT = TypeVar('DEFAULT')


# noinspection PyShadowingNames
@overload
def default(value: None, default: DEFAULT) -> DEFAULT: ...

# noinspection PyShadowingNames
@overload
def default(value: VALUE, default: DEFAULT) -> VALUE: ...

# noinspection PyShadowingNames
def default(value: VALUE | None, default: DEFAULT) -> VALUE | DEFAULT:
    if value is None:
        return default
    # end if
    return value
# end def
