## Data Source

**API:** Jikan REST API

**Base URL:**
https://api.jikan.moe/v4/

## Why Jikan API?

- Public and free API.
- No authentication required.
- Returns data in JSON format.
- Supports pagination.
- Provides multiple related entities.
- Suitable for demonstrating data ingestion, transformation, relational modeling, and database loading.

## Endpoint

**GET /top/anime**

This endpoint returns a paginated list of the highest-ranked anime on MyAnimeList.

It was selected because it provides all entities required for the MVP in a single response:

- Anime
- Genres
- Studios
- Themes

This avoids performing thousands of individual requests to `/anime/{id}`.

## Response Structure

Each response contains two main sections:

- **data**: list of anime returned for the current page.
- **pagination**: metadata required to retrieve the remaining pages.

## Pagination

The pipeline continues requesting pages while:

`has_next_page == true`

## Rate Limiting

The pipeline applies a delay between requests to stay below the API rate limit and reduce the likelihood of receiving HTTP 429 (Too Many Requests).

## Entities

| Entity | JSON Path |
|---------|-----------|
| Anime | `data[]` |
| Genre | `data[].genres[]` |
| Studio | `data[].studios[]` |
| Theme | `data[].themes[]` |

## Fields Used

### Anime

- mal_id
- title
- type
- episodes
- status
- score
- scored_by
- season
- year
- rating

### Genre

- mal_id
- name

### Studio

- mal_id
- name

### Theme

- mal_id
- name

## Out of Scope

The following fields are not used in this version:

- images
- trailer
- synopsis
- background
- broadcast
- licensors
- demographics
- explicit_genres

Reasons:

- They are not part of the proposed relational model.
- They do not add value to the analytical SQL queries.
- They increase implementation complexity without contributing to the learning objectives.

## Observations

`mal_id` values are not sequential.

During the source analysis, multiple non-existent resources returning HTTP 404 were identified.

For this reason, the pipeline retrieves data from the `/top/anime` endpoint using pagination instead of iterating over individual anime IDs.

## Design Decisions

- Use `/top/anime` as the ingestion source.
- Retrieve data using pagination.
- Preserve the original JSON responses in the Bronze layer.
- Use `mal_id` as the natural key.
- Model only Anime, Genre, Studio, Theme, and their relationships.
- Keep characters, reviews, recommendations, and other entities outside the MVP scope.
- Store the relational model in PostgreSQL (Silver layer).
- Perform analytical queries directly in SQL (Gold layer).