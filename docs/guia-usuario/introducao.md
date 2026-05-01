# Guia do Usuário BSFM

Bem-vindo ao **BSFM (Brazilian System of Food Metric)**! Este guia irá ajudá-lo a usar o protótipo da nossa plataforma de nutrição inteligente.

!!! warning "Projeto Acadêmico"
    O BSFM é um **protótipo acadêmico** desenvolvido por estudantes da UNIP. As funcionalidades são demonstrações conceituais e podem conter limitações.

---

## O que é o BSFM?

O BSFM é uma plataforma de análise nutricional que utiliza **inteligência artificial** para ajudar você a:

- **Analisar alimentos** através de fotos do seu prato
- **Escaneiar rótulos nutricionais** com OCR e receber feedback personalizado
- **Acompanhar suas métricas de saúde** como IMC, TMB e gasto calórico
- **Definir e acompanhar metas** pessoais de saúde e nutrição
- **Localizar serviços de saúde** próximos (UPAs e hospitais)
- **Planejar suas refeições** com cronogramas personalizados
- **Registrar consumo de água** diário
- **Gerenciar dados de saúde** como diabetes e intolerâncias alimentares

---

## Primeiros Passos

### 1. Crie sua Conta

1. Acesse a plataforma (URL fornecida pelo seu professor)
2. Clique em **"Cadastrar"** no canto superior direito
3. Preencha seus dados:
   - Nome completo
   - Email válido
   - Senha segura (mínimo 8 caracteres)
4. Verifique seu email e insira o código de 6 dígitos
5. Aceite os termos de uso

!!! tip "Dica"
    Use uma senha forte com letras maiúsculas, minúsculas, números e símbolos.

### 2. Complete seu Perfil

Após o cadastro, complete seu perfil para análises personalizadas:

- **Peso** (kg)
- **Altura** (cm)
- **Idade**
- **Sexo biológico**
- **Nível de atividade física**:
  - Sedentário (pouco ou nenhum exercício)
  - Levemente ativo (1-3 dias/semana)
  - Ativo (3-5 dias/semana)
  - Muito ativo (6-7 dias/semana)

### 3. Configure seus Dados de Saúde

No menu **Perfil** > **Dados de Saúde**, informe:

- **Diabetes**: Tipo 1, Tipo 2, Pré-diabetes, Gestacional ou Não
- **Intolerâncias Alimentares**: Lactose, Glúten, etc.

Esses dados são usados pela IA para personalizar o feedback nutricional.

### 4. Explore o Dashboard

Seu dashboard pessoal mostra:

- **IMC Atual** e evolução histórica
- **Taxa Metabólica Basal (TMB)**
- **Gasto Calórico Total (TDEE)**
- **Metas definidas**
- **Gráficos de progresso** de peso e IMC

---

## Funcionalidades

### Análise por IA (Prato)

1. Acesse o **Analisador IA**
2. Tire uma foto do alimento
3. Selecione o tamanho da porção (pequeno, médio, grande)
4. Veja os resultados nutricionais com feedback personalizado

### Analisador de Rótulos (OCR)

1. Acesse o **Analisador de Rótulos**
2. Aponte a câmera para a tabela nutricional de um produto
3. O sistema extrai o texto automaticamente via OCR
4. A IA analisa e retorna:
   - **Produto detectado**
   - **Health Score** (0-10)
   - **Pode Consumir** (Sim/Não/Moderado)
   - **Análise personalizada** baseada no seu perfil
   - **Dica BSFM** com sugestões

### Dashboard e Métricas

#### Índice de Massa Corporal (IMC)
```
IMC = Peso (kg) ÷ Altura (m)²
```

| Classificação | IMC |
|--------------|-----|
| Abaixo do peso | < 18.5 |
| Peso normal | 18.5 - 24.9 |
| Sobrepeso | 25 - 29.9 |
| Obesidade Grau I | 30 - 34.9 |
| Obesidade Grau II | 35 - 39.9 |
| Obesidade Grau III | ≥ 40 |

#### Taxa Metabólica Basal (TMB)
**Homens:**
```
TMB = 88.362 + (13.397 × peso kg) + (4.799 × altura cm) - (5.677 × idade)
```

**Mulheres:**
```
TMB = 447.593 + (9.247 × peso kg) + (3.098 × altura cm) - (4.330 × idade)
```

#### Gasto Calórico Total
| Nível de Atividade | Multiplicador |
|-------------------|---------------|
| Sedentário | TMB × 1.2 |
| Levemente ativo | TMB × 1.375 |
| Ativo | TMB × 1.55 |
| Muito ativo | TMB × 1.725 |

### Mapa SOS Saúde

Localize UPAs e hospitais próximos usando o mapa interativo Leaflet.

### Diário Alimentar

Registre suas refeições diárias e acompanhe seu consumo calórico.

### Plano de Refeições

Crie um plano alimentar semanal com refeições para cada dia da semana.

### Consumo de Água

Registre seu consumo diário de água e acompanhe sua hidratação.

---

## FAQ - Perguntas Frequentes

### Análise por IA

**Q: A precisão da análise é confiável?**
A: O modelo YOLO tem precisão limitada por ser um protótipo acadêmico. Os resultados são aproximados e não substituem avaliação profissional.

**Q: E se a IA não reconhecer meu alimento?**
A: Você pode tentar outra foto com melhor ângulo/iluminação ou buscar manualmente na base de dados.

### Analisador de Rótulos

**Q: Como funciona o OCR de rótulos?**
A: O Tesseract.js processa a imagem diretamente no seu navegador (nada é enviado ao servidor). Apenas o texto extraído é enviado para análise pela IA.

**Q: Preciso de internet para usar o OCR?**
A: Sim, o OCR precisa carregar o modelo Tesseract.js da CDN na primeira vez.

### Dados de Saúde

**Q: Para que servem os dados de diabetes e intolerância?**
A: A IA considera essas informações para gerar alertas personalizados. Por exemplo, se você tem diabetes, a IA alertará sobre açúcares adicionados.

**Q: Posso alterar meus dados de saúde depois?**
A: Sim, em **Perfil** > **Dados de Saúde** você pode atualizar quando quiser.

### Conta e Perfil

**Q: Posso mudar meu email?**
A: Sim, em "Perfil" > "Editar Perfil".

**Q: Esqueci minha senha, o que fazer?**
A: Clique em "Esqueci minha senha" na tela de login e siga as instruções enviadas por email.

### Métricas e Saúde

**Q: O BSFM substitui um nutricionista?**
A: **Não.** O BSFM é uma ferramenta de apoio. Sempre consulte um profissional de saúde para orientações personalizadas.

**Q: Meus dados de saúde são seguros?**
A: Usamos criptografia BCrypt para senhas. Por ser um protótipo acadêmico, recomenda-se não usar dados reais sensíveis.

---

## Suporte

- **Email:** suporte@bsfm.com.br
- **Chat online:** Disponível no site (horário comercial)

---

!!! success "Pronto para Começar?"
    **Agora você tem todas as informações para usar o BSFM.** Lembre-se: este é um protótipo acadêmico em desenvolvimento.

    **Equipe BSFM - UNIP**
