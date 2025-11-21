#!/usr/bin/env python3
"""
Improve usage examples for better grammar and context.

This script fixes grammatical issues in the generated examples.
"""

import json
import re
from pathlib import Path

def improve_example(phrase: str, example: str) -> str:
    """Improve example grammar and context."""
    
    # Handle phrases that start with conjunctions
    if phrase.startswith(("А ", "Но ", "И ", "Да ")):
        # These phrases should be used as-is, not embedded
        if f" {phrase.lower()}," in example:
            example = example.replace(f" {phrase.lower()},", f", {phrase.lower()},")
        elif f" {phrase.lower()} " in example:
            example = example.replace(f" {phrase.lower()} ", f", {phrase.lower()} ")
    
    # Fix common grammatical issues
    example = example.replace("  ", " ")  # Double spaces
    
    # Handle phrases that are questions
    if phrase.endswith("?"):
        if f" {phrase.lower()}" in example:
            example = example.replace(f" {phrase.lower()}", f", {phrase.lower()}")
    
    # Handle phrases that are already complete sentences
    if len(phrase.split()) > 3 and any(char in phrase for char in ".!?"):
        if f" {phrase.lower()}" in example:
            example = example.replace(f" {phrase.lower()}", f", {phrase}")
    
    return example.strip()

def main():
    """Main function to improve examples."""
    print("🔧 Improving usage examples...")
    
    # Load the data
    input_file = Path('table_phrases_with_examples.json')
    output_file = Path('table_phrases_improved.json')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    phrases = data['phrases']
    improved_count = 0
    
    for i, phrase_data in enumerate(phrases):
        phrase = phrase_data['phrase']
        example = phrase_data.get('usage_example', '')
        
        if example:
            improved_example = improve_example(phrase, example)
            if improved_example != example:
                phrase_data['usage_example'] = improved_example
                improved_count += 1
                print(f"[{i+1:4d}] Improved: '{phrase}'")
    
    # Save improved data
    output_data = {
        'phrases': phrases,
        'metadata': {
            **data.get('metadata', {}),
            'improved_examples': improved_count,
            'improved_at': '2024-01-20 00:00:00'
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Improved {improved_count} examples")
    print(f"💾 Saved to {output_file}")

if __name__ == "__main__":
    main()