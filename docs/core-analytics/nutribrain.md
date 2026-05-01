# NutriBrain Service

O **NutriBrainService** é o motor de inteligência artificial do BSFM.CoreAnalytics, responsável por processar o texto extraído de rótulos nutricionais e gerar análises personalizadas usando a API do **Groq** com o modelo **Llama 3**.

---

## Visão Geral

```csharp
public class NutriBrainService
{
    private const string GroqEndpoint = "https://api.groq.com/openai/v1/chat/completions";
    private const string ModeloPadrao = "llama3-70b-8192";
    
    public async Task<RotuloResponse> AnalisarRotuloAsync(
        string textoOcr, 
        string systemPrompt,
        CancellationToken ct = default)
    {
        // 1. Monta payload com SystemPrompt + texto OCR
        // 2. Envia para Groq API
        // 3. Processa resposta JSON
        // 4. Retorna análise estruturada
    }
}
```

## Funcionamento

### 1. Montagem do Payload

O serviço combina:
- **SystemPrompt**: Gerado pelo ContextInjectorService com dados do usuário
- **User Message**: Texto OCR extraído do rótulo

```json
{
  "model": "llama3-70b-8192",
  "messages": [
    {
      "role": "system",
      "content": "SystemPrompt personalizado..."
    },
    {
      "role": "user",
      "content": "Valor Energético 200kcal... Carboidratos 30g..."
    }
  ],
  "temperature": 0.3,
  "max_tokens": 1024,
  "response_format": { "type": "json_object" }
}
```

### 2. Processamento da Resposta

O Groq retorna um JSON estruturado que é desserializado em um `RotuloResponse`:

```json
{
  "produtoDetectado": "Bolacha Recheada",
  "podeConsumir": false,
  "pontuacaoSaude": 3,
  "analiseEmRelacaoAMeta": "ALERTA: Alto teor de sódio...",
  "dicaBSFM": "Experimente substituir por frutas...",
  "calorias": 200,
  "carboidratos": 30,
  "proteinas": 3,
  "gorduras": 8,
  "sodio": 450,
  "acucar": 15
}
```

### 3. Persistência

O resultado é salvo na tabela `AnalisesIA` com os novos campos:
- `PodeConsumir` (boolean)
- `PontuacaoSaude` (int)
- `AnaliseEmRelacaoAMeta` (text)
- `DicaBSFM` (text)

## Configuração

### Variável de Ambiente

```bash
GROQ_API_KEY=sua_chave_groq_aqui
```

### Fallback

Se a `GROQ_API_KEY` não estiver configurada, o serviço retorna uma análise básica sem feedback IA.

## Performance

- **Latência típica**: 200-800ms por requisição
- **Modelo**: Llama 3 70B (otimizado para análise nutricional)
- **Temperatura**: 0.3 (baixa para respostas consistentes)
- **Max tokens**: 1024 (suficiente para análise completa)

## Tratamento de Erros

```csharp
try
{
    var response = await AnalisarRotuloAsync(textoOcr, systemPrompt, ct);
    return Ok(response);
}
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "Erro ao comunicar com Groq API");
    return StatusCode(503, new { erro = "Serviço de IA temporariamente indisponível" });
}
catch (JsonException ex)
{
    _logger.LogError(ex, "Erro ao processar resposta da IA");
    return StatusCode(500, new { erro = "Erro ao processar análise" });
}
```

## Próximas Melhorias

- [ ] Cache de análises para produtos comuns
- [ ] Batch processing para múltiplos rótulos
- [ ] Fine-tuning com dados de nutrição brasileira
- [ ] Suporte a múltiplos modelos (GPT-4, Claude)
