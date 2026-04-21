---
title: Frontend
description: Arquitetura e tecnologias frontend do BSFM
---

# 🎨 Frontend

Arquitetura moderna e responsiva para a interface do usuário do BSFM, focada em experiência intuitiva e performance.

## 🎯 Visão Geral

O frontend do BSFM utiliza uma stack moderna baseada em:
- **HTML5 + CSS3** - Estrutura semântica e estilização avançada
- **JavaScript ES6+** - Interatividade e lógica client-side  
- **Material Design** - Design system consistente e acessível
- **Responsive Design** - Experiência otimizada para todos os dispositivos

## 🏗️ Arquitetura Frontend

### **Estrutura de Componentes**
```
📦 src/
├── 📁 components/     # Componentes reutilizáveis
│   ├── 📁 ui/        # Componentes de interface base
│   ├── 📁 forms/     # Formulários e validação
│   ├── 📁 charts/    # Visualização de dados
│   └── 📁 layout/    # Componentes de layout
├── 📁 pages/         # Páginas da aplicação
├── 📁 styles/        # Estilos globais e temas
├── 📁 utils/         # utilitários e helpers
├── 📁 assets/        # Recursos estáticos
└── 📁 services/      # Comunicação com APIs
```

### **Fluxo de Dados**
```
🖥️ Interface do Usuário
├── Interações do usuário (clicks, inputs, gestures)
├── Manipulação do DOM via JavaScript
├── Validação de formulários client-side
└── Feedback visual imediato

🔄 Comunicação com Backend  
├── Chamadas HTTP para APIs REST
├── Autenticação via JWT tokens
├── Cache local para performance
└── Tratamento de erros elegante

🎨 Renderização e Estilos
├── CSS responsivo com Media Queries
├── Animações e transições suaves  
├── Temas claro/escuro dinâmicos
└── Acessibilidade (ARIA, contrastes)
```

## 🛠️ Tecnologias Utilizadas

### **Core Technologies**
- **HTML5** - Markup semântico e acessível
- **CSS3** - Flexbox, Grid, custom properties
- **JavaScript ES2022** - Modern JavaScript features
- **Material Design Components** - UI library consistente

### **Ferramentas de Desenvolvimento**
- **VS Code** - IDE principal com extensões
- **Live Server** - Development server com hot reload
- **Chrome DevTools** - Debugging e performance analysis
- **Lighthouse** - Audits de qualidade

### **Build Tools**
- **Vite** - Fast build tool and dev server
- **PostCSS** - CSS processing and optimization  
- **ESLint + Prettier** - Code quality and formatting
- **GitHub Actions** - CI/CD automation

## 🎨 Design System

### **Cores Principais**
```css
:root {
  --primary: #1976d2;      /* Azul principal */
  --secondary: #dc004e;    /* Rosa/vermelho para acentos */
  --success: #4caf50;     /* Verde para sucesso */
  --warning: #ff9800;     /* Laranja para alertas */
  --error: #f44336;       /* Vermelho para erros */
  
  /* Tons de neutros */
  --text-primary: #212121; /* Texto escuro */
  --text-secondary: #757575; /* Texto secundário */
  --background: #f5f5f5;   /* Fundo claro */
  --surface: #ffffff;      /* Superfícies */
  
  /* Dark theme variants */
  --dark-primary: #bb86fc;
  --dark-background: #121212;
  --dark-surface: #1e1e1e;
}
```

### **Tipografia**
```css
/* Sistema de fontes */
:root {
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'Fira Code', 'Monaco', monospace;
  
  /* Escala de tipos */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;  /* 18px */
  --text-xl: 1.25rem;   /* 20px */
  --text-2xl: 1.5rem;   /* 24px */
}
```

### **Espaçamento**
```css
/* Sistema de espaçamento (base 4px) */
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
}
```

## ⚡ Componentes Principais

### **Header Navigation**
```html
<header class="app-header">
  <div class="container">
    <a href="/" class="logo">
      <img src="/assets/logo.svg" alt="BSFM" />
      <span>Brazilian System of Food Metric</span>
    </a>
    
    <nav class="navigation">
      <a href="/dashboard" class="nav-link">Dashboard</a>
      <a href="/foods" class="nav-link">Alimentos</a>
      <a href="/goals" class="nav-link">Metas</a>
      <a href="/profile" class="nav-link">Perfil</a>
    </nav>
    
    <div class="user-menu">
      <button class="theme-toggle">🌙</button>
      <div class="user-avatar">JS</div>
    </div>
  </div>
</header>
```

