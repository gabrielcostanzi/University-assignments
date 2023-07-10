import re
import pandas as pd


class Semantic_step:
    def __init__(self) -> None:
        self.symbol_table = pd.DataFrame(columns = ['NOME', 'TIPO', 'ESCOPO', 'SIZE'], data = [])
        self.section_data = []
        self.section_start = []
        self.lineno = 1


    def __table_insert_row(self, tree: tuple, escopo: int):
        if len(self.symbol_table.query(f'(NOME == "{tree[2]}" & ESCOPO == {escopo})')) > 0:
            raise BaseException(f'A VARIAVEL [{tree[2]}] JÁ FOI DECLARADO NO MESMO ESCOPO')
        else:
            if tree[0] == 'VAR_DECL':
                size = None
            else:
                size = tree[3]
                tipo_1 = self.verificar_expressao(size,escopo)
                if (tipo_1 != 'INTEIRO') or (size < 0):
                    raise BaseException(f'A LISTA [{tree[2]}] ACEITA APENAS TAMANHOS POSITIVOS E INTEIROS')
            self.symbol_table = pd.concat([
                            self.symbol_table,
                            pd.DataFrame({'NOME': tree[2], 'TIPO': tree[1], 'ESCOPO': escopo, 'SIZE': size},
                            index=[0])], axis=0, ignore_index=True)


    def __semantic_pos_lista(self, tree: tuple, escopo: int):
        pos = self.symbol_table.query(f'(NOME == "{tree[1]}") & (ESCOPO <= {escopo})').index
        if len(pos) == 0:
            raise BaseException(f'A VARIAVEL [{tree[1]}] NÃO FOI DECLARADO')
        else:
            size = self.symbol_table.iloc[max(pos)]['SIZE']
            tipo_1 = self.verificar_expressao(tree[1],escopo)
            tipo_2 = self.verificar_expressao(tree[2],escopo)
            if ('VETOR' not in tipo_1):
                raise BaseException(f'A VARIAVEL [{tree[1]}] NÃO É UMA LISTA')
            else:
                if (tipo_2 == 'INTEIRO'):
                    return tipo_1.replace('VETOR_', '')
                elif (tipo_2 != 'INTEIRO'):
                    raise BaseException(f'POSIÇÃO [{tree[2]}] NÃO É DO TIPO INTEIRO') 
                else:
                    raise BaseException(f'POSIÇÃO [{tree[2]}] NÃO EXSITE NA VARIAVEL [{tree[1]}]')


    def __semantic_var_atrib(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1], escopo)
        tipo_2 = self.verificar_expressao(tree[2], escopo)
        if tipo_1 != tipo_2:
            raise BaseException(f'ERRO DE TIPO PARA A VARIAVEL [{tree[1]}]')


    def __semantic_lista_atrib(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1], escopo)
        tipo_2, size_2 = self.verificar_expressao(tree[2], escopo)
        if tipo_1 != tipo_2:
            raise BaseException(f'ERRO DE TIPO PARA A VARIAVEL [{tree[1]}]')
        else:
            pos = self.symbol_table.query(f'(NOME == "{tree[1]}") & (ESCOPO <= {escopo})').index
            size_1 = self.symbol_table.iloc[max(pos)]['SIZE']
            if size_2 > size_1:
                raise BaseException(f'TAMANHO [{size_1}] DA VARIAVEL [{tree[1]}] INCOMPATÍVEL COM O TAMANHO [{size_2}] DA SEQUÊNCIA')   


    def __semantic_expressao_matematica(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1], escopo)
        tipo_2 = self.verificar_expressao(tree[2], escopo)
        if (tipo_1 == tipo_2) and (tipo_1 != 'BOOLEANO') and (tipo_1 != 'CADEIA'):
            if (tree[2] == 0) and (tree[0] == '/'):
                raise BaseException(f'NÃO É PERMITIDO DIVISÃO POR 0 (ZERO)')
            else:
                return tipo_1
        else:
            raise BaseException(f'TIPOS DIFERENTES PARA A EXPRESSÃO MATEMÁTICA ENTRE VALORES [{tipo_1}] != [{tipo_2}]')


    def __semantic_expressao_logica(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1], escopo)
        tipo_2 = self.verificar_expressao(tree[2], escopo)
        if ((tipo_1 == tipo_2) and (tipo_1 != 'BOOLEANO')) or ((re.match("==|<>", tree[0])) and ((tipo_1 == 'BOOLEANO') or (tipo_2 == 'CADEIA') and (tipo_1 == tipo_2))):
            return 'BOOLEANO'
        elif (tipo_1 == 'BOOLEANO') or (tipo_2 == 'BOOLEANO'):
            raise BaseException(f'NÃO É PERMITIDO COMPARAÇÃO DE [<,<=,>,>=] ENTRE BOOLEANOS [{tipo_1}]')
        elif (tipo_1 == 'CADEIA') or (tipo_2 == 'CADEIA'):
            raise BaseException(f'NÃO É PERMITIDO COMPARAÇÃO ENTRE CADEIA [{tipo_1}]')
        elif (tipo_1 != tipo_2):
            raise BaseException(f'TIPOS DIFERENTES PARA COMPARAÇÃO ENTRE VALORES [{tipo_1}] != [{tipo_2}]')
        
    
    def __semantic_se_enquanto(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1], escopo)
        if tipo_1 != 'BOOLEANO':
            if tree[0] == 'SE':
                raise BaseException(f'ERRO DE TIPO PARA A CONDIÇÃO SE [{tipo_1}]')
            else:
                raise BaseException(f'ERRO DE TIPO PARA A CONDIÇÃO ENQUANTO [{tipo_1}]')
        else:
            self.check_declarations(tree[2], escopo)
        if len(tree) == 4:
            self.check_declarations(tree[3], escopo)
    

    def __semantic_para(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1][1],escopo)
        tipo_2 = self.verificar_expressao(tree[1][2],escopo)
        tipo_3 = self.verificar_expressao(tree[2][2],escopo)
        tipo_4 = self.verificar_expressao(tree[3][2],escopo)
        if (tipo_1 != 'INTEIRO') or (tipo_2 != 'INTEIRO') or (tipo_3 != 'INTEIRO') or (tipo_4 != 'INTEIRO'):
            raise BaseException(f'ERRO DE TIPO PARA A ESTRUTURA PARA')
        elif tree[1][2] == 0:
            raise BaseException(f'O PASSO DA ESTRUTURA PARA DEVE SER DIFERENTE DE ZERO')
        else:
            self.check_declarations(tree[4],escopo)
    

    def __semantic_leia(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1],escopo)
        if tipo_1 != 'CADEIA':
            raise BaseException(f'O TERMO A SER LIDO DEVE SER DO TIPO [CADEIA], MAS O TERMO ESTA DO TIPO: [{tipo_1}]')
        else:
            formato = tree[1].replace('"', '')
            if (formato != '%d') and (formato != '%f') and (formato != '%s'):
                raise BaseException(f'É NECESSARIO ESPECIFICAR O TIPO A SER LIDO [%d ou %f ou %s]')
            else:
                tipo_1 = self.verificar_expressao(formato, escopo)
                tipo_2 = self.verificar_expressao(tree[2], escopo)
                if tipo_1 != tipo_2:
                    raise BaseException(f'O TERMO [{tree[2]}] É DIFERENTE DO FORMATO [{formato}]')


    def __semantic_escreva(self, tree: tuple, escopo: int):
        tipo_1 = self.verificar_expressao(tree[1], escopo)
        if tipo_1 != 'CADEIA':
            raise BaseException(f'O TERMO A SER ESCRITO DEVE SER DO TIPO [CADEIA], MAS O TERMO ESTA DO TIPO: [{tipo_1}]')
        else:
            format_list = re.findall(r'\%d|\%f|\%s', tree[1])
            if len(format_list) != len(tree[2]):
                raise BaseException(f'A QUANTIDADE DE FORMATOS [{len(format_list)}] É INCOMPATIVEL COM A QUANTIDADE DE VARIAVEIS [{len(tree[2])}]')
            for i in range(len(format_list)):
                tipo_1 = self.verificar_expressao(format_list[i], escopo)
                tipo_2 = self.verificar_expressao(tree[2][i], escopo)  
                if tipo_1 != tipo_2:
                    raise BaseException(f'O TERMO [{tree[2][i]}] É DIFERENTE DO FORMATO [{format_list[i]}]')


    def __semantic_lista(self, tree: tuple, escopo: int):
        check_list = []
        for item in tree:
            check_list.append(self.verificar_expressao(item,escopo))
        check_set = list(set(check_list))
        if len(check_set) == 1:
            return ('VETOR_' + check_set[0], len(check_list))
        else:
            raise BaseException(f'LISTA POSSUI VALORES COM TIPOS DIFERENTES')      
    

    def __semantic_variavel(self, tree: tuple, escopo: int):
        pos = self.symbol_table.query(f'(NOME == "{tree}") & (ESCOPO <= {escopo})').index
        if len(pos) == 0:
            raise BaseException(f'A VARIAVEL [{tree}] NÃO FOI DECLARADO')
        else:
            tipo = self.symbol_table.iloc[max(pos)]['TIPO']
            return tipo


    def verificar_expressao(self, tree: tuple, escopo: int):
        if type(tree) == tuple and len(tree) == 0:
            pass
        elif type(tree) == tuple:      
            if (tree[0] == 'VAR_DECL') or (tree[0] == 'LISTA_DECL'):
                self.__table_insert_row(tree, escopo)
            elif(tree[0] == 'POS_LISTA'):
                return self.__semantic_pos_lista(tree, escopo)
            elif tree[0] == 'VAR_ATRIB':
                self.__semantic_var_atrib(tree, escopo)
            elif tree[0] == 'LISTA_ATRIB':
                self.__semantic_lista_atrib(tree, escopo)
            elif re.match("[+\-*/]",tree[0]):
                return self.__semantic_expressao_matematica(tree, escopo)
            elif re.match(">=|<=|==|<>|>|<", tree[0]):
                return self.__semantic_expressao_logica(tree, escopo)
            elif (tree[0] == 'SE') or (tree[0] == 'ENQUANTO'):
                self.__semantic_se_enquanto(tree, escopo)
            elif tree[0] == 'PARA':
                self.__semantic_para(tree, escopo)
            elif tree[0]== 'LEIA':
                self.__semantic_leia(tree, escopo)
            elif tree[0] == 'ESCREVA':
                self.__semantic_escreva(tree, escopo)
        else:
            if type(tree) == int:
                return 'INTEIRO'
            elif type(tree) == float:
                return 'REAL'
            elif '"' in tree:
                return 'CADEIA'
            elif '%d' == tree:
                return 'INTEIRO'
            elif '%f' == tree:
                return 'REAL'
            elif '%s' == tree:
                return 'CADEIA'
            elif (tree == 'TRUE') or (tree == 'FALSE'):
                return 'BOOLEANO'
            elif type(tree) == list:
                return self.__semantic_lista(tree, escopo)      
            elif re.match("[a-zA-Z][a-zA-Z0-9_]*", tree):
                return self.__semantic_variavel(tree, escopo)


    def check_declarations(self, tree: tuple, escopo: int):
        escopo += 1
        for filho in tree[1:]:
            self.lineno += 1
            self.verificar_expressao(filho, escopo)
        self.symbol_table.drop(self.symbol_table.query(f'(ESCOPO == {escopo})').index, axis = 0, inplace = True)


    def initi_semantic(self, tree: tuple):
        # try:
        #     self.check_declarations(tree[:-1],  0)
        #     print('SEMÂNTICO FINALIZADO')
        # except BaseException as e:
        #     print(f'ERRO SEMÂNTICO NA LINHA {self.lineno}: {e}')
        self.check_declarations(tree[:-1],  0)
        print('SEMÂNTICO FINALIZADO')
