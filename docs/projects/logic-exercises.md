---
title: Exercícios de Lógica
description: Coleção de exercícios de programação e algoritmos desenvolvidos durante a graduação
---

# Exercícios de Lógica e Programação

## Visão Geral

Esta seção contém diversos exercícios de lógica de programação desenvolvidos durante meus estudos na ETEC, UNIP e programas da DIO. Os exercícios abrangem desde conceitos básicos até algoritmos mais complexos.

## Categorias de Exercícios

### Algoritmos Básicos

#### Verificador Par/Impar
```python
def verificador_par_impar(numero):
    """Verifica se um número é par ou ímpar"""
    if numero % 2 == 0:
        return "Par"
    else:
        return "Ímpar"

# Teste
test_numbers = [2, 7, 10, 15]
for num in test_numbers:
    print(f"{num} é {verificador_par_impar(num)}")
```

#### Jogo de Adivinhação
```python
import random

def jogo_adivinhacao():
    """Jogo onde o usuário tenta adivinhar um número entre 1-100"""
    numero_secreto = random.randint(1, 100)
    tentativas = 0
    
    print("Adivinhe o número entre 1 e 100!")
    
    while True:
        try:
            palpite = int(input("Seu palpite: "))
            tentativas += 1
            
            if palpite < numero_secreto:
                print("Tente um número maior!")
            elif palpite > numero_secreto:
                print("Tente um número menor!")
            else:
                print(f"Parabéns! Você acertou em {tentativas} tentativas!")
                break
        except ValueError:
            print("Por favor, digite um número válido.")
```

### Estruturas de Dados

#### Sistema de Pilha
```python
class Pilha:
    """Implementação de uma pilha (LIFO) em Python"""
    
    def __init__(self):
        self.itens = []
    
    def empilhar(self, item):
        """Adiciona um item ao topo da pilha"""
        self.itens.append(item)
    
    def desempilhar(self):
        """Remove e retorna o item do topo"""
        if not self.esta_vazia():
            return self.itens.pop()
        return None
    
    def esta_vazia(self):
        """Verifica se a pilha está vazia"""
        return len(self.itens) == 0
    
    def topo(self):
        """Retorna o item do topo sem remover"""
        if not self.esta_vazia():
            return self.itens[-1]
        return None
```

#### Busca Binária em Vetor
```python
def busca_binaria_vetor(vetor, alvo):
    """Implementação da busca binária em vetor ordenado"""
    esquerda, direita = 0, len(vetor) - 1
    
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        
        if vetor[meio] == alvo:
            return meio
        elif vetor[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    return -1  # Não encontrado

# Exemplo de uso
vetor_ordenado = [1, 3, 5, 7, 9, 11, 13, 15]
alvo = 9
resultado = busca_binaria_vetor(vetor_ordenado, alvo)
print(f"Elemento {alvo} encontrado no índice {resultado}")
```

### Sistemas Completos

#### Sistema de Login
```python
def sistema_login():
    """Sistema simples de autenticação"""
    usuarios = {
        "admin": "senha123",
        "usuario": "password"
    }
    
    tentativas = 3
    
    while tentativas > 0:
        username = input("Usuário: ")
        password = input("Senha: ")
        
        if username in usuarios and usuarios[username] == password:
            print("Login bem-sucedido!")
            return True
        else:
            tentativas -= 1
            print(f"Credenciais inválidas. Tentativas restantes: {tentativas}")
    
    print("Número máximo de tentativas excedido.")
    return False
```

#### Controle de Acesso
```python
def controle_acesso(nivel_usuario, recurso):
    """Sistema de controle de acesso baseado em roles"""
    permissoes = {
        "admin": ["todos"],
        "usuario": ["leitura", "download"],
        "visitante": ["leitura"]
    }
    
    if nivel_usuario in permissoes:
        if recurso in permissoes[nivel_usuario] or "todos" in permissoes[nivel_usuario]:
            return True
    
    return False

# Teste
print(controle_acesso("admin", "escrita"))      # True
print(controle_acesso("usuario", "escrita"))   # False
print(controle_acesso("visitante", "leitura")) # True
```

