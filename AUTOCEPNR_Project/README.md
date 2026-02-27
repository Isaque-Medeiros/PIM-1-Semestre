# AutoCEP‑NR

**LATAM Auto‑Filler (Sabre Interact → CEPNR)**

Este repositório abriga o esqueleto de um aplicativo Windows capaz de
preencher automaticamente o formulário de *estouro de classe* da LATAM
(CEPNR) usando dados extraídos da tela do Sabre Interact.

---

## 🧩 Visão geral

O objetivo é criar um **programa standalone (.exe)** semelhante ao Psiphon:
roda localmente, sem depender de VPN ou trocar de rede, e é resistente a
bloqueios de intranet.

O software deve:

1. Capturar imagens da tela do Sabre Interact (via `CTRL+V` ou arquivo).
2. Analisar o conteúdo usando OCR e regras definidas.
3. Identificar a aba/página ativa do navegador (Chrome/Edge).
4. Preencher os campos específicos do formulário CEPNR conforme a
   especificação.
5. Registrar e validar ações com arquivos auxiliares (regras PIC, correção
   de nome, etc.).

O desenvolvimento seguirá a metodologia **Spec‑Driven Development (SDD)**
e orientado a objetos, com os artefatos estruturados em Markdown.

---

## 🛠 Tecnologias sugeridas

| Propósito                   | Tecnologias recomendadas                 |
|----------------------------|------------------------------------------|
| OCR                         | `easyocr` (treinado para fontes Sabre)   |
| Manipulação de imagens       | `opencv-python`                          |
| Automação de navegador       | `selenium` ou `pyautogui` como fallback |
| Interface (status/Alertas)   | Tkinter, PyQt ou simples console         |
| Empacotamento `.exe`         | `pyinstaller` ou `cx_Freeze`             |
| Execução SDD / Testes        | `pytest`, Markdown para specs           |
| Gestão de projeto            | GitHub Remote Codespaces                 |

Recomenda‑se Python 3.11+ para aproveitar os recursos de tipagem e
performance necessários.

---

## 📁 Estrutura base criada

O repositório já contém uma base de pacotes e pastas que facilita a
implementação SDD:

```
AUTOCEPNR_Project/
├─ docs/                # documentação Markdown (specs, regras, mapeamentos)
├─ rules/               # JSON/MD com regras de negócio
├─ src/autocepnr/       # pacote Python (engine, automação, UI)
├─ tests/               # primeiros casos de teste Pytest
├─ requirements.txt     # dependências iniciais
├─ pyproject.toml       # metadados do pacote
├─ README.md            # você está lendo
└─ LICENSE              # MIT por enquanto
```

Esta organização suporta evoluir as especificações no `docs/` e gerar
o código a partir delas.

---

## 📌 Passo de execução para IA (etapa atual)

1. Analisar toda a especificação introdutória (já documentada em
   `docs/specification.md`).
2. Identificar melhores tecnologias e padrões (lista acima).
3. Gerar uma estrutura de especificação em formato Markdown para SDD.
4. Recomendar o uso do GitHub Remote Codespaces para ambiente de dev
   portátil.

---

## 🚀 Próximos passos

* Preencher os arquivos de especificação adicionais em `docs/` com mais
detalhes (objetos, validações, transformações, etc.).
* Implementar os módulos stub no pacote `src/autocepnr` seguindo a
especificação.
* Escrever testes Pytest baseados nos exemplos de captura/saída.
* Configurar o processo de empacotamento com PyInstaller.

---

Qualquer dúvida ou se precisar de ajuda para elaborar um novo artefato
Markdown (padrões, templates, etc.), é só avisar!
