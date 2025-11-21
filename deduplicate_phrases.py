#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Скрипт для поиска и удаления дубликатов в table_phrases.json."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def normalize_phrase(phrase: str) -> str:
    """Нормализуем фразу: удаляем лишние пробелы и приводим к нижнему регистру."""
    return " ".join(phrase.lower().strip().split())


def merge_duplicate_entries(entries: List[Dict]) -> Dict:
    """Объединяет несколько записей в одну, собирая все уникальные данные."""
    base = entries[0]
    merged = {k: v for k, v in base.items() if k not in {"phrase", "meanings", "etymology", "source_url", "category"}}
    merged["phrase"] = " ".join(base.get("phrase", "").strip().split())

    # Meanings
    merged_meanings: List[str] = []
    seen_meanings = set()
    for entry in entries:
        for meaning in entry.get("meanings", []) or []:
            normalized = meaning.strip()
            if normalized and normalized not in seen_meanings:
                seen_meanings.add(normalized)
                merged_meanings.append(normalized)
    merged["meanings"] = merged_meanings

    # Etymology
    merged["etymology"] = ""
    for entry in entries:
        etym = (entry.get("etymology") or "").strip()
        if etym:
            merged["etymology"] = etym
            break

    # Categories
    categories: List[str] = []
    seen_categories = set()
    for entry in entries:
        category = (entry.get("category") or "").strip()
        if category and category not in seen_categories:
            seen_categories.add(category)
            categories.append(category)
    if len(categories) > 1:
        merged["category"] = ", ".join(categories)
    elif categories:
        merged["category"] = categories[0]
    else:
        merged["category"] = ""

    # Source URLs
    source_urls: List[str] = []
    seen_urls = set()
    for entry in entries:
        url = (entry.get("source_url") or "").strip()
        if url and url not in seen_urls:
            seen_urls.add(url)
            source_urls.append(url)
    if len(source_urls) > 1:
        merged["source_url"] = " | ".join(source_urls)
    elif source_urls:
        merged["source_url"] = source_urls[0]
    else:
        merged["source_url"] = ""

    return merged


def group_phrases(phrases: List[Dict]) -> Tuple[Dict[str, List[Dict]], List[str]]:
    """Группируем фразы по нормализованному ключу и сохраняем порядок появления."""
    groups: Dict[str, List[Dict]] = {}
    order: List[str] = []

    for entry in phrases:
        normalized = normalize_phrase(entry.get("phrase", ""))
        if normalized not in groups:
            groups[normalized] = []
            order.append(normalized)
        groups[normalized].append(entry)

    return groups, order


