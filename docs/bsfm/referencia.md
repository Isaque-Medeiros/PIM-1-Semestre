---
title: "BSFM - Referência Técnica"
date: "2026"
layout: default
---

# Referência Técnica BSFM

Esta página contém informações técnicas de referência sobre o projeto BSFM.

## Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Backend | ASP.NET Core | 8.0 |
| ORM | Entity Framework Core | 8.0 |
| Banco (Produção) | PostgreSQL | 15+ |
| Banco (Dev) | SQLite | 3.x |
| IA (Visão) | YoloDotNet + ONNX | - |
| IA (Texto) | Groq API (Llama 3) | - |
| OCR | Tesseract.js | 5.x |
| Frontend | HTML/CSS/JS + Tailwind | 3.0 |
| Gráficos | Chart.js | 4.x |
| Mapas | Leaflet.js | 1.9 |
| Ícones | Font Awesome | 6.4.0 |
| Deploy | Render | - |
| Documentação | MkDocs + Material | - |

## Endpoints da API

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/solicitar-codigo` | Solicita código de verificação |
| POST | `/cadastrar-usuario-final` | Finaliza cadastro do usuário |
| POST | `/login` | Realiza login |
| POST | `/esqueci-senha` | Solicita redefinição de senha |
| POST | `/redefinir-senha` | Redefine a senha |

### Usuário
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/usuario/{id}` | Obtém dados do perfil |
| PUT | `/usuario/atualizar-nome` | Atualiza nome |
| PUT | `/usuario/atualizar-senha` | Atualiza senha |
| PUT | `/usuario/atualizar-data-nascimento` | Atualiza data de nascimento |
| GET | `/dashboard` | Obtém dados do dashboard |
| GET | `/evolucao/{usuarioId}` | Obtém dados de evolução (peso/IMC) |

### Análise de Alimentos
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/analisar-prato` | Analisa imagem de alimento (YOLO + USDA + Groq) |
| GET | `/historico-analises/{usuarioId}` | Histórico de análises |

### Análise de Rótulos (OCR)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/rotulo/analisar` | Analisa texto OCR de rótulo nutricional via Groq |

### Dados de Saúde
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/saude/{id}` | Retorna diabetes e intolerância |
| PUT | `/api/saude/atualizar` | Atualiza diabetes e intolerância |

### Refeições e Planos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/refeicoes-semana/{usuarioId}` | Lista refeições agendadas |
| POST | `/salvar-refeicao-semana` | Salva refeição agendada |
| DELETE | `/remover-refeicao-semana/{id}` | Remove refeição agendada |

### Consumo de Água
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/agua-diario/{usuarioId}` | Consumo de água do dia |
| GET | `/agua-semanal/{usuarioId}` | Consumo de água da semana |
| POST | `/registrar-agua` | Registra consumo de água |
| DELETE | `/remover-ultima-agua/{usuarioId}` | Remove último registro |

### Metas
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/definir-meta` | Define meta de peso |
| POST | `/atualizar-medicao` | Registra nova medição |

### Hospitais
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/hospitais` | Lista hospitais cadastrados |

### Health Check
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Verifica status da aplicação |

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | Sim | Connection string do banco |
| `USDA_API_KEY` | Não | Chave da API USDA |
| `BREVO_API_KEY` | Não | Chave da API Brevo |
| `GROQ_API_KEY` | Não | Chave da API Groq (para feedback IA) |
| `ASPNETCORE_ENVIRONMENT` | Não | Ambiente (Development/Production) |
| `PORT` | Não | Porta do servidor (Render) |

## Licença

Projeto acadêmico - UNIP - Análise e Desenvolvimento de Sistemas - 3º Semestre - 2026
