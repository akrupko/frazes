# Инструкция по импорту базы данных фразеологизмов на Timeweb

## Обзор

База данных содержит 1,140 русских фразеологизмов со следующими полями:
- `id` - уникальный идентификатор
- `phrase` - фразеологизм
- `meaning` - значение фразеологизма
- `etymology` - происхождение (может быть NULL)
- `usage_example` - пример использования (изначально NULL, для заполнения позже)
- `categories` - категория фразеологизма
- `source_url` - источник из Wiktionary

## Файлы

- `phraseological_dict.sql` - SQL дамп базы данных
- `create_mysql_db.py` - Python скрипт для генерации SQL дампа

## Способ 1: Импорт через phpMyAdmin (рекомендуется)

1. Войдите в панель управления Timeweb
2. Перейдите в раздел "Базы данных"
3. Создайте новую базу данных (например, `phraseological_db`)
4. Откройте phpMyAdmin для созданной базы данных
5. Выберите вкладку "Импорт"
6. Выберите файл `phraseological_dict.sql`
7. Убедитесь, что кодировка установлена как `utf8mb4`
8. Нажмите "Вперед" для импорта

## Способ 2: Импорт через SSH

Если у вас есть доступ к SSH:

1. Загрузите файл `phraseological_dict.sql` на сервер:
   ```bash
   scp phraseological_dict.sql user@your-server:/path/to/
   ```

2. Подключитесь к серверу по SSH

3. Импортируйте базу данных:
   ```bash
   mysql -u username -p database_name < phraseological_dict.sql
   ```

## Способ 3: Импорт через MySQL консоль

1. Подключитесь к MySQL:
   ```bash
   mysql -u username -p
   ```

2. Создайте базу данных:
   ```sql
   CREATE DATABASE phraseological_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   USE phraseological_db;
   ```

3. Импортируйте данные:
   ```sql
   SOURCE /path/to/phraseological_dict.sql;
   ```

## Проверка импорта

После импорта выполните запрос для проверки:

```sql
-- Проверить количество записей
SELECT COUNT(*) FROM phraseological_dict;

-- Посмотреть примеры данных
SELECT * FROM phraseological_dict LIMIT 5;

-- Проверить категории
SELECT DISTINCT categories FROM phraseological_dict ORDER BY categories;
```

## Структура таблицы

```sql
CREATE TABLE `phraseological_dict` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phrase` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Фразеологизм',
  `meaning` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Значение фразеологизма',
  `etymology` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Происхождение фразеологизма',
  `usage_example` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Пример использования фразеологизма в тексте',
  `categories` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Категория фразеологизма',
  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Источник',
  PRIMARY KEY (`id`),
  UNIQUE KEY `phrase` (`phrase`),
  KEY `categories` (`categories`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Словарь фразеологизмов русского языка';
```

## Доступные категории

База данных содержит 25 категорий:

- `general` - общие
- `animals` - животные
- `body_parts` - части тела
- `character_behavior` / `character_behaviour` - поведение характера
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
- `religion_mythology` / `religion_methology` - религия/мифология
- `speech_communication` - речь/общение
- `swearing` - ругательства
- `time_age` - время/возраст
- `transport_travel` - транспорт/путешествия
- `war_conflict` - война/конфликты
- `weather_nature` - погода/природа
- `work_labor` - работа/труд

## Примеры запросов для тренажера

```sql
-- Получить случайный фразеологизм
SELECT * FROM phraseological_dict ORDER BY RAND() LIMIT 1;

-- Получить фразеологизмы по категории
SELECT * FROM phraseological_dict WHERE categories = 'animals' LIMIT 10;

-- Поиск по фразеологизму
SELECT * FROM phraseological_dict WHERE phrase LIKE '%вода%';

-- Получить фразеологизмы с происхождением
SELECT phrase, etymology FROM phraseological_dict WHERE etymology IS NOT NULL LIMIT 5;
```

## Возможные проблемы и решения

1. **Проблема с кодировкой**: Убедитесь, что база данных и таблицы используют `utf8mb4`
2. **Большой размер файла**: Если файл слишком большой для импорта через phpMyAdmin, используйте SSH или разделите файл
3. **Права доступа**: Убедитесь, что у пользователя есть права на создание таблиц и вставку данных

## Пересоздание базы данных

Если вам нужно пересоздать базу данных:

1. Установите Python (если еще не установлен)
2. Запустите скрипт генерации:
   ```bash
   python3 create_mysql_db.py
   ```

Это создаст новый файл `phraseological_dict.sql` с актуальными данными.

## Поддержка

Если возникнут проблемы с импортом на Timeweb, обратитесь в техническую поддержку Timeweb или проверьте документацию по импорту баз данных в их панели управления.