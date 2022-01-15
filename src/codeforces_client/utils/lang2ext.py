def lang2ext(programmingLanguage: str) -> str:
    """Return file extention by programming language name"""
    if 'py' in programmingLanguage.lower():
        return 'py'

    if 'c++' in programmingLanguage.lower():
        return 'cpp'

    if 'c#' in programmingLanguage.lower():
        return 'cs'

    if 'c11' in programmingLanguage.lower():
        return 'c'

    if 'js' in programmingLanguage.lower() or 'javascript' in programmingLanguage.lower():
        return 'js'

    if 'java' in programmingLanguage.lower():
        return 'java'

    if 'delphi' in programmingLanguage.lower():
        return 'pas'

    if 'pascal' in programmingLanguage.lower():
        return 'pas'

    return programmingLanguage.lower()
