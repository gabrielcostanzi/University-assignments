import ply.lex as lex


tokens_reserved = {
    'INICIO': 'INICIO',
    'FIM': 'FIM',
    'SE': 'SE',
    'ENTAO': 'ENTAO',
    'FIMSE': 'FIMSE',
    'SENAO': 'SENAO',
    'ENQUANTO': 'ENQUANTO',
    'FIMENQUANTO': 'FIMENQUANTO',
    'PARA': 'PARA',
    'DE': 'DE',
    'ATE': 'ATE',
    'PASSO': 'PASSO',
    'FIMPARA': 'FIMPARA',
    'ESCREVA': 'ESCREVA',
    'LEIA': 'LEIA',
    'INTEIRO': 'INTEIRO',
    'VETOR_INTEIRO': 'VETOR_INTEIRO',
    'REAL':'REAL',
    'VETOR_REAL': 'VETOR_REAL',
    'BOOLEANO': 'BOOLEANO',
    'VETOR_BOOLEANO': 'VETOR_BOOLEANO',
    'CADEIA': 'CADEIA',
    'FACA': 'FACA'
}


tokens = [
    'VARIAVEL',
    'BAD_VARIAVEL',
    'BAD_CADEIA',
    'STRING_CADEIA',
    'NUM_INTEIRO',
    'NUM_FLOAT',
    'NUM_BOOLEANO',
    'OP_SOMA',
    'OP_MULT',
    'OP_DIV',
    'OP_SUB',
    'OP_ATRIBUI',
    'OP_MENOR',
    'OP_MAIOR',
    'OP_MENOR_IGUAL',
    'OP_MAIOR_IGUAL',
    'OP_AND',
    'OP_OR',
    'OP_IGUAL',
    'OP_DIFF',
    'FIM_LINHA',
    'VIRGULA',
    'COMENTARIO',
    'ABRE_PARENTESES',
    'FECHA_PARENTESES',
    'ABRE_COLCHETES',
    'FECHA_COLCHETES'
] + list(tokens_reserved.values())



t_OP_SOMA = r"\+"
t_OP_MULT = r'\*'
t_OP_DIV = r'/'
t_OP_SUB = r'-'
t_OP_IGUAL = r'\=\='
t_OP_ATRIBUI = r'\='
t_OP_DIFF = r'\<\>'
t_OP_MENOR_IGUAL = r'\<\='
t_OP_MAIOR_IGUAL = r'\>\='
t_OP_MENOR = r'\<'
t_OP_MAIOR = r'\>'
t_OP_AND = r'\&'
t_OP_OR = r'\|'
t_FIM_LINHA = r'\;'
t_VIRGULA = r'\,'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_ABRE_COLCHETES = r'\['
t_FECHA_COLCHETES = r'\]'


def t_COMENTARIO(t):
    r'\#.*[\n$]'


def t_NUM_BOOLEANO(t):
    r'TRUE|FALSE'
    return t


def t_NUM_FLOAT(t):
    r'(-)?\d+\.\d+'
    t.value = float(t.value)
    return t


def t_BAD_VARIAVEL(t):
    r'([a-zA-Z_0-9]*[@!$%.]+[a-zA-Z_]*)|([0-9]+[a-zA-Z_]+[a-zA-Z_0-9]*)'
    return t


def t_STRING_CADEIA(t):
    r'"[^"]*"'
    return t

def t_BAD_CADEIA(t):
    r'"[^"]*'
    return t


def t_VARIAVEL(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = tokens_reserved.get(t.value.upper(), 'VARIAVEL')
    return t


def t_NUM_INTEIRO(t):
    r'(-)?\d+'
    t.value = int(t.value)
    return t


def t_NOVA_LINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ESPACO_BRANCO(t):
    r'\s+'


def t_TAB(t):
    r'\t+'


def t_error(t):
    print(f"ERROR GENÉRICO LÉXICO NA LINHA {t.lineno} para o símbolo {t.value}")


lexer = lex.lex()
