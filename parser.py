import ply.lex as lex

DEBUG_STATUS = False
DEBUG_TABLES = False

OPTIMIZE = False

keywords = (
    'TYPE', 'ENUM', 'IMPLEMENTS', 'INTERFACE',
)

tokens = keywords + (
    'ID', 'COLON', 'BANG', 'STRING', 'INT', 'LSQUARE', 'RSQUARE',
    'LBRACE', 'RBRACE', 'COMMA', 'LPAREN', 'RPAREN',
)

t_ignore = ' \t\n'

t_COMMA = r'\,'
t_COLON = r'\:'
t_BANG = r'\!'
t_LSQUARE = r'\['
t_RSQUARE= r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r"'([^\\']+|\\'|\\\\)*'"
    t.value = t.value[1:-1]
    return t


def t_error(t):
    raise SyntaxError("Unknown symbol %r" % (t.value[0],))
    print("Skipping", repr(t.value[0]))
    t.lexer.skip(1)

    
def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, 'ID')
    return t


reserved_map = { }
for r in keywords:
    reserved_map[r.lower()] = r

lex.lex(debug=DEBUG_STATUS, optimize=OPTIMIZE)


import ply.yacc as yacc


def p_schema(p):
    '''schema : schema schema_base_elems
              | schema_base_elems
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1], p[2]]


def p_schema_base_elems(p):
    '''schema_base_elems : schema_type_element
                         | schema_enum_element
                         | schema_interface_element
    '''
    p[0] = p[1]


def p_schema_type_element(p):
    '''schema_type_element : TYPE ID schema_type_element_def
                           | TYPE ID IMPLEMENTS ID schema_type_element_def
    '''
    if len(p) == 6:
        p[0] = ('TYPE', p[2], p[4], p[5])
    else:
        p[0] = ('TYPE', None, p[2], p[3])


def p_scheme_type_element_def(p):
    '''schema_type_element_def : LBRACE field_decl_list RBRACE
    '''
    p[0] = p[2]


def p_schema_enum_element(p):
    '''schema_enum_element : ENUM ID LBRACE id_list RBRACE
    '''
    p[0] = ('ENUM', p[2], p[4])


def p_schema_interface_element(p):
    '''schema_interface_element : INTERFACE ID schema_type_element_def
    '''
    p[0] = ('INTERFACE', p[2], p[3])


def p_schema_id_list(p):
    ''' id_list : ID
                | id_list COMMA ID
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1], p[3]]


def p_field_decl_list(p):
    '''field_decl_list : field_decl
                       | field_decl_list field_decl
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1], p[2]]


def p_field_decl(p):
    '''field_decl : ID COLON gql_type'''
    p[0] = (p[1], p[3])


def p_gql_type(p):
    '''gql_type : LSQUARE gql_target_type RSQUARE
                | LSQUARE gql_target_type RSQUARE BANG
                | gql_target_type
    '''
    if len(p) == 2:
        p[0] = ('GRAPHQL_ATOM', p[1])
    elif len(p) == 5:
        p[0] = ('GRAPHQL_NON-NULLABLE_LIST', p[2])
    else:
        # its a list type
        p[0] = ('GRAPHQL_LIST', p[2])


def p_gql_target_type(p):
    '''gql_target_type : ID BANG
                       | ID'''
    if len(p ) == 3:
        p[0] = ('GRAPHQL_TYPE', 'NON-NULLABLE', p[1])
    else:
        p[0] = ('GRAPHQL_TYPE', 'NULLABLE', p[1])


def p_error(p):
    if not p:
        print('Syntax Error at EOF')
    else:
        print('Syntax Error on {0}'.format(p))

        
parser = yacc.yacc(write_tables=DEBUG_TABLES)


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p


code_sample_basic = """
type Post implements Item {
  id: String!
  title: String
  publishedAt: DateTime
  blog: [Blog]!
  likes: [Like!]
}
type Blog {
  id: String!
  name: String!
  description: String
  posts: [Post!]
}
type QueryType {
    hero(episode: Episode): Character
    human(id : String) : Human
    droid(id: ID!): Droid
}
interface Item {
  title: String!
}
enum Category {
  PROGRAMMING_LANGUAGES,
  API_DESIGN
}
enum Category2 {
  PROGRAMMING_LANGUAGES2,
  API_DESIGN2
 }
"""


if __name__ == ('__main__'):
    print(parser.parse(code_sample_basic))
