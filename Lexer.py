# coding: utf-8
# Realizado por XinZhe Jin y José Carlos Tollar García
from sly import Lexer
import os
import re
import ast
PRACTICA = os.path.join("C:/Users/anton/Desktop/LenguajesProgramacion/practica1/")
PRACTICA = os.path.join("C:/Users/USUARIO/lexer")
DIR = os.path.join(PRACTICA, "grading")
FICHEROS = os.listdir(DIR)
TESTS =  [fich for fich in FICHEROS
          if os.path.isfile(os.path.join(DIR, fich)) and fich.endswith(".cool")]
TESTS.sort()

class comen(Lexer):

    tokens = {INSIDE, OUTSIDE, COMMEN,ERROR}
    profundidad = 1
    def salida(self, t):
        return []
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    @_(r'\*\)\Z')
    def ERROR(self, t):
        self.profundidad -= 1
        self.profundidad = 1
        self.begin(CoolLexer)
    @_(r'\*\)')
    def INSIDE(self, t):
        self.profundidad -= 1
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)
    @_(r'\(\*')
    def OUTSIDE(self,t):
        self.profundidad += 1
    @_(r'.')
    def COMMEN(self,t):
        if t.value == '\Z':
            t.type = "ERROR"
            t.value = '"EOF in comment"'
            return t
        else:
            pass


