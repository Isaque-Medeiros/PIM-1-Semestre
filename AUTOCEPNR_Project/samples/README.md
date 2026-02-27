# Samples / Fixtures for AutoCEPNR

Este diretório destina-se a armazenar exemplos de telas do Sabre Interact
assim como arquivos de saída gerados pela análise OCR. Você irá utilizá-los
ao desenvolver e testar o motor de extração e o preenchimento do formulário
CEPNR.

## O que capturar

1. **Screenshots reais** do Sabre Interact, incluindo:
   * PNR com status, classes e segmentos visíveis
   * Tela de emissão do bilhete
   * Qualquer outro passo relevante para a lógica de "estouro de classe"

   Salve como `sabrescreen_01.png`, `sabrescreen_02.jpg`, etc.

2. **Prints do formulário CEPNR** na LATAM com os campos vazios (e
   eventualmente com valores preenchidos) para uso em testes de automação.

   Ex: `cepnr_empty.png` e `cepnr_filled.png`.

3. **JSON de saída** de processamento OCR simulada. Quando você desenvolver
   `process_image()` em `src/autocepnr/automation.py`, faça com que crie
   arquivos de exemplo — copie-os aqui como `ocr_output_01.json`.

## O que fazer se você não tiver capturas reais

* Use uma ferramenta de desenho (Paint, Photoshop) para simular a tela do
  Sabre: crie retângulos e textos fictícios com hashtags para cada campo.
* Grave um pequeno script Python que gera imagens com `Pillow` e texto
  monoespaçado, replicando o layout de Sabre.
* Peça a colegas que compartilhem capturas; altere dados sensíveis antes de
  encaminhar.

## Objetivo

Ter amostras suficientes para:

- Treinar/ajustar o modelo de OCR (`EasyOCR`) às fontes do Sabre.
- Escrever testes unitários e de integração que compararem o JSON esperado
  com o retornado pelos métodos.
- Demonstrar o fluxo de preenchimento do formulário contra imagens reais.

> **Nota:** nunca inclua dados pessoais de passageiros reais nos samples;
altere ou anonimizar os PNRs antes de salvar.
