# Ouedkniss GraphQL Scraper

Scraper Python pour récupérer les annonces publiques d’Ouedkniss via son API
GraphQL. Le projet est organisé autour de trois idées simples : découvrir les
catégories, parcourir les résultats paginés, puis récupérer et normaliser le
détail de chaque annonce.

## Guide rapide

### Prérequis

- Python 3.10 ou une version plus récente
- Une connexion Internet
- Un environnement virtuel recommandé

Depuis PowerShell, à la racine du projet :

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloque l’activation dans la session courante :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### Lancer le scraper

Mode interactif, recommandé pour commencer :

```powershell
python main.py interactive
```

Le menu affiche les catégories et accepte un chemin comme `2` ou `2.1`.
Il accepte aussi `quick` pour un petit test et `all` pour lancer la collecte
complète.

Mode rapide : trois catégories, une page et cinq annonces par catégorie :

```powershell
python main.py quick
```

Mode complet : toutes les catégories et toutes les pages disponibles :

```powershell
python main.py full
```

Le mode complet peut effectuer beaucoup de requêtes. Il est préférable de
tester d’abord le mode `quick` ou une catégorie depuis le menu interactif.

### Tester le projet

Les tests sont unitaires et n’appellent pas l’API réelle :

```powershell
python -m unittest discover -s tests -v
```

Vérification syntaxique complémentaire :

```powershell
python -m compileall -q main.py scraper tests
```

### Fichiers produits

Les résultats sont écrits dans `output/` :

- `selected_category.json` pour une catégorie choisie dans le menu
- `quick_test.json` pour le mode rapide
- `all_categories.json` pour le mode complet

Les fichiers JSON contiennent les annonces normalisées, les erreurs et le
nombre de doublons détectés.

## Fonctionnement en détail

Le flux d’une collecte est le suivant :

```text
menu GraphQL
   -> catégories
   -> recherche paginée
   -> IDs des annonces
   -> détails GraphQL
   -> parsing / normalisation
   -> déduplication
   -> fichier JSON
```

1. `main.py` choisit le mode d’exécution.
2. `scraper/categories.py` récupère et normalise l’arbre des catégories.
3. `scraper/search.py` prépare les variables de recherche et utilise la
  requête définie dans `scraper/graphql/queries/search.py`.
4. `scraper/details.py` récupère le détail complet avec la requête définie
  dans `scraper/graphql/queries/announcement.py`.
5. `scraper/parser.py` réduit la réponse GraphQL à une structure JSON simple.
6. `scraper/pipeline.py` gère les pages, les retries, les erreurs et les
  doublons.
7. `main.py` écrit le résultat final dans `output/`.

La couche GraphQL est séparée de l’orchestration :

- `graphql/client.py` gère la session HTTP et les erreurs GraphQL ;
- `graphql/queries/` contient les opérations exécutées ;
- `graphql/fragments/` contient les morceaux réutilisables ;
- les modules du dossier `scraper/` préparent les variables et traitent les
  réponses.

Le mode complet réutilise une session HTTP, suit `hasMorePages` jusqu’à la
dernière page et déduplique les annonces par leur ID, y compris entre deux
catégories différentes.

This project is a Python scraper designed to collect structured listing data from Ouedkniss by querying its GraphQL API instead of parsing HTML pages. The main objective is to build a reliable, modular, and extensible data collection pipeline that can work across categories and subcategories rather than only a single hardcoded category.

The project was built from a practical research approach: I inspected the live API structure, tested the GraphQL payloads directly, and iteratively adapted the queries until the category hierarchy and announcement data were properly exposed. The result is a project that works as a foundation for scraping real-world marketplace data in a structured way.

## Why this project exists

When scraping e-commerce or marketplace websites, the biggest challenge is not always the HTTP request itself. It is usually the data model: identifying the right endpoints, understanding the category tree, extracting nested fields, and creating a pipeline that can survive API changes.

This project addresses that by:

