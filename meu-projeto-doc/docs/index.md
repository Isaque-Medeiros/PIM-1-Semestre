# 🚀 Portfólio Técnico | Isaque Medeiros

Desenvolvedor focado em soluções estruturadas, com experiência acadêmica e técnica em múltiplas linguagens. Este espaço consolida meus projetos mais relevantes, organizados por domínio tecnológico.

---

## 🐍 Automação e Inteligência de Dados (Python)
*Foco em scripts de automação, processamento de dados e ETL (Extração, Transformação e Carga).*

### 🛠️ Projetos em Destaque
*   **Sistema Escolar com C++:** Extração de dados via scripts C++ com saída estruturada em JSON e também txt.
*   **Cadastros de Cursos (ONG):** Estruturação de dados acadêmicos utilizando arquivos JSONL para persistência leve.
*   **Trilha Machine Learning:** Documentação de estudos e implementação de algoritmos fundamentais.

??? example "Ver Amostra de Código SysEscolar (Python)"

    ```python
    import json
    import os

    lista_de_cursos = (
    "Curso de Python Inicial", 
    "Curso de Python Intermediário", 
    "Curso de Python Final"
    )

    meus_cursos = []

    ARQUIVO = "JSONNC.jsonl"

    def carregar_cursos():
    """Carrega os cursos do arquivo JSON, se existir."""
    global meus_cursos
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as arquivo:
            meus_cursos = json.load(arquivo)
    else:
        meus_cursos = []

    def salvar_cursos():
    """Salva os cursos no arquivo JSON."""
    with open(ARQUIVO, 'w') as arquivo:
        json.dump(meus_cursos, arquivo, indent=4)


    def verCursos():
    print("\n--- Cursos Disponíveis ---")
    if not lista_de_cursos:
        print("Nenhum curso disponível no momento.")
    else:
        for i, curso in enumerate(lista_de_cursos):
            print(f"{i + 1}. {curso}")
    print("--------------------------")

    def meusCursos():
    """Exibe os cursos que o usuário já assinou."""
    print("\n--- Meus Cursos ---")
    if not meus_cursos:
        print("Você ainda não possui nenhum curso =/, que tal tentar assinar um?")
    else:
        for i, curso in enumerate(meus_cursos):
            print(f"{i + 1}. {curso}")
    print("-------------------")

    def addCurso():
    """Permite ao usuário adicionar um curso da lista de disponíveis aos seus cursos."""
    print("\n--- Adicionar Curso ---")
    if not lista_de_cursos:
        print("Não há cursos disponíveis para adicionar no momento.")
        return

    verCursos()

    try:
        escolha = input("Digite o número do curso que deseja adicionar (ou '0' para cancelar): ")
        escolha = int(escolha)

        if escolha == 0:
            print("Operação cancelada.")
            return

        indice_curso = escolha - 1

        if 0 <= indice_curso < len(lista_de_cursos):
            curso_selecionado = lista_de_cursos[indice_curso]

            if curso_selecionado in meus_cursos:
                print(f"'{curso_selecionado}' já está nos seus cursos!")
            else:
                meus_cursos.append(curso_selecionado)
                salvar_cursos()  # Salva após adicionar
                print(f"'{curso_selecionado}' foi adicionado aos seus cursos com sucesso!")
        else:
            print("Número de curso inválido. Por favor, tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    print("-----------------------")


    # --- Programa principal ---

    carregar_cursos()  # Carrega os cursos salvos ao iniciar

    x = input("Digite 'x' para iniciar: ") 
    if x == "x":
    print("\nOlá!\nBem vindo/a ao nosso site de aprendizagem! \nSelecione uma das opções abaixo para prosseguir.")

    while True:
        print("\n--- Menu ---")
        print("1. Ver Cursos Disponíveis")
        print("2. Ver Meus Cursos")
        print("3. Adicionar Curso")
        print("4. Sair")
        print("------------")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            verCursos()
        elif opcao == "2":
            meusCursos()
        elif opcao == "3":
            addCurso()
        elif opcao == "4":
            print("Obrigado por visitar! Até mais.")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção entre 1 e 4.")
    else:
    print("Entrada incorreta. O programa não foi iniciado.")
    ```

