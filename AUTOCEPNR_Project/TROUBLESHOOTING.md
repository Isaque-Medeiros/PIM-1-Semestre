# Guia de Troubleshooting - Latam Auto-Filler

Guia completo para diagnóstico e resolução de problemas do Latam Auto-Filler.

## 🚨 **Problemas Comuns e Soluções**

### 🔍 **Problemas de Instalação**

#### **EasyOCR não funciona**
```bash
# Erro: "ModuleNotFoundError: No module named 'easyocr'"
# Solução:
pip install easyocr
python -c "import easyocr; print('EasyOCR OK')"
```

**Problema**: Modelos do EasyOCR não baixam automaticamente
```bash
# Solução: Forçar download dos modelos
python -c "
import easyocr
reader = easyocr.Reader(['en', 'pt'])
print('Modelos baixados com sucesso')
"
```

#### **Playwright não instala**
```bash
# Erro: "playwright._impl._api_types.Error: Executable doesn't exist"
# Solução:
python -m playwright install
```

#### **Dependências faltando**
```bash
# Solução completa:
pip install -r requirements.txt
python -m playwright install
```

### 🖼️ **Problemas de OCR**

#### **OCR não detecta texto**
**Causas comuns:**
- Imagem com baixa qualidade (< 800x600)
- Imagem muito escura ou muito clara
- Formato de tela Sabre não reconhecido

**Soluções:**
```bash
# Verifique qualidade da imagem
python -c "
import cv2
img = cv2.imread('sua_imagem.png')
print(f'Resolução: {img.shape[1]}x{img.shape[0]}')
print(f'Brilho médio: {img.mean()}')
"
```

**Teste OCR isoladamente:**
```bash
python -c "
from src.ocr.sabre_ocr import SabreOCR
from src.core.rules_engine import RulesEngine
ocr = SabreOCR(RulesEngine())
ocr.initialize()
# Teste com imagem conhecida
"
```

#### **OCR detecta texto incorreto**
**Causas:**
- Fontes monospace do Sabre mal interpretadas
- Ruído na imagem
- Formato de data/hora incorreto

**Soluções:**
- Aumente a qualidade da captura de tela
- Use imagens em formato PNG (melhor compressão)
- Verifique se a fonte do Sabre está legível

### 🤖 **Problemas de Automação Browser**

#### **Navegador não inicia**
**Causas:**
- Chrome/Edge não instalado
- Playwright não instalado corretamente
- Permissões de firewall

**Soluções:**
```bash
# Verifique navegador
python -c "
import sys
sys.path.append('.')
from src.automation.browser_manager import BrowserManager
from src.core.rules_engine import RulesEngine
browser = BrowserManager(RulesEngine())
import asyncio
asyncio.run(browser.initialize())
print('Navegador OK')
"
```

#### **Formulário Latam não encontrado**
**Causas:**
- URL do formulário incorreto
- Seletores CSS mudaram
- Formulário não carregado

**Soluções:**
1. Verifique se o formulário está aberto no navegador
2. Confira os seletores CSS em `src/core/latam_form.py`
3. Teste manualmente se o formulário carrega

#### **Campos não são preenchidos**
**Causas:**
- Delays muito curtos
- Campos com validação JavaScript
- Problemas de foco no campo

**Soluções:**
- Aumente o delay em `latam_form.py` (linha 102)
- Verifique se os seletores CSS estão corretos
- Teste com campos diferentes

### 🎨 **Problemas de Interface**

#### **UI não aparece**
**Causas:**
- Tkinter não disponível
- Permissões de janela
- Conflito com outros aplicativos

**Soluções:**
```bash
# Teste Tkinter
python -c "import tkinter; print('Tkinter OK')"
```

#### **UI não responde**
**Causas:**
- Loop principal travado
- Erros não tratados
- Conflito de threads

**Soluções:**
- Reinicie o aplicativo
- Verifique logs em `latam_autofiller.log`
- Execute em modo sem UI: `python main.py --no-ui`

### 📋 **Problemas de Regras de Negócio**

#### **Validação de PNR falha**
**Causas:**
- Formato de PNR incorreto
- PNR com caracteres inválidos

**Soluções:**
```bash
# Teste validação de PNR
python -c "
from src.core.rules_engine import RulesEngine
rules = RulesEngine()
result = rules.validate_pnr_format('ABC123')
print(f'PNR válido: {result.is_valid}')
"
```

#### **Validação de classe falha**
**Causas:**
- Classe não elegível para estouro
- Código de autorização inválido

