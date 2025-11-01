import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculadoraFilas(tk.Tk):
    """
    Classe principal da aplicação de calculadora de Teoria das Filas com interface Tkinter.
    """
    
    def __init__(self):
        super().__init__()
        
        # --- Configuração da Janela Principal ---
        self.title("Calculadora de Teoria das Filas")
        self.geometry("600x650")
        
        # Define um estilo para os widgets
        style = ttk.Style(self)
        style.configure('TButton', padding=5, font=('Helvetica', 10))
        style.configure('TLabel', padding=2, font=('Helvetica', 10))
        style.configure('TEntry', padding=5, font=('Helvetica', 10))
        style.configure('TLabelFrame.Label', font=('Helvetica', 11, 'bold'))

        # --- Criação das Abas (Notebook) ---
        self.notebook = ttk.Notebook(self)
        
        # Cria as 3 abas, uma para cada modelo
        self.tab_mm1 = ttk.Frame(self.notebook, padding=10)
        self.tab_mmc = ttk.Frame(self.notebook, padding=10)
        self.tab_mm1k = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.tab_mm1, text='  M/M/1  ')
        self.notebook.add(self.tab_mmc, text='  M/M/c (M/M/s)  ')
        self.notebook.add(self.tab_mm1k, text='  M/M/1/K  ')
        
        self.notebook.pack(pady=10, padx=10, fill="x")
        
        # --- Popula cada aba com seus campos e botões ---
        self.criar_aba_mm1()
        self.criar_aba_mmc()
        self.criar_aba_mm1k()
        
        # --- Área de Resultados (Comum a todas as abas) ---
        resultado_frame = ttk.LabelFrame(self, text="Resultados", padding=10)
        resultado_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.resultado_texto = tk.Text(resultado_frame, height=15, width=60, font=("Courier New", 10), wrap=tk.WORD, state='disabled', bg="#f0f0f0")
        self.resultado_texto.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- Botões de Ação (Comuns) ---
        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.btn_limpar = ttk.Button(botoes_frame, text="Limpar", command=self.limpar_tudo)
        self.btn_limpar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_ajuda = ttk.Button(botoes_frame, text="Ajuda", command=self.mostrar_ajuda)
        self.btn_ajuda.pack(side="left", expand=True, fill="x", padx=5)

    # --- Funções para Criar as Abas ---

    def criar_aba_mm1(self):
        """Popula a aba M/M/1 com campos de entrada e botão."""
        frame = ttk.LabelFrame(self.tab_mm1, text="Parâmetros M/M/1")
        frame.pack(fill="x", padx=5, pady=5)
        
        # Labels e Entradas
        ttk.Label(frame, text="Taxa de Chegada (λ):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.mm1_lambda = ttk.Entry(frame, width=15)
        self.mm1_lambda.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Taxa de Atendimento (μ):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mm1_mu = ttk.Entry(frame, width=15)
        self.mm1_mu.grid(row=1, column=1, padx=10, pady=5)
        
        # Botão de Cálculo
        btn_calc = ttk.Button(self.tab_mm1, text="Calcular M/M/1", command=self.calcular_mm1)
        btn_calc.pack(pady=10)

    def criar_aba_mmc(self):
        """Popula a aba M/M/c com campos de entrada e botão."""
        frame = ttk.LabelFrame(self.tab_mmc, text="Parâmetros M/M/c (M/M/s)")
        frame.pack(fill="x", padx=5, pady=5)

        # Labels e Entradas
        ttk.Label(frame, text="Taxa de Chegada (λ):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.mmc_lambda = ttk.Entry(frame, width=15)
        self.mmc_lambda.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Taxa de Atendimento (μ):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mmc_mu = ttk.Entry(frame, width=15)
        self.mmc_mu.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Nº de Servidores (s ou c):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.mmc_c = ttk.Entry(frame, width=15)
        self.mmc_c.grid(row=2, column=1, padx=10, pady=5)

        # Botão de Cálculo
        btn_calc = ttk.Button(self.tab_mmc, text="Calcular M/M/c", command=self.calcular_mmc)
        btn_calc.pack(pady=10)

    def criar_aba_mm1k(self):
        """Popula a aba M/M/1/K com campos de entrada e botão."""
        frame = ttk.LabelFrame(self.tab_mm1k, text="Parâmetros M/M/1/K")
        frame.pack(fill="x", padx=5, pady=5)

        # Labels e Entradas
        ttk.Label(frame, text="Taxa de Chegada (λ):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.mm1k_lambda = ttk.Entry(frame, width=15)
        self.mm1k_lambda.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Taxa de Atendimento (μ):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mm1k_mu = ttk.Entry(frame, width=15)
        self.mm1k_mu.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Capacidade (K):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.mm1k_k = ttk.Entry(frame, width=15)
        self.mm1k_k.grid(row=2, column=1, padx=10, pady=5)

        # Botão de Cálculo
        btn_calc = ttk.Button(self.tab_mm1k, text="Calcular M/M/1/K", command=self.calcular_mm1k)
        btn_calc.pack(pady=10)

    # --- Funções de Callback dos Botões ---

    def exibir_resultado(self, texto):
        """Atualiza a caixa de texto com os resultados formatados."""
        self.resultado_texto.config(state='normal')
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, texto)
        self.resultado_texto.config(state='disabled')

    def limpar_tudo(self):
        """Limpa todos os campos de entrada e a área de resultados."""
        # Limpa entradas M/M/1
        self.mm1_lambda.delete(0, tk.END)
        self.mm1_mu.delete(0, tk.END)
        
        # Limpa entradas M/M/c
        self.mmc_lambda.delete(0, tk.END)
        self.mmc_mu.delete(0, tk.END)
        self.mmc_c.delete(0, tk.END)
        
        # Limpa entradas M/M/1/K
        self.mm1k_lambda.delete(0, tk.END)
        self.mm1k_mu.delete(0, tk.END)
        self.mm1k_k.delete(0, tk.END)
        
        # Limpa resultado
        self.exibir_resultado("")

    def mostrar_ajuda(self):
        """Exibe uma janela de pop-up com informações de ajuda."""
        titulo = "Ajuda - Conceitos de Teoria das Filas"
        mensagem = (
            "--- Parâmetros de Entrada ---\n\n"
            "λ (Lambda): Taxa de Chegada\n"
            "É a frequência com que os clientes chegam ao sistema (ex: 10 clientes/hora).\n\n"
            "μ (Mi): Taxa de Atendimento (por servidor)\n"
            "É a capacidade com que um único servidor processa os clientes (ex: 12 clientes/hora).\n\n"
            "s (ou c): Número de Servidores\n"
            "A quantidade de canais de atendimento paralelos disponíveis (para o modelo M/M/c).\n\n"
            "K: Capacidade do Sistema\n"
            "O número total de clientes permitidos no sistema (fila + atendimento) (para o modelo M/M/1/K).\n\n"
            "--- Modelos ---\n\n"
            "M/M/1: 1 servidor, fila infinita.\n"
            "M/M/c: 'c' servidores, fila infinita.\n"
            "M/M/1/K: 1 servidor, fila finita (capacidade K).\n\n"
            "--- Métricas de Saída ---\n\n"
            "ρ (Rho): Utilização do sistema.\n"
            "P₀: Probabilidade de o sistema estar vazio.\n"
            "L: Número médio de clientes no sistema (na fila + em atendimento).\n"
            "Lq: Número médio de clientes na fila (apenas esperando).\n"
            "W: Tempo médio que um cliente passa no sistema (espera + atendimento).\n"
            "Wq: Tempo médio que um cliente passa na fila (apenas esperando)."
        )
        messagebox.showinfo(titulo, mensagem)

    # --- Funções de Cálculo (Handlers) ---

    def calcular_mm1(self):
        """Pega os dados da aba M/M/1, chama a lógica e exibe os resultados."""
        try:
            lambda_ = float(self.mm1_lambda.get())
            mu_ = float(self.mm1_mu.get())
            
            if lambda_ <= 0 or mu_ <= 0:
                self.exibir_resultado("Erro: λ e μ devem ser maiores que zero.")
                return

            if lambda_ >= mu_:
                self.exibir_resultado(f"--- SISTEMA INSTÁVEL ---\n\n"
                                      f"Taxa de chegada (λ = {lambda_}) é maior ou igual à taxa de atendimento (μ = {mu_}).\n"
                                      "A fila crescerá infinitamente.")
                return

            # Chama a função de lógica pura
            resultados = self.logica_mm1(lambda_, mu_)
            
            # Formata a saída
            texto = "--- Resultados M/M/1 ---\n\n"
            texto += f"ρ (Utilização): {resultados['rho']:.4f}\n"
            texto += f"   ↳ O servidor está ocupado {resultados['rho']*100:.2f}% do tempo.\n\n"
            texto += f"P₀ (Sistema Vazio): {resultados['P0']:.4f}\n"
            texto += f"   ↳ A probabilidade de não haver ninguém no sistema é de {resultados['P0']*100:.2f}%\n\n"
            texto += f"L (Clientes no Sistema): {resultados['L']:.4f}\n"
            texto += f"   ↳ Em média, há {resultados['L']:.4f} clientes no sistema (na fila + sendo atendidos).\n\n"
            texto += f"Lq (Clientes na Fila): {resultados['Lq']:.4f}\n"
            texto += f"   ↳ Em média, há {resultados['Lq']:.4f} clientes esperando na fila.\n\n"
            texto += f"W (Tempo no Sistema): {resultados['W']:.4f}\n"
            texto += f"   ↳ Um cliente passa, em média, {resultados['W']:.4f} unidades de tempo no total.\n\n"
            texto += f"Wq (Tempo na Fila): {resultados['Wq']:.4f}\n"
            texto += f"   ↳ Um cliente espera, em média, {resultados['Wq']:.4f} unidades de tempo na fila."
            
            self.exibir_resultado(texto)

        except ValueError:
            self.exibir_resultado("Erro: Verifique se os valores de λ e μ são números válidos.")
        except Exception as e:
            self.exibir_resultado(f"Erro inesperado: {e}")

    def calcular_mmc(self):
        """Pega os dados da aba M/M/c, chama a lógica e exibe os resultados."""
        try:
            lambda_ = float(self.mmc_lambda.get())
            mu_ = float(self.mmc_mu.get())
            c_ = int(self.mmc_c.get())
            
            if lambda_ <= 0 or mu_ <= 0 or c_ <= 0:
                self.exibir_resultado("Erro: λ, μ e c devem ser maiores que zero (e 'c' deve ser inteiro).")
                return

            if lambda_ >= (c_ * mu_):
                self.exibir_resultado(f"--- SISTEMA INSTÁVEL ---\n\n"
                                      f"Taxa de chegada (λ = {lambda_}) é maior ou igual à capacidade total de atendimento (c*μ = {c_*mu_}).\n"
                                      "A fila crescerá infinitamente.")
                return

            # Chama a função de lógica pura
            resultados = self.logica_mmc(lambda_, mu_, c_)
            
            # Formata a saída
            texto = "--- Resultados M/M/c ---\n\n"
            texto += f"ρ (Utilização por Servidor): {resultados['rho']:.4f}\n"
            texto += f"   ↳ Cada servidor está ocupado, em média, {resultados['rho']*100:.2f}% do tempo.\n\n"
            texto += f"P₀ (Sistema Vazio): {resultados['P0']:.4f}\n"
            texto += f"   ↳ A probabilidade de todos os {c_} servidores estarem livres é de {resultados['P0']*100:.2f}%\n\n"
            texto += f"P_wait (Prob. de Esperar): {resultados['Pw']:.4f}\n"
            texto += f"   ↳ A probabilidade de um cliente chegar e todos os servidores estarem ocupados (ter que esperar) é de {resultados['Pw']*100:.2f}%\n\n"
            texto += f"L (Clientes no Sistema): {resultados['L']:.4f}\n"
            texto += f"   ↳ Em média, há {resultados['L']:.4f} clientes no sistema.\n\n"
            texto += f"Lq (Clientes na Fila): {resultados['Lq']:.4f}\n"
            texto += f"   ↳ Em média, há {resultados['Lq']:.4f} clientes esperando na fila.\n\n"
            texto += f"W (Tempo no Sistema): {resultados['W']:.4f}\n"
            texto += f"   ↳ Um cliente passa, em média, {resultados['W']:.4f} unidades de tempo no total.\n\n"
            texto += f"Wq (Tempo na Fila): {resultados['Wq']:.4f}\n"
            texto += f"   ↳ Um cliente espera, em média, {resultados['Wq']:.4f} unidades de tempo na fila."
            
            self.exibir_resultado(texto)

        except ValueError:
            self.exibir_resultado("Erro: Verifique se λ e μ são números e 'c' é um inteiro.")
        except Exception as e:
            self.exibir_resultado(f"Erro inesperado: {e}")

    def calcular_mm1k(self):
        """Pega os dados da aba M/M/1/K, chama a lógica e exibe os resultados."""
        try:
            lambda_ = float(self.mm1k_lambda.get())
            mu_ = float(self.mm1k_mu.get())
            k_ = int(self.mm1k_k.get())
            
            if lambda_ <= 0 or mu_ <= 0 or k_ <= 0:
                self.exibir_resultado("Erro: λ, μ e K devem ser maiores que zero (e 'K' deve ser inteiro).")
                return

            # Este modelo é sempre estável, não precisa de verificação de rho.

            # Chama a função de lógica pura
            resultados = self.logica_mm1k(lambda_, mu_, k_)
            
            # Formata a saída
            texto = "--- Resultados M/M/1/K ---\n\n"
            texto += f"ρ (Taxa de Tráfego): {resultados['rho']:.4f}\n"
            texto += f"   ↳ Relação entre chegada e atendimento (pode ser > 1).\n\n"
            texto += f"P₀ (Sistema Vazio): {resultados['P0']:.4f}\n"
            texto += f"   ↳ A probabilidade de o sistema estar vazio é de {resultados['P0']*100:.2f}%\n\n"
            texto += f"Pk (Sistema Cheio/Perda): {resultados['Pk']:.4f}\n"
            texto += f"   ↳ A probabilidade de o sistema estar cheio (K={k_}) é de {resultados['Pk']*100:.2f}%. Novas chegadas serão perdidas.\n\n"
            texto += f"λ_eff (Taxa de Chegada Efetiva): {resultados['lambda_eff']:.4f}\n"
            texto += f"   ↳ Taxa de chegada real de clientes que entram no sistema (não são perdidos).\n\n"
            texto += f"L (Clientes no Sistema): {resultados['L']:.4f}\n"
            texto += f"   ↳ Em média, há {resultados['L']:.4f} clientes no sistema.\n\n"
            texto += f"Lq (Clientes na Fila): {resultados['Lq']:.4f}\n"
            texto += f"   ↳ Em média, há {resultados['Lq']:.4f} clientes esperando na fila.\n\n"
            texto += f"W (Tempo no Sistema): {resultados['W']:.4f}\n"
            texto += f"   ↳ Um cliente que entra no sistema passa, em média, {resultados['W']:.4f} unidades de tempo no total.\n\n"
            texto += f"Wq (Tempo na Fila): {resultados['Wq']:.4f}\n"
            texto += f"   ↳ Um cliente que entra no sistema espera, em média, {resultados['Wq']:.4f} unidades de tempo na fila."
            
            self.exibir_resultado(texto)

        except ValueError:
            self.exibir_resultado("Erro: Verifique se λ e μ são números e 'K' é um inteiro.")
        except Exception as e:
            self.exibir_resultado(f"Erro inesperado: {e}")

    # --- Funções de LÓGICA PURA (Cálculos Matemáticos) ---

    def logica_mm1(self, lambda_, mu_):
        """Calcula as métricas M/M/1. Assume lambda_ < mu_."""
        
        rho = lambda_ / mu_
        L = lambda_ / (mu_ - lambda_)
        Lq = (lambda_**2) / (mu_ * (mu_ - lambda_))
        W = 1 / (mu_ - lambda_)
        Wq = lambda_ / (mu_ * (mu_ - lambda_))
        P0 = 1 - rho
        
        return {"rho": rho, "L": L, "Lq": Lq, "W": W, "Wq": Wq, "P0": P0}

    def logica_mmc(self, lambda_, mu_, c_):
        """Calcula as métricas M/M/c. Assume lambda_ < c_ * mu_."""
        
        rho = lambda_ / (c_ * mu_)
        r = lambda_ / mu_  # Intensidade de tráfego (Erlangs)
        
        # Cálculo de P0 (Probabilidade do sistema vazio)
        sum_term = 0
        for n in range(c_):
            sum_term += (r**n) / math.factorial(n)
        
        term_c = (r**c_) / (math.factorial(c_) * (1 - rho))
        P0 = 1 / (sum_term + term_c)
        
        # Probabilidade de espera (Fórmula C de Erlang)
        Pw = term_c * P0
        
        # Métricas de desempenho
        Lq = Pw * (rho / (1 - rho))
        Wq = Lq / lambda_
        W = Wq + (1 / mu_)
        L = lambda_ * W
        
        return {"rho": rho, "P0": P0, "Pw": Pw, "L": L, "Lq": Lq, "W": W, "Wq": Wq}

    def logica_mm1k(self, lambda_, mu_, k_):
        """Calcula as métricas M/M/1/K."""
        
        rho = lambda_ / mu_
        
        # Cálculo de P0
        if rho == 1:
            P0 = 1 / (k_ + 1)
        else:
            P0 = (1 - rho) / (1 - rho**(k_ + 1))
            
        # Probabilidade de perda (sistema cheio)
        Pk = P0 * (rho**k_)
        
        # Taxa de chegada efetiva
        lambda_eff = lambda_ * (1 - Pk)
        
        # Cálculo de L
        if rho == 1:
            L = k_ / 2
        else:
            L = rho * (1 - (k_ + 1) * rho**k_ + k_ * rho**(k_ + 1)) / ((1 - rho) * (1 - rho**(k_ + 1)))
            
        # Métricas de desempenho (baseadas na taxa efetiva)
        W = L / lambda_eff
        
        # L = Lq + Ls_avg (Ls_avg = número médio em serviço)
        # Ls_avg = 1 - P0 (pois só há serviço se o sistema não está vazio)
        Lq = L - (1 - P0)
        
        Wq = Lq / lambda_eff
        
        return {"rho": rho, "P0": P0, "Pk": Pk, "lambda_eff": lambda_eff, "L": L, "Lq": Lq, "W": W, "Wq": Wq}


if __name__ == "__main__":
    app = CalculadoraFilas()
    app.mainloop()