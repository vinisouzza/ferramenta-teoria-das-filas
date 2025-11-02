import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
from datetime import datetime
import re # Importa regex para facilitar a extração dos parâmetros

class CalculadoraFilas(tk.Tk):
    """
    Classe principal da aplicação de calculadora de Teoria das Filas com interface Tkinter.
    """
    
    def __init__(self):
        super().__init__()
        
        # Variáveis para armazenar o último resultado e o modelo para salvar
        self.ultimo_resultado_texto = ""
        self.ultimo_modelo = ""

        # --- Configuração da Janela Principal ---
        self.title("Calculadora de Teoria das Filas")
        self.geometry("700x650") # Aumentei um pouco a largura para acomodar mais botões
        
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
        
        # Liga o evento de mudança de aba à função de controle
        self.notebook.bind("<<NotebookTabChanged>>", self.controle_estado_salvar)
        
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
        
        # Botão Carregar
        self.btn_carregar = ttk.Button(botoes_frame, text="Carregar Resultado", command=self.carregar_resultado_do_arquivo)
        self.btn_carregar.pack(side="left", expand=True, fill="x", padx=5)
        
        self.btn_limpar = ttk.Button(botoes_frame, text="Limpar", command=self.limpar_tudo)
        self.btn_limpar.pack(side="left", expand=True, fill="x", padx=5)
        
        # Botão Salvar
        self.btn_salvar = ttk.Button(botoes_frame, text="Salvar Resultado", command=self.salvar_resultado_em_arquivo, state='disabled')
        self.btn_salvar.pack(side="left", expand=True, fill="x", padx=5)
        
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

    # --- Funções de Controle de Estado ---

    def controle_estado_salvar(self, event=None):
        """
        Desabilita o botão 'Salvar Resultado' sempre que a aba é trocada.
        O botão só será reativado se for realizado um novo cálculo bem-sucedido.
        """
        self.btn_salvar.config(state='disabled')
        # Limpa o texto da área de resultado ao trocar de aba e reseta o estado
        self.exibir_resultado("")
        self.ultimo_resultado_texto = ""
        self.ultimo_modelo = ""

    def exibir_resultado(self, texto):
        """Atualiza a caixa de texto com os resultados formatados e armazena o texto."""
        self.resultado_texto.config(state='normal')
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, texto)
        self.resultado_texto.config(state='disabled')
        
        # Armazena o texto completo para a função de salvar
        self.ultimo_resultado_texto = texto
        
        # Habilita o botão Salvar se o texto não for um erro/vazio
        if texto and "Erro:" not in texto and "SISTEMA INSTÁVEL" not in texto:
            self.btn_salvar.config(state='normal')
        else:
            self.btn_salvar.config(state='disabled')

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
        
        # Limpa resultado e variáveis de estado
        self.exibir_resultado("")
        self.ultimo_resultado_texto = ""
        self.ultimo_modelo = ""
        self.btn_salvar.config(state='disabled')


    def salvar_resultado_em_arquivo(self):
        """Abre uma caixa de diálogo para salvar o último resultado em um arquivo .txt."""
        
        if not self.ultimo_resultado_texto:
            messagebox.showwarning("Atenção", "Nenhum resultado válido para salvar.")
            return

        # PADRÃO DE NOME DE ARQUIVO: HH-mm-ss-DD-MM-YYYY-MODELO.txt
        timestamp = datetime.now().strftime("%H-%M-%S-%d-%m-%Y")
        modelo_safe = self.ultimo_modelo.replace('/', '_')
        sugestao_nome = f"{timestamp}-{modelo_safe}.txt" 

        # Abre a caixa de diálogo para salvar
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
            initialfile=sugestao_nome,
            title="Salvar Resultados de Teoria das Filas"
        )
        
        if not filepath:
            return # Usuário cancelou

        try:
            # Prepara o conteúdo completo
            conteudo_completo = (
                f"================================================\n"
                f"  RESULTADO DA CALCULADORA DE TEORIA DAS FILAS  \n"
                f"================================================\n"
                f"MODELO: {self.ultimo_modelo}\n"
                f"DATA E HORA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"------------------------------------------------\n"
                f"PARÂMETROS UTILIZADOS:\n"
                f"{self.obter_parametros_atuais()}\n"
                f"------------------------------------------------\n"
                f"MÉTRICAS DE SAÍDA:\n"
                f"{self.ultimo_resultado_texto.replace('--- Resultados', '')}\n" # Remove o cabeçalho duplicado
                f"================================================\n"
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(conteudo_completo)
            
            messagebox.showinfo("Sucesso", f"Resultados salvos com sucesso em:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo: {e}")

    
    def carregar_resultado_do_arquivo(self):
        """Abre uma caixa de diálogo para carregar um arquivo de resultado e setar os parâmetros."""
        
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Resultado de Filas", "*.txt"), ("Todos os Arquivos", "*.*")],
            title="Carregar Resultados de Teoria das Filas"
        )
        
        if not filepath:
            return # Usuário cancelou

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            # 1. Encontrar o Modelo
            modelo_match = re.search(r'MODELO: (M/M/1/K|M/M/c|M/M/1)', conteudo)
            if not modelo_match:
                messagebox.showerror("Erro de Leitura", "Não foi possível identificar o modelo de filas no arquivo.")
                return
            modelo = modelo_match.group(1)

            # 2. Encontrar os Parâmetros (Busca os parâmetros logo após o cabeçalho)
            param_section_match = re.search(r'PARÂMETROS UTILIZADOS:\n(.*?)\n-{3,}', conteudo, re.DOTALL)
            if not param_section_match:
                 messagebox.showerror("Erro de Leitura", "Não foi possível encontrar a seção de parâmetros no arquivo.")
                 return
            param_section = param_section_match.group(1).strip() # O conteúdo entre o cabeçalho e os traços

            # Expressões para extrair valores, tolerante a ponto decimal
            lambda_match = re.search(r'λ \(Chegada\): ([\d\.]+)', param_section)
            mu_match = re.search(r'μ \(Atendimento\): ([\d\.]+)', param_section)

            lambda_ = lambda_match.group(1) if lambda_match else None
            mu_ = mu_match.group(1) if mu_match else None
            
            if lambda_ is None or mu_ is None:
                 messagebox.showerror("Erro de Leitura", "Parâmetros básicos (λ ou μ) não encontrados ou formatados incorretamente.")
                 return

            # Limpa todos os campos antes de carregar
            self.limpar_tudo()

            if modelo == 'M/M/1':
                # Seta os campos e muda para a aba M/M/1
                self.mm1_lambda.insert(0, lambda_)
                self.mm1_mu.insert(0, mu_)
                self.notebook.select(self.tab_mm1)
                messagebox.showinfo("Sucesso", f"Parâmetros do modelo {modelo} carregados com sucesso.")

            elif modelo == 'M/M/c':
                c_match = re.search(r'c \(Servidores\): ([\d]+)', param_section)
                c_ = c_match.group(1) if c_match else None
                
                if c_ is None:
                    messagebox.showerror("Erro de Leitura", "Parâmetro 'c' não encontrado para o modelo M/M/c.")
                    return
                
                # Seta os campos e muda para a aba M/M/c
                self.mmc_lambda.insert(0, lambda_)
                self.mmc_mu.insert(0, mu_)
                self.mmc_c.insert(0, c_)
                self.notebook.select(self.tab_mmc)
                messagebox.showinfo("Sucesso", f"Parâmetros do modelo {modelo} carregados com sucesso.")

            elif modelo == 'M/M/1/K':
                k_match = re.search(r'K \(Capacidade\): ([\d]+)', param_section)
                k_ = k_match.group(1) if k_match else None
                
                if k_ is None:
                    messagebox.showerror("Erro de Leitura", "Parâmetro 'K' não encontrado para o modelo M/M/1/K.")
                    return

                # Seta os campos e muda para a aba M/M/1/K
                self.mm1k_lambda.insert(0, lambda_)
                self.mm1k_mu.insert(0, mu_)
                self.mm1k_k.insert(0, k_)
                self.notebook.select(self.tab_mm1k)
                messagebox.showinfo("Sucesso", f"Parâmetros do modelo {modelo} carregados com sucesso.")

            # Garante que a área de resultados e o botão de salvar sejam resetados
            self.exibir_resultado("")
            self.btn_salvar.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível ler o arquivo ou extrair os dados.\nDetalhe: {e}")
            # Se der erro, garante que os campos estejam limpos
            self.limpar_tudo()

    def obter_parametros_atuais(self):
        """Retorna uma string com os parâmetros da aba que gerou o último cálculo."""
        
        if self.ultimo_modelo == 'M/M/1':
            return (f"λ (Chegada): {self.mm1_lambda.get()}\n"
                    f"μ (Atendimento): {self.mm1_mu.get()}")
        elif self.ultimo_modelo == 'M/M/c':
            return (f"λ (Chegada): {self.mmc_lambda.get()}\n"
                    f"μ (Atendimento): {self.mmc_mu.get()}\n"
                    f"c (Servidores): {self.mmc_c.get()}")
        elif self.ultimo_modelo == 'M/M/1/K':
            return (f"λ (Chegada): {self.mm1k_lambda.get()}\n"
                    f"μ (Atendimento): {self.mm1k_mu.get()}\n"
                    f"K (Capacidade): {self.mm1k_k.get()}")
        else:
            return "Parâmetros não disponíveis."

    def mostrar_ajuda(self):
        """Exibe uma janela de pop-up com informações de ajuda em abas."""

        ajuda_janela = tk.Toplevel(self)
        ajuda_janela.title("Ajuda - Conceitos de Teoria das Filas")
        ajuda_janela.geometry("680x550")
        ajuda_janela.transient(self)
        ajuda_janela.grab_set()
        ajuda_janela.resizable(False, False)

        parametros_frame = ttk.LabelFrame(ajuda_janela, text="Parâmetros de Entrada", padding=10)
        parametros_frame.pack(fill="x", padx=10, pady=(10, 5))

        parametros_texto = (
            "λ (Lambda) — Taxa média de chegada de clientes ao sistema (por unidade de tempo).\n"
            "μ (Mi) — Taxa média de atendimento de um único servidor.\n"
            "s (ou c) — Número de servidores em paralelo (exclusivo para o modelo M/M/c).\n"
            "K — Capacidade máxima do sistema (fila + atendimento) no modelo M/M/1/K."
        )

        ttk.Label(parametros_frame, text=parametros_texto, justify="left").pack(anchor="w")

        notebook = ttk.Notebook(ajuda_janela)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)

        def criar_aba(notebook_widget, titulo, conteudo):
            frame = ttk.Frame(notebook_widget, padding=15)
            notebook_widget.add(frame, text=titulo)

            texto = tk.Text(
                frame,
                wrap=tk.WORD,
                height=16,
                font=("Helvetica", 10),
                background="#f7f7f7",
                relief="flat",
            )
            texto.insert(tk.END, conteudo)
            texto.config(state="disabled")
            texto.pack(fill="both", expand=True)

        conteudo_mm1 = (
            "Modelo M/M/1\n"
            "================\n"
            "• Sistema com um único servidor e capacidade infinita de fila.\n"
            "• A chegada dos clientes segue uma distribuição de Poisson e os tempos de atendimento são exponenciais.\n"
            "• O sistema é estável quando λ < μ.\n\n"
            "Interpretação das métricas:\n"
            "  - ρ (rho) representa a fração de tempo em que o servidor está ocupado.\n"
            "  - P₀ é a probabilidade de não haver clientes no sistema.\n"
            "  - L indica o número médio de clientes na fila e em atendimento.\n"
            "  - Lq mostra quantos clientes esperam na fila, em média.\n"
            "  - W é o tempo médio total que o cliente passa no sistema (espera + serviço).\n"
            "  - Wq corresponde ao tempo médio de espera na fila antes do atendimento.\n\n"
            "Boas práticas:\n"
            "  • Se ρ estiver próximo de 1, considere aumentar a taxa de atendimento ou reduzir a taxa de chegada.\n"
            "  • Utilize este modelo quando houver apenas um ponto de atendimento com fila ilimitada."
        )

        conteudo_mmc = (
            "Modelo M/M/c (ou M/M/s)\n"
            "========================\n"
            "• Sistema com 'c' servidores idênticos trabalhando em paralelo e fila infinita.\n"
            "• As chegadas são Poisson e os tempos de serviço seguem distribuição exponencial.\n"
            "• A utilização média por servidor é dada por ρ = λ / (c·μ). O sistema é estável se ρ < 1.\n\n"
            "Como interpretar:\n"
            "  - P₀ indica a probabilidade de todos os servidores estarem livres.\n"
            "  - L e Lq mostram, respectivamente, o tamanho médio do sistema e da fila considerando múltiplos servidores.\n"
            "  - W e Wq revelam os tempos médios de permanência do cliente, levando em conta a possibilidade de atendimento imediato.\n\n"
            "Dicas de uso:\n"
            "  • Aumentar o número de servidores reduz o tempo de espera, porém aumenta o custo operacional.\n"
            "  • Utilize quando existir atendimento paralelo (ex.: caixas de banco, guichês, call centers)."
        )

        conteudo_mm1k = (
            "Modelo M/M/1/K\n"
            "================\n"
            "• Variante do M/M/1 com capacidade total limitada a K clientes (fila + atendimento).\n"
            "• Quando o sistema atinge a capacidade máxima, novos clientes são bloqueados ou perdidos.\n"
            "• A estabilidade depende da relação entre λ, μ e K; mesmo com λ ≥ μ, o sistema não explode, mas há rejeição.\n\n"
            "Métricas específicas:\n"
            "  - P₀ é a probabilidade do sistema estar vazio e Pₖ (não exibido) representa o bloqueio (sistema cheio).\n"
            "  - L e Lq refletem o número médio de clientes presentes respeitando a capacidade finita.\n"
            "  - W e Wq consideram apenas os clientes aceitos pelo sistema.\n\n"
            "Aplicações e recomendações:\n"
            "  • Adequado para processos com limite físico de espera (ex.: vagas de estacionamento, canais de comunicação).\n"
            "  • Avalie Pₖ para medir a taxa de perdas e tomar decisões sobre expansão de capacidade."
        )

        criar_aba(notebook, "  M/M/1  ", conteudo_mm1)
        criar_aba(notebook, "  M/M/c  ", conteudo_mmc)
        criar_aba(notebook, "  M/M/1/K  ", conteudo_mm1k)

        metricas_frame = ttk.LabelFrame(ajuda_janela, text="Métricas de Saída Apresentadas", padding=10)
        metricas_frame.pack(fill="x", padx=10, pady=(5, 10))

        metricas_texto = (
            "ρ (Rho) — Utilização média do(s) servidor(es).\n"
            "P₀ — Probabilidade de o sistema estar vazio.\n"
            "L — Número médio de clientes no sistema.\n"
            "Lq — Número médio de clientes aguardando na fila.\n"
            "W — Tempo médio total no sistema.\n"
            "Wq — Tempo médio de espera na fila."
        )

        ttk.Label(metricas_frame, text=metricas_texto, justify="left").pack(anchor="w")

        botoes_frame = ttk.Frame(ajuda_janela)
        botoes_frame.pack(pady=(0, 10))

        ttk.Button(botoes_frame, text="Fechar", command=ajuda_janela.destroy).pack()

    # --- Funções de Cálculo (Handlers) ---

    def calcular_mm1(self):
        """Pega os dados da aba M/M/1, chama a lógica e exibe os resultados."""
        self.ultimo_modelo = 'M/M/1'
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
            texto += f"Parâmetros: λ={lambda_}, μ={mu_}\n\n" 
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
        self.ultimo_modelo = 'M/M/c'
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
            texto += f"Parâmetros: λ={lambda_}, μ={mu_}, c={c_}\n\n" 
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
            texto += f"   ↳ Unidades de tempo no total: {resultados['W']:.4f}\n\n"
            texto += f"Wq (Tempo na Fila): {resultados['Wq']:.4f}\n"
            texto += f"   ↳ Unidades de tempo na fila: {resultados['Wq']:.4f}"
            
            self.exibir_resultado(texto)

        except ValueError:
            self.exibir_resultado("Erro: Verifique se λ e μ são números e 'c' é um inteiro.")
        except Exception as e:
            self.exibir_resultado(f"Erro inesperado: {e}")

    def calcular_mm1k(self):
        """Pega os dados da aba M/M/1/K, chama a lógica e exibe os resultados."""
        self.ultimo_modelo = 'M/M/1/K'
        try:
            lambda_ = float(self.mm1k_lambda.get())
            mu_ = float(self.mm1k_mu.get())
            k_ = int(self.mm1k_k.get())
            
            if lambda_ <= 0 or mu_ <= 0 or k_ <= 0:
                self.exibir_resultado("Erro: λ, μ e K devem ser maiores que zero (e 'K' deve ser inteiro).")
                return

            # Chama a função de lógica pura
            resultados = self.logica_mm1k(lambda_, mu_, k_)
            
            # Formata a saída
            texto = "--- Resultados M/M/1/K ---\n\n"
            texto += f"Parâmetros: λ={lambda_}, μ={mu_}, K={k_}\n\n" 
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
        # Ls_avg = (1 - P0) é o número médio de clientes em serviço (já que é M/M/1)
        Lq = L - (1 - P0)
        
        Wq = Lq / lambda_eff
        
        return {"rho": rho, "P0": P0, "Pk": Pk, "lambda_eff": lambda_eff, "L": L, "Lq": Lq, "W": W, "Wq": Wq}


if __name__ == "__main__":
    app = CalculadoraFilas()
    app.mainloop()