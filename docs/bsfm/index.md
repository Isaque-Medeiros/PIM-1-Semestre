---
title: "BSFM - Brazilian System of Food Metric"
description: "Documentação oficial do protótipo BSFM - Projeto acadêmico UNIP"
layout: default
hide:
  - navigation
  - toc
---

<div class="bsfm-hero">
  <h1>BSFM - Brazilian System of Food Metric</h1>
  <p>Projeto acadêmico de plataforma de nutrição inteligente desenvolvido por estudantes da UNIP. Este é um <strong>protótipo em desenvolvimento</strong> que utiliza inteligência artificial para análise nutricional de alimentos.</p>
  
  <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
    <a href="../guia-usuario/introducao.html" class="bsfm-btn">
      <svg style="margin-right: 0.5rem;" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12,2L14.85,8.15L21,11L14.85,13.85L12,20L9.15,13.85L3,11L9.15,8.15L12,2M12,17.27L13.1,14.9L15.47,13.8L13.1,12.7L12,10.33L10.9,12.7L8.53,13.8L10.9,14.9L12,17.27Z"/>
      </svg>
      Guia do Usuário
    </a>
    <a href="../guia-desenvolvedor/index.html" class="bsfm-btn bsfm-btn-secondary">
      <svg style="margin-right: 0.5rem;" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13,9V3.5L18.5,9H13Z"/>
      </svg>
      Guia do Desenvolvedor
    </a>
  </div>
</div>

<div class="bsfm-stats">
  <div class="bsfm-stat-card">
    <div class="bsfm-stat-number">Protótipo</div>
    <div class="bsfm-stat-label">Status do Projeto</div>
  </div>
  <div class="bsfm-stat-card">
    <div class="bsfm-stat-number">UNIP</div>
    <div class="bsfm-stat-label">Instituição de Ensino</div>
  </div>
  <div class="bsfm-stat-card">
    <div class="bsfm-stat-number">4</div>
    <div class="bsfm-stat-label">Integrantes do Grupo</div>
  </div>
  <div class="bsfm-stat-card">
    <div class="bsfm-stat-number">.NET 8</div>
    <div class="bsfm-stat-label">Tecnologia Principal</div>
  </div>
</div>

<div class="bsfm-feature-grid">
  <div class="bsfm-feature-item">
    <div class="bsfm-feature-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12,2L14.85,8.15L21,11L14.85,13.85L12,20L9.15,13.85L3,11L9.15,8.15L12,2M12,17.27L13.1,14.9L15.47,13.8L13.1,12.7L12,10.33L10.9,12.7L8.53,13.8L10.9,14.9L12,17.27Z"/>
      </svg>
    </div>
    <h3>Análise por IA</h3>
    <p>Detecção visual de alimentos usando YOLO Object Detection com modelo ONNX. A IA identifica alimentos em fotos e consulta dados nutricionais da API USDA.</p>
  </div>
  
  <div class="bsfm-feature-item">
    <div class="bsfm-feature-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M19,3H5C3.89,3 3,3.89 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.89 20.1,3 19,3M19,19H5V5H19V19M7,12H9V17H7V12M11,7H13V17H11V7M15,10H17V17H15V10Z"/>
      </svg>
    </div>
    <h3>Dashboard Personalizado</h3>
    <p>Acompanhe métricas de saúde (IMC, TMB, Gasto Calórico) com gráficos de progresso e evolução histórica de peso.</p>
  </div>
  
  <div class="bsfm-feature-item">
    <div class="bsfm-feature-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
      </svg>
    </div>
    <h3>Sistema de Usuários</h3>
    <p>Cadastro com verificação por email via Brevo API, autenticação com BCrypt e redefinição de senha.</p>
  </div>
  
  <div class="bsfm-feature-item">
    <div class="bsfm-feature-icon">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12,2C8.13,2 5,5.13 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9C19,5.13 15.87,2 12,2M12,11.5C10.62,11.5 9.5,10.38 9.5,9C9.5,7.62 10.62,6.5 12,6.5C13.38,6.5 14.5,7.62 14.5,9C14.5,10.38 13.38,11.5 12,11.5Z"/>
      </svg>
    </div>
    <h3>Mapa SOS Saúde</h3>
    <p>Localize UPAs e hospitais próximos usando Leaflet. Funcionalidade de emergência para encontrar atendimento médico.</p>
  </div>
</div>

