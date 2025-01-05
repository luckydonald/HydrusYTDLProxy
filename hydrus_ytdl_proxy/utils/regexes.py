import re


def normalize_multiline_regex(multiline_regex):  # noinspection GrazieInspection
    r"""
            Normalize a multiline regex by removing comments and unnecessary whitespace.

            Args:
                multiline_regex (str): A multiline regex string.

            Returns:
                str: A normalized regex string.

            Examples:
                >>> example_regex = r'''
                ...     (?P<name>\w+)  # Match a name
                ...     \s*            # Match any whitespace
                ...     (?P<age>\d+)   # Match an age
                ... '''
                >>> normalize_multiline_regex(example_regex)
                '(?P<name>\\w+)\\s*(?P<age>\\d+)'
            """
    # Remove comments and unnecessary whitespace
    cleaned_lines = []
    for line in multiline_regex.splitlines():
        # Remove comments and strip leading/trailing whitespace
        cleaned_line = re.sub(r'#.*$', '', line)  # Remove comments
        cleaned_line = cleaned_line.strip()  # Strip leading/trailing whitespace
        if cleaned_line:  # Only add non-empty lines
            cleaned_lines.append(cleaned_line)
        # end if

    # Join the cleaned lines without any additional space
    normalized_regex = ''.join(cleaned_lines)
    return normalized_regex
# end def


def example():
    from textwrap import dedent

    # Example usage
    multiline_example = r"""
    (?P<name>\w+)  # Match a name
      \s*            # Match any whitespace
    (?P<age>\d+)   # Match an age
    """

    normalized = normalize_multiline_regex(multiline_example)
    print('Converting Multiline Regex to Normal Regex.')
    print('='*20)
    print("Input regex:")
    print('"""' + dedent(multiline_example) + '"""')
    print("Input regex (repr):")
    print(repr(multiline_example))
    print('=' * 20)
    print("Converted to:")
    print(normalized)
    print('Converted to (repr):')
    print(repr(normalized))
    print('=' * 20)
# end def


if __name__ == '__main__':
    import doctest
    example()
    doctest.testmod()  # Run the doctests in the module
# end if