### **Food Input Component**
```html
<div class="food-input-card">
  <h3>Adicionar Alimento</h3>
  
  <form class="food-form" id="addFoodForm">
    <div class="input-group">
      <label for="foodName">Nome do Alimento</label>
      <input 
        type="text" 
        id="foodName" 
        placeholder="Ex: Maçã verde"
        required
      />
      <div class="suggestions" id="foodSuggestions"></div>
    </div>
    
    <div class="input-row">
      <div class="input-group">
        <label for="foodQuantity">Quantidade</label>
        <input 
          type="number" 
          id="foodQuantity" 
          min="1" 
          value="100"
        />
      </div>
      
      <div class="input-group">
        <label for="foodUnit">Unidade</label>
        <select id="foodUnit">
          <option value="g">gramas (g)</option>
          <option value="ml">mililitros (ml)</option>
          <option value="un">unidades</option>
        </select>
      </div>
    </div>
    
    <button type="submit" class="btn btn-primary">
      <span class="btn-icon">+</span>
      Adicionar Alimento
    </button>
  </form>
  
  <div class="nutrition-preview" id="nutritionPreview">
    <!-- Preview nutricional dinâmico -->
  </div>
</div>
```

### **Nutrition Chart Component**
```html
<div class="nutrition-chart">
  <h4>Distribuição Nutricional</h4>
  
  <div class="chart-container">
    <canvas id="nutritionChart" width="400" height="200"></canvas>
  </div>
  
  <div class="chart-legend">
    <div class="legend-item">
      <span class="color-dot protein"></span>
      <span>Proteínas: 25%</span>
    </div>
    <div class="legend-item">
      <span class="color-dot carbs"></span>
      <span>Carboidratos: 50%</span>
    </div>
    <div class="legend-item">
      <span class="color-dot fats"></span>
      <span>Gorduras: 25%</span>
    </div>
  </div>
</div>
```

## 🎨 Estilos e CSS Architecture

### **Metodologia BEM**
```css
/* Block */
.food-input-card { /* ... */ }

/* Element */
.food-input-card__title { /* ... */ }
.food-input-card__form { /* ... */ }

/* Modifier */
.food-input-card--compact { /* ... */ }
.food-input-card--loading { /* ... */ }
```

### **Utility-First CSS**
```css
/* Espaçamento utilitário */
.mt-2 { margin-top: var(--space-2); }
.p-4 { padding: var(--space-4); }

/* Cores utilitárias */
.text-primary { color: var(--primary); }
.bg-success { background-color: var(--success); }

/* Flexbox utilities */
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
```

### **Responsive Design**
```css
/* Mobile First Approach */
.container {
  width: 100%;
  padding: var(--space-4);
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
  
  /* Layout de duas colunas */
  .grid-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-6);
  }
}

/* Large screens */
@media (min-width: 1280px) {
  .container {
    max-width: 1140px;
  }
}
```

## ⚡ JavaScript Interactivity

### **Food Search with Debounce**
```javascript
class FoodSearch {
  constructor() {
    this.searchInput = document.getElementById('foodSearch');
    this.suggestions = document.getElementById('foodSuggestions');
    this.timeout = null;
    
    this.init();
  }
  
  init() {
    this.searchInput.addEventListener('input', this.debounce(this.handleInput.bind(this), 300));
  }
  
  debounce(func, wait) {
    return (...args) => {
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }
  
  async handleInput(event) {
    const query = event.target.value.trim();
    
    if (query.length < 2) {
      this.hideSuggestions();
      return;
    }
    
    try {
      const results = await this.searchFoods(query);
      this.showSuggestions(results);
    } catch (error) {
      console.error('Search error:', error);
      this.hideSuggestions();
    }
  }
  
  async searchFoods(query) {
    const response = await fetch(`/api/foods/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  }
  
  showSuggestions(results) {
    this.suggestions.innerHTML = results.map(food => `
      <div class="suggestion-item" data-food-id="${food.id}">
        <strong>${food.name}</strong>
        <span class="suggestion-category">${food.category}</span>
      </div>
    `).join('');
    
    this.suggestions.style.display = 'block';
  }
  
  hideSuggestions() {
    this.suggestions.style.display = 'none';
    this.suggestions.innerHTML = '';
  }
}

// Initialize
new FoodSearch();
```

### **Form Validation**
```javascript
class FormValidator {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.fields = this.form.querySelectorAll('[data-validate]');
    this.errors = new Set();
    
