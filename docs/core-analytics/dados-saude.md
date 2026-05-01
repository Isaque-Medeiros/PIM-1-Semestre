# Dados de Saúde do Usuário

O módulo de **Dados de Saúde** permite que os usuários informem condições médicas relevantes para a análise nutricional, como diabetes e intolerâncias alimentares. Esses dados são utilizados pelo **ContextInjectorService** para personalizar o feedback da IA.

---

## Funcionalidades

### Cadastro de Condições

O usuário pode informar no **Perfil** > **Dados de Saúde**:

#### Diabetes
| Tipo | Descrição |
|------|-----------|
| Tipo 1 | Diabetes autoimune, dependente de insulina |
| Tipo 2 | Resistência à insulina, mais comum em adultos |
| Pré-diabetes | Glicemia alterada, risco de desenvolver diabetes |
| Gestacional | Diabetes durante a gravidez |
| Não | Sem diabetes |

#### Intolerâncias Alimentares
| Tipo | Descrição |
|------|-----------|
| Lactose | Dificuldade de digerir lactose (açúcar do leite) |
| Glúten | Intolerância ao glúten (doença celíaca) |
| Ambas | Intolerância a lactose e glúten |
| Nenhuma | Sem intolerâncias conhecidas |

### API Endpoints

#### GET /api/saude/{id}
Retorna dados de saúde do usuário.

**Response:**
```json
{
  "usuarioId": 1,
  "diabetes": "Tipo 2",
  "intolerancia": "Lactose"
}
```

#### PUT /api/saude/atualizar
Atualiza dados de saúde do usuário.

**Request:**
```json
{
  "usuarioId": 1,
  "diabetes": "Tipo 2",
  "intolerancia": "Lactose"
}
```

## Impacto nas Análises

### Exemplo 1: Usuário com Diabetes Tipo 2

Ao escanear um refrigerante:
- **Health Score**: 1 (reduzido por alto teor de açúcar + diabetes)
- **podeConsumir**: false
- **Feedback**: "ALERTA: Alto teor de açúcar. Para seu perfil com diabetes Tipo 2, evite completamente."

### Exemplo 2: Usuário com Intolerância à Lactose

Ao escanear um leite integral:
- **Health Score**: 3 (reduzido por intolerância)
- **podeConsumir**: false
- **Feedback**: "Este produto contém lactose. Para seu perfil de intolerância, recomendamos versão zero lactose."

### Exemplo 3: Usuário sem Condições

Ao escanear o mesmo leite integral:
- **Health Score**: 7
- **podeConsumir**: true
- **Feedback**: "Boa fonte de cálcio e proteínas. Consuma com moderação."

## Modelo de Dados

```csharp
public class Usuario
{
    public int Id { get; set; }
    public string Nome { get; set; }
    public string Email { get; set; }
    // ... outros campos
    
    // Campos de saúde (adicionados via migração automática)
    public string? Diabetes { get; set; }
    public string? Intolerancia { get; set; }
}
```

## Migração Automática

Os campos de saúde são adicionados automaticamente via migração no startup:

```csharp
// Program.cs - Migração automática
await using var context = new PonteDB();
await context.Database.EnsureCreatedAsync();

// Adiciona colunas se não existirem
await context.Database.ExecuteSqlRawAsync(@"
    DO $$ 
    BEGIN
        BEGIN
            ALTER TABLE ""Usuarios"" ADD COLUMN ""Diabetes"" VARCHAR(50);
        EXCEPTION WHEN duplicate_column THEN NULL;
        END;
        BEGIN
            ALTER TABLE ""Usuarios"" ADD COLUMN ""Intolerancia"" TEXT;
        EXCEPTION WHEN duplicate_column THEN NULL;
        END;
    END $$;
");
```

## Privacidade

- Os dados de saúde são armazenados apenas no banco de dados do BSFM
- Utilizados exclusivamente para personalizar o feedback nutricional
- O usuário pode atualizar ou remover esses dados a qualquer momento
- Por ser um protótipo acadêmico, recomenda-se não usar dados reais sensíveis

## Próximas Melhorias

- [ ] Adicionar alergias alimentares (amendoim, frutos do mar, etc.)
- [ ] Suporte a múltiplas condições simultâneas
- [ ] Histórico de alterações nos dados de saúde
- [ ] Recomendações de profissionais especializados
