# OCR e Tesseract.js

O **Tesseract.js** é a biblioteca de OCR (Optical Character Recognition) utilizada no BSFM.CoreAnalytics para extrair texto de tabelas nutricionais diretamente no navegador do usuário.

---

## Visão Geral

O Tesseract.js executa o reconhecimento de caracteres em um **Web Worker** separado, garantindo que a interface do usuário não congele durante o processamento.

### Princípio de Privacidade

> **A imagem NUNCA sai do navegador.** Apenas o texto extraído é enviado ao servidor.

## Funcionamento

### 1. Captura da Imagem

O usuário pode:
- **Tirar foto** com a câmera do celular
- **Selecionar arquivo** da galeria

### 2. Pré-processamento

Antes do OCR, a imagem é otimizada:
- Redimensionada para 2000px na maior dimensão
- Convertida para escala de cinza
- Aumento de contraste
- Redução de ruído

### 3. OCR com Tesseract.js

```javascript
// Web Worker - tesseract-worker.js
import Tesseract from 'tesseract.js';

self.onmessage = async (event) => {
    const { imageData, language } = event.data;
    
    const result = await Tesseract.recognize(
        imageData,
        language || 'por',
        {
            logger: (m) => self.postMessage({ type: 'progress', data: m }),
        }
    );
    
    self.postMessage({ 
        type: 'result', 
        data: result.data.text 
    });
};
```

### 4. Pós-processamento

O texto extraído passa por correções:

```javascript
function posProcessarTexto(texto) {
    return texto
        // Correção de caracteres comuns
        .replace(/0/g, 'O')
        .replace(/1/g, 'l')
        .replace(/5/g, 'S')
        // Correção de unidades
        .replace(/kcal/g, 'kcal')
        .replace(/g\b/g, 'g')
        .replace(/mg\b/g, 'mg')
        // Remoção de linhas vazias
        .split('\n')
        .filter(line => line.trim())
        .join('\n');
}
```

## Configuração

### Instalação

```html
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js">
</script>
```

### Parâmetros

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `language` | `por` | Português brasileiro |
| `workerPath` | CDN | Caminho do worker |
| `corePath` | CDN | Caminho do core WASM |
| `logger` | Function | Callback de progresso |

## Performance

- **Tamanho do modelo**: ~4MB (idioma português)
- **Tempo médio**: 2-5 segundos (depende da qualidade da imagem)
- **Precisão**: ~85% em tabelas nutricionais bem iluminadas
- **Cache**: Modelo é cacheado após primeiro download

## Limitações Conhecidas

1. **Qualidade da imagem**: Fotos borradas ou com baixa iluminação reduzem precisão
2. **Fontes decorativas**: Algumas fontes de tabelas nutricionais são difíceis de reconhecer
3. **Layouts complexos**: Tabelas com muitas colunas podem ter extração imperfeita
4. **Idioma**: Modelo português pode ter dificuldade com termos em inglês

## Melhorias Planejadas

- [ ] Treinar Tesseract com fontes de tabelas nutricionais brasileiras
- [ ] Implementar detecção automática de layout de tabela
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Melhorar pré-processamento para fotos com flash
