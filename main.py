from Cargas import Circuito
circuito = Circuito(220,60)
print(circuito.cargas)
print("\n"*2)
circuito.adicionaCarga('P',3.5*0.7457,0.65,True)
circuito.adicionaCarga('P',2.2,1,True)
circuito.adicionaCarga('P',15*0.11,1,True)
circuito.adicionaCarga('Q',2.4,0.75,False)
print(circuito.cargas)
print(abs(circuito.I)*1000)
print(circuito.S)
#print("\n"*5)


