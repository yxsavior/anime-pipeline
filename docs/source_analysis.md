## Fonte
API: Jikan REST API

Base URL:
https://api.jikan.moe/v4/

### Motivos da escolha
- API pública e gratuita.
- Não exige autenticação.
- Dados em formato JSON.
- Possui paginação.
- Possui múltiplas entidades relacionadas.
- Permite demonstrar ingestão, transformação, modelagem relacional e carga em banco de dados.

## Endpoint utilizado
GET /top/anime

Este endpoint retorna uma lista paginada dos animes mais bem classificados no MyAnimeList.

Foi escolhido porque fornece, em uma única resposta, todas as entidades necessárias para o MVP:

- Anime
- Genres
- Studios
- Themes

Sem necessidade de realizar milhares de requisições individuais para `/anime/{id}`.

## Estrutura da resposta
A resposta possui dois elementos principais:

- data: lista de animes retornados na página.
- pagination: informações necessárias para percorrer todas as páginas

## Paginação
O pipeline continuará realizando requisições enquanto
`has_next_page == true`.

## Rate limit
O pipeline utilizará um intervalo entre requisições para permanecer abaixo do limite da API e reduzir a chance de respostas HTTP 429.

## Entidades
| Entidade | Origem       |
| -------- | ------------ |
| Anime    | data         |
| Genre    | data.genres  |
| Studio   | data.studios |
| Theme    | data.themes  |

## Campos utilizados
### Anime
- mal_id
- title
- type
- episodes
- status
- score
- season
- year

### Genre
- mal_id
- name

### Studio
- mal_id
- name

### Theme
- mal_id
- name

## Campos fora do escopo
Os seguintes campos não serão utilizados nesta versão:
- images
- trailer
- synopsis
- background
- broadcast
- licensors
- demographics
- explicit_genres

Motivos:
- não participam da modelagem relacional proposta;
- não agregam valor às consultas SQL do MVP;
- aumentariam a complexidade sem contribuir para os objetivos de aprendizagem.

## Observações importantes
Os identificadores (mal_id) não são contínuos.
Durante a exploração da API foram encontrados diversos recursos inexistentes que retornam HTTP 404.
Por esse motivo, a ingestão utilizará o endpoint `/top/anime` com paginação, em vez de iterar sobre identificadores individuais.

## Decisões tomadas
- Utilizar `/top/anime` como fonte de ingestão.
- Utilizar paginação para percorrer os registros.
- Preservar o JSON original na camada Bronze.
- Utilizar `mal_id` como chave natural.
- Modelar apenas Anime, Genre, Studio e Theme.
- Manter personagens, reviews e demais entidades fora do MVP.
- Utilizar PostgreSQL como camada Silver.
- Produzir consultas analíticas diretamente em SQL na camada Gold.
