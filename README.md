Ouedkniss GraphQL Scraper

A flexible scraper built to extract structured data from Ouedkniss using
its GraphQL API. The project is designed with a modular architecture to
support multiple categories in the future.

Overview

This scraper communicates directly with the Ouedkniss GraphQL backend
instead of parsing HTML pages.

The scraping process includes: 1. Discovering GraphQL operations used by
the website. 2. Building reusable GraphQL queries and fragments. 3.
Fetching category metadata. 4. Retrieving announcement lists. 5.
Extracting detailed announcement information. 6. Parsing and normalizing
the data. 7. Exporting structured JSON output.

GraphQL Operations

SearchMetaQuery

Retrieves category information: - Category hierarchy - Subcategories -
Specifications - Available filters - Cities and regions

SearchAnnouncementsQuery

Retrieves announcement lists: - Announcement IDs - Pagination -
Filtering - Ordering

AnnouncementGet

Retrieves full announcement details: - Title - Description - Price -
Images - Location - Specifications - User/store information

GraphQL Fragments

Fragments are used to organize and reuse GraphQL fields.

Example structure:

SearchAnnouncementsQuery | +– SearchAnnouncementsContent | +–
AnnouncementContentNoUserReaction

This keeps queries clean and easier to maintain.

Scraping Workflow

Category | v SearchMetaQuery | v SearchAnnouncementsQuery | v
Announcement IDs | v AnnouncementGet | v Parsed Data | v JSON Output

Data Processing

Raw GraphQL responses are converted into normalized objects.

Example:

Before: { specification: { label: “Marque” }, valueText: [“Geely”] }

After:

{ “marque-voiture”: “Geely” }

Extracted Data

Basic information: - ID - Title - Description - Price - Status

Location: - City - Region

Media: - Images - Media URLs

Specifications: - Dynamic specifications extracted from GraphQL

Example:

{ “annee”: “2026”, “marque-voiture”: “Geely”, “modele”: “Coolray”,
“energie”: “Essence”, “transmission”: “Automatique” }

Architecture

Ouedkniss-scraper/

-   main.py

-   graphql/

    -   queries.py
    -   fragments.py

-   scraper/

    -   client.py
    -   search.py
    -   announcement.py

-   parser/

    -   announcement_parser.py
    -   category_parser.py

-   output/

    -   cars.json

Current Features

-   GraphQL API scraping
-   Category metadata extraction
-   Announcement search
-   Pagination handling
-   Detailed information extraction
-   Dynamic specification parsing
-   Image extraction
-   Duplicate handling
-   JSON export

Future Improvements

-   Support multiple categories dynamically
-   Database integration
-   Async requests
-   Scheduled scraping
-   Data cleaning pipeline
-   API layer for extracted data

Technologies

-   Python
-   GraphQL
-   Requests
-   JSON