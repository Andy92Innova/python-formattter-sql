import re

def tokenizesql(query):
    # Expresión regular para palabras clave, operadores, paréntesis y cadenas
    token_pattern = r"""
           (\bORDER\s+BY\b|\bGROUP\s+BY\b|\bINNER\s+JOIN\b|\bLEFT\s+JOIN\b|\bRIGHT\s+JOIN\b|
           \bSELECT\b|\bFROM\b|\bWHERE\b|\bCASE\b|\bWHEN\b|\bTHEN\b|\bEND\b|
           \bON\b|\bAND\b|\bOR\b|\bLIMIT\b|\bAS\b|\ASC\b|\bDESC\b|       # Palabras clave SQL
           [a-zA-Z_][a-zA-Z0-9_]*|                      # Identificadores (columnas, tablas, alias)
           [<>!=]=|<=|>=|<>|=|                          # Operadores
           [(),*]|                                      # Símbolos
           '.*?'|                                       # Cadenas entre comillas simples
           \s+)                                         # Espacios (pueden ser eliminados más tarde)
       """
    # Compilar la expresión regular para mayor claridad
    pattern = re.compile(token_pattern, re.IGNORECASE | re.VERBOSE)

    # Buscar todos los tokens en la query
    tokens = pattern.findall(query)
    # Limpiar los tokens (eliminar espacios en blancos y descartar token vacíos)
    return [token.strip() for token in tokens if token.strip()]

def format_query(query):
    tokens = tokenizesql(query)

    formatted_query = []
    indent_level = 0
    newline_keywords = {'SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'INNER JOIN',
                        'LEFT JOIN', 'RIGHT JOIN', 'ON', 'AND', 'CASE', 'WHEN'}
    indent_keywords = {'SELECT', 'WHERE', 'ORDER BY', 'GROUP BY', 'CASE'}

    for token in tokens:
        upper_token = token.upper()

        if upper_token in newline_keywords:
            formatted_query.append('\n'+'   ' * indent_level + upper_token)
            if upper_token in indent_keywords:
                indent_level += 1
        elif token == ',':
            formatted_query[-1] += ','  # Add comma to the previous line
        elif token == ')' or upper_token == 'END':
            indent_level -= 1
            formatted_query.append('\n'+'   ' * indent_level + upper_token)
            indent_level -= 1
        elif token == '(' or upper_token == 'CASE':
            formatted_query.append(token)
            indent_level += 1
        else:
            formatted_query.append(' ' + token if len(formatted_query) > 0 else token)

    return ''.join(formatted_query)

# Ejemplo de uso
sql = "SELECT columna1,columna2, columna3 = case when columna4 = 'test' then 'saltito' else 'no saltito' end  from tabla where age > 110 and status = 'active' order by name desc;"
formatted_sql = format_query(sql)

print(formatted_sql)







