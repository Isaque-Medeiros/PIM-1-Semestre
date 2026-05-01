# Health Score

O **Health Score** é uma pontuação de 0 a 10 atribuída pela IA a cada alimento analisado, baseada em regras restritivas que consideram a composição nutricional do produto e o perfil de saúde do usuário.

---

## Como Funciona

### Pontuação Base

| Faixa | Classificação | Significado |
|-------|---------------|-------------|
| 8-10 | ✅ Excelente | Produto saudável, pode consumir livremente |
| 5-7 | ⚠️ Moderado | Consumir com moderação |
| 0-4 | ❌ Ruim | Evitar consumo |

### Regras de Pontuação

A IA avalia os seguintes critérios:

| Critério | Impacto | Descrição |
|----------|---------|-----------|
| **Sódio** | Alto | > 400mg por porção reduz pontuação |
| **Açúcar** | Alto | > 15g por porção reduz pontuação |
| **Gorduras Saturadas** | Alto | > 5g por porção reduz pontuação |
| **Gorduras Trans** | Crítico | Qualquer quantidade reduz drasticamente |
| **Fibras** | Positivo | > 3g por porção aumenta pontuação |
| **Proteínas** | Positivo | > 10g por porção aumenta pontuação |

### Regras Especiais por Perfil

#### Diabetes
- **Açúcar > 5g**: Alerta amarelo
- **Açúcar > 15g**: Alerta vermelho, `podeConsumir = false`
- **Açúcar > 30g**: Health Score máximo 3

#### Intolerância à Lactose
- **Produto lácteo**: `podeConsumir = false`
- **Queijos maturados**: Alerta moderado (baixa lactose)

#### Hipertensão (futuro)
- **Sódio > 600mg**: `podeConsumir = false`

## Exemplos

### Produto Saudável
```json
{
  "produtoDetectado": "Iogurte Natural Desnatado",
  "podeConsumir": true,
  "pontuacaoSaude": 8,
  "analiseEmRelacaoAMeta": "Ótima escolha! Baixo teor de gordura e rico em proteínas.",
  "dicaBSFM": "Combine com frutas frescas para um café da manhã completo."
}
```

### Produto Não Recomendado
```json
{
  "produtoDetectado": "Refrigerante",
  "podeConsumir": false,
  "pontuacaoSaude": 1,
  "analiseEmRelacaoAMeta": "ALERTA: Alto teor de açúcar (39g por lata). Para seu perfil com diabetes Tipo 2, evite completamente.",
  "dicaBSFM": "Experimente água com gás e limão - zero calorias e refrescante!"
}
```

## Implementação

A lógica do Health Score é implementada no **SystemPrompt** do Groq Llama 3:

```
REGRAS DE PONTUAÇÃO (Health Score 0-10):
- Base: 7 pontos
- Sódio > 400mg: -2 pontos
- Açúcar > 15g: -2 pontos
- Gorduras saturadas > 5g: -2 pontos
- Gorduras trans > 0g: -3 pontos
- Fibras > 3g: +1 ponto
- Proteínas > 10g: +1 ponto
- Se usuário tem diabetes e açúcar > 15g: -3 pontos adicionais
- Se usuário tem intolerância a lactose e produto é lácteo: -5 pontos
```

## Próximas Melhorias

- [ ] Adicionar perfil de hipertensão
- [ ] Considerar colesterol na pontuação
- [ ] Adicionar vitaminas e minerais como bônus
- [ ] Histórico de Health Score do usuário
- [ ] Metas personalizadas de melhoria