- querying the GraphQL backend directly
- extracting category metadata and hierarchy
- fetching announcement listings by category
- loading each item details page
- parsing and normalizing the raw response into structured objects
- exporting the final result as JSON

## Core idea

The scraper does not try to parse HTML. Instead, it targets the GraphQL API used by the site and requests exactly the data it needs. That approach is more stable and more maintainable than brittle DOM scraping.

A typical flow is:

1. Fetch the category tree from the menu API
2. Select a category or a branch of categories
3. Search announcements inside that category
4. Extract announcement IDs
5. Request full announcement details
6. Parse the normalized fields
7. Save the data to JSON

## Category hierarchy

One of the most important points in this project is the category hierarchy.

The website does not simply expose a flat list of categories. It has a tree-like structure, where a parent category may contain several subcategories. For example:

- Automobiles & Véhicules
  - Voitures
  - Utilitaire
  - Motos & Scooters
  - Quads
  - Fourgon
  - Camion
  - Bus
  - Engin
  - Tracteurs
  - Remorques
  - Bateaux & Barques

This hierarchy matters because it determines how the scraper should be organized. If the scraper only targets a single category slug, it misses the rest of the marketplace. If it understands the category tree, it can:

- browse categories by branch
- select specific subcategories
- scrape targeted segments instead of everything at once
- scale to a larger data collection process

This was one of the main lessons discovered during the investigation: a lot of initial attempts fail because the code only queries a flat menu and ignores the nested category structure. The fix was to request the `children` and related category fields from GraphQL and normalize them into a tree.

## Project structure

```text
Ouedkniss-scraper/
├── main.py
├── README.md
├── requirements.txt
├── categories/
│   └── cars.py
├── output/
│   ├── cars.json
│   ├── quick_test.json
│   └── selected_category.json
├── scraper/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── client.py
│   ├── details.py
│   ├── parser.py
│   ├── pipeline.py
│   ├── search.py
│   └── graphql/
│       ├── __init__.py
│       ├── client.py
│       ├── fragments/
│       │   ├── __init__.py
│       │   ├── announcement.py
│       │   ├── category.py
│       │   └── specification.py
│       └── queries/
│           ├── __init__.py
│           ├── announcement.py
│           ├── menu.py
│           ├── promotion.py
│           └── search.py
└── tests/
    └── test_categories.py
```

## Main modules

### 1. scraper/graphql/client.py

This file contains the HTTP client used to send GraphQL requests to Ouedkniss. It creates a session, injects the necessary headers, and sends the JSON payload to the GraphQL endpoint.

It also validates the response by checking for GraphQL errors and raising a failure if the API returns them.

### 2. scraper/graphql/queries/menu.py

This query retrieves the category menu. This is critical because it exposes the hierarchy and allows the scraper to understand the site structure instead of assuming that everything is only one level deep.

The key part is the category tree structure, especially `children`, `parent`, and `parentTree` fields.

### 3. scraper/categories.py

This module is responsible for normalizing the menu data into a tree-like representation.

It has two main responsibilities:

- `fetch_categories()` -> returns a flat list of categories
- `fetch_category_tree()` -> returns a hierarchical category tree

This distinction is important. A flat list is useful for quick testing and a simple CLI. A tree is useful for real-world usage when categories must be browsed by branch.

### 4. scraper/search.py

This file defines the search query used to locate announcements inside a category. It includes filters such as:

- category slug
- page
- count
- ordering
- region/city filters if needed

### 5. scraper/details.py

This module requests the full details of each announcement. It is critical because the search result only gives a summary. The detailed query returns richer fields such as:

- title
- description
- price
- media URLs
- specifications
- city / region
- store / user info
- status and metadata

### 6. scraper/parser.py

This file converts the raw GraphQL response into a cleaner structure that is easy to export and reuse.

The parser extracts:

- IDs
- title and description
- price and price unit
- location
- category
- specifications as a dictionary
- images list

