# API de Rótulos

A **API de Rótulos** é o endpoint RESTful que recebe o texto OCR extraído do navegador e retorna a análise nutricional completa processada pelo Groq Llama 3.

---

## Endpoint

### POST /api/rotulo/analisar

Analisa o texto OCR de um rótulo nutricional e retorna feedback personalizado.

#### Request

```json
{
  "usuarioId": 1,
  "textoOcr": "Valor Energético 200kcal... Carboidratos 30g... Proteínas 5g... Gorduras Totais 8g... Gorduras Saturadas 3g... Gorduras Trans 0g... Fibra Alimentar 2g... Sódio 400mg... Açúcares 15g..."
}
```

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `usuarioId` | int | Sim | ID do usuário no sistema |
| `textoOcr` | string | Sim | Texto extraído via OCR |

#### Response (Sucesso - 200)

```json
{
  "sucesso": true,
  "analise": {
    "produtoDetectado": "Bolacha Recheada",
    "podeConsumir": false,
    "pontuacaoSaude": 3,
    "analiseEmRelacaoAMeta": "ALERTA: Alto teor de sódio (400mg) e açúcares (15g). Para seu perfil com diabetes Tipo 2, este produto não é recomendado.",
    "dicaBSFM": "Experimente substituir por frutas frescas ou iogurte natural. Mais nutritivo e sem açúcares adicionados!",
    "calorias": 200,
    "carboidratos": 30,
    "proteinas": 5,
    "gorduras": 8,
    "gordurasSaturadas": 3,
    "gordurasTrans": 0,
    "fibras": 2,
    "sodio": 400,
    "acucar": 15
  }
}
```

#### Response (Erro - 400)

```json
{
  "sucesso": false,
  "erro": "Texto OCR não pode estar vazio"
}
```

#### Response (Erro - 503)

```json
{
  "sucesso": false,
  "erro": "Serviço de IA temporariamente indisponível"
}
```

## Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class RotuloController : ControllerBase
{
    private readonly NutriBrainService _nutriBrain;
    private readonly ContextInjectorService _contextInjector;
    
    [HttpPost("analisar")]
    public async Task<IActionResult> AnalisarRotulo(
        [FromBody] RotuloRequest request,
        CancellationToken ct)
    {
        if (string.IsNullOrWhiteSpace(request.TextoOcr))
            return BadRequest(new { sucesso = false, erro = "Texto OCR não pode estar vazio" });
        
        var systemPrompt = await _contextInjector
            .MontarSystemPromptAsync(request.UsuarioId);
        
        var analise = await _nutriBrain
            .AnalisarRotuloAsync(request.TextoOcr, systemPrompt, ct);
        
        return Ok(new { sucesso = true, analise });
    }
}
```

## Modelos

### RotuloRequest

```csharp
public class RotuloRequest
{
    public int UsuarioId { get; set; }
    public string TextoOcr { get; set; }
}
```

### RotuloResponse

```csharp
public class RotuloResponse
{
    public string ProdutoDetectado { get; set; }
    public bool PodeConsumir { get; set; }
    public int PontuacaoSaude { get; set; }
    public string AnaliseEmRelacaoAMeta { get; set; }
    public string DicaBSFM { get; set; }
    public double Calorias { get; set; }
    public double Carboidratos { get; set; }
    public double Proteinas { get; set; }
    public double Gorduras { get; set; }
    public double GordurasSaturadas { get; set; }
    public double GordurasTrans { get; set; }
    public double Fibras { get; set; }
    public double Sodio { get; set; }
    public double Acucar { get; set; }
}
```

## Exemplo de Uso (Frontend)

```javascript
async function analisarRotulo(textoOcr, usuarioId) {
    const response = await fetch('/api/rotulo/analisar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            usuarioId: usuarioId,
            textoOcr: textoOcr
        })
    });
    
    const data = await response.json();
    
    if (data.sucesso) {
        exibirResultado(data.analise);
    } else {
        exibirErro(data.erro);
    }
}
```

## Rate Limiting

- **Máximo**: 10 requisições por minuto por usuário
- **Cooldown**: 6 segundos entre requisições

## Tratamento de Erros

| Código | Significado | Ação |
|--------|-------------|------|
| 200 | Sucesso | Processar resposta |
| 400 | Bad Request | Verificar payload |
| 503 | Service Unavailable | Tentar novamente em 30s |
| 429 | Too Many Requests | Aguardar rate limit |

## Próximas Melhorias

- [ ] Suporte a batch (múltiplos rótulos)
- [ ] Cache de análises para produtos comuns
- [ ] Webhook para notificações de análise completa
- [ ] Histórico de análises por produto