---

## ⚙️ Engenharia de Sistemas e Hardware (C/C++)
*Lógica de programação, estruturas de dados e sistemas embarcados.*

### 🛠️ Projetos em Destaque

*   **Tinkercad & Arduino:** Desenvolvimento de lógica para hardware (LEDs de 7 segmentos, Semáforos e Sensores) com linguagem C pura.

??? example "Ver Amostra de Código LED 7 Seg (C)"

    ```C
        // PRIGRAMA DE EXEMPLO
    int vNumeros [][7] = {{1, 1, 1, 1, 1, 1, 0},// combinações para formar um caracter, sendo 1 para acender e 0 para apagar.
                        {0, 1, 1, 0, 0, 0, 0},// 1
                        {1, 1, 0, 1, 1, 0, 1},//2
                        {1, 1, 1, 1, 0, 0, 1},//3
                        {0, 1, 1, 0, 0, 1, 1},//4
                        {1, 0, 1, 1, 0, 1, 1},//5
                        {1, 0, 1, 1, 1, 1, 1},//6
                        {1, 1, 1, 0, 0, 0, 0},//7
                        {1, 1, 1, 1, 1, 1, 1},//8
                        {1, 1, 1, 1, 0, 1, 1},//9
                        {1, 1, 1, 0, 1, 1, 1},//A
                        {0, 0, 0, 1, 1, 1, 0},//L
                        {0, 1, 1, 1, 1, 1, 0}};//U

    void setup()
    {
    for(int nCont=2; nCont<9; nCont++)
    {
        pinMode(nCont, OUTPUT); //pinMode para usar a porta, sendo output ou input
        digitalWrite(nCont, 0);//Semelhante a Print, colocar o valor 1 de 2 a 8.
    }
    pinMode(14, OUTPUT); 
    digitalWrite(14, 0);
    pinMode(15, OUTPUT); 
    digitalWrite(15, 0);
    pinMode(16, OUTPUT); 
    digitalWrite(16, 0);
    pinMode(17, OUTPUT); 
    digitalWrite(17, 0);
    pinMode(18, OUTPUT); 
    digitalWrite(18, 0);
    }

    void loop()
    {
    Escrever(5, 14);
    delay(10);
    Escrever(10, 15);
    delay(10);
    Escrever(12, 16);
    delay(10);
    Escrever(11, 17);
    delay(10);
    Escrever(0, 18);
    delay(10);

    }

    void Escrever(int nNum, int nDig)
    {
    digitalWrite(14, 1);
    digitalWrite(15, 1);
    digitalWrite(16, 1);
    digitalWrite(17, 1);
    digitalWrite(18, 1);
    digitalWrite(nDig, 0);
    
    for(int nCont=2; nCont<9; nCont++)
        digitalWrite(nCont, vNumeros[nNum][nCont - 2]);
    
    }
    ```

---

## 🌐 Desenvolvimento Web e Cloud
*Criação de interfaces modernas e arquitetura em nuvem.*

### 🛠️ Projetos em Destaque

*   **AWS Cloud:** Implementação de arquiteturas básicas em infraestrutura de nuvem. (em processo)
*   **Landing Pages:** Projetos institucionais utilizando HTML5 e CSS3 moderno.

---

## 📊 Business Intelligence & Automação Office
*Uso de tecnologias para otimização de fluxos de trabalho corporativos.*

*   **Excel Avançado:** Desenvolvimento de dashboards e automação de atendimento via JavaScript/Office Scripts.
*   **Organização de Processos:** Estruturação de planilhas inteligentes para gestão de tempo e tarefas.

---

### 📬 Contato e Redes