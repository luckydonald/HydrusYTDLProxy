from typing import overload, TypeVar

A = TypeVar('A', bound=object)  # A can be any type, but not None
B = TypeVar('B')


@overload
def default(a: None, b: B) -> B: ...

@overload
def default(a: A, b: B) -> A: ...

def default(a: A | None, b: B) -> A | B:
    if a is None:
        return b
    # end if
    return a
# end def