**Soluções:**
- Verifique se a classe é Q, S ou Y
- Confira o código PIC (ex: PIC_S23)

### 🔧 **Problemas de Performance**

#### **Processamento muito lento**
**Causas:**
- Imagens muito grandes
- OCR processando lentamente
- Delays muito longos

**Soluções:**
- Reduza o tamanho das imagens
- Ajuste os delays em `latam_form.py`
- Use imagens em escala de cinza

#### **Consumo de memória alto**
**Causas:**
- Múltiplas instâncias do navegador
- Imagens não liberadas da memória
- EasyOCR mantendo modelos em memória

**Soluções:**
- Feche instâncias do navegador após uso
- Limpe imagens da memória
- Use `gc.collect()` para forçar coleta de lixo

## 📊 **Diagnóstico Avançado**

### **Logs e Depuração**

#### **Níveis de Log**
```python
# Aumente o nível de log para depuração
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Arquivos de Log**
- `latam_autofiller.log` - Logs principais
- `comprehensive_test.log` - Logs de teste
- `test_report.json` - Relatório de testes

#### **Modo Verbose**
```bash
# Execute com mais detalhes
python main.py --verbose
```

### **Testes de Diagnóstico**

#### **Teste de Componentes Individuais**
```bash
# Teste apenas o OCR
python -c "
from src.ocr.image_processor import ImageProcessor
from src.core.rules_engine import RulesEngine
processor = ImageProcessor(RulesEngine())
# Teste com imagem
"

# Teste apenas o navegador
python -c "
from src.automation.browser_manager import BrowserManager
from src.core.rules_engine import RulesEngine
browser = BrowserManager(RulesEngine())
import asyncio
asyncio.run(browser.initialize())
"
```

#### **Teste de Integração**
```bash
# Teste completo
python test_comprehensive.py
```

### **Verificação de Requisitos**

#### **Verifique Dependências**
```bash
python -c "
import sys
modules = ['easyocr', 'cv2', 'numpy', 'playwright', 'tkinter']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        print(f'❌ {module}')
"
```

#### **Verifique Versões**
```bash
python -c "
import easyocr
import cv2
import numpy as np
print(f'EasyOCR: {easyocr.__version__}')
print(f'OpenCV: {cv2.__version__}')
print(f'NumPy: {np.__version__}')
"
```

## 🚨 **Procedimentos de Emergência**

### **Reinstalação Completa**
```bash
# 1. Limpe o ambiente
pip uninstall -y -r requirements.txt
pip cache purge

# 2. Reinstale tudo
pip install -r requirements.txt
python -m playwright install

# 3. Teste novamente
python test_system.py
```

### **Reset de Configuração**
```bash
# Remova arquivos de configuração
rm -rf debug_images/ models/ user_networks/ logs/

# Recrie diretórios
mkdir debug_images models user_networks logs
```

### **Modo Seguro**
```bash
# Execute sem UI e com logs mínimos
python main.py --no-ui --test
```

## 📞 **Suporte Técnico**

### **Informações para Reportar Erros**

Quando reportar um problema, inclua:

1. **Versão do Python**: `python --version`
2. **Versão do Sistema**: Windows 10/11
3. **Logs Completos**: Conteúdo de `latam_autofiller.log`
4. **Passos para Reproduzir**: Sequência exata de ações
5. **Imagem de Teste**: Arquivo que causa o problema
6. **Screenshot do Erro**: Captura da tela com erro

### **Comandos de Diagnóstico**
```bash
# Informações do sistema
python -c "
import platform
import sys
print(f'Python: {sys.version}')
print(f'Plataforma: {platform.platform()}')
print(f'Sistema: {platform.system()} {platform.release()}')
"

# Teste rápido de componentes
python test_system.py
python test_comprehensive.py
```

## 🔒 **Problemas de Segurança**

### **Permissões de Arquivo**
```bash
# Verifique permissões
ls -la AUTOCEPNR_Project/
# No Windows:
# Verifique propriedades do arquivo > Segurança
```

### **Antivirus Interferência**
- Adicione a pasta `AUTOCEPNR_Project` à lista de exclusões
- Desative temporariamente o antivirus para testes
- Verifique logs do antivirus para bloqueios

### **Firewall**
- Permita Python no firewall
- Permita Chrome/Edge no firewall
- Verifique conexões de saída

---

**⚠️ Importante**: Sempre faça backup dos arquivos de configuração antes de realizar alterações.

**💡 Dica**: Mantenha este guia atualizado com novos problemas e soluções encontradas.