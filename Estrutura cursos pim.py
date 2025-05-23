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