class CoolLexer(Lexer):
    tokens = { OBJECTID, INT_CONST, BOOL_CONST,TYPEID,NUMBER,ERROR1,ERROR3,ERROR4,ERROR5,ERROR6,ASSIGN, COMENT,LINECOMMENT, ERROR2, DARROW,LE, ELSE, STR_CONST, CASE, CLASS, ESAC, FI, IF, IN, INHERITS,ISVOID,LET,LOOP,NEW,NOT,OF, POOL,THEN,WHILE, ERROR}
    literals = { '=', '+', '-', '*', '/', '(', ')', '<', '.',',','~',';',':','(',')', '@', '{','}'}
    asci = {'','','','','',''}

    ELSE =r'[eE][lL][sS][eE]\b'
    CASE =r'[cC][aA][sS][eE]\b'
    CLASS =r'[cC][lL][aA][sS][sS]\b'
    ESAC =r'[eE][sS][aA][cC]\b'
    FI =r'[fF][iI]\b'
    IF =r'[iI][fF]\b'
    IN =r'[iI][nN]\b'
    INHERITS = r'[iI][nN][hH][eE][rR][iI][tT][sS]\b'
    ISVOID = r'[iI][sS][vV][oO][iI][dD]\b'
    LET = r'[lL][eE][tT]\b'
    LOOP = r'[lL][oO][oO][pP]\b'
    NEW = r'[nN][eE][wW]\b'
    NOT = r'[nN][oO][tT]\b'
    OF = r'[oO][fF]\b'
    POOL = r'[pP][oO][oO][lL]\b'
    THEN = r'[tT][hH][eE][nN]\b'
    WHILE = r'[wW][hH][iI][lL][eE]\b'
    ASSIGN = r'<-'
    DARROW = r'=>'
    LE = r'<='
    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                        for i in ['0','1']
                        for j in range(16)]
    CARACTERES_CONTROL += [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    @_(r'("(?:\\["]|[^"\\\n]|\\[\n\\a-zA-Z\d\x00\t\b\f\x0c\x1b\-])*")')
    def STR_CONST(self, t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        if '\\\x00' in t.value:
            t.type = 'ERROR'
            t.value = '"String contains escaped null character."'
            return t

        elif '\x00' in t.value:
            t.type = 'ERROR'
            t.value = '"String contains null character."'
            return t
        p = t.value
        num_bn = p.count('\\n')
        num_bb = p.count('\\\\')
        p = p.replace('\\\n','\n')
        p = p.replace('\\','') 
        if len(p)+num_bb-2>1024:
            t.type = 'ERROR'
            t.value = '"String constant too long"'
            return t
        t.value = t.value.replace('\\\n','\\n')
        t.value = t.value.replace('\\\t',r'\t')
        t.value = t.value.replace('\\\b',r'\b')
        t.value = t.value.replace('\\\f',r'\f')
        t.value = t.value.replace('\t',r'\t')
        t.value = t.value.replace('\f',r'\f')
        r = re.compile(r'(?<!\\)\\([^nftb"\\])')
        t.value = r.sub(r'\1', t.value)
        lista = []
        for w in t.value:
            if w in self.CARACTERES_CONTROL:
                lista.append('\\'+str(oct(int(w.encode("ascii").hex(),16))).replace('o','0')[-3:])
            else:
                lista.append(w)
        t.value=''.join(lista)
        return t    
    @_(r'"([^"\n\x00]*\\\x00[^"\n\x00]*)+"?')
    def ERROR6(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"String contains escaped null character."'
        return t
    @_(r'"([^"\n\x00]*\x00[^"\n\x00]*)+"?')
    def ERROR5(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"String contains null character."'
        return t
    @_(r'("(?:\\["]|[^"\\\n]|\\[\n\\a-zA-Z\d\x00])*)\n')
    def ERROR1(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"Unterminated string constant"'
        return t

    @_(r'\"([^\"]|\\\")*\Z')
    def ERROR4(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"EOF in string constant"'
        return t
    @_(r'\(\*')
    def COMENT(self,t):
        t = self.begin(comen)
        return t

    @_(r'--.*')
    def LINECOMMENT(self, t):
        self.lineno+=t.value.count('\n')
        pass

    @_(r'[!#$%^&_>\?`\[\]\\\|\x00]')
    def ERROR(self,t):
        t.type = "ERROR"
        if t.value == "\\":
            t.value = "\\\\"
        if t.value in self.CARACTERES_CONTROL:
            t.value = '\\'+str(oct(int(t.value.encode("ascii").hex(),16))).replace('o','0')[-3:]
        t.value = '"'+t.value+'"'
        return t

    @_(r'\*\)')
    def ERROR2(self,t):
        t.type = "ERROR"
        t.value = '"Unmatched *)"'
        return t

    @_(r'\d+')
    def INT_CONST(self, t):
        return t

    @_(r'(t[rR][uU][eE]\b|f[aA][lL][sS][eE]\b)')
    def BOOL_CONST(self, t):
        if t.value[0] == "t":
            t.value = True
        else:
            t.value = False
        return t
    
    @_(r'[A-Z][a-zA-Z0-9_]*')
    def TYPEID(self, t):
        t.value =str(t.value)
        return t

    @_(r'[a-z_][a-zA-Z0-9_]*')
    def OBJECTID(self,t):
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
    
    @_(r'\t| ')
    def spaces(self, t):
        pass

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
   


    def salida(self, texto):
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type == 'STR_CONST':
                result += f"{str(token.value)}"
            elif token.type == 'ERROR':
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\' '
            elif token.type == 'INT_CONST':
                result += f"{str(token.value)}"
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append(result)
        open_p = texto.count('(*') 
        closed_p = texto.count('*)')
        if open_p > closed_p:
            result = f'#{self.lineno} ERROR "EOF in comment"'
            list_strings.append(result)
        return list_strings
    def tests(self):
        for fich in TESTS:
            f = open(os.path.join(DIR,fich),'r')
            g = open(os.path.join(DIR,fich+ '.out'),'r')
            resultado = g.read()
            entrada =  f.read()
            texto = '\n'.join(self.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            f.close(), g.close()
            if texto.strip().split() != resultado.strip().split():
                print(f"Revisa el fichero {fich}")

lexer = CoolLexer()
                
if __name__ == '__main__':
    for fich in TESTS:
            lexer = CoolLexer()
            f = open(os.path.join(DIR,fich),'r',newline='')
            g = open(os.path.join(DIR,fich+ '.out'),'r',newline='')
            resultado = g.read()
            entrada =  f.read()
            texto = '\n'.join(lexer.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            f.close(), g.close()
            if texto.strip().split() != resultado.strip().split():
                print(f"Revisa el fichero {fich}")
    fich = "opencomment.cool"
    f = open(os.path.join(DIR,fich),'r',newline='')
    text = f.read()
    print('\n'.join(lexer.salida(text)))