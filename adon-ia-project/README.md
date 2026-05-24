# Adon-ia

**Adon-ia** é uma interface web minimalista para interagir com modelos de linguagem (LLMs) localmente via [Ollama](https://ollama.ai). Utiliza o modelo **Qwen3.5 4B** (da Alibaba) servido via Ollama.

> ⚠️ **Aviso:** Esta é uma versão de estudos de IA. Não foi desenvolvida para produção, mas pode ser adaptada para pequenos projetos que utilizam LLMs locais.

---

## Desempenho com GPU

O projeto foi testado com sucesso utilizando uma **NVIDIA GeForce RTX 3060 Ti (8 GB VRAM)** em duas configurações de máquina:

- **Ryzen 9 5950X** — inferência rápida com o modelo carregando inteiramente na VRAM
- **Dual Xeon E5-2680 v4 (X99, placa MD8)** — mesmo desempenho de GPU, dependendo apenas do barramento PCIe

A RTX 3060 Ti (Compute Capability 8.6, 8 GB) consegue rodar o **Qwen3.5 4B (~3.4 GB)** inteiro em VRAM, entregando **tokens por segundo muito superiores** à execução em CPU.

---

## Como foi construído

```
Qwen3.5 4B (Alibaba)
    → baixado via Ollama (ollama pull qwen3.5:4b)
    → servido localmente via API do Ollama (porta 11434)
    → interface web própria (Flask, porta 12800)
```

### Stack

| Componente | Tecnologia |
|-----------|-----------|
| Modelo | Qwen3.5 4B (Ollama) |
| Servidor da API | Ollama |
| Backend web | Python + Flask |
| Frontend | HTML + CSS + JavaScript (sem dependências) |
| Script de inicialização | Python (`run.py`) / PowerShell (`run.ps1`) |

---

## Requisitos

- Windows 10/11
- [Ollama](https://ollama.ai/download) instalado
- Python 3.12+
- Flask instalado (`pip install flask`)

---

## Como usar

### 1. Iniciar tudo (recomendado)

```bash
cd C:\Users\seu-usuario\Documents\adon-ia-project
.\run.ps1          # PowerShell
# ou
python run.py      # Python
```

Pressione **ESC** para parar todos os processos.

### 2. Iniciar manualmente

```bash
# Terminal 1 — Ollama (já inicia com o Windows)
# ou force manualmente:
ollama serve

# Terminal 2 — WebUI
cd C:\Users\seu-usuario\Documents\adon-ia-project
python app.py
```

Acesse **http://localhost:12800**

---

## Estrutura do projeto

```
adon-ia-project/
├── app.py           # Servidor Flask (porta 12800)
├── run.py           # Gerenciador Python (inicia/para tudo)
├── run.ps1          # Gerenciador PowerShell
├── templates/
│   └── index.html   # Interface web única
├── static/          # (reservado para CSS/JS extras)
└── README.md
```

---

## Funcionalidades

- Chat em tempo real com LLM local
- Exibe métricas de desempenho: tempo de resposta, tokens gerados, tokens por segundo
- Sem necessidade de internet (após baixar o modelo)
- Sem cadastro ou login
- Leve e de código aberto

---

## Modificação para outros modelos

Para usar outro modelo, edite `app.py`:

```python
MODEL = 'nome-do-modelo'   # Ex: 'llama3.2', 'mistral', 'gemma3'
```

O modelo deve estar disponível no Ollama:

```bash
ollama pull nome-do-modelo
```

---

## Limitações

- Interface single-page simples (sem histórico persistente)
- Desenvolvido para estudos e experimentação
- Consumo de recursos depende do modelo escolhido (Qwen3 4B usa ~2.5 GB de RAM/VRAM)
