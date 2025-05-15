# Codex Data

A simple data processing tool for manipulating structured data.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic usage example:

```bash
python -m codex_data.main --input data.csv --output result.csv
```

### Operations

You can perform various operations on your data:

#### Filter data

```bash
python -m codex_data.main --input data.csv --output result.csv --operation filter column age condition greater_than value 30
```

#### Select columns

```bash
python -m codex_data.main --input data.csv --output result.csv --operation select columns name age salary
```

#### Rename columns

```bash
python -m codex_data.main --input data.csv --output result.csv --operation rename mapping old_name new_name
```

#### Sort data

```bash
python -m codex_data.main --input data.csv --output result.csv --operation sort column age ascending false
```

### Multiple operations

You can chain multiple operations:

```bash
python -m codex_data.main --input data.csv --output result.csv \
  --operation filter column age condition greater_than value 30 \
  --operation select columns name age salary \
  --operation sort column salary ascending false
```

## Supported formats

- CSV (.csv)
- Excel (.xls, .xlsx)
- JSON (.json)