### Exercícios Avançados

#### Análise de Temperaturas
```python
def analise_temperaturas(temperaturas):
    """Analisa uma lista de temperaturas e retorna estatísticas"""
    if not temperaturas:
        return None
    
    media = sum(temperaturas) / len(temperaturas)
    maxima = max(temperaturas)
    minima = min(temperaturas)
    
    return {
        "media": round(media, 2),
        "maxima": maxima,
        "minima": minima,
        "amplitude": maxima - minima
    }

# Exemplo
temps = [22.5, 23.1, 21.8, 24.3, 22.9, 20.5, 25.1]
stats = analise_temperaturas(temps)
print(f"Média: {stats['media']}°C")
print(f"Máxima: {stats['maxima']}°C")
print(f"Mínima: {stats['minima']}°C")
```

#### Estatísticas de Notas
```python
def estatisticas_notas(notas):
    """Calcula estatísticas de uma lista de notas"""
    if not notas:
        return None
    
    media = sum(notas) / len(notas)
    aprovados = sum(1 for nota in notas if nota >= 6)
    taxa_aprovacao = (aprovados / len(notas)) * 100
    
    return {
        "total_alunos": len(notas),
        "media_turma": round(media, 2),
        "aprovados": aprovados,
        "taxa_aprovacao": round(taxa_aprovacao, 2)
    }

# Exemplo
notas_turma = [7.5, 8.0, 5.5, 6.8, 9.2, 4.5, 7.0, 6.5]
resultado = estatisticas_notas(notas_turma)
print(f"Média da turma: {resultado['media_turma']}")
print(f"Taxa de aprovação: {resultado['taxa_aprovacao']}%")
```

## Projetos de Circuitos (Tinkercad)

### Semáforo com Arduino
```c
// Código para semáforo com pedestre
int ledVermelho = 2;
int ledAmarelo = 3;
int ledVerde = 4;
int botaoPedestre = 5;

void setup() {
    pinMode(ledVermelho, OUTPUT);
    pinMode(ledAmarelo, OUTPUT);
    pinMode(ledVerde, OUTPUT);
    pinMode(botaoPedestre, INPUT);
}

void loop() {
    // Ciclo normal do semáforo
    digitalWrite(ledVerde, HIGH);
    delay(5000);
    digitalWrite(ledVerde, LOW);
    
    digitalWrite(ledAmarelo, HIGH);
    delay(2000);
    digitalWrite(ledAmarelo, LOW);
    
    digitalWrite(ledVermelho, HIGH);
    delay(5000);
    digitalWrite(ledVermelho, LOW);
    
    // Verificar botão de pedestre
    if (digitalRead(botaoPedestre) == HIGH) {
        atenderPedestre();
    }
}

void atenderPedestre() {
    digitalWrite(ledAmarelo, HIGH);
    delay(1000);
    digitalWrite(ledAmarelo, LOW);
    
    digitalWrite(ledVermelho, HIGH);
    delay(7000);  // Tempo para pedestre atravessar
    digitalWrite(ledVermelho, LOW);
}
```

## Competências Desenvolvidas

- **Lógica de Programação**: Resolução de problemas complexos
- **Estruturas de Dados**: Arrays, pilhas, filas, algoritmos de busca
- **Orientação a Objetos**: Classes, métodos, encapsulamento
- **Controle de Fluxo**: Condicionais, loops, recursão
- **Manipulação de Arquivos**: Leitura e escrita de dados
- **Circuitos Eletrônicos**: Programação de microcontroladores

## Próximos Desafios

- [ ] Implementar algoritmos de ordenação
- [ ] Desenvolver estruturas de dados mais complexas
- [ ] Criar projetos com Internet das Coisas (IoT)
- [ ] Explorar machine learning básico
- [ ] Desenvolver APIs RESTful

## Links Relacionados

- [Repositório de Exercícios](https://github.com/isaque/exercicios)
- [Documentação Python](https://docs.python.org/)
- [Tinkercad Projects](https://www.tinkercad.com/)