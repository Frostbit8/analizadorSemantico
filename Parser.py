# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *
DIRECTORIO = os.path.join("C:/Users/anton/Desktop/LenguajesProgramacion/practica2/")
#DIRECTORIO = os.path.join("C:/Users/USUARIO/parser/")

sys.path.append(DIRECTORIO)

GRADING = os.path.join(DIRECTORIO, 'grading')
FICHEROS = os.listdir(GRADING)

TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(GRADING, fich))
         and fich.endswith(".test")]

class CoolParser(Parser):
    nombre_fichero = "Salida"
    tokens = CoolLexer.tokens
    debugfile = 'salida.out'
    errores = []
    debugfile="debug.txt"
    tokens = CoolLexer.tokens
    precedence = (
        ('left', 'IN','LET'),
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', '<','LE','='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'ISVOID'),
        ('left', '@'),
        ('left', '.'),
        ('right', '~')
    )

    @_('l_class')
    def program(self, p):
        return Programa(p.l_class[-1].linea,p.l_class)

    @_('clase ";"')
    def l_class(self, p):
        return [p.clase]

    @_('clase ";" l_class')
    def l_class(self, p):
        return  [p.clase] + p.l_class

    @_('CLASS TYPEID herencia "{" l_feature "}"')
    def clase(self, p):
        return Clase(p.lineno,p.TYPEID,p.herencia,self.nombre_fichero,p.l_feature)

    @_('INHERITS TYPEID')
    def herencia(self, p):
        return p.TYPEID

    @_('empty')
    def herencia(self, p):
        return "Object"

    @_('empty')
    def l_feature(self, p):
        return []
    @_('error ";"')
    def l_feature(self, p):
        return []
    @_('l_feature feature ";"')
    def l_feature(self, p):
        return p.l_feature + [p.feature]

    @_('OBJECTID "(" l_formal ")" ":" TYPEID "{" expr "}" ')
    def feature(self, p):
        return Metodo(p.lineno,p.OBJECTID,p.TYPEID,p.expr, p.l_formal)
    @_('OBJECTID "(" l_formal ")" ":" TYPEID "{" error "}" ')
    def feature(self, p):
        return Nodo(p.lineno)
    @_('OBJECTID ":" TYPEID inicializador')
    def feature(self, p):
        return Atributo(p.lineno,p.OBJECTID,p.TYPEID,p.inicializador)
    @_('empty')
    def l_formal(self,p):
        return []
    @_('formal')
    def l_formal(self,p):
        return [p.formal]
    @_('l_formal "," formal')
    def l_formal(self,p):
        return p.l_formal + [p.formal]
    @_('error ";" formal')
    def l_formal(self,p):
        return [Nodo(p.lineno)]

    @_('OBJECTID ":" TYPEID')
    def formal(self,p):
        return Formal(p.lineno, p.OBJECTID, p.TYPEID)

    @_('ASSIGN expr')
    def inicializador(self, p):
        return p.expr

    @_('empty')
    def inicializador(self, p):
        return NoExpr(-1)

    @_('')
    def empty(self, p):
        pass

    @_('empty')
    def l_expr(self,p):
        return []

    @_(' expr ";" l_expr')
    def l_expr(self,p):
        return  [p.expr] + p.l_expr

    @_('"{" expr ";" l_expr "}"')
    def expr(self, p):
        return Bloque(p.lineno, [p.expr] + p.l_expr )
        
    @_('"{" error ";" l_expr "}"')
    def expr(self, p):
        return [Nodo(p.lineno)]
    @_(' error ";" l_expr')
    def l_expr(self,p):
        return  [Nodo(p.lineno)]

    @_('expr')
    def lista_argumentos(self, p):
        return [p.expr]
    @_('lista_argumentos "," expr')
    def lista_argumentos(self, p):
        return p.lista_argumentos + [p.expr]
    @_('lista_argumentos')
    def s_expr(self, p):
        return p.lista_argumentos
    
    @_('empty')
    def s_expr(self, p):
        return []

    @_('OBJECTID ASSIGN expr')
    def expr(self, p):
        return Asignacion(p.lineno, p.OBJECTID, p.expr)
    
    @_('expr "." OBJECTID "(" s_expr ")" ')
    def expr(self, p):
            return LlamadaMetodo(p.lineno, p.expr, p.OBJECTID, p.s_expr)
    @_('expr "@" TYPEID "." OBJECTID "(" s_expr ")" ')
    def expr(self, p):
            return LlamadaMetodoEstatico(p.lineno, p.expr, p.TYPEID, p.OBJECTID, p.s_expr)
    @_('OBJECTID "(" s_expr ")"')
    def expr(self, p):
        return LlamadaMetodo(p.lineno, Objeto(p.lineno,"self"),p.OBJECTID, p.s_expr)
    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        return Condicional(p.lineno,p.expr0,p.expr1,p.expr2)

    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        return Bucle(p.lineno,p.expr0,p.expr1)

    @_('LET l_decl IN expr ')
    def expr(self, p):
        lets = p.expr
        for i in reversed(p.l_decl):
            lets = Let(p.expr.linea, *i, lets)
        return lets

    @_('decl')
    def l_decl(self,p):
        return [p.decl]

    @_('error "," decl')
    def l_decl(self,p):
        return [Nodo(p.lineno)]

    @_('l_decl "," decl')
    def l_decl(self,p):
        return   p.l_decl + [p.decl] 


    @_('OBJECTID ":" TYPEID inicializador')
    def decl(self,p):
        return (p.OBJECTID,p.TYPEID,p.inicializador)

    @_('CASE expr OF l_ramacase ESAC ')
    def expr(self, p):
        return Swicht(p.lineno,p.expr,p.l_ramacase)

    @_('NEW TYPEID')
    def expr(self, p):
        return Nueva(p.lineno,p.TYPEID)

    @_('ISVOID expr')
    def expr(self, p):
        return EsNulo(p.lineno,p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return Suma(p.lineno,p.expr0,p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return Resta(p.lineno,p.expr0,p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return Multiplicacion(p.lineno,p.expr0,p.expr1)

    @_('expr LE expr')
    def expr(self, p):
        return LeIgual(p.lineno,p.expr0,p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return Menor(p.lineno,p.expr0,p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return Division(p.lineno,p.expr0,p.expr1)

    @_('"~" expr')
    def expr(self, p):
        return Neg(p.lineno,p.expr)

    @_('expr "=" expr')
    def expr(self, p):
        return Igual(p.lineno,p.expr0,p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return Not(p.lineno,p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('OBJECTID')
    def expr(self, p):
        return Objeto(p.lineno,p.OBJECTID)

    @_('INT_CONST')
    def expr(self, p):
        return Entero(p.lineno,p.INT_CONST)

    @_('STR_CONST')
    def expr(self, p):
        return String(p.lineno,p.STR_CONST)

    @_('BOOL_CONST')
    def expr(self, p):
        return Booleano(p.lineno,p.BOOL_CONST)

    @_('OBJECTID  ":" TYPEID DARROW expr ";"')
    def ramacase(self, p):
        return RamaCase(p.lineno,p.OBJECTID,p.TYPEID,p.expr)
    @_('ramacase')
    def l_ramacase(self, p):
        return [p.ramacase]     
    @_(' l_ramacase ramacase')
    def l_ramacase(self, p):
        return p.l_ramacase + [p.ramacase]          
    def error(self, p):
        if p!= None:
            temp = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near '
            if p.type in {'IF', 'FI','OF', 'ELSE', 'POOL', 'LOOP', 'LE'}:
                temp += f'{p.type}'
            elif p.type in CoolLexer.tokens:
                temp += f'{p.type} = {p.value}'
            elif p.type in CoolLexer.literals:
                temp += f"'{p.type}'"
        else:
            temp = '"emptyprogram.test", line 0: syntax error at or near EOF'
        self.errores.append(temp)


for fich in TESTS:
    f = open(os.path.join(GRADING, fich), 'r')
    g = open(os.path.join(GRADING, fich + '.out'), 'r')
    lexer = CoolLexer()
    lexer1 = CoolLexer()
    parser = CoolParser()
    parser.nombre_fichero = fich
    parser.errores = []
    bien = ''.join([c for c in g.readlines() if c and '#' not in c])
    entrada = f.read()
    j = parser.parse(lexer.tokenize(entrada))
    for t0 in lexer1.tokenize(entrada):
        pass
    if j and not parser.errores:
        resultado = '\n'.join([c for c in j.str(0).split('\n')
                               if c and '#' not in c])
    else:
        resultado = '\n'.join(parser.errores)
        resultado += '\n' + "Compilation halted due to lex and parse errors"
    f.close(), g.close()
    if resultado.lower().strip().split() != bien.lower().strip().split():
        print(f"Revisa el fichero {fich}")
        f = open(os.path.join(GRADING, fich)+'.nuestro', 'w')
        g = open(os.path.join(GRADING, fich)+'.bien', 'w')
        f.write(resultado.strip())
        g.write(bien.strip())
        f.close()
        g.close()




    
