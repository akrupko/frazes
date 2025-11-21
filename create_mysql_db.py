#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate MySQL database from table_phrases.json
"""

import json
import os
import sys

def escape_sql_string(text):
    """Escape string for SQL"""
    if text is None:
        return 'NULL'
    # Replace single quotes and backslashes
    escaped = text.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"

def generate_sql_dump():
    """Generate SQL dump file from JSON data"""
    
    # Read JSON data
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    phrases = data['phrases']
    
    # Generate SQL content
    sql_content = []
    
    # Add header
    sql_content.append("-- MySQL dump for phraseological dictionary")
    sql_content.append("-- Generated from table_phrases.json")
    sql_content.append(f"-- Total phrases: {len(phrases)}")
    sql_content.append("")
    sql_content.append("SET NAMES utf8mb4;")
    sql_content.append("SET FOREIGN_KEY_CHECKS = 0;")
    sql_content.append("")
    
    # Drop table if exists
    sql_content.append("-- Drop table if exists")
    sql_content.append("DROP TABLE IF EXISTS `phraseological_dict`;")
    sql_content.append("")
    
    # Create table
    sql_content.append("-- Table structure for phraseological_dict")
    sql_content.append("CREATE TABLE `phraseological_dict` (")
    sql_content.append("  `id` int(11) NOT NULL AUTO_INCREMENT,")
    sql_content.append("  `phrase` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Фразеологизм',")
    sql_content.append("  `meaning` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Значение фразеологизма',")
    sql_content.append("  `etymology` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Происхождение фразеологизма',")
    sql_content.append("  `usage_example` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Пример использования фразеологизма в тексте',")
    sql_content.append("  `categories` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Категория фразеологизма',")
    sql_content.append("  `source_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Источник',")
    sql_content.append("  PRIMARY KEY (`id`),")
    sql_content.append("  UNIQUE KEY `phrase` (`phrase`),")
    sql_content.append("  KEY `categories` (`categories`)")
    sql_content.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Словарь фразеологизмов русского языка';")
    sql_content.append("")
    sql_content.append("-- Data for table phraseological_dict")
    sql_content.append("LOCK TABLES `phraseological_dict` WRITE;")
    sql_content.append("")
    
    # Insert data
    for i, phrase_data in enumerate(phrases, 1):
        phrase = phrase_data['phrase']
        meaning = phrase_data['meanings'][0] if phrase_data['meanings'] else ''
        etymology = phrase_data.get('etymology', None)
        categories = phrase_data.get('category', '')
        source_url = phrase_data.get('source_url', None)
        
        # Handle empty category
        if categories == '':
            categories = None
            
        sql_line = f"INSERT INTO `phraseological_dict` (`id`, `phrase`, `meaning`, `etymology`, `usage_example`, `categories`, `source_url`) VALUES ({i}, {escape_sql_string(phrase)}, {escape_sql_string(meaning)}, {escape_sql_string(etymology)}, NULL, {escape_sql_string(categories)}, {escape_sql_string(source_url)});"
        sql_content.append(sql_line)
    
    sql_content.append("")
    sql_content.append("UNLOCK TABLES;")
    sql_content.append("SET FOREIGN_KEY_CHECKS = 1;")
    
    # Write SQL dump
    with open('phraseological_dict.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_content))
    
    print(f"SQL dump created successfully: phraseological_dict.sql")
    print(f"Total phrases processed: {len(phrases)}")
    
    return len(phrases)

def main():
    """Main function to generate SQL dump"""
    
    # Database configuration - modify these settings as needed
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'charset': 'utf8mb4'
    }
    
    print("Note: For direct database import, install mysql-connector-python:")
    print("pip install mysql-connector-python")
    print("Then uncomment the create_database_and_import() call below.")
    print()

if __name__ == "__main__":
    print("Generating MySQL database from table_phrases.json...")
    
    # Check if JSON file exists
    if not os.path.exists('table_phrases.json'):
        print("Error: table_phrases.json not found!")
        sys.exit(1)
    
    # Generate SQL dump
    phrase_count = generate_sql_dump()
    
    print(f"\nGenerated files:")
    print("1. phraseological_dict.sql - SQL dump ready for import")
    print(f"\nDatabase structure:")
    print("- Table: phraseological_dict")
    print("- Columns: id, phrase, meaning, etymology, usage_example, categories, source_url")
    print(f"- Total records: {phrase_count}")
    print("\nReady for import to Timeweb or any MySQL hosting!")