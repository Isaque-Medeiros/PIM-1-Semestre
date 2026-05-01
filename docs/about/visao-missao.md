# Visão e Missão do BSFM

!!! warning "Projeto Acadêmico - Protótipo"
    O **BSFM (Brazilian System of Food Metric)** é um projeto acadêmico desenvolvido por estudantes do curso de Análise e Desenvolvimento de Sistemas da **UNIP (Universidade Paulista)**. Este documento descreve a visão conceitual do projeto, que simula uma ONG de nutrição como parte do trabalho semestral.

## Nossa Visão (Conceitual)

**Ser um sistema de referência em métricas alimentares no Brasil, democratizando o acesso à nutrição de qualidade através da tecnologia.**

> "Imaginamos um Brasil onde cada cidadão tenha acesso fácil e gratuito a análises nutricionais precisas, onde a tecnologia elimina barreiras e promove hábitos alimentares saudáveis."

## Nossa Missão (Conceitual)

**Utilizar inteligência artificial para fornecer análises nutricionais precisas, acompanhamento personalizado e educação alimentar acessível a todos os brasileiros.**

### Pilares da Nossa Missão:

1. **Inovação Tecnológica**
   - Desenvolver soluções de IA que reconheçam e analisem alimentos
   - Criar interfaces intuitivas que qualquer pessoa possa usar
   - Integrar pesquisas em nutrição e machine learning
   - Implementar Split Architecture para análise de rótulos (OCR + LLM)

2. **Contexto Brasileiro**
   - Adaptar tecnologias globais à realidade alimentar brasileira
   - Incluir alimentos regionais e tradições culinárias locais

3. **Impacto na Saúde Pública**
   - Apoiar a redução de índices de obesidade e diabetes
   - Contribuir para políticas públicas de alimentação saudável
   - Oferecer feedback personalizado baseado em condições de saúde (diabetes, intolerâncias)

4. **Acesso Democrático**
   - Oferecer serviços gratuitos para a população
   - Garantir acessibilidade para pessoas com deficiência
   - Disponibilizar análise nutricional via PWA em dispositivos móveis

## Valores Fundamentais

!!! note "Transparência"
    **Acreditamos que dados nutricionais devem ser abertos e acessíveis.** Documentamos publicamente nossas metodologias e fontes de dados.

!!! check "Precisão Científica"
    **Cada análise é baseada em fontes científicas como USDA FoodData Central e TACO.**

!!! heart "Impacto Social"
    **Medimos nosso sucesso pelo potencial de impacto na saúde das pessoas.**

!!! bulb "Inovação Contínua"
    **Estamos sempre evoluindo.** Acompanhamos as últimas pesquisas em IA e nutrição.

## Público-Alvo (Conceitual)

### 1. População em Geral
!!! info "Acesso Universal"
    - Pessoas que buscam melhorar hábitos alimentares
    - Comunidades com acesso limitado a nutricionistas
    - Usuários de aplicativos de saúde e bem-estar
    - Pessoas com diabetes ou intolerâncias alimentares

### 2. Profissionais de Saúde
!!! check "Ferramentas de Apoio"
    - Nutricionistas que desejam ferramentas digitais
    - Médicos interessados em monitoramento de pacientes

### 3. Educadores e Escolas
!!! school "Educação Alimentar"
    - Professores de ciências e biologia
    - Escolas que promovem educação nutricional

## Fontes de Dados Utilizadas

```yaml
nutricionais:
  - USDA FoodData Central: Base de dados nutricional americana
  - TACO: Tabela Brasileira de Composição de Alimentos

ia:
  - YOLO Custom Model: Modelo de detecção de alimentos
  - ONNX Runtime: Inferência otimizada
  - Groq Llama 3: LLM para feedback nutricional personalizado
  - Tesseract.js: OCR para escaneamento de rótulos

email:
  - Brevo API: Serviço de email transacional
```

## Status Atual do Projeto

- **Início do desenvolvimento:** 29 de fevereiro de 2026
- **Status:** Protótipo acadêmico em desenvolvimento
- **Versão atual:** 1.3.5 (CoreAnalytics)
- **Equipe:** 4 estudantes de ADS - UNIP
- **Funcionalidades implementadas:** Cadastro, login, dashboard, análise de alimentos por IA, analisador de rótulos OCR, mapa de hospitais, diário alimentar, plano de refeições, consumo de água, dados de saúde (diabetes/intolerâncias), Health Score com feedback Groq
- **Próximos passos:** Refinamento da IA, correção de bugs, melhorias de UI/UX

---

!!! quote "Nosso Compromisso"
    **"Acreditamos que tecnologia e saúde devem andar juntas. Este projeto acadêmico é o primeiro passo para construir um Brasil mais saudável, começando pelo prato de cada brasileiro."**

*Equipe BSFM - Projeto Acadêmico UNIP - Transformando bytes em saúde desde fevereiro de 2026*