This normalization step is essential because raw GraphQL results may contain nested objects or repeated fields that need to be simplified into a clear format.

### 7. scraper/pipeline.py

This is the orchestration layer. It does the real work of scraping a page and then a category.

Important parts:

- `scrape_page()` fetches a page of announcements and fetches detail for each item
- `scrape_category()` loops through pages and reuses the same logic across pages
- duplicate detection is handled to avoid repeated IDs
- errors are accumulated and returned for later inspection

### GraphQL architecture

GraphQL documents are kept under `scraper/graphql/` and are separated from
the services that execute them:

- `graphql/client.py` owns the HTTP session and GraphQL error handling
- `graphql/queries/` contains operation documents
- `graphql/fragments/` contains reusable GraphQL fragments
- `categories.py`, `search.py`, and `details.py` prepare variables and call
  the client without embedding large query documents

This separation makes API changes local to the GraphQL layer and keeps the
scraping pipeline focused on orchestration and parsing.

## How the scraper works

The flow is straightforward:

```python
categories = fetch_category_tree()
for category in categories:
    scrape_category(category_slug=category["slug"], max_pages=1, count=5)
```

A page scrape does this:

1. search announcements for the chosen category
2. loop through the results
3. fetch announcement details for each item
4. parse the data
5. add it to the accumulated list
6. skip duplicates

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the interactive menu

```bash
python main.py interactive
```

This displays the available categories and allows selection by number or hierarchical path.

Examples:

- `2`
- `2.1`
- `2.2`

You can also use:

- `quick` to test a few categories quickly
- `full` to scrape all categories
- `q` to exit

### 3. Run a quick smoke test

```bash
python main.py quick
```

This is intended for validation and debugging. It scrapes only a small number of announcements so you can test the full pipeline fast.

### 4. Run the full scrapper

```bash
python main.py full
```

The full mode follows pagination until the API reports `hasMorePages: false`.
It reuses one HTTP session and removes duplicate announcement IDs across
categories. It should be used with caution depending on the amount of data
you want to fetch.

## Notes from practical testing

This project was developed through an iterative debugging approach. A few important lessons were discovered during the testing phase:

### 1. A flat category list is not enough

At first, the scraper only used a flat category list and that was a limitation. The website exposes categories in a hierarchical way, and ignoring that structure caused the scraper to lose context and reduce its usefulness.

### 2. GraphQL must request nested data explicitly

The menu API does not magically expose children unless the query asks for them. This is one of the most common traps in GraphQL-based scraping: if the field is not included in the request, it will not appear in the response.

The fix was to add:

- `children`
- `parent`
- `parentTree`

to the category query.

### 3. Small tests are better than huge runs

When developing a scraper, it is much safer to begin with a tiny smoke test:

- 1 category
- 1 page
- 5 items

This makes debugging much faster and prevents unnecessary data collection while the pipeline is still being refined.

### 4. Duplicate handling matters

In listing pages, the same ad can appear multiple times across queries or pages. This is why the scraper includes a deduplication mechanism using IDs. Without that, the exported dataset gets noisy and less trustworthy.

### 5. The GraphQL schema is sensitive to missing fields

Sometimes the API returns partial data or nested fields that are not always present. This project handles that by using safe access patterns such as `dict.get(...)` and by checking whether `children` or `specs` exist before processing them.

## Data output example

The scraper exports a JSON structure that includes:

```json
{
  "category": "Automobiles & Véhicules",
  "category_slug": "automobiles_vehicules",
  "pages": 1,
  "count": 5,
  "duplicates": 0,
  "errors": [],
  "announcements": [
    {
      "id": "57467943",
      "title": "Example listing title",
      "description": "Example description",
      "price": 2600000,
      "price_unit": null,
      "location": {
        "city": "Algiers",
        "region": "Algiers"
      },
      "category": {
        "slug": "automobiles_vehicules"
      },
      "specifications": {
        "marque-voiture": "Toyota",
        "modele": "Corolla"
      },
      "images": [
        "https://example.com/image.jpg"
      ]
    }
  ]
}
```

