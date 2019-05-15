# coding: utf-8
from dataclasses import dataclass, field
from typing import List
from copy import deepcopy
class Arbol():
    self.raiz = None
    self.tamano = 0
    def __init__ (self, raiz):
         self.raiz=raiz
         self.tamano += 1
    def buscaNodo(self,valor):
        return buscaAux(valor,self.raiz)
    def buscaAux(self,valor,raiz):
        if self.tamano == 0:
            return None
        if self.tamano == 1:
            if self.raiz.valor==valor:
                return raiz
            else:
                return None
        if len(raiz.hijos)==0:
            return None
        for nodo in raiz.hijos:
            if nodo.dato == valor:
                return nodo
            resultado = buscaAux(self,valor,nodo)
        return resultado
    def mca(a,b):
        nodoA = self.buscaNodo(a)
        nodoB = self.buscaNodo(b)
        if a==b:
            return a
        elif nodoA.nivel > nodoB.nivel
            return mca(nodoA.padre.valor,b)
        else:
            return mca(a,nodoB.padre.valor)

    def anhade(self,padre,valor):
        if self.raiz == None:
            self.raiz= Hoja(valor,None)
            self.tamano = self.tamano + 1
        else:
            self.buscaNodo(padre).anhadeHijo(hoja(valor,padre))
            self.tamano = self.tamano + 1
class Hoja:
    self.valor = None 
    self.padre = None 
    self.hijos = None 
    self.nivel = None
    def __init__ (self, padre, valor):
        self.valor = valor
        self.padre = padre
        self.hijos = list()
        if self.padre == None:
            self.nivel=0
        else:
            self.nivel = self.padre.nivel
    def anhadeHijo(self,nodo):
        self.hijos.append(nodo)

@dataclass
class Nodo:
    linea: int

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'


@dataclass
class Formal(Nodo):
    nombre_variable: str
    tipo: str
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado


class Expresion(Nodo):
    cast: str


@dataclass
class Asignacion(Expresion):
    nombre: str
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        if self.cuerpo.calculaTipo(ambito, arbol_clases, diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        cast_nombre = ambito[self.nombre]
        if arbol_clases.subtipo(self.cuerpo.cast, cast_nombre):
            self.cast = 'Object'
        else:
            self.cast = 'Object'
            return "ERROR_TIPO"

@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion
    clase: str
    nombre_metodo: str
    argumentos: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        if self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        for a in self.argumentos:
            a.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        
        


@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion
    nombre_metodo: str
    argumentos: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        for e in self.argumentos:
            e.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos)

@dataclass
class Condicional(Expresion):
    condicion: Expresion
    verdadero: Expresion
    falso: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n+2)
        resultado += self.verdadero.str(n+2)
        resultado += self.falso.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.condicion.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.verdadero.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.falso.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        self.cast=arbol_clases.mca(verdadero.cast,falso.cast)

@dataclass
class Bucle(Expresion):
    condicion: Expresion
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.condicion.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        self.cast=self.cuerpo.cast

