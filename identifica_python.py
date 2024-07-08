import re

# Definição dos padrões de tokens
token_specification = [
    ('FUNC_DECL', r'def\s+[a-zA-Z_][a-zA-Z_0-9]*\s*\(.*\)\s*:'),  # Declaração de função
    ('IF_ELSE', r'if\s+.*?:\s*.*else\s*:'),                        # Bloco if-else
    ('IF', r'if\s+.*:'),                                          # Bloco if
    ('ELSE', r'else\s*:'),                                        # Bloco else
    ('VAR_DECL', r'[a-zA-Z_][a-zA-Z_0-9]*\s*=\s*'),               # Declarações de variáveis
    ('BOOL', r'\bTrue\b|\bFalse\b'),                              # Valores booleanos
    ('PRINT', r'print\s*\(.*\)'),                                 # Comando de escrita
    ('FUNC_CALL', r'[a-zA-Z_][a-zA-Z_0-9]*\s*\(.*\)'),            # Chamadas de funções
    ('EXPR', r'[a-zA-Z_][a-zA-Z_0-9]*\s*([+\-*/<>=!]\s*[a-zA-Z_0-9.]+)+'), # Expressões aritméticas e comparativas
    ('Nreal', r'\d+\.\d+'),                                       # Números reais
    ('Nint', r'\d+'),                                             # Números inteiros
    ('COMMENT', r'#.*'),                                          # Comentários
    ('DOCSTRING', r'"""(.|\n)*?"""|\'\'\'(.|\n)*?\'\'\''),        # Docstrings
    ('STRING', r'\".*?\"|\'.*?\''),                               # Strings
    ('COLON', r':'),                                              # Dois-pontos
    ('NEWLINE', r'\n'),                                           # Quebra de linha
    ('SKIP', r'[ \t]+'),                                          # Espaços e tabulações
    ('MISMATCH', r'.'),                                           # Qualquer outro caractere
]

# Compilação das expressões regulares
token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification), re.MULTILINE)

def le_token(code):
    """
    Função geradora que retorna tokens de um código fonte
    """
    line_num = 1
    line_start = 0
    tokens = []
    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind in ('SKIP', 'COMMENT', 'DOCSTRING'):
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado na linha {line_num}')
        elif kind == 'VAR_DECL':
            # Verificar a declaração da variável
            decl_match = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*\s*=\s*(True|False|\d+(\.\d+)?|\".*?\"|\'.*?\')', value)
            if decl_match:
                tokens.append((kind, value.strip(), line_num, column))
            else:
                raise RuntimeError(f'Declaração de variável inválida na linha {line_num}: {value.strip()}')
        else:
            tokens.append((kind, value.strip(), line_num, column))
    return tokens

def testar_arquivo(filename):
    print(f'Testando arquivo: {filename}')
    try:
        with open(filename, 'r') as f:
            code = f.read()
        tokens = le_token(code)
        for token in tokens:
            print(token)
        print(f'O arquivo {filename} foi analisado com sucesso.\n')
    except RuntimeError as e:
        print(f'Erro léxico encontrado no arquivo {filename}: {e}\n')

if __name__ == '__main__':
    testar_arquivo('teste1.py')
    testar_arquivo('teste2.py')
