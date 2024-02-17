from tree_sitter import Language

def build_language_library():
    Language.build_library(
        'language/my-languages.so',
        ['vendor/tree-sitter-java', 'vendor/tree-sitter-python']
    )

def main():
    build_language_library()

if __name__ == "__main__":
    main()