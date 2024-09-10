import math
import cmath
from math import sin, cos, tan, asin, acos, atan
from Cargas import Circuito
from copy import copy, deepcopy
circuito = Circuito(220,60)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def abrir_adicionar_carga():
    # Cria uma nova janela para adicionar carga
    janela_adicionar_carga = tk.Toplevel(root)
    janela_adicionar_carga.title("Adicionar Carga")

    # Função para processar e salvar as informações
    def processar_adicionar_carga():
        unidade = unidade_var.get()
        potencia_nominal = potencia_entry.get()
        fator_potencia = fator_entry.get()
        tipo_fp = tipo_fp_var.get()

        try:
            potencia_nominal = float(potencia_nominal)
        except ValueError:
            messagebox.showwarning("Aviso", "O campo 'Potência Nominal' deve ser um número.")
            return
        try:
            angle = acos(float(fator_potencia))
        except ValueError:
            messagebox.showwarning("Aviso", "O campo 'Fator de Potência' deve ser um número entre 0 e 1.")
            return


        if(unidade=='kW'):
            circuito.adicionaCarga('P',float(potencia_nominal),float(fator_potencia),tipo_fp=='Atrasado')
        if(unidade=='kVAr'):
            circuito.adicionaCarga('Q',float(potencia_nominal),float(fator_potencia),tipo_fp=='Atrasado')
        if(unidade=='kVA'):
            circuito.adicionaCarga('S',float(potencia_nominal),float(fator_potencia),tipo_fp=='Atrasado')

        
        if not potencia_nominal or not fator_potencia:
            messagebox.showwarning("Aviso", "Os campos 'Potência Nominal' e 'Fator de Potência' não podem estar vazios.")
            return
        
        messagebox.showinfo("Informação", f"Carga Adicionada:\nUnidade: {unidade}\nPotência Nominal: {potencia_nominal}\nFator de Potência: {fator_potencia} ({tipo_fp})")
        janela_adicionar_carga.destroy()

    # Layout da nova janela
    tk.Label(janela_adicionar_carga, text="Unidade da Potência Nominal:").pack(pady=5)
    
    unidade_var = tk.StringVar()
    unidade_combobox = ttk.Combobox(janela_adicionar_carga, textvariable=unidade_var, values=["kW", "kVAr", "kVA"])
    unidade_combobox.pack(pady=5)
    unidade_combobox.set("kW")  # Valor padrão

    tk.Label(janela_adicionar_carga, text="Potência Nominal:").pack(pady=5)
    
    potencia_entry = tk.Entry(janela_adicionar_carga)
    potencia_entry.pack(pady=5)

    tk.Label(janela_adicionar_carga, text="Fator de Potência:").pack(pady=5)
    
    fator_entry = tk.Entry(janela_adicionar_carga)
    fator_entry.pack(pady=5)

    tk.Label(janela_adicionar_carga, text="Tipo de Fator de Potência:").pack(pady=5)
    
    tipo_fp_var = tk.StringVar()
    tipo_fp_combobox = ttk.Combobox(janela_adicionar_carga, textvariable=tipo_fp_var, values=["Atrasado", "Adiantado"])
    tipo_fp_combobox.pack(pady=5)
    tipo_fp_combobox.set("Atrasado")  # Valor padrão

    # Botão para processar e adicionar carga
    tk.Button(janela_adicionar_carga, text="Adicionar Carga", command=processar_adicionar_carga).pack(pady=10)

def abrir_corrigir_fp():
    # Cria uma nova janela para corrigir o fator de potência
    janela_corrigir_fp = tk.Toplevel(root)
    janela_corrigir_fp.title("Corrigir FP")

    # Função para salvar e abrir a janela de resultados
    def salvar_corrigir_fp():
        novo_fp = novo_fp_entry.get()
        preco_kwh = preco_kwh_entry.get()
        horas_consumo = horas_consumo_entry.get()
        
        if float(novo_fp)<=circuito.fp:
            messagebox.showwarning("Aviso", "Fator de Potência já é superior ao fator de potência informado")
            return
        
        if not novo_fp or not preco_kwh or not horas_consumo:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
            return
        try:
            preco_kwh = float(preco_kwh)
            horas_consumo = float(horas_consumo)
        except ValueError:
            messagebox.showwarning("Aviso", "Os campos 'Preço do KWh' e 'Quantidade de Horas de Consumo' devem ser números.")
            return
        try:
            angle = acos(float(novo_fp))
        except ValueError:
            messagebox.showwarning("Aviso", "O fator de potência deve ser um número entre 0 e 1")
            return
        
        # Mostrar a janela com a tabela
        mostrar_resultados(float(preco_kwh), int(horas_consumo), float(novo_fp))
        janela_corrigir_fp.destroy()

    # Layout da nova janela
    tk.Label(janela_corrigir_fp, text="Novo Fator de Potência:").pack(pady=5)
    
    novo_fp_entry = tk.Entry(janela_corrigir_fp)
    novo_fp_entry.pack(pady=5)

    tk.Label(janela_corrigir_fp, text="Preço do KWh:").pack(pady=5)
    
    preco_kwh_entry = tk.Entry(janela_corrigir_fp)
    preco_kwh_entry.pack(pady=5)

    tk.Label(janela_corrigir_fp, text="Quantidade de Horas de Consumo:").pack(pady=5)
    
    horas_consumo_entry = tk.Entry(janela_corrigir_fp)
    horas_consumo_entry.pack(pady=5)

    tk.Button(janela_corrigir_fp, text="OK", command=salvar_corrigir_fp).pack(pady=10)

    tk.Button(janela_corrigir_fp, text="Voltar", command=janela_corrigir_fp.destroy).pack(pady=10)

