from Cargas import Circuito
circuito = Circuito(220,60)
print(circuito.cargas)
print("\n"*2)
circuito.adicionaCarga('P',15,0.85,True)
print(circuito.cargas)
print(abs(circuito.I)*1000)
print(circuito.S)
print("\n"*5)

circuito.adicionaCarga('S',3,0.9,False)
print(circuito.cargas)
print(abs(circuito.I)*1000)
print(circuito.S)


