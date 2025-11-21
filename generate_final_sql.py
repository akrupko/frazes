#!/usr/bin/env python3
"""
Generate final SQL dump with improved usage examples.
"""

import json
from pathlib import Path
from datetime import datetime

def escape_sql(value):
    """Escape value for SQL."""
    if value is None:
        return 'NULL'
    return "'" + str(value).replace("'", "\\'").replace("\\", "\\\\") + "'"

def generate_sql_dump():
    """Generate SQL dump from improved JSON data."""
    input_file = Path('table_phrases_improved.json')
    output_file = Path('phraseological_dict_final.sql')
    
    print(f"📂 Loading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    phrases = data['phrases']
    
    print(f"📊 Processing {len(phrases)} phraseological units...")
    
    sql_lines = [
        "-- MySQL dump for phraseological dictionary",
        "-- Generated with filled usage examples",
        f"-- Total phrases: {len(phrases)}",
        f"-- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "SET NAMES utf8mb4;",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "",
        "-- Drop table if exists",
        "DROP TABLE IF EXISTS `phraseological_dict`;",
        "",
        "-- Table structure for phraseological_dict",
        "CREATE TABLE `phraseological_dict` (",
        "  `id` int(11) NOT NULL AUTO_INCREMENT,",
        "  `phrase` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Фразеологизм',",
        "  `meaning` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Значение фразеологизма',",
        "  `etymology` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Происхождение фразеологизма',",
        "  `usage_example` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Пример использования фразеологизма в тексте',",
        "  `categories` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Категория фразеологизма',",
        "  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Источник',",
        "  PRIMARY KEY (`id`),",
        "  UNIQUE KEY `phrase` (`phrase`),",
        "  KEY `categories` (`categories`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Словарь фразеологизмов русского языка';",
        "",
        "-- Data for table phraseological_dict",
        "LOCK TABLES `phraseological_dict` WRITE;",
    ]
    
    # Add INSERT statements
    for i, phrase_data in enumerate(phrases, 1):
        meaning = '; '.join(phrase_data.get('meanings', []))
        
        sql_lines.append(
            f"INSERT INTO `phraseological_dict` (`id`, `phrase`, `meaning`, `etymology`, `usage_example`, `categories`, `source_url`) VALUES ({i}, {escape_sql(phrase_data['phrase'])}, {escape_sql(meaning)}, {escape_sql(phrase_data.get('etymology', ''))}, {escape_sql(phrase_data.get('usage_example'))}, {escape_sql(phrase_data.get('category', ''))}, {escape_sql(phrase_data.get('source_url', ''))});"
        )
    
    sql_lines.extend([
        "",
        "UNLOCK TABLES;",
        "",
        "SET FOREIGN_KEY_CHECKS = 1;"
    ])
    
    # Write SQL dump
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines))
    
    print(f"💾 SQL dump saved to {output_file}")
    
    # Generate report
    with_examples = sum(1 for p in phrases if p.get('usage_example'))
    
    print("\n" + "="*60)
    print("📊 FINAL REPORT")
    print("="*60)
    print(f"Total phraseological units: {len(phrases)}")
    print(f"With usage examples: {with_examples}")
    print(f"Without examples: {len(phrases) - with_examples}")
    print(f"Coverage: {with_examples/len(phrases)*100:.1f}%")
    print(f"SQL file size: {output_file.stat().st_size / 1024:.1f} KB")
    print("="*60)
    
    return output_file

if __name__ == "__main__":
    generate_sql_dump()