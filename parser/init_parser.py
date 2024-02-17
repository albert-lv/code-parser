from tree_sitter import Language, Parser

def init_parser(language_name):
    LANGUAGE = Language('language/my-languages.so', language_name)

    parser = Parser()
    parser.set_language(LANGUAGE)
    return parser