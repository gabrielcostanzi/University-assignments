import ply.yacc as yacc
from step.lexer_step import tokens


precedence = (
    ('left', 'OP_SOMA', 'OP_SUB'),
    ('right', 'OP_MULT', 'OP_DIV')
)


def p_inicia_programa(p):
    '''programa : INICIO declaracoes FIM
    '''
    if type(p[2]) == list:
        p[0] = tuple([p[1]] + p[2] + [p[3]])
    else:
        p[0] = (p[1], p[2], p[3])


def p_declaracoes(p):
    '''declaracoes :  declaracao declaracoes
    | estrutura declaracoes
    |
    '''
    if len(p) == 3:
        if p[2]:
            p[0] = [p[1]] + list(p[2])
        else:
            p[0] = [p[1]]
    elif len(p) == 1:
        p[0] = None


def p_declaracao(p):
    '''declaracao : expressao FIM_LINHA
    | initi_var FIM_LINHA
    | atrib_var FIM_LINHA
    | leia FIM_LINHA
    | escreva FIM_LINHA
    '''    
    p[0] = p[1]


def p_inicializa_variavel(p):
    '''initi_var : INTEIRO VARIAVEL
    | REAL VARIAVEL
    | BOOLEANO VARIAVEL
    | CADEIA VARIAVEL
    | VETOR_INTEIRO VARIAVEL ABRE_COLCHETES NUM_INTEIRO FECHA_COLCHETES
    | VETOR_REAL VARIAVEL ABRE_COLCHETES NUM_INTEIRO FECHA_COLCHETES
    | VETOR_BOOLEANO VARIAVEL ABRE_COLCHETES NUM_INTEIRO FECHA_COLCHETES
    '''    
    if len(p) == 6:
        p[0] = ('LISTA_DECL', p[1], p[2], p[4])
    else:
        p[0] = ('VAR_DECL', p[1], p[2])


def p_atrib_variavel(p):
    '''atrib_var : VARIAVEL OP_ATRIBUI expressao
    | VARIAVEL OP_ATRIBUI ABRE_COLCHETES cria_sequencia FECHA_COLCHETES
    | pos_lista OP_ATRIBUI expressao
    '''    
    if len(p) == 4:
        p[0] = ('VAR_ATRIB', p[1], p[3])
    else:
        p[0] = ('LISTA_ATRIB', p[1], p[4])


def p_pos_lista(p):
    '''pos_lista : VARIAVEL ABRE_COLCHETES expressao FECHA_COLCHETES
    '''    
    p[0] = ('POS_LISTA', p[1], p[3])


def p_cria_sequencia(p):
    '''cria_sequencia : termo VIRGULA cria_sequencia
    | termo
    '''    
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_leia(p):
    '''leia : LEIA ABRE_PARENTESES termo VIRGULA VARIAVEL FECHA_PARENTESES
    '''
    p[0] =(p[1], p[3], p[5])


def p_escreva(p):
    '''escreva : ESCREVA ABRE_PARENTESES termo VIRGULA cria_sequencia FECHA_PARENTESES 
    | ESCREVA ABRE_PARENTESES termo FECHA_PARENTESES
    '''
    if len(p) == 7:
        p[0] =(p[1], p[3], p[5])
    else:
        p[0] = (p[1], p[3], [])

def p_estrutura(p):
    '''estrutura :  se
    | enquanto
    | para
    '''    
    p[0] = p[1]


def p_estrutura_se(p):
    '''se : SE ABRE_PARENTESES expressao FECHA_PARENTESES ENTAO declaracoes FIMSE 
    | SE ABRE_PARENTESES expressao FECHA_PARENTESES ENTAO declaracoes SENAO declaracoes FIMSE
    '''
    if not p[6]:
        p[6] = []
    if len(p) == 10:
        if not p[8]:
            p[8] = []
        p[0] = (p[1], p[3], tuple(['BODY'] + p[6]), tuple(['BODY'] + p[8]))
    else:
        p[0] = (p[1], p[3], tuple(['BODY'] + p[6]))
       

def p_estrutura_para(p):
    '''para : PARA VARIAVEL DE termo ATE termo PASSO termo FACA declaracoes FIMPARA
    '''
    if not p[10]:
        p[10] = []
    if p[8] > 0:
        p[0] = (p[1], ('<=', p[2], p[6]), ('VAR_ATRIB', p[2], p[4]), ('VAR_ATRIB', p[2], ('+', p[2], p[8])), tuple(['BODY'] + p[10]))
    else:
        p[0] = (p[1], ('>=', p[2], p[6]), ('VAR_ATRIB', p[2], p[4]), ('VAR_ATRIB', p[2], ('+', p[2], p[8])), tuple(['BODY'] + p[10]))


def p_estrutura_enquanto(p):
    '''enquanto : ENQUANTO ABRE_PARENTESES expressao FECHA_PARENTESES FACA declaracoes FIMENQUANTO
    '''
    if not p[6]:
        p[6] = []
    p[0] = (p[1], p[3], tuple(['BODY'] + p[6]))
    

def p_expressao(p):
    '''
    expressao : termo OP_SOMA expressao
    | termo OP_SUB expressao
    | termo OP_MULT expressao
    | termo OP_DIV expressao
    | termo OP_MENOR expressao
    | termo OP_MAIOR expressao
    | termo OP_MENOR_IGUAL expressao
    | termo OP_MAIOR_IGUAL expressao
    | termo OP_IGUAL expressao
    | termo OP_DIFF expressao
    | termo OP_AND expressao
    | termo OP_OR expressao
    | termo
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_termo(p):
    '''termo : NUM_INTEIRO
    | NUM_FLOAT
    | ABRE_PARENTESES expressao FECHA_PARENTESES
    | NUM_BOOLEANO
    | STRING_CADEIA
    | VARIAVEL
    | pos_lista
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_error(p):
    print(f"ERROR SINTÁTICO NA LINHA {p.lineno} para o símbolo {p.value}")


parser = yacc.yacc()
