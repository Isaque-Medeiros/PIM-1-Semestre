# KNOWLEDGE BASE: POLÍTICA DE CORREÇÃO DE NOME LATAM

## 1. DEFINIÇÕES GERAIS (Global Rules)
- **Custo:** $0 (Isento de multa, taxa de serviço ou diferença tarifária) para itinerários 100% LATAM.
- **Premissa:** Manter mesmo passageiro e mesma viagem (voos, datas, tarifas inalterados).
- **Limite:** Permitido apenas 01 (uma) correção por bilhete.
- **Upgrade/Cortesia:** Se houver Upgrade de Leilão ou Cortesia confirmado, a postulação DEVE ser anulada antes da correção.

---

## 2. ENGINE DE DECISÃO: FERRAMENTAS (Tools Selector)

### 2.1 AGENTE 360 (Prioridade 1)
**Condições de Uso:**
- Itinerário 100% LATAM.
- Ordens geradas no site LATAM ou Agente 360.
- Voos dentro da janela comercial.
- **Bloqueios (NÃO usar Agente 360 se):**
    - Reserva com Passageiro Infante (INF).
    - Inclui número de sócio LATAM Pass (FFN).
    - Itinerários Multidestinos.
    - Reserva com Upgrade confirmado.

### 2.2 FERRAMENTAS DE BACKUP (Sabre / Allegro / APEC)
**Condições de Uso:**
- Casos negados pelo Agente 360.
- Casos de determinação legal (casamento, divórcio, adoção, gênero).
- Presença de voos parceiros (Interline / Codeshare).
- Reemissão de INF (Infante).

---

## 3. MATRIZ DE TIPOS DE ERRO (Error Classification)

| ID | Tipo de Erro | Regra Lógica | Exemplo |
| :--- | :--- | :--- | :--- |
| **01** | Ortográfico / Fonético | Máximo de 3 letras (nome ou sobrenome) | GONSALES -> GONZALEZ |
| **02** | Nomes Invertidos | Troca entre campo Nome e Sobrenome | LUISA/GALVEZ -> GALVEZ/LUISA |
| **03** | Adição de Nome/Sobre. | Adicionar sem substituir o original | SILVA/ALBERTO -> SILVA/LUIS ALBERTO |
| **04** | Duplicidade | Eliminar nome ou sobrenome repetido | SMITH/EMMA EMMA -> SMITH/EMMA |
| **05** | Agnome (Afixo) | Adição ou exclusão (JR, Neto, Filho, etc) | PEREIRA/JOSE -> PEREIRA JR/JOSE |
| **06** | Mudança Legal | Determinação Judicial (Exige 2 Docs: Antigo + Novo) | Casamento, Divórcio, Gênero |
| **07** | Comprovação | Outros casos que comprovem mesmo passageiro | MARTINES -> MARTINEZ (Doc Necessário) |

---

## 4. FLUXO OPERACIONAL (Process Logic)

### 4.1 Via Agente 360 (Automático)
1. PNR > Revisar dados do passageiro.
2. Selecionar "Nome ou sobrenome correto".
3. Executar modificação conforme Matriz de Erro (Tipos 1 a 5).
4. Salvar (O sistema gera "Dados corrigidos" com data).
5. **Obs:** Não altera número da passagem nem CUV.

### 4.2 Via Sabre/Allegro (Manual/Backup) -- PERMITIDO NO Formulário CEPNR
1. Validar status do cupom ("OK" para alteração).
2. Criar Novo PNR na classe original.
3. Se Itinerário 100% LATAM: Reemissão **Involuntária** (Isenta).
4. **Campo Endossos (Endorsement):** `NM CORREÇÃO` (ou `NM CORREÇÃO ATO` se no aeroporto).
5. Se Houver EMD (Assentos/Bagagem): O EMD deve ser reemitido para o novo nome.

---

## 5. REGRAS PARA PARCEIROS (Partner & Interline Logic)

### 5.1 Voos DELTA (Exceção Especial)
- **Ortografia (< 3 letras) & > 48h:** Suporte (HVC/Support Desk) corrige no mesmo PNR.
- **Outros casos / < 48h:** Novo PNR, classe original. Se indisponível, classe mais baixa na mesma cabine.
- **Endossos:** `NM Correction`.

### 5.2 Outras Cias (OLA) / Interline
- Reservar OLA na classe original.
- Se mesma classe indisponível: Reservar na mesma cabine (classe disponível).
- Diferenças tarifárias devem ser pagas via método AD (Ajuste). Isenção apenas de multa e taxa.

---

## 6. MUDANÇA DE TIPO DE PASSAGEIRO (PTC: ADT / CHD / INF)
- **ADT p/ CHD ou INF:** Sem multa/taxa, reembolsa diferença via EMD-S.
- **INF p/ CHD ou ADT:** Sem multa/taxa, **cobra** diferença tarifária (Reemissão Voluntária Path).
- **Procedimento INF (Sabre):** Remover INF do PNR -> Adicionar INF com nome correto associado ao ADT -> Reemissão Involuntária.

---

## 7. EXCEÇÕES E BLOQUEIOS (Failure Cases)
- **Erro Duplo (Nome + Doc):** Se não for possível validar que é a mesma pessoa, correção NEGADA.
- **Solução Contingencial:** Cliente compra nova passagem (mesmo voo/data) e solicita reembolso da errada via Agente 360 (Motivo: `DUPLICIDAD TKT/EMD - DUPE INEXATA`).
- **Aeroporto (ATO):** Voos 100% domésticos (Brasil, Chile, Peru) permitem embarque com erro de nome sem reemissão. Demais rotas exigem reemissão `NM CORREÇÃO ATO`.

---

## 8. ELEMENTOS DE SISTEMA PARA PNR (Command Support)
- **OSI (Other Service Information):** `OSI: NM CORRECTION FROM [NAME_ANTIGO] TO [NAME_NOVO]`
- **Waiver:** Não necessário para 100% LATAM (exceto casos 6 e 7 em CTO/ATO).

---
