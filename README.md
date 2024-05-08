# API for WebScraping and Treating Embrapa Data

## Overview

This is an API used to grab data from Embrapa Website.

### An Example

Given the inputs:

- year = 2022
- option_id = producao
- suboption_id = None

that form the HTTP request:
`/read_clean_data/year=2022/option=producao/suboption=None`

the following response data is returned:

```{
  "data_producao": [
    {
      "option": "producao",
      "suboption": null,
      "col_key_name": "Produto",
      "col_value_name": [
        "Quantidade (L.)"
      ],
      "category": "vinho de mesa",
      "key": "tinto",
      "value": [
        162844214
      ],
      "ano": 2022
    },
    {
      "option": "producao",
      "suboption": null,
      "col_key_name": "Produto",
      "col_value_name": [
        "Quantidade (L.)"
      ],
      "category": "vinho de mesa",
      "key": "branco",
      "value": [
        30198430
      ],
      "ano": 2022
    },
    ...
```

## How does it work?

```bash
📦TechChallenge1
├── LICENSE
├── README.md
└── src
    ├── auth
    │   ├── Auth.py
    │   ├── fake_users_db.json
    │   ├── __init__.py
    │   └── post_token.py
    ├── EmbrapaDefs.py
    ├── EmbrapaTreatData.py
    ├── EmbrapaWebScrap.py
    └── main.py
```

We have four main source files:

- `main.py`: this file has the `main()` function to start the API. Also, it has all the API working paths.
- `EmbrapaDefs.py`: this file has important definitions (constants, literals) regarding Embrapa webpage.
- `EmbrapaWebScrap.py`: this file has a Class to deal with the Web Scraping.
- `EmbrapaTreatData.py`: this file has all methods to treat/clean data gathered from web scraping.

We also have an `auth` directory containing all the files required to protect the API with JWT authentication.

## Requirements and Assumptions

The following topics are a guide for those who want to reproduce and make their changes based on this first release:

- This software has been built using OS Windows 11 22H2.
- `Python 3.12.3` has been used.
- `pip 24.0` has been used to intall libraries.
- Libraries needed and their versions can be found on `requirements.txt`. This can also be used via `pip` with command `python -m pip install -r requirements.txt`.

## Limitations

- This API is a graduate homework for FIAP.
- The app was built considering a brazilian person as a user, and many hard-coded strings are in protuguese.
- There are more limitation possibly not mapped.

## Licenses

This is licensed under GNU General Public License v3.0 (GNU GPLv3)