<div class="bsfm-card">
  <h2>Sobre o Projeto</h2>
  <p>O <strong>BSFM (Brazilian System of Food Metric)</strong> é um projeto acadêmico desenvolvido por alunos do curso de Análise e Desenvolvimento de Sistemas da <strong>UNIP (Universidade Paulista)</strong>.</p>
  
  <p>Este é um <strong>protótipo</strong> de uma plataforma que simula uma ONG de nutrição, ainda em estágio inicial de desenvolvimento. O projeto vem sendo construído desde <strong>29 de fevereiro de 2026</strong> e tem como objetivo demonstrar conceitos de engenharia de software, desenvolvimento web e inteligência artificial aplicados à saúde alimentar.</p>

  <div class="bsfm-alert bsfm-alert-warning">
    <strong>⚠️ Projeto Acadêmico:</strong> Este é um protótipo educacional. Não possui parcerias reais, dados de usuários reais ou certificações. As funcionalidades são demonstrações conceituais.
  </div>
</div>

<div class="bsfm-card">
  <h2>Nossa Visão</h2>
  <p>Acreditamos que a tecnologia pode democratizar o acesso à informação nutricional de qualidade. Nosso objetivo é construir uma ferramenta que ajude as pessoas a entenderem melhor sua alimentação de forma simples e acessível.</p>
  
  <p>Como projeto acadêmico, buscamos aplicar conceitos de:</p>
  <ul>
    <li><strong>Inteligência Artificial</strong> — Reconhecimento de alimentos por imagem e análise de rótulos com OCR + LLM</li>
    <li><strong>Engenharia de Software</strong> — Arquitetura limpa e boas práticas de desenvolvimento</li>
    <li><strong>UX/UI Design</strong> — Interfaces intuitivas e acessíveis</li>
    <li><strong>Banco de Dados</strong> — Modelagem e persistência de dados</li>
  </ul>
</div>

<div class="bsfm-card">
  <h2>Funcionalidades Implementadas</h2>
  <p>Atualmente, o protótipo conta com as seguintes funcionalidades em desenvolvimento:</p>
  
  <ul>
    <li>✅ <strong>Cadastro e Login</strong> — Autenticação com verificação por email</li>
    <li>✅ <strong>Dashboard</strong> — Métricas de IMC, TMB e gasto calórico com gráficos</li>
    <li>✅ <strong>Analisador IA</strong> — Detecção de alimentos por foto com dados nutricionais</li>
    <li>✅ <strong>Analisador de Rótulos (OCR)</strong> — Escaneamento de tabelas nutricionais com feedback IA (Groq Llama 3)</li>
    <li>✅ <strong>Diário Alimentar</strong> — Registro de refeições analisadas</li>
    <li>✅ <strong>Plano de Refeições</strong> — Agendamento semanal de refeições</li>
    <li>✅ <strong>Consumo de Água</strong> — Registro e acompanhamento de hidratação</li>
    <li>✅ <strong>Mapa SOS Saúde</strong> — Localização de UPAs e hospitais</li>
    <li>✅ <strong>Central LIBRAS</strong> — Conteúdo em Língua Brasileira de Sinais</li>
    <li>✅ <strong>PWA</strong> — Aplicação instalável em dispositivos móveis</li>
    <li>✅ <strong>Dados de Saúde</strong> — Cadastro de diabetes e intolerâncias alimentares</li>
    <li>✅ <strong>Health Score</strong> — Pontuação de saúde com feedback personalizado</li>
  </ul>
</div>

<div class="bsfm-card">
  <h2>Metas e Próximos Passos</h2>
  <p>Como projeto em desenvolvimento, temos as seguintes metas para o futuro:</p>
  
  <ul>
    <li>⬜ <strong>Melhorar precisão da IA</strong> — Treinar modelo com mais alimentos brasileiros</li>
    <li>⬜ <strong>Modo escuro completo</strong> — Tema escuro consistente em todas as páginas</li>
    <li>⬜ <strong>Notificações</strong> — Lembretes de refeições e hidratação</li>
    <li>⬜ <strong>Exportação de dados</strong> — Gerar relatórios em PDF</li>
    <li>⬜ <strong>App mobile nativo</strong> — Versão para iOS e Android</li>
    <li>⬜ <strong>Melhorias no OCR</strong> — Treinar Tesseract com fontes de tabelas nutricionais brasileiras</li>
  </ul>
</div>

<div class="bsfm-card">
  <h2>Navegação Rápida</h2>
  <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
    <a href="../about/visao-missao.html" class="bsfm-btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Visão e Missão</a>
    <a href="../roadmap/index.html" class="bsfm-btn bsfm-btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Roadmap</a>
    <a href="../changelog/index.html" class="bsfm-btn bsfm-btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Changelog</a>
    <a href="../caso-de-uso/index.html" class="bsfm-btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Casos de Uso</a>
    <a href="../glossario/index.html" class="bsfm-btn bsfm-btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Glossário</a>
  </div>
</div>
