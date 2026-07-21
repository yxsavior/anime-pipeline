### This document describes the relational data model implemented in the Silver layer. The Bronze layer preserves the raw JSON responses obtained from the Jikan API. The Gold layer consists of analytical SQL queries executed on the relational model to support data analysis.

## anime
| Column      | Type    | Description                                                  |
| ----------- | ------- | ------------------------------------------------------------ |
| `mal_id`    | INTEGER | Unique MyAnimeList identifier. Natural key of the table      |
| `title`     | TEXT    | Primary title of the anime                                   |
| `episodes`  | INTEGER | Total number of episodes                                     |
| `score`     | NUMERIC | Average user rating                                          |
| `scored_by` | INTEGER | Number of users who rated the anime                          |
| `year`      | INTEGER | Release year                                                 |
| `season`    | TEXT    | Release season (`winter`, `spring`, `summer`, or `fall`)     |
| `type`      | TEXT    | Anime format (e.g., `TV`, `Movie`, `OVA`, `ONA`, `Special`)  |
| `status`    | TEXT    | Airing status of the anime                                   |
| `rating`    | TEXT    | Age rating assigned to the anime                             |

## genre
| Column   | Type    | Description                                              |
| -------- | ------- | -------------------------------------------------------- |
| `mal_id` | INTEGER | Unique MyAnimeList identifier. Natural key of the table  |
| `name`   | TEXT    | Genre name                                               |

## theme
| Column   | Type    | Description                                              |
| -------- | ------- | -------------------------------------------------------- |
| `mal_id` | INTEGER | Unique MyAnimeList identifier. Natural key of the table  |
| `name`   | TEXT    | Theme name                                               |

## studio
| Column   | Type    | Description                                              |
| -------- | ------- | -------------------------------------------------------- |
| `mal_id` | INTEGER | Unique MyAnimeList identifier. Natural key of the table. |
| `name`   | TEXT    | Animation studio name                                    |

## anime_genre
| Column         | Type    | Description                             |
| -------------- | ------- | --------------------------------------- |
| `anime_mal_id` | INTEGER | Foreign key referencing `anime.mal_id`  |
| `genre_mal_id` | INTEGER | Foreign key referencing `genre.mal_id`  |

## anime_theme
| Column         | Type    | Description                             |
| -------------- | ------- | --------------------------------------- |
| `anime_mal_id` | INTEGER | Foreign key referencing `anime.mal_id`  |
| `theme_mal_id` | INTEGER | Foreign key referencing `theme.mal_id`  |

## anime_studio
| Column          | Type    | Description                              |
| --------------- | ------- | ---------------------------------------- |
| `anime_mal_id`  | INTEGER | Foreign key referencing `anime.mal_id`   |
| `studio_mal_id` | INTEGER | Foreign key referencing `studio.mal_id`  |


