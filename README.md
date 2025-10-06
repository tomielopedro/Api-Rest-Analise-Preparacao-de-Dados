# API REST com Flask e MVC

Este projeto é uma API REST desenvolvida com Flask que segue o padrão de arquitetura MVC (Model-View-Controller). A API oferece endpoints para consultar e filtrar dados de séries, lendo as informações de um arquivo CSV.

## O que é o padrão MVC?

O padrão de arquitetura **MVC (Model-View-Controller)** é um padrão de design de software que separa a representação da informação da interação do usuário com ela. Ele divide a aplicação em três partes interconectadas:

*   **Model (Modelo):** A camada de dados da aplicação. É responsável por gerenciar os dados e a lógica de negócios. No nosso caso, a classe `Serie` e a leitura do arquivo `series.csv` representam o Model.
*   **View (Visão):** A camada de apresentação da aplicação. É responsável por exibir os dados ao usuário. Em uma API REST, a View é a representação dos dados em formato JSON que é enviada como resposta às requisições.
*   **Controller (Controlador):** A camada de controle da aplicação. É responsável por receber as requisições do usuário, interagir com o Model para obter os dados e enviar a resposta para a View. No nosso projeto, os arquivos em `app/controllers` são os Controllers.



## Estrutura do Projeto

A estrutura de diretórios do projeto foi organizada da seguinte forma:

```
api-rest-flask/
├── app/
│   ├── __init__.py               # Inicializa o Flask e registra os blueprints
│   ├── controllers/              # Contém as rotas da API
│   │   ├── __init__.py
│   │   ├── series_controller.py  # Endpoints relacionados a séries
│   │   └── filtro_controller.py  # Endpoint de filtros dinâmicos
│   ├── models/                   # Representação dos dados
│   │   ├── __init__.py
│   │   └── serie.py              # Classe Serie (dataclass)
│   └── data/
│       └── series.csv            # Dataset de séries
├── main.py                       # Ponto de entrada da aplicação
├── requirements.txt              # Dependências do projeto
└── README.md                     # Documentação do projeto
```

### `app/`

Este diretório contém o núcleo da aplicação Flask.

*   **`__init__.py`**: Arquivo de inicialização do Flask. Aqui, a instância do Flask é criada e os *blueprints* dos controllers são registrados.
*   **`controllers/`**: Contém os controladores da aplicação, que são responsáveis por definir as rotas (endpoints) da API.
    *   **`series_controller.py`**: Define os endpoints para consultar, adicionar, editar e deletar a lista de séries.
    *   **`filtro_controller.py`**: Define o endpoint para realizar filtros dinâmicos nos dados das séries.
*   **`models/`**: Contém os modelos de dados da aplicação.
    *   **`serie.py`**: Define a classe `Serie`, que representa a estrutura de dados de uma série.
*   **`data/`**: Contém os arquivos de dados utilizados pela aplicação.
    *   **`series.csv`**: O dataset de séries que a API consome.

### `main.py`

O ponto de entrada da aplicação. Este arquivo é responsável por executar o servidor de desenvolvimento do Flask.

### `requirements.txt`

Lista todas as dependências Python do projeto. Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```


## Como Executar o Projeto

1. **Clone o repositório** (se aplicável):
   ```bash
   git clone <url-do-repositorio>
   cd api-rest-flask
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**:
   ```bash
   python main.py
   ```

4. **Acesse a API**:
   A API estará disponível em `http://localhost:5000`
   Documentação Swagger da api disponível em `http://localhost:5000/apidocs`

## Vantagens do Padrão MVC

O uso do padrão MVC neste projeto oferece várias vantagens:

| Vantagem | Descrição |
|----------|-----------|
| **Separação de Responsabilidades** | Cada camada tem uma responsabilidade específica, facilitando a manutenção |
| **Reutilização de Código** | Os modelos podem ser reutilizados em diferentes controllers |
| **Facilidade de Teste** | Cada camada pode ser testada independentemente |
| **Escalabilidade** | Novos controllers e modelos podem ser adicionados facilmente |
| **Organização** | O código fica mais organizado e fácil de navegar |

## Fluxo de Funcionamento

O fluxo de uma requisição na aplicação segue o padrão MVC:

1. **Requisição HTTP** chega ao servidor Flask
2. **Controller** recebe a requisição através das rotas definidas
3. **Controller** interage com o **Model** para obter ou processar dados
4. **Model** acessa os dados (no caso, o arquivo CSV)
5. **Controller** processa os dados e prepara a resposta
6. **View** (resposta JSON) é enviada de volta ao cliente

## Tecnologias Utilizadas

- **Flask**: Framework web para Python
- **Python**: Linguagem de programação
- **CSV**: Formato de dados para armazenamento das séries
- **JSON**: Formato de resposta da API

## Estrutura dos Dados

O arquivo `series.csv` contém informações sobre séries de TV, incluindo campos como título, ano de lançamento, classificação, entre outros. A classe `Serie` no arquivo `models/serie.py` define a estrutura desses dados usando dataclasses do Python.

