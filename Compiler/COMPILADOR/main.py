from step.lexer_step import lexer
from step.syntax_step import parser
import step.semantic_step
import step.code_generator
import sys


def input(filename: str) -> str:
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def check_lexer() -> bool:
    for token in lexer:
        if token.type == 'BAD_VARIAVEL':
            print(f"ERROR LÉXICO NA LINHA {token.lineno} para a variavel mal formada {token.value}")
            return False
        elif token.type == 'BAD_CADEIA':
            print(f"ERROR LÉXICO NA LINHA {token.lineno} para a cadeia mal formada {token.value}")
            return False
    lexer.lineno = 1
    return True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    path = 'outros/codigo.txt'
    lexer.input(input(path))
    if check_lexer():
        tree = parser.parse(input(path), lexer = lexer)
        print(tree)
    semantic = step.semantic_step.Semantic_step()
    semantic.initi_semantic(tree)
    generator = step.code_generator.Generator_step()
    generator.initi_code_generator(tree)

