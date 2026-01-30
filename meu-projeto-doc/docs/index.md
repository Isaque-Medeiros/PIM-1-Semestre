# 🚀 Portfólio Técnico | Isaque Medeiros

Desenvolvedor focado em soluções estruturadas, com experiência acadêmica e técnica em múltiplas linguagens. Este espaço consolida meus projetos mais relevantes, organizados por domínio tecnológico.

---

## 🐍 Automação e Inteligência de Dados (Python)
*Foco em scripts de automação, processamento de dados e ETL (Extração, Transformação e Carga).*

### 🛠️ Projetos em Destaque
*   **Sistema Escolar com C++:** Extração de dados via scripts C++ com saída estruturada em JSON e também txt.
*   **Cadastros de Cursos (ONG):** Estruturação de dados acadêmicos utilizando arquivos JSONL para persistência leve.
*   **Trilha Machine Learning:** Documentação de estudos e implementação de algoritmos fundamentais.

???- example "Ver Amostra de Código SysEscolar (Python)"

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
    ![Imagem Arduino](assets/captura-arduino.png)

    ```c
    // Matriz de caracteres: I, S, A, Q, U, E
    char vNum[][35] = {
        {0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 1,1,1,1,1,1,1, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0}, // I
        {1,0,0,1,1,1,1, 1,0,0,1,0,0,1, 1,0,0,1,0,0,1, 1,0,0,1,0,0,1, 1,1,1,1,0,0,1}, // S
        {1,1,1,1,1,1,1, 1,0,0,1,0,0,0, 1,0,0,1,0,0,0, 1,0,0,1,0,0,0, 1,1,1,1,1,1,1}, // A
        {0,1,1,1,1,0,0, 1,0,0,0,0,1,0, 1,0,0,0,1,1,1, 1,0,0,0,0,1,0, 0,1,1,1,1,0,1}, // Q
        {1,1,1,1,1,1,1, 0,0,0,0,0,0,1, 0,0,0,0,0,0,1, 0,0,0,0,0,0,1, 1,1,1,1,1,1,1}, // U
        {1,1,1,1,1,1,1, 1,0,0,1,0,0,1, 1,0,0,1,0,0,1, 1,0,0,1,0,0,1, 1,0,0,1,0,0,1}  // E
    };

    int nAux, nCont, nCont2, volta;

    void setup() {
        for (nCont = 2; nCont < 14; nCont++) {
            pinMode(nCont, OUTPUT);
        }
    }

    void loop() {
        // Percorre cada uma das 6 letras definidas na matriz vNum
        for (int i = 0; i < 6; i++) {
            
            // Controla o tempo que cada letra fica exibida (persistência)
            for (volta = 0; volta < 20; volta++) {
                nAux = -7;
                
                // Varredura dos displays (Multiplexação) - Pinos 6 a 2
                for (nCont = 6; nCont > 1; nCont--) {
                    nAux += 7;
                    fnApagar();
                    
                    digitalWrite(nCont, 0); // Ativa o dígito comum (catodo/anodo)
                    
                    // Liga os segmentos correspondentes (Pinos 7 a 13)
                    for (nCont2 = 7; nCont2 < 14; nCont2++) {
                        digitalWrite(nCont2, vNum[i][(nCont2 - 7) + nAux]);
                    }
                }
            }
        }
    }

    void fnApagar() {
        delay(5); // Um delay menor (5-10ms) ajuda a evitar cintilação (flicker)
        for (int i = 2; i < 7; i++) {
            digitalWrite(i, 1); // Desliga os comuns
        }
        for (int i = 7; i < 14; i++) {
            digitalWrite(i, 0); // Desliga os segmentos
        }
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

Abaixo, apresento um projeto de **automação para preenchimento de formulários do Google Forms** utilizando dados extraídos diretamente de planilhas, visando otimizar processos repetitivos.

[Baixar Planilha](assets/projeto-planilha.xlsx){ .md-button } 

O script lê os dados da planilha (Excel/CSV) e utiliza uma logica em Java Script para preencher cada campo do formulário automaticamente.

??? "Ver JavaScript da Planilha"

    ```JavaScript
        function onEdit(e) {
        // Define os nomes das abas
        const abaEntrada = 'Pagina de busca'; 
        const abaDestino = 'Pagina de Sistema';

        const range = e.range;
        const sheet = range.getSheet();

        // Garante que a edição ocorreu na aba correta antes de prosseguir
        if (sheet.getName() !== abaEntrada) {
            return;
        }

        const notation = range.getA1Notation();
        const ss = e.source;
        const sheetEntrada = ss.getSheetByName(abaEntrada);
        const sheetDestino = ss.getSheetByName(abaDestino);

        // --- Processo de Salvar Dados e Limpar ---
        if (notation === 'B10') {
            // Pega todos os valores de B5:B10 (retorna uma matriz 2D)
            const valoresDeEntrada = sheetEntrada.getRange('B5:B10').getValues();

            // Verifica se algum campo está vazio usando o método some()
            // flat() transforma a matriz [[v1],[v2]] em [v1, v2]
            if (valoresDeEntrada.flat().some(celula => celula === '')) {
            return; 
            }

            // Mapeamento das variáveis (índices do array valoresDeEntrada)
            const [bp, nome, motivo, codigo, nota, comentario] = valoresDeEntrada.flat();

            // Encontra a próxima linha de forma instantânea
            const proximaLinha = sheetDestino.getLastRow() + 1;

            // Grava os dados. Usar setValues em bloco é muito mais rápido que vários setValue
            // A=bp, B=nome, C=codigo, D=motivo, E=nota
            sheetDestino.getRange(proximaLinha, 1, 1, 5).setValues([[bp, nome, codigo, motivo, nota]]);
            // H=comentario (Coluna 8)
            sheetDestino.getRange(proximaLinha, 8).setValue(comentario);

            // Chama a função de limpeza comum
            limparEntrada(sheetEntrada);

        // --- Processo de Limpeza Independente (G5) ---
        } else if (notation === 'G5') {
            limparEntrada(sheetEntrada);
        }
        }

    // Função auxiliar para evitar repetição de código
    function limparEntrada(sheet) {
    sheet.getRange('B5:B10').clearContent();
    // Insere a fórmula novamente com a concatenação correta de strings
    sheet.getRange('B6').setFormula('=INDEX(AF:AF; MATCH(B5; AA:AA; 0))');
    }
    ```

---

### 📬 Contato e Redes