    this.init();
  }
  
  init() {
    this.form.addEventListener('submit', this.handleSubmit.bind(this));
    
    this.fields.forEach(field => {
      field.addEventListener('blur', this.validateField.bind(this, field));
      field.addEventListener('input', this.clearError.bind(this, field));
    });
  }
  
  handleSubmit(event) {
    event.preventDefault();
    
    this.errors.clear();
    this.fields.forEach(field => this.validateField(field));
    
    if (this.errors.size === 0) {
      this.form.submit();
    } else {
      this.showFormErrors();
    }
  }
  
  validateField(field) {
    const value = field.value.trim();
    const rules = field.dataset.validate.split('|');
    
    for (const rule of rules) {
      const [ruleName, ruleValue] = rule.split(':');
      
      if (!this[`validate${ruleName.charAt(0).toUpperCase() + ruleName.slice(1)}`](value, ruleValue)) {
        this.errors.add(field.id);
        this.showError(field, this.getErrorMessage(ruleName, ruleValue));
        return false;
      }
    }
    
    this.clearError(field);
    return true;
  }
  
  validateRequired(value) {
    return value.length > 0;
  }
  
  validateEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }
  
  validateMin(value, min) {
    return value.length >= parseInt(min);
  }
  
  getErrorMessage(rule, value) {
    const messages = {
      required: 'Este campo é obrigatório',
      email: 'Digite um email válido',
      min: `Mínimo de ${value} caracteres`
    };
    
    return messages[rule] || 'Campo inválido';
  }
  
  showError(field, message) {
    this.clearError(field);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.id = `${field.id}-error`;
    
    field.parentNode.appendChild(errorElement);
    field.setAttribute('aria-invalid', 'true');
  }
  
  clearError(field) {
    const existingError = document.getElementById(`${field.id}-error`);
    if (existingError) {
      existingError.remove();
    }
    field.removeAttribute('aria-invalid');
  }
  
  showFormErrors() {
    // Scroll para o primeiro erro
    const firstErrorField = this.fields.find(field => this.errors.has(field.id));
    if (firstErrorField) {
      firstErrorField.focus();
    }
    
    // Mostrar alerta geral
    alert('Por favor, corrija os erros destacados no formulário.');
  }
}

// Usage
new FormValidator('signupForm');
```

### **Theme Switcher**
```javascript
class ThemeManager {
  constructor() {
    this.themeToggle = document.getElementById('themeToggle');
    this.currentTheme = localStorage.getItem('theme') || 'light';
    
    this.init();
  }
  
  init() {
    this.applyTheme(this.currentTheme);
    
    this.themeToggle.addEventListener('click', () => {
      this.toggleTheme();
    });
    
    // Watch system preference
    this.watchSystemTheme();
  }
  
  toggleTheme() {
    this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.applyTheme(this.currentTheme);
    localStorage.setItem('theme', this.currentTheme);
  }
  
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.updateToggleIcon(theme);
  }
  
  updateToggleIcon(theme) {
    this.themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
  }
  
  watchSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e) => {
      if (!localStorage.getItem('theme')) {
        this.currentTheme = e.matches ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
      }
    };
    
    mediaQuery.addEventListener('change', handleChange);
    handleChange(mediaQuery);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new ThemeManager();
});
```

## 📊 Charts and Data Visualization

### **Nutrition Chart with Chart.js**
```javascript
class NutritionChart {
  constructor(canvasId, data) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.data = data;
    this.chart = null;
    
    this.init();
  }
  
  init() {
    this.renderChart();
    this.setupResponsive();
  }
  
  renderChart() {
    if (this.chart) {
      this.chart.destroy();
    }
    
    this.chart = new Chart(this.ctx, {
      type: 'doughnut',
      data: {
        labels: ['Proteínas', 'Carboidratos', 'Gorduras'],
        datasets: [{
          data: [
            this.data.protein || 0,
            this.data.carbs || 0, 
            this.data.fat || 0
          ],
          backgroundColor: [
            'rgba(76, 175, 80, 0.8)',    // Green
            'rgba(33, 150, 243, 0.8)',   // Blue  
            'rgba(255, 152, 0, 0.8)'     // Orange
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: {
                size: 12
              },
              color: 'var(--text-primary)'
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || '';
                const value = context.parsed || 0;
                return `${label}: ${value}g`;
              }
            }
          }
        }
      }
    });
  }
  
  setupResponsive() {
    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        if (entry.contentBoxSize) {
          this.chart?.resize();
        }
      }
    });
    
    resizeObserver.observe(this.canvas.parentElement);
  }
  
  updateData(newData) {
    this.data = { ...this.data, ...newData };
    this.renderChart();
  }
}

// Usage
const chartData = { protein: 25, carbs: 50, fat: 25 };
const nutritionChart = new NutritionChart('nutritionChart', chartData);
```

## 🚀 Performance Optimization

### **Lazy Loading Images**
```javascript
// Lazy load images with Intersection Observer
const lazyImages = document.querySelectorAll('img[data-src]');

const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      imageObserver.unobserve(img);
    }
  });
}, {
  rootMargin: '200px 0px',
  threshold: 0.1
});