def find_and_remove_duplicates(input_path: Path, output_path: Path) -> Dict:
    """Анализирует файл, выводит статистику и записывает очищенную версию."""
    print("=" * 80)
    print("АНАЛИЗ И ОЧИСТКА ДУБЛИКАТОВ В table_phrases.json")
    print("=" * 80)
    print()

    with input_path.open("r", encoding="utf-8") as source_file:
        data = json.load(source_file)

    phrases = data.get("phrases", [])
    total_before = len(phrases)
    print(f"📊 Всего фразеологизмов до очистки: {total_before}")
    print()

    phrase_groups, order = group_phrases(phrases)

    duplicates: Dict[str, List[Dict]] = {}
    duplicates_order: List[str] = []
    for normalized in order:
        entries = phrase_groups[normalized]
        if len(entries) > 1:
            duplicates[normalized] = entries
            duplicates_order.append(normalized)

    num_duplicates = len(duplicates)
    total_duplicate_entries = sum(len(entries) - 1 for entries in duplicates.values())
    print(f"🔍 Найдено уникальных фраз с дубликатами: {num_duplicates}")
    print(f"🔍 Всего дублирующихся записей: {total_duplicate_entries}")
    print()

    if duplicates:
        print("=" * 80)
        print("СПИСОК ДУБЛИКАТОВ")
        print("=" * 80)
        print()
        for idx, normalized in enumerate(duplicates_order, 1):
            entries = duplicates[normalized]
            merged = merge_duplicate_entries(entries)
            print(f"{idx}. Фраза: '{merged['phrase']}'")
            print(f"   Количество повторений: {len(entries)}")
            print("   Варианты записей:")
            for variant_idx, entry in enumerate(entries, 1):
                print(f"      {variant_idx}) '{entry.get('phrase', '')}'")
                print(f"         Meanings: {entry.get('meanings', [])}")
                print(f"         Category: {entry.get('category', '')}")
                print(f"         Etymology: {'Есть' if entry.get('etymology') else 'Нет'}")
                print(f"         Source URL: {entry.get('source_url', '')}")
            print("   Объединенный результат:")
            print(f"      Meanings ({len(merged['meanings'])}): {merged['meanings']}")
            print(f"      Category: {merged.get('category', '')}")
            print(f"      Source URL: {merged.get('source_url', '')}")
            print(f"      Etymology: {'Есть' if merged.get('etymology') else 'Нет'}")
            print()

    cleaned_phrases: List[Dict] = []
    for normalized in order:
        cleaned_phrases.append(merge_duplicate_entries(phrase_groups[normalized]))

    total_after = len(cleaned_phrases)
    with output_path.open("w", encoding="utf-8") as cleaned_file:
        json.dump({"phrases": cleaned_phrases}, cleaned_file, ensure_ascii=False, indent=2)

    print("=" * 80)
    print("ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 80)
    print(f"📊 Всего фразеологизмов до очистки: {total_before}")
    print(f"🔍 Найдено уникальных фраз с дубликатами: {num_duplicates}")
    print(f"🗑️  Удалено дублирующихся записей: {total_duplicate_entries}")
    print(f"✅ Фразеологизмов после очистки: {total_after}")
    print(f"📝 Результат сохранен в: {output_path}")
    print()

    return {
        "total_before": total_before,
        "duplicates_found": num_duplicates,
        "duplicate_entries_removed": total_duplicate_entries,
        "total_after": total_after,
        "duplicates_detail": duplicates,
        "duplicates_order": duplicates_order,
    }


def generate_markdown_report(
    results: Dict,
    report_path: Path,
    *,
    main_file: Path,
    cleaned_file: Path,
    backup_file: Path,
) -> None:
    """Создает отчёт в формате Markdown со статистикой и списком дубликатов."""
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    lines: List[str] = [
        "# Отчёт об очистке дубликатов в table_phrases.json",
        "",
        f"**Дата выполнения:** {timestamp}",
        "**Скрипт:** `deduplicate_phrases.py`",
        "",
        "---",
        "",
        "## 📊 Статистика",
        "",
        "| Параметр | Значение |",
        "|----------|----------|",
        f"| **Всего фразеологизмов до очистки** | {results['total_before']} |",
        f"| **Найдено уникальных фраз с дубликатами** | {results['duplicates_found']} |",
        f"| **Всего дублирующихся записей удалено** | {results['duplicate_entries_removed']} |",
        f"| **Фразеологизмов после очистки** | {results['total_after']} |",
        "",
        "---",
        "",
        "## 🔍 Найденные дубликаты",
        "",
    ]

    duplicates_detail: Dict[str, List[Dict]] = results["duplicates_detail"]
    duplicates_order: List[str] = results["duplicates_order"]

    if not duplicates_detail:
        lines.append("Дубликаты не обнаружены.")
        lines.append("")
    else:
        for idx, normalized in enumerate(duplicates_order, 1):
            entries = duplicates_detail[normalized]
            merged = merge_duplicate_entries(entries)
            lines.append(f"### {idx}. Фраза: \"{merged['phrase']}\"")
            lines.append("")
            lines.append(f"**Количество повторений:** {len(entries)}")
            lines.append("")
            lines.append("#### Исходные варианты записей:")
            lines.append("")
            for variant_idx, entry in enumerate(entries, 1):
                lines.append(f"**Вариант {variant_idx}:**")
                lines.append(f"- **Phrase:** {entry.get('phrase', '')}")
                meanings = entry.get("meanings", []) or []
                if meanings:
                    lines.append("- **Meanings:**")
                    for meaning in meanings:
                        lines.append(f"  - {meaning}")
                else:
                    lines.append("- **Meanings:** _нет данных_")
                category = entry.get("category") or ""
                lines.append(f"- **Category:** {category if category else '_нет данных_'}")
                etymology = entry.get("etymology") or ""
                lines.append(f"- **Etymology:** {'Есть' if etymology.strip() else 'Нет'}")
                source = entry.get("source_url") or ""
                lines.append(f"- **Source URL:** {source if source else '_не указан_'}")
                lines.append("")

            lines.append("#### Объединённый результат:")
            lines.append("")
            merged_meanings = merged.get("meanings", [])
            if merged_meanings:
                lines.append("- **Meanings:**")
                for meaning in merged_meanings:
                    lines.append(f"  - {meaning}")
            else:
                lines.append("- **Meanings:** _нет данных_")
            merged_category = merged.get("category") or ""
            lines.append(f"- **Category:** {merged_category if merged_category else '_нет данных_'}")
            merged_etymology = merged.get("etymology") or ""
            if merged_etymology:
                lines.append(f"- **Etymology:** {merged_etymology}")
            else:
                lines.append("- **Etymology:** _нет данных_")
            merged_source = merged.get("source_url") or ""
            lines.append(f"- **Source URL:** {merged_source if merged_source else '_не указан_'}")
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.extend(
        [
            "## 📁 Сгенерированные файлы",
            "",
            f"1. **{main_file.name}** — очищенный основной файл",
            f"2. **{cleaned_file.name}** — резервная копия очищенного файла",
            f"3. **{backup_file.name}** — резервная копия исходных данных",
            "4. **DEDUPLICATION_REPORT.md** — данный отчёт",
            "",
            "---",
            "",
            "## 🔄 Повторный запуск",
            "",
            "При необходимости можно восстановить исходные данные из backup и повторно запустить скрипт:",
            "",
            "```bash",
            f"cp {backup_file.name} {main_file.name}",
            "python3 deduplicate_phrases.py",
            "```",
            "",
            "Скрипт автоматически создаст новую резервную копию, найдет дубликаты и обновит отчёт.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    input_path = Path("table_phrases.json")
    cleaned_path = Path("table_phrases_cleaned.json")
    backup_path = Path(f"table_phrases_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    report_path = Path("DEDUPLICATION_REPORT.md")

    results = find_and_remove_duplicates(input_path, cleaned_path)

    shutil.copy2(input_path, backup_path)
    print(f"💾 Создан backup исходного файла: {backup_path}")

    shutil.copy2(cleaned_path, input_path)
    print(f"✅ Исходный файл {input_path.name} заменен на очищенную версию")

    generate_markdown_report(
        results,
        report_path,
        main_file=input_path,
        cleaned_file=cleaned_path,
        backup_file=backup_path,
    )
    print(f"📝 Отчёт сохранен в: {report_path}")

    print("\n" + "=" * 80)
    print("✅ ОЧИСТКА ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 80)


if __name__ == "__main__":
    main()
