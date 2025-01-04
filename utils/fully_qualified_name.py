

def fqn(clazz: type) -> str:
    """
    The fully qualified name of a class or function.
    """
    return f"{clazz.__module__}.{clazz.__qualname__}"
# end def