@dataclass
class Let(Expresion):
    nombre: str
    tipo: str
    inicializacion: Expresion
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_let\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.inicializacion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        nuevo_ambito = deepcopy(ambito)
        nuevo_ambito[self.nombre] = self.tipo
        if self.cuerpo.calculaTipo(nuevo_ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        self.cast = self.cuerpo.cast


@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += ''.join([e.str(n+2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += '\n'
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        aux = self.expresiones[0].cast
        for e in self.expresiones[1:]:
            if e.calculaTipo(ambito, arbol_clases, diccionario_metodos) == "ERROR_TIPO":
                return "ERROR_TIPO"
            aux = arbol_clases.mca(e.cast,aux)
        self.cast=aux



@dataclass
class RamaCase(Expresion):
    nombre_variable: str
    tipo: str
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if arbol_clases(self.cuerpo.cast,tipo)!=None:
            self.cast = self.tipo
        else:
            return "ERROR_TIPO"


@dataclass
class Swicht(Expresion):
    expr: Expresion
    casos: List[RamaCase]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n+2)
        resultado += ''.join([c.str(n+2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.expr.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        tipoRC = casos[0].cast
        for rc in casos[1:]:
            tipoRC = arbol_clases.mca(rc.cast,tipoRC)
        self.cast = tipoRC
        
@dataclass
class Nueva(Expresion):
    tipo: str
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self):
        self.cast = self.tipo
        
@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion
    derecha: Expresion
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if arbol_clases.subTipo(izquierda.cast,"Int") and arbol_clases.subTipo(derecha.cast,"Int"):
            self.cast = arbol_clases.mca(izquierda.cast,derecha.cast)
        else:
            return "ERROR_TIPO"
@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

        
@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado



@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


@dataclass
class Menor(OperacionBinaria):
    operando: str = '<'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_lt\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if arbol_clases.subTipo(izquierda.cast,"Int") and arbol_clases.subTipo(derecha.cast,"Int"):
            self.cast = "Bool"
        else:
            return "ERROR_TIPO"

@dataclass
class LeIgual(OperacionBinaria):
    operando: str = '<='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if arbol_clases.subTipo(izquierda.cast,"Int") and arbol_clases.subTipo(derecha.cast,"Int"):
            self.cast = "Bool"
        else:
            return "ERROR_TIPO"


@dataclass
class Igual(OperacionBinaria):
    operando: str = '='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        if self.izquierda.calculaTipo(self,ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if self.derecha.calculaTipo(self,ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        if arbol_clases.mca(izquierda.cast,derecha.cast) != None:
            self.cast = "Bool"
        else:
            self.cast = "ERROR_TIPO"


@dataclass
class Neg(Expresion):
    expr: Expresion
    operador: str = '~'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.expr.calculaTipo(self,ambito,arbol_clases,diccionario_metodos)
        self.cast = self.expr.cast


@dataclass
class Not(Expresion):
    expr: Expresion
    operador: str = 'NOT'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "Bool"


@dataclass
class EsNulo(Expresion):
    expr: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        self.cast = "Object"




@dataclass
class Objeto(Expresion):
    nombre: str

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = ambito[self.nombre]
        



@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        self.cast = "Object"


@dataclass
class Entero(Expresion):
    valor: int

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "Int"

@dataclass
class String(Expresion):
    valor: str

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "String"


@dataclass
class Booleano(Expresion):
    valor: bool

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "Bool"
@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado
    
    def calculaTipo(self, ambito = dict(), arbol_clases = Arbol(), diccionario_metodos = dict()):
        error = []
        for s in self.secuencia:
            self.arbol_clases.anhade(self,s.padre,s.nombre)
        for s in self.secuencia:
            error+=s.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        
        return error
        


@dataclass
class Caracteristica(Expresion):
    nombre: str
    tipo: str
    cuerpo: Expresion

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        if self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos) == "ERROR_TIPO":
            return "ERROR_TIPO"
        self.cast = self.tipo
            
        
        


@dataclass
class Clase(Nodo):
    nombre: str
    padre: str
    nombre_fichero: str
    caracteristicas: List[Caracteristica] = field(default_factory=list)


    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.caracteristicas])
        resultado += '\n'
        resultado += f'{(n+2)*" "})\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        nuevo_ambito = deepcopy(ambito)
        for c in self.caracteristicas:
            c.calculaTipo(ambito, arbol_clases, diccionario_metodos)
            if type(c) == Metodo:
                diccionario_metodos[(self.nombre,c.nombre)]=(c.argumentos,c.tipo)
            else:
                nuevo_ambito[c.nombre] = c.tipo
        for c in self.caracteristicas:
            c.calculaTipo(nuevo_ambito,arbol_clases,diccionario_metodos)


@dataclass
class Metodo(Caracteristica):
    formales: List[Formal]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
        


class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
