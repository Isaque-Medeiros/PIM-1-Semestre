# Casos de Uso do BSFM

Esta página documenta os principais casos de uso do Brazilian System of Food Metric, demonstrando como diferentes perfis de usuários podem se beneficiar da plataforma.

!!! warning "Projeto Acadêmico"
    Os casos de uso abaixo são **conceituais** e representam o planejamento do projeto. As funcionalidades implementadas podem variar.

---

## Índice de Casos de Uso

1. [Usuário Final](#usuário-final)
2. [Nutricionista](#nutricionista)
3. [Desenvolvedor](#desenvolvedor)

---

## Usuário Final

### Cenário
João quer melhorar seus hábitos alimentares e precisa de orientação acessível.

### Fluxo de Uso
1. **Cadastro e Perfil**
   - Cria conta gratuita
   - Informa dados básicos (idade, peso, altura)
   - Define objetivos pessoais
   - Informa condições de saúde (diabetes, intolerâncias)

2. **Acompanhamento Diário**
   - Registra refeições via web
   - Recebe análise nutricional com IA
   - Escaneia rótulos de produtos com OCR
   - Visualiza progresso em gráficos

3. **Recomendações Personalizadas**
   - Recebe feedback IA baseado no perfil de saúde
   - Health Score com alertas restritivos
   - Sugestões de substituições alimentares

### Funcionalidades Implementadas
- ✅ Cadastro e login
- ✅ Dashboard com métricas (IMC, TMB, TDEE)
- ✅ Análise de alimentos por IA (YOLO + USDA)
- ✅ Análise de rótulos (OCR + Groq LLM)
- ✅ Diário alimentar
- ✅ Plano de refeições semanal
- ✅ Consumo de água
- ✅ Gráficos de evolução
- ✅ Mapa SOS Saúde
- ✅ Dados de saúde (diabetes, intolerâncias)
- ✅ Health Score com feedback personalizado

---

## Nutricionista

### Cenário
Maria é nutricionista e quer usar ferramentas digitais para acompanhar pacientes.

### Fluxo de Uso
1. **Cadastro de Paciente**
   - Importa dados básicos do paciente
   - Define objetivos
   - Registra preferências alimentares
   - Anota condições de saúde (diabetes, intolerâncias)

2. **Análise Automática**
   - Sistema analisa padrões alimentares
   - Identifica deficiências nutricionais
   - Sugere ajustes na dieta
   - IA gera feedback personalizado por paciente

3. **Monitoramento**
   - Acompanha progresso em tempo real
   - Ajusta recomendações
   - Gera relatórios

### Status
- ⏳ Em planejamento para versões futuras

---

## Desenvolvedor

### Cenário
Um desenvolvedor quer integrar análise nutricional em seu aplicativo.

### Fluxo de Uso
1. **Integração API**
   - Conhece os endpoints disponíveis
   - Implementa chamadas HTTP
   - Processa respostas JSON

2. **Testes**
   - Usa ambiente de desenvolvimento
   - Valida integrações
   - Otimiza performance

### Endpoints Disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/analisar-prato` | Analisa imagem de alimento |
| POST | `/api/rotulo/analisar` | Analisa texto OCR de rótulo |
| GET | `/api/saude/{id}` | Dados de saúde do usuário |
| PUT | `/api/saude/atualizar` | Atualiza dados de saúde |
| GET | `/dashboard` | Dados do dashboard |
| GET | `/health` | Health check |

---

## Métricas de Sucesso

| Caso de Uso | Métrica | Meta |
|-------------|---------|------|
| Usuário Final | Satisfação | 4/5 |
| Nutricionista | Pacientes ativos | 50 |
| Desenvolvedor | Integrações | 5 |

---

## Próximos Passos

1. **Escolha seu perfil** acima
2. **Registre-se** na plataforma
3. **Explore** as funcionalidades disponíveis
4. **Forneça feedback** para melhorias

---

**Última atualização:** 01 de Maio de 2026