## GraphQL schema used in this project

The scraper is built around a small but important GraphQL model. The following schema summarizes the main objects and relationships used in the project.

```graphql
scalar ID
scalar String
scalar Int
scalar Boolean

interface CategoryNode {
  id: ID!
  name: String
  slug: String
  icon: String
  children: [CategoryNode!]
  parent: CategoryNode
  parentTree: [CategoryNode!]
}

type Category implements CategoryNode {
  id: ID!
  name: String
  slug: String
  icon: String
  active: Boolean
  rank: Int
  delivery: Boolean
  deliveryType: String
  isWithoutExchange: Boolean
  priceUnits: [String!]
  children: [Category!]
  parent: Category
  parentTree: [Category!]
  specifications: [SpecificationEntry!]
}

type SpecificationEntry {
  isRequired: Boolean
  specification: Specification
}

type Specification {
  id: ID!
  codename: String
  label: String
  type: String
  class: String
  datasets: [SpecificationDataset!]
  dependsOn: [Specification!]
  subSpecifications: [Specification!]
  allSubSpecificationCodenames: [String!]
}

type SearchResult {
  active: [SearchCategory!]
  suggested: [SearchCategory!]
}

type SearchCategory {
  category: Category
  count: Int
  filter: SearchFilter
}

type SearchFilter {
  cities: [City!]
  regions: [Region!]
}

type Announcement {
  id: ID!
  title: String
  slug: String
  description: String
  createdAt: String
  price: Float
  pricePreview: Float
  oldPrice: Float
  oldPricePreview: Float
  priceType: String
  exchangeType: String
  priceUnit: String
  status: String
  defaultMedia: [Media!]
  medias: [Media!]
  cities: [City!]
  category: Category
  specs: [AnnouncementSpec!]
  user: User
  store: Store
  variants: [Variant!]
}

type AnnouncementSpec {
  specification: Specification
  value: String
  valueText: [String!]
}

type City {
  id: ID!
  name: String
  slug: String
  region: Region
}

type Region {
  id: ID!
  name: String
  slug: String
}

type Media {
  mediaUrl: String
  mimeType: String
  thumbnail: String
}

type User {
  id: ID!
  username: String
  displayName: String
  avatarUrl: String
}

type Store {
  id: ID!
  name: String
  slug: String
  imageUrl: String
  url: String
}
```

## GraphQL queries used in the project

### 1. Category menu query

This is used to discover the marketplace structure and the hierarchy.

```graphql
query listingMenu($menuFilter: MenuFilterInput) {
  listingMenu: menuFetch(menuFilter: $menuFilter) {
    target {
      ... on Category {
        id
        name
        slug
        icon
        children {
          id
          name
          slug
        }
        parent {
          id
          name
          slug
        }
        parentTree {
          id
          name
          slug
        }
      }
    }
  }
}
```

This query is the most important one for the hierarchical logic. Without it, the scraper sees only a flat list and loses the model of the site.

### 2. Search metadata query

This query provides category metadata, fixed filters, cities, and related search information.

```graphql
query SearchMetaQuery($q: String, $filter: SearchFilterInput) {
  search(q: $q, filter: $filter) {
    active {
      category {
        id
        name
        slug
        children {
          id
          name
          slug
        }
      }
      filter {
        cities {
          id
          name
        }
        regions {
          id
          name
        }
      }
    }
  }
}
```

### 3. Search announcements query

This query fetches listing pages for a category.

```graphql
query SearchAnnouncementsQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {
  search(q: $q, filter: $filter) {
    announcements {
      data {
        id
        title
        slug
        price
        description
        cities {
          id
          name
          region {
            id
            name
          }
        }
        defaultMedia(size: $mediaSize) {
          mediaUrl
        }
      }
      paginatorInfo {
        lastPage
        hasMorePages
      }
    }
  }
}
```