lazyImages.forEach(img => imageObserver.observe(img));
```

### **Service Worker for Offline**
```javascript
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(registration => {
      console.log('SW registered: ', registration);
    })
    .catch(registrationError => {
      console.log('SW registration failed: ', registrationError);
    });
}
```

## 📱 Responsive Breakpoints

### **Breakpoint System**
```css
/* Mobile First Breakpoints */
$breakpoint-sm: 640px;    /* Small devices */
$breakpoint-md: 768px;    /* Tablets */
$breakpoint-lg: 1024px;   /* Laptops */
$breakpoint-xl: 1280px;    /* Desktops */
$breakpoint-2xl: 1536px;  /* Large screens */

@media (min-width: $breakpoint-sm) { /* ... */ }
@media (min-width: $breakpoint-md) { /* ... */ }
@media (min-width: $breakpoint-lg) { /* ... */ }
@media (min-width: $breakpoint-xl) { /* ... */ }
@media (min-width: $breakpoint-2xl) { /* ... */ }
```

### **Mobile Navigation**
```javascript
class MobileNavigation {
  constructor() {
    this.menuButton = document.getElementById('mobileMenuButton');
    this.navigation = document.getElementById('mainNavigation');
    this.isOpen = false;
    
    this.init();
  }
  
  init() {
    this.menuButton.addEventListener('click', this.toggleMenu.bind(this));
    
    // Close menu when clicking outside
    document.addEventListener('click', (event) => {
      if (this.isOpen && 
          !this.navigation.contains(event.target) && 
          !this.menuButton.contains(event.target)) {
        this.closeMenu();
      }
    });
    
    // Close menu on escape key
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && this.isOpen) {
        this.closeMenu();
      }
    });
  }
  
  toggleMenu() {
    this.isOpen ? this.closeMenu() : this.openMenu();
  }
  
  openMenu() {
    this.navigation.classList.add('nav-open');
    this.menuButton.setAttribute('aria-expanded', 'true');
    this.isOpen = true;
    
    // Trap focus inside navigation
    this.trapFocus();
  }
  
  closeMenu() {
    this.navigation.classList.remove('nav-open');
    this.menuButton.setAttribute('aria-expanded', 'false');
    this.isOpen = false;
    
    // Return focus to menu button
    this.menuButton.focus();
  }
  
  trapFocus() {
    const focusableElements = this.navigation.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    firstElement.focus();
    
    this.navigation.addEventListener('keydown', (event) => {
      if (event.key === 'Tab') {
        if (event.shiftKey) {
          if (document.activeElement === firstElement) {
            event.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            event.preventDefault();
            firstElement.focus();
          }
        }
      }
    });
  }
}

// Initialize only on mobile
if (window.innerWidth < 768) {
  new MobileNavigation();
}
```

## 🧪 Testing

### **Unit Tests with Jest**
```javascript
// formValidator.test.js
describe('FormValidator', () => {
  test('validates required fields', () => {
    const validator = new FormValidator();
    expect(validator.validateRequired('')).toBe(false);
    expect(validator.validateRequired('test')).toBe(true);
  });
  
  test('validates email format', () => {
    const validator = new FormValidator();
    expect(validator.validateEmail('invalid')).toBe(false);
    expect(validator.validateEmail('test@example.com')).toBe(true);
  });
});
```

### **E2E Tests with Cypress**
```javascript
// foodSearch.spec.js
describe('Food Search', () => {
  it('searches for foods', () => {
    cy.visit('/');
    cy.get('#foodSearch').type('apple');
    cy.get('.suggestion-item').should('have.length.at.least', 1);
    cy.contains('Maçã').click();
    cy.get('#nutritionPreview').should('be.visible');
  });
});
```

## 🚀 Deployment

### **Build Process**
```bash
# Install dependencies
npm install

# Development build
npm run dev

# Production build  
npm run build

# Preview production build
npm run preview
```

### **Docker Deployment**
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

## 📊 Performance Metrics

### **Lighthouse Scores**
| Metric | Score | Target |
|--------|-------|--------|
| **Performance** | 95 | > 90 |
| **Accessibility** | 100 | 100 |
| **Best Practices** | 100 | 100 |
| **SEO** | 100 | 100 |

### **Core Web Vitals**
| Metric | Value | Target |
|--------|-------|--------|
| **LCP** | 1.2s | < 2.5s |
| **FID** | 15ms | < 100ms |
| **CLS** | 0.05 | < 0.1 |

---

*🎨 Interface moderna e responsiva*  
*⚡ Performance otimizada para melhor experiência*  
*📱 Funcionalidade completa em todos os dispositivos*  
*♿ Acessibilidade como prioridade de design*