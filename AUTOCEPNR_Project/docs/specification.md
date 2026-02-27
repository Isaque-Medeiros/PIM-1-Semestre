# ESPECIFICAÇÃO DO SISTEMA: LATAM AUTO-FILLER (SABRE INTERACT)

## 1. Visão Geral
**Objetivo:** Automatizar o preenchimento de formulários de "Estouro de Classe" a partir de dados visuais do Sabre Interact.
**Metodologia:** Spec-Driven Development (SDD).
**Target:** Executável Windows standalone (.exe).
Este documento define o de-para (mapping) dos dados extraídos via OCR/Clipboard do sistema Sabre Interact para os seletores HTML específicos do formulário de Estouro de Classe da Latam.

## 2. Objetos de Dados (Data Objects)
Definição dos campos capturados no Sabre e seu destino no HTML:

| Campo (Sabre Interact) | Identificador HTML (CSS Selector) | Regra de Transformação / Ação |
| :--- | :--- | :--- |
| **Código de PNR** | `input[id="form:txt_pnrCdg"]` | Extrair do PNR; converter para UPPERCASE. |
| **Ciudad** | `input[id="form:ciudadPrioridadNombreCiudad_input"]` | Inserir código IATA. Aciona preenchimento de País. |
| **País** | `input[id="form:ciudadPrioridadNombrePais"]` | Somente Leitura (Read-only); validar preenchimento. |
| **Depto** | `label[id="form:departamentos_label"]` | Objeto Select; Clicar e selecionar Depto técnico. |
| **Razón** | `label[id="form:razonEnabled_label"]` | Objeto Select; Selecionar motivo via regra PIC. |
| **Autorizador** | `label[id="form:authorizerEnabled_label"]` | Objeto Select; Nome do Supervisor autorizado. |
| **Núm. Segmento** | `input[id="form:txt_segmentNum"]` | Extrair índice da linha do voo no Sabre. |
| **Carrier** | `label[id="form:carrierEnabled_label"]` | Objeto Select; Mapear código (LA, LP, 4C, JJ). |
| **Vuelo** | `input[id="form:txt_vuelotNum"]` | Extrair apenas dígitos numéricos (max 4). |
| **Clase** | `label[id="form:classEnabled_label"]` | Objeto Select; Classe original da reserva. |
| **Fecha de Vuelo** | `input[id="form:dateFlight_input"]` | Converter data para formato brasileiro DD/MM/YYYY. |
| **Segmento** | `input[id="form:txt_segment"]` | Formato trecho: ORIGEM/DESTINO (Ex: GRUSCL). |
| **Pax** | `label[id="form:pax_paxID_label"]` | Objeto Select; Selecionar ID do passageiro. |
| **Cto Des.** | `input[id="form:txt_ctoDes"]` | Designador de Tarifa / Código de upgrade. |

## 3. Requisitos Funcionais (FuncSpec)

### RF001: Captura de Imagem (Input)
- O sistema deve aceitar entrada via CTRL+V (Clipboard).
- O sistema deve aceitar upload de arquivos (.png, .jpg).
- **Especificação:** O módulo de visão deve detectar o padrão de tela do Sabre Interact v2.1.

### RF002: Processamento OCR (Análise)
- Utilizar OCR para identificar coordenadas de campos fixos.
- Cruzar dados extraídos com o arquivo de `Regras_PIC_Latam.json`.
- Também verificar o arquivo de correção de nome `correcao_de_nome.txt`
- Validar se o "Estouro de Classe" é permitido pela regra X (ex: tarifa paga vs ocupação).

### RF003: Injeção de Dados (Output)
- Identificar a aba ativa do navegador (Chrome/Edge).
- Preencher campos utilizando seletores CSS ou ID.
- Simular "Delay Humano" de 200ms entre campos para evitar bloqueios de segurança.

## 4. Lógica de Negócio (Business Logic - SDD Object Oriented)

### Objeto `SabreScreen`
- **Atributos:** RawImage, ExtractedText, Timestamp.
- **Métodos:** `parse_fields()`, `validate_integrity()`.

### Objeto `LatamForm`
- **Atributos:** BrowserTabURL, InputFieldsList.
- **Métodos:** `focus()`, `fill_all()`, `submit_form()`.

## 5. Especificações Técnicas (Technical Specs)
- **Engine:** Python 3.11+.
- **OCR:** EasyOCR com modelo treinado para fontes monoespaçadas (SABRE).
- **Interface:** Janela "Always on Top" transparente para feedback.
- **Segurança:** O binário não deve realizar requisições externas não autorizadas (trabalho offline/VPN).

## 6. Mapeamento de Regras (Rules Engine)
- SE `Class_S_P` no Sabre == 'Y' E `Auth_Code` == 'PIC_S23'
- ENTÃO permitir preenchimento de `Premium Economy`.