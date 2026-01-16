# 🛰️ Sistema de Rastreamento Satelital – INPE

Sistema web desenvolvido para **uso pessoal e interno**, com o objetivo de **monitorar e validar o recebimento de arquivos de satélites** provenientes de diferentes estações de rastreamento do **INPE (Instituto Nacional de Pesquisas Espaciais)**.

A aplicação permite visualizar, de forma organizada, as **janelas de comunicação**, o **nome do satélite** e os **horários de início e fim** das passagens, auxiliando na verificação se os dados foram enviados corretamente.

---

## 📌 Funcionalidades

- Tela inicial com seleção da estação de rastreamento
- Visualização dos dados de passagem de satélites por estação
- Listagem ordenada por data/hora mais recente
- Interface moderna, responsiva e focada em usabilidade
- Consulta direta ao banco de dados MySQL
- Estrutura preparada para expansão (novas estações)

---

## 🖥️ Telas do Sistema

### 🔹 Tela Inicial
- Apresenta o painel principal
- Permite selecionar a estação de rastreamento desejada

### 🔹 Estação Formosa
- Lista os registros de rastreamento
- Exibe:
  - Ordem
  - Nome do satélite
  - Horário de início da passagem
  - Horário de fim da passagem

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Flask**
- **MySQL**
- **HTML5**
- **CSS3**
- **Jinja2**

---

## 📂 Estrutura do Projeto

```
├── app.py
├── templates
│ ├── home.html
│ └── usuarios.html
├── static
│ └── img
│ ├── estacao.png
│ └── antena.png
└── README.md
```

## ⚙️ Configuração do Ambiente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

### 2️⃣ Instalar dependências
```bash
pip install flask mysql-connector-python
```

## 🗄️ Banco de Dados

### Banco: MySQL

### Tabela utilizada: informacoes_formosa

### Estrutura esperada da tabela:

```bash
CREATE TABLE informacoes_formosa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    inicio DATETIME,
    fim DATETIME
);
```

## ▶️ Executando o Projeto

```bash
python app.py
```

### A aplicação estará disponível em:
```bash
http://localhost:5002/home
```

## 🔒 Observações Importantes

- Este projeto é de uso pessoal/institucional
- Não possui fins comerciais
- Não expõe dados sensíveis
- Desenvolvido para monitoramento e validação de arquivos recebidos
- Estrutura preparada para inclusão de novas estações futuramente

## 👨‍💻 Autor
Bruno Torres - Desenvolvedor Full-Stack

Projeto desenvolvido para apoio operacional e monitoramento interno.
