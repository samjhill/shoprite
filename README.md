# Shoprite

Automatically adds items to your Shoprite cart based on the frequently-ordered-items list.

## Setup

Clone this repository.

Create a `.env` file at the root of this directory with the following content:

```
SHOPRITE_USERNAME="...."
SHOPRITE_PASSWORD="...."
```


```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```shell
python -m get_products
python -m main
```