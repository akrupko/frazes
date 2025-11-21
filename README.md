# MySQL Database for Russian Phraseological Dictionary

## Описание проекта

Этот проект создает MySQL базу данных из JSON файла с русскими фразеологизмами для использования в тренажере по запоминанию фразеологизмов.

## Статистика

- **Всего фразеологизмов**: 1,140
- **Категорий**: 25
- **Источник**: Wiktionary
- **Язык**: Русский

## Файлы проекта

- `table_phrases.json` - исходный JSON файл с данными
- `phraseological_dict.sql` - готовый SQL дамп для импорта в MySQL
- `create_mysql_db.py` - Python скрипт для генерации SQL дампа
- `TIMEWEB_IMPORT_INSTRUCTIONS.md` - подробная инструкция по импорту на Timeweb

## Структура базы данных

### Таблица: `phraseological_dict`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INT AUTO_INCREMENT | Уникальный идентификатор |
| `phrase` | VARCHAR(500) | Фразеологизм |
| `meaning` | TEXT | Значение фразеологизма |
| `etymology` | TEXT | Происхождение (может быть NULL) |
| `usage_example` | TEXT | Пример использования (изначально NULL) |
| `categories` | VARCHAR(100) | Категория |
| `source_url` | TEXT | Источник из Wiktionary |

## Быстрый старт

1. **Для импорта базы данных**:
   - Используйте файл `phraseological_dict.sql`
   - Следуйте инструкции в `TIMEWEB_IMPORT_INSTRUCTIONS.md`

2. **Для пересоздания SQL дампа**:
   ```bash
   python3 create_mysql_db.py
   ```

## Категории фразеологизмов

- `general` - общие
- `animals` - животные  
- `body_parts` - части тела
- `character_behavior` - поведение характера
- `colors_light` - цвета/свет
- `emotions_feelings` - эмоции/чувства
- `family_relationships` - семья/отношения
- `food_drink` - еда/напитки
- `health_disease` - здоровье/болезни
- `house_home` - дом/жилье
- `luck_fortune` - удача/судьба
- `mind_intelligence` - ум/интеллект
- `money_wealth` - деньги/богатство
- `quantity_measure` - количество/меры
- `religion_mythology` - религия/мифология
- `speech_communication` - речь/общение
- `swearing` - ругательства
- `time_age` - время/возраст
- `transport_travel` - транспорт/путешествия
- `war_conflict` - война/конфликты
- `weather_nature` - погода/природа
- `work_labor` - работа/труд

## Примеры данных

```sql
-- Пример записи из базы данных
INSERT INTO phraseological_dict (id, phrase, meaning, etymology, usage_example, categories, source_url) 
VALUES (1, 'А был ли мальчик?', 'Употребляется при сомнениях в наличии самого предмета, давшего повод для беспокойства, хлопот.', 'Взято из романа М. Горького ”Жизнь Клима Самгина”', NULL, 'general', 'https://ru.wiktionary.org/wiki/...');
```

## Использование в тренажере

### Базовые запросы

```sql
-- Получить случайный фразеологизм
SELECT * FROM phraseological_dict ORDER BY RAND() LIMIT 1;

-- Получить фразеологизмы по категории
SELECT * FROM phraseological_dict WHERE categories = 'animals';

-- Поиск по содержанию
SELECT * FROM phraseological_dict 
WHERE phrase LIKE '%вода%' OR meaning LIKE '%вода%';
```

### Для тренировочных режимов

```sql
-- Режим "Угадай значение" - получаем фразеологизм без значения
SELECT id, phrase, categories FROM phraseological_dict ORDER BY RAND() LIMIT 1;

-- Режим "Угадай фразеологизм" - получаем значение без фразеологизма  
SELECT id, meaning, categories FROM phraseological_dict ORDER BY RAND() LIMIT 1;

-- Режим "Категории" - получаем фразеологизмы из конкретной категории
SELECT * FROM phraseological_dict WHERE categories = 'animals' ORDER BY RAND() LIMIT 10;
```

## Особенности

- ✅ Полная поддержка UTF-8 (utf8mb4) для корректного отображения русских символов
- ✅ Оптимизированные индексы для быстрого поиска
- ✅ Уникальные фразеологизмы (UNIQUE constraint)
- ✅ Готовность к использованию на Timeweb и других MySQL хостингах
- ✅ Включены источники для каждого фразеологизма

## Лицензия

Данные взяты из Wiktionary и распространяются в соответствии с лицензией CC BY-SA.