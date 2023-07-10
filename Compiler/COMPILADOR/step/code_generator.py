import re
import pandas as pd


class Generator_step:
    def __init__(self) -> None:
        self.symbol_table = pd.DataFrame(columns = ['NOME', 'AUX_NOME', 'TIPO', 'ESCOPO', 'SIZE'], data = [])
        self.section_data = ['.section .data']
        self.section_start = ['.section .text', '.globl _start', '_start:', 'finit']
        self.lineno = 1


    def __generate_formats(self):
        self.section_data.append('tipoNum: .asciz "%d"')
        self.section_data.append('tipoFloat: .asciz "%f"')
        self.section_data.append('tipoString: .asciz "%s"')
        self.section_data.append('escreva: .space 1000')


    def __table_insert_row(self, tree: tuple, escopo: int):
        if len(self.symbol_table.query(f'(NOME == "{tree[2]}" & ESCOPO == {escopo})')) > 0:
            raise BaseException(f'A VARIAVEL [{tree[2]}] JÁ FOI DECLARADO NO MESMO ESCOPO')
        else:
            if tree[0] == 'VAR_DECL':
                size = None
            else:
                size = tree[3]
            self.symbol_table = pd.concat([
                            self.symbol_table,
                            pd.DataFrame({'NOME': tree[2], 'AUX_NOME': tree[2] + f'_{self.lineno}', 'TIPO': tree[1], 'ESCOPO': escopo, 'SIZE': size},
                            index=[0])], axis=0, ignore_index=True)


    def __generator_var_decl(self, tree: tuple):
        if tree[1] == 'INTEIRO':
            self.section_data.append(f'{tree[2] + f"_{self.lineno}"}: .int 0')
        elif tree[1] == 'REAL':
            self.section_data.append(f'{tree[2] + f"_{self.lineno}"}: .float 0.0')
        elif tree[1] == 'BOOLEANO':
            self.section_data.append(f'{tree[2] + f"_{self.lineno}"}: .int 0')
        elif tree[1] == 'CADEIA':
            self.section_data.append(f'{tree[2] + f"_{self.lineno}"}: .space 1000')
        elif 'VETOR' in tree[1]:
            self.section_data.append(f'{tree[2] + f"_{self.lineno}"}: .space {4 * tree[3]}')


    def __generator_expressao_matematica(self, tree: tuple, escopo: int):
        tipo_1 = self.gerar_linha_codigo(tree[2], escopo)
        self.gerar_linha_codigo(tree[1], escopo)
        if (tipo_1 == 'INTEIRO'):
            self.section_start.append(f'popl %eax')
            self.section_start.append(f'popl %ebx')
            if tree[0] == '+':
                self.section_start.append(f'addl %ebx, %eax')
            elif tree[0] == '-':
                self.section_start.append(f'subl %ebx, %eax')
            elif tree[0] == '*':
                self.section_start.append(f'imull %ebx')
            elif tree[0] == '/':
                self.section_start.append(f'idivl %ebx')
            self.section_start.append(f'pushl %eax')
        else:
            if tree[0] == '+':
                self.section_start.append(f'fadd %st(1), %st(0)')
            elif tree[0] == '-':
                self.section_start.append(f'fsub %st(1), %st(0)')
            elif tree[0] == '*':
                self.section_start.append(f'fdiv %st(1), %st(0)')
            elif tree[0] == '/':
                self.section_start.append(f'fmul %st(1), %st(0)')
        return tipo_1


    def __generator_expressao_logica(self, tree: tuple, escopo: int, label: str = None):
        self.gerar_linha_codigo(tree[2], escopo)
        self.gerar_linha_codigo(tree[1], escopo)
        self.section_start.append(f'popl %eax')
        self.section_start.append(f'popl %ebx')
        self.section_start.append(f'cmpl %ebx, %eax')
        if label:
            if tree[0] == '>=':
                self.section_start.append(f'jl {label}')
            elif tree[0] == '<=':
                self.section_start.append(f'jg {label}')
            elif tree[0] == '>':
                self.section_start.append(f'jle {label}')
            elif tree[0] == '<':
                self.section_start.append(f'jge {label}')
            elif tree[0] == '==':
                self.section_start.append(f'jne {label}')
            elif tree[0] == '<>':
                self.section_start.append(f'je {label}')
        else:
            label_true = f"logica_true_{self.lineno}"
            label_cont = f"logica_cont_{self.lineno}"
            if tree[0] == '>=':
                self.section_start.append(f'jge {label_true}')
            elif tree[0] == '<=':
                self.section_start.append(f'jle {label_true}')
            elif tree[0] == '>':
                self.section_start.append(f'jg {label_true}')
            elif tree[0] == '<':
                self.section_start.append(f'jl {label_true}')
            elif tree[0] == '==':
                self.section_start.append(f'je {label_true}')
            elif tree[0] == '<>':
                self.section_start.append(f'jne {label_true}')
            self.section_start.append(f'pushl $0')
            self.section_start.append(f'jmp {label_cont}')
            self.section_start.append(f'{label_true}:')
            self.section_start.append(f'pushl $1')
            self.section_start.append(f'{label_cont}:')


    def __generator_escreva(self, tree: tuple, escopo: int):
        self.section_start.append(f'pushl %eax')
        self.section_start.append(f'pushl %ebx')
        self.section_start.append(f'pushl %ecx')
        self.section_start.append(f'pushl %edx')
        addl_value = 0
        tree[2].reverse()
        for var in tree[2]:
            if (type(var) == str) and ('"' in var):
                var_size = len(var.replace('"', '')) + 1
                self.section_start.append(f'pushl ${var_size}')
                self.section_start.append(f'call malloc')
                self.section_start.append(f'addl $4, %esp')
                self.section_start.append(f'movl %eax, %edi')
                self.gerar_linha_codigo(var, escopo)
                self.section_start.append(f'pushl %eax')
                addl_value += 4
            else:
                self.gerar_linha_codigo(var, escopo)
                if type(var) == float:
                    self.section_start.append(f'subl $8, %esp')
                    self.section_start.append(f'fstl (%esp)')
                    addl_value += 8
                else:
                    addl_value += 4
        if len(self.symbol_table.query(f"(NOME == '{tree[1]}') & (ESCOPO <= {escopo})")) > 0:
            self.gerar_linha_codigo(tree[1], escopo)
        else:
            self.section_start.append(f'lea escreva, %edi')
            self.gerar_linha_codigo(tree[1], escopo)
            self.section_start.append(f'pushl $escreva')
        self.section_start.append(f'call printf')
        self.section_start.append(f'addl ${4 + addl_value}, %esp')
        self.section_start.append(f'popl %edx')
        self.section_start.append(f'popl %ecx')
        self.section_start.append(f'popl %ebx')
        self.section_start.append(f'popl %eax')


    def __generator_leia(self, tree: tuple, escopo: int):
        pos = self.symbol_table.query(f'(NOME == "{tree[2]}") & (ESCOPO <= {escopo})').index
        aux_var = self.symbol_table.iloc[max(pos)]['AUX_NOME']
        self.section_start.append(f'pushl ${aux_var}')
        self.gerar_linha_codigo(tree[1].replace('"', ''), escopo)
        self.section_start.append(f'call scanf')
        self.section_start.append(f'addl $8, %esp')


    def __generator_var_atrib(self, tree: tuple, escopo: int):
        if type(tree[1]) != tuple:
            pos = self.symbol_table.query(f'(NOME == "{tree[1]}") & (ESCOPO <= {escopo})').index
            tipo = self.symbol_table.iloc[max(pos)]['TIPO']
            aux_var = self.symbol_table.iloc[max(pos)]['AUX_NOME']
            if ('CADEIA') in tipo:
                self.section_start.append(f'lea {aux_var}, %edi')
            self.gerar_linha_codigo(tree[2], escopo)
            if ('INTEIRO' in tipo) or ('BOOLEANO' in tipo):
                self.section_start.append(f'popl %eax')
                self.section_start.append(f'movl %eax, {aux_var}')
            elif 'REAL' in tipo:
                self.section_start.append(f'fstl {aux_var}')
        else:
            self.__semantic_pos_lista(tree[1], escopo)
            self.section_start.append(f'pushl %edi')
            self.gerar_linha_codigo(tree[2], escopo)
            self.section_start.append(f'popl %eax')
            self.section_start.append(f'popl %edi')
            self.section_start.append(f'movl %eax, (%edi)')


    def __semantic_pos_lista(self, tree: tuple, escopo: int):
        pos = self.symbol_table.query(f'(NOME == "{tree[1]}") & (ESCOPO <= {escopo})').index
        tipo = self.symbol_table.iloc[max(pos)]['TIPO']
        aux_var = self.symbol_table.iloc[max(pos)]['AUX_NOME']
        self.section_start.append(f'movl ${aux_var}, %edi')
        if 'REAL' in tipo:
            value = 8
        else:
            value = 4
        self.gerar_linha_codigo(tree[2], escopo)
        self.section_start.append(f'popl %eax')
        self.section_start.append(f'movl ${value}, %ebx')
        self.section_start.append(f'imull %ebx')
        self.section_start.append(f'addl %eax, %edi')
        self.section_start.append(f'pushl (%edi)')
        return tree[1]


    def __generator_se(self, tree: tuple, escopo: int):
        linha = self.lineno
        label = f'se_false_{linha}'
        if len(tree) == 4:
            self.__generator_expressao_logica(tree[1], escopo, f'senao_{linha}')
        self.__generator_expressao_logica(tree[1], escopo, label)
        self.check_declarations(tree[2], escopo)
        if len(tree) == 4:
            self.section_start.append(f'jmp {label}')
            self.section_start.append(f'senao_{linha}:')
            self.check_declarations(tree[3], escopo)
        self.section_start.append(f'{label}:')

  
    def __generator_enquanto(self, tree: tuple, escopo: int):
        label = f'enquanto_false_{self.lineno}'
        label2 = f'enquanto_true_{self.lineno}'
        self.section_start.append(f'{label2}:')
        self.__generator_expressao_logica(tree[1], escopo, label)
        self.check_declarations(tree[2], escopo)
        self.section_start.append(f'jmp {label2}')
        self.section_start.append(f'{label}:')


    def __generator_para(self, tree: tuple, escopo: int):
        label_false = f'para_false_{self.lineno}'
        label_true = f'para_true_{self.lineno}'
        self.__generator_var_atrib(tree[2], escopo)
        self.section_start.append(f'{label_true}:')
        self.__generator_expressao_logica(tree[1], escopo, label_false)
        self.check_declarations(tree[4], escopo)
        self.__generator_var_atrib(tree[3], escopo)
        self.section_start.append(f'jmp {label_true}')
        self.section_start.append(f'{label_false}:')


    def gerar_linha_codigo(self, tree: tuple, escopo: int):
        if type(tree) == tuple and len(tree) == 0:
            pass
        elif type(tree) == tuple:
            if (tree[0] == 'VAR_DECL') or (tree[0] == 'LISTA_DECL'):
                self.__generator_var_decl(tree)
                self.__table_insert_row(tree, escopo)
            elif(tree[0] == 'POS_LISTA'):
                return self.__semantic_pos_lista(tree, escopo)
            elif tree[0] == 'VAR_ATRIB':
                self.__generator_var_atrib(tree, escopo)
            elif tree[0] == 'LISTA_ATRIB':
                pos = self.symbol_table.query(f'(NOME == "{tree[1]}") & (ESCOPO <= {escopo})').index
                tipo = self.symbol_table.iloc[max(pos)]['TIPO']
                aux_var = self.symbol_table.iloc[max(pos)]['AUX_NOME']
                self.section_start.append(f'movl ${aux_var}, %edi')
                i = 0
                for item in tree[2]:
                    i += 1
                    self.gerar_linha_codigo(item, escopo)        
                    if 'REAL' in tipo:
                        self.section_start.append(f'fstl (%edi)')
                        value = 8
                    else:
                        self.section_start.append(f'popl (%edi)')
                        value = 4
                    if i < (len(tree[2]) - 1):
                        self.section_start.append(f'addl ${value}, %edi')
            elif re.match("[+\-*/]",tree[0]):
                return self.__generator_expressao_matematica(tree, escopo)
            elif re.match(">=|<=|==|<>|>|<", tree[0]):
                return self.__generator_expressao_logica(tree, escopo)
            elif (tree[0] == 'SE'):
                self.__generator_se(tree, escopo)
            elif (tree[0] == 'ENQUANTO'):
                self.__generator_enquanto(tree, escopo)
            elif (tree[0] == 'PARA'):
                self.__generator_para(tree, escopo)
            elif tree[0] == 'ESCREVA':
                self.__generator_escreva(tree, escopo)
            elif tree[0] == 'LEIA':
                self.__generator_leia(tree, escopo)
        else:       
            if type(tree) == int:
                self.section_start.append(f'pushl ${tree}')
                return 'INTEIRO'
            elif type(tree) == float:
                self.section_start.append(f'lea  escreva, %edi')
                self.gerar_linha_codigo(f'"{tree}"', escopo)
                self.section_start.append(f'pushl $escreva')
                self.section_start.append(f'call atof')
                self.section_start.append(f'addl $4, %esp')
            elif '%d' == tree:
                self.section_start.append(f'pushl $tipoNum')
                return 'INTEIRO'
            elif '%f' == tree:
                self.section_start.append(f'pushl $tipoFloat')
                return 'REAL'
            elif '%s' == tree:
                self.section_start.append(f'pushl $tipoString')
                return 'CADEIA'
            elif '"' in tree:
                for caractere in tree[1:-1]:
                    self.section_start.append(f"movb $'{caractere}', (%edi)")
                    self.section_start.append(f"inc %edi")
                self.section_start.append(f"movb $0, (%edi)")
            elif (tree == 'TRUE'):
                self.section_start.append(f'pushl $1')
            elif (tree == 'FALSE'):
                self.section_start.append(f'pushl $0')
            elif re.match("[a-zA-Z][a-zA-Z0-9_]*", tree):  
                pos = self.symbol_table.query(f'(NOME == "{tree}") & (ESCOPO <= {escopo})').index
                tipo = self.symbol_table.iloc[max(pos)]['TIPO']
                aux_var = self.symbol_table.iloc[max(pos)]['AUX_NOME']
                if tipo == 'CADEIA':
                    self.section_start.append(f'pushl ${aux_var}')
                elif tipo == 'REAL':
                    self.section_start.append(f'fldl {aux_var}')
                    self.section_start.append(f'subl $8, %esp')
                    self.section_start.append(f'fstl (%esp)')
                else:
                    self.section_start.append(f'pushl {aux_var}')
                return tipo


    def check_declarations(self, tree: tuple, escopo: int):
        escopo += 1
        for filho in tree[1:]:
            self.lineno += 1
            self.gerar_linha_codigo(filho, escopo)
        self.symbol_table.drop(self.symbol_table.query(f'(ESCOPO == {escopo})').index, axis = 0, inplace = True)


    def save_assembly_code(self, code: str) -> None:
        with open('main.s', 'w') as f:
            f.write(code)


    def initi_code_generator(self, tree: tuple):
        # try:
        #     self.check_declarations(tree[:-1])
        #     for var in self.section_data:
        #         print(var)
        #     print()
        #     for line in self.section_start:
        #         print(line)       
        # except BaseException as e:
        #     print(e)
        self.__generate_formats()
        self.check_declarations(tree[:-1], 0)
        self.section_start.append('pushl $0')
        self.section_start.append('call exit')
        assembly_code = '\n'.join(self.section_data + ['\n'] + self.section_start)
        assembly_code += '\n'
        self.save_assembly_code(assembly_code)
        
