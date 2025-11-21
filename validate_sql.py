#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation script for the generated SQL dump
"""

import re

def validate_sql_dump():
    """Validate the SQL dump file"""
    
    print("Валидация SQL дампа...")
    
    with open('phraseological_dict.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for basic SQL structure
    checks = [
        ("CREATE TABLE", "Проверка создания таблицы", "CREATE TABLE `phraseological_dict`"),
        ("PRIMARY KEY", "Проверка первичного ключа", "PRIMARY KEY (`id`)"),
        ("AUTO_INCREMENT", "Проверка автоинкремента", "AUTO_INCREMENT"),
        ("utf8mb4", "Проверка кодировки", "utf8mb4"),
        ("INSERT INTO", "Проверка вставки данных", "INSERT INTO `phraseological_dict`"),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, description, pattern in checks:
        if pattern in content:
            print(f"✅ {description}: Пройдено")
            passed += 1
        else:
            print(f"❌ {description}: Не найдено")
    
    # Count INSERT statements
    insert_count = len(re.findall(r'INSERT INTO `phraseological_dict`', content))
    print(f"📊 Найдено INSERT statements: {insert_count}")
    
    # Check for special characters handling
    if "\\'" in content:
        print("✅ Проверка экранирования кавычек: Пройдено")
    else:
        print("⚠️  Проверка экранирования кавычек: Не найдено экранированных кавычек")
    
    # Final result
    print(f"\nРезультат валидации: {passed}/{total} проверок пройдено")
    
    if passed == total and insert_count == 1140:
        print("🎉 SQL дамп прошел все проверки!")
        return True
    else:
        print("⚠️  Обнаружены проблемы в SQL дампе")
        return False

if __name__ == "__main__":
    validate_sql_dump()