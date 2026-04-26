---
title: PIM - 1º Semestre
description: Projeto acadêmico de desenvolvimento web com foco em estruturação semântica, layout responsivo e usabilidade
---

# PIM - 1º Semestre

<div class="project-card">

## :material-information: Visão Geral

**PIM (Projeto Integrado Multidisciplinar)** desenvolvido durante o primeiro semestre do curso de Análise e Desenvolvimento de Sistemas. O projeto consolida fundamentos de desenvolvimento front-end com foco em organização de conteúdo, estruturação semântica e experiência do usuário.

### :material-check-circle: Status do Projeto
- **Status:** :material-check-circle:{ style="color: #10b981" } Publicado e ativo
- **Última atualização:** 2025
- **Disponibilidade:** [Acessar projeto](https://isaque-medeiros.github.io/PIM-1-Semestre/)
- **Repositório:** [GitHub](https://github.com/Isaque-Medeiros/PIM-1-Semestre)

### :material-tag: Tags
<span class="badge">Acadêmico</span>
<span class="badge">Front-end</span>
<span class="badge">HTML/CSS</span>
<span class="badge">JavaScript</span>
<span class="badge">Responsivo</span>

</div>

---

## :material-cog: Stack Tecnológico

| Tecnologia | Versão | Propósito |
| :--- | :--- | :--- |
| **HTML5** | Semântico | Estruturação do conteúdo |
| **CSS3** | Moderno | Estilização e layout |
| **JavaScript** | Vanilla | Interatividade básica |
| **Git/GitHub** | Controle de versão | Versionamento e deploy |

## :material-feature-search: Funcionalidades

### 1. Estrutura Semântica
- Uso correto de tags HTML5 (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- Hierarquia de títulos adequada (`<h1>` a `<h6>`)
- Atributos ARIA para acessibilidade básica

### 2. Layout Responsivo
- Design mobile-first
- Media queries para diferentes breakpoints
- Flexbox para organização de elementos
- Grid para layouts complexos

### 3. Navegação Intuitiva
- Menu de navegação principal
- Links internos com scroll suave
- Breadcrumbs para orientação do usuário
- Footer com informações de contato

### 4. Conteúdo Organizado
- Seções bem definidas (Home, Sobre, Serviços, Contato)
- Cards para apresentação de informações
- Formulários de contato funcionais
- Galeria de imagens responsiva

## :material-folder: Estrutura do Projeto

```
PIM-1-Semestre/
├── index.html          # Página principal
├── sobre.html          # Página "Sobre"
├── servicos.html       # Página "Serviços"
├── contato.html        # Página "Contato"
├── css/
│   ├── style.css       # Estilos principais
│   ├── responsive.css  # Estilos responsivos
│   └── reset.css       # Reset CSS
├── js/
│   └── main.js         # JavaScript principal
├── images/             # Imagens e assets
└── README.md           # Documentação
```

## :material-chart-line: Objetivos de Aprendizado

### Técnicos
1. **HTML Semântico:** Prática de estruturação correta de páginas web
2. **CSS Moderno:** Uso de Flexbox, Grid e media queries
3. **JavaScript Básico:** Manipulação do DOM e eventos
4. **Responsive Design:** Adaptação para diferentes dispositivos
5. **Versionamento:** Controle com Git e deploy no GitHub Pages

### Profissionais
1. **Organização de Projeto:** Estruturação de pastas e arquivos
2. **Documentação:** README claro e comentários no código
3. **Deploy:** Publicação em ambiente de produção
4. **Manutenção:** Código limpo e fácil de manter

## :material-eye: Visualização

### Screenshots
<div class="grid" markdown>

- **Desktop**
    
    ![Desktop View](https://via.placeholder.com/800x450/0f172a/87ceeb?text=Desktop+View+PIM)

- **Mobile**
    
    ![Mobile View](https://via.placeholder.com/400x700/0f172a/87ceeb?text=Mobile+View+PIM)

</div>

### Link para Visualização
[:material-eye: Acessar Projeto Publicado](https://isaque-medeiros.github.io/PIM-1-Semestre/){ .md-button .md-button--primary }

## :material-code-braces: Trechos de Código

### HTML Semântico
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PIM - Projeto Integrado Multidisciplinar</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header class="site-header" role="banner">
        <nav class="navbar" aria-label="Navegação principal">
            <!-- Menu de navegação -->
        </nav>
    </header>
    
    <main class="main-content" id="conteudo-principal">
        <section class="hero" aria-labelledby="hero-title">
            <h1 id="hero-title">Bem-vindo ao PIM 1º Semestre</h1>
            <!-- Conteúdo hero -->
        </section>
        
        <section class="features" aria-labelledby="features-title">
            <!-- Seção de funcionalidades -->
        </section>
    </main>
    
    <footer class="site-footer" role="contentinfo">
        <!-- Rodapé com informações -->
    </footer>
    
    <script src="js/main.js"></script>
</body>
</html>
```

### CSS Responsivo
```css
/* Mobile First Approach */
.container {
    width: 100%;
    padding: 0 1rem;
    margin: 0 auto;
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
        padding: 0 2rem;
    }
    
    .grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
    }
    
    .grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

## :material-book: Lições Aprendidas

### Acertos
1. **Estruturação semântica** correta facilitou a manutenção
2. **Abordagem mobile-first** garantiu boa experiência em todos os dispositivos
3. **Organização do CSS** com metodologia BEM (Block Element Modifier)
4. **Deploy automatizado** com GitHub Pages

### Desafios Superados
1. **Compatibilidade entre navegadores** - Uso de prefixos e fallbacks
2. **Performance em mobile** - Otimização de imagens e lazy loading
3. **Acessibilidade** - Implementação de atributos ARIA e contrastes adequados
4. **Versionamento** - Aprendizado do fluxo Git (branch, commit, push, pull request)

## :material-arrow-right: Próximos Passos (Melhorias Futuras)

### Planejadas
1. **Refatoração para componentes** - Modularização do CSS
2. **Implementação de SASS/SCSS** - Para variáveis e mixins
3. **Adição de animações CSS** - Transições e keyframes
4. **Otimização de performance** - Minificação e bundling
5. **Testes de acessibilidade** - Ferramentas como Lighthouse

### Em Consideração
1. **Migração para React/Vue** - Componentização avançada
2. **Backend simples** - API para formulário de contato
3. **CMS headless** - Para gerenciamento de conteúdo
4. **PWA features** - Instalação como app e offline capability

## :material-download: Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/Isaque-Medeiros/PIM-1-Semestre.git

# Acesse a pasta do projeto
cd PIM-1-Semestre

# Abra no navegador (ou use um servidor local)
# Para Python:
python -m http.server 8000

# Para Node.js:
npx serve .
```

## :material-share: Contribuições

Este projeto é aberto para contribuições educacionais. Se você é estudante ou iniciante em desenvolvimento web:

1. **Fork o repositório**
2. **Crie uma branch** (`git checkout -b feature/nova-funcionalidade`)
3. **Commit suas mudanças** (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push para a branch** (`git push origin feature/nova-funcionalidade`)
5. **Abra um Pull Request**

## :material-help-circle: Suporte e Dúvidas

- **Issues do GitHub:** [Reportar problemas](https://github.com/Isaque-Medeiros/PIM-1-Semestre/issues)
- **Email:** medeiroisaque765@gmail.com
- **LinkedIn:** [Isaque Medeiros](https://www.linkedin.com/in/isaque-medeiros-a99421268/)

---

:material-lightbulb: **Para estudantes:** Este projeto serve como referência para trabalhos acadêmicos similares. Sinta-se à vontade para usar como base, mas sempre cite a fonte original.

*Projeto desenvolvido como parte da formação em Análise e Desenvolvimento de Sistemas - 2024*