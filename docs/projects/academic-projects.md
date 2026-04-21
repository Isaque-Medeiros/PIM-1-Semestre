---
title: Projetos Acadêmicos
description: Trabalhos e projetos desenvolvidos durante a graduação em Análise e Desenvolvimento de Sistemas
---

# Projetos Acadêmicos

## Visão Geral

Esta seção documenta os principais projetos acadêmicos desenvolvidos durante meu curso de Análise e Desenvolvimento de Sistemas. Os projetos abrangem diversas áreas da computação, desde desenvolvimento web até sistemas embarcados.

## Projetos em Destaque

### 1. Sistema de Gestão Acadêmica (SysAcad)

**Descrição**: Sistema completo para gestão de instituições de ensino, desenvolvido em C++ para o trabalho do primeiro semestre.

**Funcionalidades Principais**:
- Cadastro de alunos, professores e disciplinas
- Controle de notas e frequência
- Geração de relatórios acadêmicos
- Sistema de filas para atendimento

**Tecnologias Utilizadas**:
- Linguagem C++
- Arquivos texto para persistência
- Estruturas de dados personalizadas

**Estrutura de Arquivos**:
```
ProgramaSysAcad/
├── alunos.txt          # Base de dados de alunos
├── materias.txt        # Disciplinas cadastradas
├── notas.txt          # Registro de notas
├── turmas.txt         # Turmas e horários
├── fila.txt           # Sistema de fila de atendimento
├── relatorio.txt      # Relatórios gerados
├── funcoes.cpp        # Funções principais do sistema
└── homepage.cpp       # Interface principal
```

**Código Exemplo - Funções Principais**:
```cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

// Estrutura para representar um aluno
struct Aluno {
    int matricula;
    string nome;
    string curso;
    int semestre;
};

// Função para cadastrar novo aluno
void cadastrarAluno() {
    Aluno novoAluno;
    
    cout << "=== CADASTRO DE ALUNO ===" << endl;
    cout << "Matrícula: ";
    cin >> novoAluno.matricula;
    cout << "Nome: ";
    cin.ignore();
    getline(cin, novoAluno.nome);
    cout << "Curso: ";
    getline(cin, novoAluno.curso);
    cout << "Semestre: ";
    cin >> novoAluno.semestre;
    
    // Salvar no arquivo
    ofstream arquivo("alunos.txt", ios::app);
    if (arquivo.is_open()) {
        arquivo << novoAluno.matricula << "," 
                << novoAluno.nome << "," 
                << novoAluno.curso << "," 
                << novoAluno.semestre << endl;
        arquivo.close();
        cout << "Aluno cadastrado com sucesso!" << endl;
    } else {
        cout << "Erro ao abrir arquivo!" << endl;
    }
}
```

### 2. Projeto ONG - Trabalho Escolar

**Descrição**: Sistema para gestão de cursos e atividades de uma organização não-governamental, desenvolvido em Python.

**Funcionalidades**:
- Gerenciamento de cursos oferecidos
- Controle de participantes
- Geração de certificados
- Relatórios de atividades

**Estrutura de Dados**:
```python
# Estrutura JSON para cursos
essructura_curso = {
    "id_curso": "string",
    "nome_curso": "string", 
    "instrutor": "string",
    "carga_horaria": "int",
    "participantes": ["lista_de_matriculas"],
    "data_inicio": "datetime",
    "data_termino": "datetime"
}
```

### 3. Assistente Virtual com IA

**Descrição**: Projeto final do programa DIO desenvolvendo um assistente virtual inteligente com capacidades de processamento de linguagem natural.

**Arquitetura do Sistema**:
```
ProjetoFinalAssistente/
├── app/
│   ├── ai_engine.py          # Motor de IA
│   ├── file_manager.py       # Gerenciador de arquivos
│   ├── main.py              # Aplicação principal
│   ├── app_web.py           # Interface web
│   └── requirements.txt     # Dependências
├── config/
│   └── settings.json        # Configurações
├── data/
│   ├── input/               # Dados de entrada
│   └── output/              # Dados processados
└── interface/
    └── index.html           # Frontend web
```