def mostrar_resultados(preco_kwh, horas_consumo,novo_fp):
    # Cria uma nova janela para mostrar os resultados
    print(circuito.fp)
    Qc = circuito.P*(tan(acos(circuito.fp))-tan(acos(novo_fp)))
    compensado = deepcopy(circuito)
    compensado.adicionaCarga('Q',Qc,0,False)
    C = (Qc*1e3/(2*math.pi*60*(220**2)))*1e6
    messagebox.showwarning("Capacitor", "O capacitor para calculado é de "+str(C)+" uF")

    janela_resultados = tk.Toplevel(root)
    janela_resultados.title("Resultados")

    # Layout da tabela
    tabela = ttk.Treeview(janela_resultados, columns=("col1", "Não compensado", "Compensado"), show="headings")
    tabela.pack(pady=10, padx=10)

    # Cabeçalhos das colunas
    tabela.heading("col1", text="")
    tabela.heading("Não compensado", text="Não Compensado")
    tabela.heading("Compensado", text="Compensado") 

    # Adiciona linhas na tabela com rótulos
    custoBase = circuito.P*preco_kwh*horas_consumo
    if(circuito.fp>=.9):
        custoEnergiaAntes = custoBase-int((circuito.fp-.85)*100)*0.001*custoBase
    if(circuito.fp < 0.9 and circuito.fp > 0.85):
        custoEnergiaAntes = custoBase-int((circuito.fp-.85)*100)*0.001*custoBase+int((.9-circuito.fp)*10)*0.001*custoBase
    if(circuito.fp < 0.85):
        custoEnergiaAntes = custoBase+int((.9-circuito.fp)*100)*0.001*custoBase

    if(novo_fp>=.9):
        custoEnergiaCompensado = custoBase-int((novo_fp-.85)*100)*0.001*custoBase
    if(novo_fp < 0.9 and novo_fp > 0.85):
       custoEnergiaCompensado = custoBase-int((novo_fp-.85)*100)*0.001*custoBase+int((.9-novo_fp)*10)*0.001*custoBase
    if(novo_fp < 0.85):
        custoEnergiaCompensado = custoBase+int((.9-novo_fp)*100)*0.001*custoBase

    tabela.insert("", "end", values=("Corrente", abs(circuito.I)*1000, abs(compensado.I)*1000))
    tabela.insert("", "end", values=("Custo do Consumo de Energia", custoEnergiaAntes, custoEnergiaCompensado))

    tk.Button(janela_resultados, text="Voltar", command=janela_resultados.destroy).pack(pady=10)

def exibir_cargas():
    #messagebox.showinfo("Exibir Cargas", "Opção 'Exibir Cargas' selecionada.")
     # Cria uma nova janela para mostrar os resultados
    janela_cargas = tk.Toplevel(root)
    janela_cargas.title("Cargas adicionadas ao circuito")

    # Layout da tabela
    tabela = ttk.Treeview(janela_cargas, columns=("Carga", "P", "Q","S","I"), show="headings")
    tabela.pack(pady=10, padx=10)

    # Cabeçalhos das colunas
    tabela.heading("Carga", text="Carga")
    tabela.heading("P", text="P(kW)")
    tabela.heading("Q", text="Q(kVAr)")
    tabela.heading("S", text="S(kVA)") 
    tabela.heading("I", text="I(A)") 
    for i, carga in enumerate(circuito.cargas):
        tabela.insert("", "end", values=("Carga "+str(i+1), carga.P, carga.Q, abs(carga.S), 1000*abs(carga.I)))
        
    tabela.insert("", "end", values=("Total", circuito.P, circuito.Q, abs(circuito.S), 1000*abs(circuito.I)))
    

    tk.Button(janela_cargas, text="Voltar", command=janela_cargas.destroy).pack(pady=10)

def triangulo_de_potencias():
    circuito.mostrarTriangulo()
    #messagebox.showinfo("Triângulo de Potências", "Opção 'Triângulo de Potências' selecionada.")

def desenvolvedores():
    messagebox.showinfo("Desenvolvedores", "Desenvolvido por:\n Arthur Rodrigues Campos\n Fabio Carvalho Everton\n Kelwyn Lourhan Monteiro Pinheiro\n Rhaylson Ribeiro Moreira")

# Criação da janela principal
root = tk.Tk()
root.title("Interface Principal")

# Configuração do layout
frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

# Botões da interface
btn_adicionar_carga = tk.Button(frame, text="Adicionar Carga", command=abrir_adicionar_carga, width=20)
btn_adicionar_carga.pack(pady=5)

btn_exibir_cargas = tk.Button(frame, text="Exibir Cargas", command=exibir_cargas, width=20)
btn_exibir_cargas.pack(pady=5)

btn_triangulo_potencias = tk.Button(frame, text="Triângulo de Potências", command=triangulo_de_potencias, width=20)
btn_triangulo_potencias.pack(pady=5)

btn_corrigir_fp = tk.Button(frame, text="Corrigir FP", command=abrir_corrigir_fp, width=20)
btn_corrigir_fp.pack(pady=5)

btn_desenvolvedores = tk.Button(frame, text="Desenvolvedores", command=desenvolvedores, width=20)
btn_desenvolvedores.pack(pady=5)

# Inicia o loop principal da interface
root.mainloop()



