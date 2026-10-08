# 🏥 Чат-бот для лікарні

Чат-бот на Streamlit з двома інструментами:

- **Pinecone** — пошук за документами лікарні (векторна БД)
- **Supabase** — SQL-запити до даних лікарні (реляційна БД, `SQLDatabase`)

Агент сам обирає, який інструмент використати для відповіді.

## Структура проєкту

```
exam/
├── main.py                    # Streamlit-застосунок
├── agent.py                   # агент та system message
├── llm.py                     # LLM (Gemini)
├── env.example                # приклад .env
├── requirements.txt
├── config/
│   └── config.py              # налаштування: секрети з .env, решта — дефолти
├── prompts/
│   └── prompts.py             # системний промпт
├── tools/
│   ├── document_search.py     # пошук по документах (Pinecone)
│   └── sql_tools.py           # інструменти для SQL (Supabase)
├── database/
│   ├── vector_db.py           # підключення до Pinecone
│   ├── sql_db.py              # підключення до Supabase
│   └── fill_vector_db.py      # наповнення векторної бази (скрипт)
└── data/                      # документи лікарні (.txt)
```

## Запуск

```bash
pip install -r requirements.txt
cp env.example .env
```

Заповніть `.env`:

```
GEMINI_API_KEY=...
PINECONE_API_KEY=...
DATABASE_URL=...
```

Решта налаштувань (версії моделей, індекс Pinecone тощо) мають дефолтні значення в `config/config.py` і при потребі також можуть бути перевизначені через `.env`.

1. Покладіть документи лікарні (`general.txt`, `for_workers.txt`) у папку `data/`.
2. Наповніть векторну базу:

```bash
python -m database.fill_vector_db
```

> При створенні векторної бази даних буде створено файл `id.json` з ID завантажених блоків. Він у `.gitignore`, у репозиторій не потрапляє.

3. Запустіть застосунок:

```bash
streamlit run main.py
```

## Як це працює

**Векторна БД:** файли з `data/` розбиваються на блоки завантажуються в Pinecone, а їхні ID зберігаються у `id.json`.

**Реляційна БД:** агент працює з таблицями Supabase через `SQLDatabase` та `SQLDatabaseToolkit`.

**Агент:** `agent.py` збирає LLM, інструменти (`tools/`) та системний промпт (`prompts/prompts.py`).