**Funcionalidades do Assistente**:
- Processamento de comandos de voz
- Respostas inteligentes baseadas em contexto
- Integração com APIs externas
- Interface web responsiva

### 4. Projetos Microsoft Azure

**Descrição**: Conjunto de projetos desenvolvidos durante o programa Microsoft Azure da DIO.

**Projeto 1 - Ambiente Cloud**:
- Configuração de ambiente Azure
- Scripts PowerShell para automação
- Deploy de aplicações

**Projeto 2 - Blog em Azure**:
- Aplicação web com Docker
- HTML5, CSS3, JavaScript
- Deploy automatizado

**Projeto 3 - Infraestrutura como Código**:
- Templates ARM
- Automação de recursos cloud
- Gestão de infraestrutura

### 5. Circuitos Eletrônicos (Tinkercad)

**Projetos Desenvolvidos**:

#### Semáforo Inteligente
- Microcontrolador Arduino
- LEDs para sinalização
- Botão para pedestres
- Temporização programável

**Código Arduino**:
```c
void setup() {
    pinMode(ledVermelho, OUTPUT);
    pinMode(ledAmarelo, OUTPUT);
    pinMode(ledVerde, OUTPUT);
    pinMode(botaoPedestre, INPUT);
}

void loop() {
    // Lógica de controle do semáforo
    cicloNormal();
    
    if (digitalRead(botaoPedestre) == HIGH) {
        atenderPedestre();
    }
}
```

#### Display LED 7 Segmentos
- Controle de display numérico
- Multiplexação de LEDs
- Exibição de caracteres

#### Sistema RGB com Botão
- LEDs RGB endereçáveis
- Controle de cores
- Interface com botões

### 6. Projeto AWS

**Descrição**: Projeto de cloud computing utilizando Amazon Web Services para deploy de aplicações.

**Componentes**:
- EC2: Instâncias virtuais
- S3: Armazenamento de objetos
- Lambda: Computação serverless
- API Gateway: Gerenciamento de APIs

### 7. Organização de Planilhas

**Descrição**: Projeto de automação para organização e análise de planilhas Excel usando JavaScript.

**Funcionalidades**:
- Leitura de arquivos XLSX
- Transformação de dados
- Geração de relatórios
- Automação de processos

**Tecnologias**:
- JavaScript/Node.js
- Bibliotecas para Excel
- Algoritmos de processamento

## Competências Desenvolvidas

### Habilidades Técnicas
- **Programação**: C++, Python, JavaScript, Arduino C
- **Banco de Dados**: Estruturas de arquivos, JSON
- **Web Development**: HTML5, CSS3, JavaScript
- **Cloud Computing**: Azure, AWS
- **Embedded Systems**: Arduino, Tinkercad
- **Version Control**: Git, GitHub

### Habilidades de Gestão
- **Metodologias Ágeis**: Scrum, Kanban
- **Documentação**: Technical writing, READMEs
- **Apresentação**: Demonstração de projetos
- **Trabalho em Equipe**: Projetos colaborativos

## Resultados e Conquistas

- ✅ Sistema SysAcad implementado com sucesso
- ✅ Assistente virtual funcional com IA
- ✅ Projetos cloud deployados na Azure
- ✅ Circuitos eletrônicos operacionais
- ✅ Documentação técnica completa

## Próximos Passos

- [ ] Expandir funcionalidades do SysAcad
- [ ] Adicionar machine learning ao assistente
- [ ] Implementar mais projetos cloud
- [ ] Desenvolver aplicações mobile
- [ ] Explorar IoT e robótica

## Links e Recursos

- [Repositório GitHub](https://github.com/isaque/academic-projects)
- [Galeria de Projetos](index.md)
- [Perfil Profissional](../about/profile.md)
- [LinkedIn Acadêmico](https://linkedin.com/in/isaque)