from math import sin, cos, tan, asin, acos, atan
class Carga():
    def __init__(self):
        #Fator de Potência
        self.fp = 0
        #fp atrasado ou adiantado?
        self.fpAdiantado = True
        #Potência Aparente Nominal
        self.S = 0
        #Potência Ativa(Real) Nominal
        self.P = 0
        #Potência Reativa Nominal
        self.Q = 0
        #Corrente na Carga
        self.I = 0
        #Potência Complexa
        self.Scplx = 0

class CargaP(Carga):
    def __init__(self,V,P,fp,fpAdiantado):
        self.fp = fp
        self.P = P
        self.S = self.P/fp
        if(fpAdiantado):
            self.Q = (self.S)*sin(acos(self.fp))
        else:
            self.Q = -(self.S)*sin(acos(self.fp))
        
        self.Scplx = complex(self.P,self.Q)
        self.I = V/self.Scplx

class CargaQ(Carga):
    def __init__(self,V,Q,fp,fpAdiantado):
        self.fp = fp
        if(fpAdiantado):
            self.Q = abs(Q)
        else:
            self.Q = -abs(Q)
        self.S = abs(self.Q)/sin(acos(fp))
        self.P = self.S * fp
        self.Scplx = complex(self.P,self.Q)
        self.I = V/self.Scplx

class CargaS(Carga):
    def __init__(self,V,S,fp,fpAdiantado):
        self.fp = fp
        self.S = S
        if(fpAdiantado):
            self.Q = S*sin(acos(fp))
        else:
            self.Q = -S*sin(acos(fp))
        self.P = S*fp
        self.Scplx = complex(self.P,self.Q)


class Circuito():
    def __init__(self,Vin,f):
        #Tensão de Alimentação
        self.Vin = Vin
        #Frequência da tensão de alimentação
        self.f = f
        #Cargas no circuito
        self.cargas = []
        self.P = 0
        self.Q = 0
        self.S = 0
        self.fp = 0
        self.Scplx = 0

    def adicionaCarga(self,tipoCarga,Pot,fp,fpAtrasado):
        if(tipoCarga=='P'):
            self.cargas.append(CargaP(self.Vin,Pot,fp,fpAtrasado))
            self.atualizarCircuito()
        if(tipoCarga=='Q'):
            self.cargas.append(CargaQ(self.Vin,Pot,fp,fpAtrasado))
            self.atualizarCircuito()
        if(tipoCarga=='S'):
            self.cargas.append(CargaS(self.Vin,Pot,fp,fpAtrasado))
            self.atualizarCircuito()
    
    def atualizarCircuito(self):
        sumP = 0
        sumQ = 0
        for i in self.cargas:
            sumP += i.P
            sumQ += i.Q
        self.P = sumP
        self.Q = sumQ
        self.S = complex(self.P,self.Q)
        self.I = self.S/self.Vin

