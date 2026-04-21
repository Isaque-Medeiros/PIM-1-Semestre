---
title: Portfolio Landing Page
description: Página inicial do meu portfólio pessoal com projetos acadêmicos e profissionais
---

# Portfolio Landing Page

## Visão Geral

Esta é a página inicial do meu portfólio pessoal, desenvolvida para demonstrar minhas habilidades em desenvolvimento web, programação e projetos acadêmicos.

## Características Principais

- **Design Responsivo**: Layout adaptável para desktop, tablet e mobile
- **Navegação Intuitiva**: Menu de fácil acesso a todas as seções
- **Projetos em Destaque**: Exibição dos principais trabalhos acadêmicos
- **Tecnologias Modernas**: Utilização de HTML5, CSS3 e JavaScript

## Tecnologias Utilizadas

- **HTML5**: Estrutura semântica moderna
- **CSS3**: Estilização avançada com Flexbox e Grid
- **JavaScript**: Interatividade e funcionalidades dinâmicas
- **Fontes Personalizadas**: Tipografia ARCADE para elementos específicos

## Estrutura do Projeto

```bash
Meus-ProjetosAcad/
├── css/
│   ├── style.css          # Estilos principais
│   ├── port.css           # Estilos do portfólio
│   └── variables.css      # Variáveis CSS
├── images/                # Assets visuais
├── functions/
│   └── main.js            # JavaScript principal
└── index.html             # Página principal
```

## Funcionalidades Implementadas

### Seção de Hero
- Apresentação pessoal com nome e título
- Background visual atraente
- Call-to-action para navegação

### Grid de Projetos
- Exibição em cards dos projetos principais
- Filtros por categoria (Frontend, Backend, Cloud, Embedded)
- Links para repositórios e demonstrações

### Navegação por Categorias
- **Frontend**: HTML, CSS, JavaScript, React
- **Backend**: Python, Node.js, APIs
- **Cloud**: AWS, Azure, Deployments
- **Embedded**: Arduino, Tinkercad, Circuitos
- **Academic**: Trabalhos universitários

## Design e UX

### Paleta de Cores
- Cores principais: Azul escuro (#1a1a2e) e Laranja (#ff7b00)
- Tons de cinza para backgrounds
- Cores de destaque para elementos interativos

### Tipografia
- **ARCADE_I**, **ARCADE_N**, **ARCADE_R**: Fontes personalizadas para títulos
- Fontes padrão do sistema para conteúdo
- Hierarquia visual clara com diferentes pesos

## Código Exemplo

### HTML Principal
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Portfólio - Isaque</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/port.css">
</head>
<body>
    <header class="hero">
        <h1>Isaque - Desenvolvedor & Estudante</h1>
        <p>Transformando ideias em código</p>
    </header>
    
    <main class="projects-grid">
        <!-- Grid de projetos -->
    </main>
</body>
</html>
```

### CSS Responsivo
```css
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white;
    text-align: center;
    padding: 4rem 2rem;
}

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 2rem;
}

@media (max-width: 768px) {
    .projects-grid {
        grid-template-columns: 1fr;
        padding: 1rem;
    }
}
```

## Próximas Melhorias

- [ ] Adicionar modo escuro/claro
- [ ] Implementar animações CSS
- [ ] Adicionar filtros avançados
- [ ] Integrar com APIs de redes sociais
- [ ] Otimizar performance e SEO

## Links Relacionados

- [Repositório GitHub](https://github.com/isaque)
- [LinkedIn Profissional]
- [Projetos Academicos](./academic-projects.md)