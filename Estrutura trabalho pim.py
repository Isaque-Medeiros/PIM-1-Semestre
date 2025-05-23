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
    global meus_cursos
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, 'r') as arquivo:
                conteudo = arquivo.read().strip()
                if conteudo:
                    meus_cursos = json.loads(conteudo)
                else:
                    meus_cursos = []
        except (json.JSONDecodeError, FileNotFoundError):
            print("Arquivo corrompido ou inválido. Iniciando com lista vazia.")
            meus_cursos = []
    else:
        meus_cursos = []

def salvar_cursos():
    with open(ARQUIVO, 'w') as arquivo:
        json.dump(meus_cursos, arquivo, indent=4)


def verCursos():
    print("\n--- Cursos Disponíveis ---")
    for i, curso in enumerate(lista_de_cursos):
        print(f"{i + 1}. {curso}")
    print("--------------------------")

def meusCursos():
    print("\n--- Meus Cursos ---")
    if not meus_cursos:
        print("Você ainda não possui nenhum curso.")
    else:
        for i, curso in enumerate(meus_cursos):
            print(f"{i + 1}. {curso}")
    print("-------------------")

def addCurso():
    print("\n--- Adicionar Curso ---")
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
                salvar_cursos()
                print(f"'{curso_selecionado}' foi adicionado com sucesso!")
        else:
            print("Número inválido. Tente novamente.")
    except ValueError:
        print("Por favor, digite um número válido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# --- Programa Principal ---

carregar_cursos()

x = input("Digite 'x' para iniciar: ")
if x.lower() == "x":
    print("\nBem-vindo(a) à plataforma de cursos!")

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
            print("Obrigado por usar! Até logo.")
            break
        else:
            print("Opção inválida. Tente novamente.")
else:
    print("Entrada incorreta. Programa encerrado.")