### 4. Announcement details query

This query is used to fetch the full detail of a single advertisement, including price, media, specs, user/store information, and variants.

```graphql
query AnnouncementGet($id: ID!) {
  announcement: announcementDetails(id: $id) {
    id
    title
    description
    price
    priceUnit
    status
    category {
      id
      name
      slug
      parentTree {
        id
        name
        slug
      }
    }
    cities {
      id
      name
      region {
        id
        name
        slug
      }
    }
    specs {
      specification {
        codename
        label
      }
      valueText
    }
    medias(size: LARGE) {
      mediaUrl
      mimeType
      thumbnail
    }
    user {
      id
      username
      displayName
      avatarUrl
    }
    store {
      id
      name
      slug
      imageUrl
      url
    }
  }
}
```

## Mapping between GraphQL fields and code modules

| Concern | GraphQL field / query | Module |
| --- | --- | --- |
| Category tree | `listingMenu`, `children`, `parentTree` | `scraper/categories.py` |
| Search results | `search(...).announcements` | `scraper/search.py` |
| Details fetch | `announcementDetails(id: ...)` | `scraper/details.py` |
| Normalization | `parse_announcement`, `parse_specs` | `scraper/parser.py` |
| Orchestration | `scrape_page`, `scrape_category` | `scraper/pipeline.py` |
| HTTP execution | `client.execute(...)` | `scraper/graphql/client.py` |

## Why this matters for the project

This project is not only about sending requests. It is about understanding the data model of a marketplace platform and mapping it into a usable, structured pipeline.

The key points a mentor should notice are:

- GraphQL is used instead of HTML parsing
- category hierarchy is explicitly modeled
- nested fields are requested and normalized
- data is gathered in stages
- parsing converts raw API payloads into clean business objects
- the project keeps the code modular and testable

## Current implementation status

The project is already working as a functional scraper prototype. It demonstrates:

- category discovery from the menu
- hierarchical category handling
- search by category
- announcement detail fetching
- parsing and normalization
- JSON export
- quick test and real menu-driven execution

## Limitation and next steps

This is a strong foundation, but there are still a few improvements worth making for a larger production-style workflow:

- add filtering for only relevant categories
- support recursive scraping of entire branches
- improve logging and error traces
- add more resilient retry/backoff logic
- save output per category instead of a single mixed file
- add database persistence or a proper ETL pipeline
- include scheduling or asynchronous scraping

## Final thoughts

This project is a good example of how GraphQL scraping can be approached in a clean and engineering-focused way. The biggest lesson from the research phase is that understanding the data model matters as much as the request itself. In this case, the category hierarchy was the key missing piece. Once it was discovered and properly requested, the scraper became much more realistic, scalable, and useful.

The repository is therefore not just a quick script; it is a small project architecture for structured marketplace data extraction.

## Technologies used

- Python
- Requests
- GraphQL
- JSON
- unittest for validation

## License

This project is intended for educational and research-oriented use. Please respect the terms and policies of the target website when scraping data.

This is a strong foundation, but there are still a few improvements worth making for a larger production-style workflow:

- add filtering for only relevant categories
- support recursive scraping of entire branches
- improve logging and error traces
- add more resilient retry/backoff logic
- save output per category instead of a single mixed file
- add database persistence or a proper ETL pipeline
- include scheduling or asynchronous scraping

## Final thoughts

This project is a good example of how GraphQL scraping can be approached in a clean and engineering-focused way. The biggest lesson from the research phase is that understanding the data model matters as much as the request itself. In this case, the category hierarchy was the key missing piece. Once it was discovered and properly requested, the scraper became much more realistic, scalable, and useful.

The repository is therefore not just a quick script; it is a small project architecture for structured marketplace data extraction.

## Technologies used

- Python
- Requests
- GraphQL
- JSON
- unittest for validation

## License

This project is intended for educational and research-oriented use. Please respect the terms and policies of the target website when scraping data.
