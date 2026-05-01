# Context Injector Service

O **ContextInjectorService** é responsável por montar o **SystemPrompt** personalizado que é enviado ao Groq Llama 3 junto com o texto OCR do rótulo. Ele injeta dados biométricos, condições de saúde e histórico alimentar do usuário para gerar análises verdadeiramente personalizadas.

---

## Visão Geral

```csharp
public class ContextInjectorService
{
    public async Task<string> MontarSystemPromptAsync(int usuarioId)
    {
        var usuario = await _db.Usuarios.FindAsync(usuarioId);
        var analisesRecentes = await _db.AnalisesIA
            .Where(a => a.UsuarioId == usuarioId)
            .OrderByDescending(a => a.DataAnalise)
            .Take(5)
            .ToListAsync();
        
        return $@"
Você é um nutricionista IA especializado em análise de rótulos...
        
DADOS DO USUÁRIO:
- Nome: {usuario.Nome}
- Idade: {usuario.Idade} anos
- Peso: {usuario.Peso} kg
- Altura: {usuario.Altura} cm
- IMC: {usuario.Imc:F1}
- TMB: {usuario.Tmb:F0} kcal
- Diabetes: {usuario.Diabetes ?? "Não informado"}
- Intolerância: {usuario.Intolerancia ?? "Não informada"}
- Meta: {usuario.MetaPeso} kg
...
";
    }
}
```

## Dados Injetados

### 1. Dados Biométricos
- **Nome** do usuário
- **Idade** (calculada da data de nascimento)
- **Peso** atual (kg)
- **Altura** (cm)
- **IMC** calculado
- **TMB** (Taxa Metabólica Basal)
- **TDEE** (Gasto Calórico Total)
- **Meta de peso**

### 2. Condições de Saúde
- **Diabetes**: Tipo 1, Tipo 2, Pré-diabetes, Gestacional
- **Intolerâncias**: Lactose, Glúten, etc.

### 3. Histórico Alimentar
- Últimas 5 análises realizadas
- Alimentos consumidos nas últimas 48h
- Padrões alimentares detectados

## Exemplo de SystemPrompt

```
Você é um nutricionista IA especializado em análise de rótulos 
nutricionais de alimentos industrializados.

DADOS DO USUÁRIO:
- Nome: Maria Silva
- Idade: 35 anos
- Peso: 72 kg
- Altura: 165 cm
- IMC: 26.4 (Sobrepeso)
- TMB: 1480 kcal
- Diabetes: Tipo 2
- Intolerância: Lactose
- Meta: 65 kg

REGRAS:
1. Analise APENAS o texto da tabela nutricional fornecido
2. Retorne SEMPRE em formato JSON
3. Se o produto contiver lactose e o usuário for intolerante, 
   marque podeConsumir como false
4. Se o produto tiver alto teor de açúcar e o usuário tiver 
   diabetes, alerte na análise
5. Health Score (0-10): baseado em sódio, açúcar, gorduras 
   saturadas e perfil do usuário
6. Seja direto e educativo na dica BSFM
```

## Benefícios

- ✅ **Análise contextualizada**: Considera condições de saúde reais
- ✅ **Alertas inteligentes**: Produtos com lactose para intolerantes, açúcar para diabéticos
- ✅ **Feedback personalizado**: Dicas baseadas no perfil e metas
- ✅ **Histórico considerado**: Evita recomendações repetitivas

## Tratamento de Dados Ausentes

Se o usuário não informou diabetes ou intolerância, o SystemPrompt usa valores padrão:

```csharp
var diabetes = usuario.Diabetes ?? "Não informado";
var intolerancia = usuario.Intolerancia ?? "Não informada";
```

## Próximas Melhorias

- [ ] Incluir alergias alimentares
- [ ] Considerar restrições calóricas
- [ ] Histórico de compras do usuário
- [ ] Preferências alimentares (vegetariano, vegano)
