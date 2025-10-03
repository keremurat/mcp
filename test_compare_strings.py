#!/usr/bin/env python3
"""
JSON Karşılaştırma MCP Tool Test Script (String-based)
"""
import json
from app import compare_json_strings

def print_result(title: str, result: dict):
    """Test sonucunu formatla ve yazdır"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print('='*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()


def main():
    print("🔍 JSON Karşılaştırma MCP Tool - String Test Suite")
    print("=" * 60)

    # Test 1: İdentik JSON'lar (farklı sıralamada)
    json1 = '''
    {
        "user": {
            "id": 12345,
            "name": "Ahmet",
            "email": "ahmet@example.com"
        },
        "active": true
    }
    '''

    json2 = '''
    {
        "active": true,
        "user": {
            "email": "ahmet@example.com",
            "name": "Ahmet",
            "id": 12345
        }
    }
    '''

    print("\n📋 Test 1: Aynı içerik, farklı sıralama")
    result1 = compare_json_strings(json1, json2)
    print_result("Sıra-bağımsız karşılaştırma (identical olmalı)", result1)

    # Test 2: Farklı değerler
    json3 = '''
    {
        "user": {
            "id": 12345,
            "name": "Mehmet",
            "email": "mehmet@example.com"
        },
        "active": false
    }
    '''

    print("\n📋 Test 2: Farklı değerler")
    result2 = compare_json_strings(json1, json3)
    print_result("Farklılık tespiti", result2)

    # Test 3: Eksik ve fazla anahtarlar
    json4 = '''
    {
        "user": {
            "id": 12345,
            "name": "Ahmet"
        },
        "active": true,
        "newField": "extra"
    }
    '''

    print("\n📋 Test 3: Eksik ve fazla anahtarlar")
    result3 = compare_json_strings(json1, json4)
    print_result("Eksik/Fazla anahtar tespiti", result3)

    # Test 4: Array karşılaştırma
    json5 = '{"items": [1, 2, 3], "tags": ["a", "b", "c"]}'
    json6 = '{"items": [3, 2, 1], "tags": ["c", "b", "a"]}'

    print("\n📋 Test 4: Array karşılaştırma (sıra-bağımsız)")
    result4 = compare_json_strings(json5, json6)
    print_result("Array içerik karşılaştırma", result4)

    # Test 5: Geçersiz JSON
    json7 = '{"invalid": json}'

    print("\n📋 Test 5: Geçersiz JSON")
    result5 = compare_json_strings(json7, json1)
    print_result("Hata yönetimi", result5)

    # Test Özeti
    print("\n" + "="*60)
    print("📊 TEST ÖZETİ")
    print("="*60)
    print(f"✅ Test 1 - Sıra-bağımsız: {'BAŞARILI' if result1['status'] == 'identical' else 'BAŞARISIZ'}")
    print(f"✅ Test 2 - Farklılık tespiti: {'BAŞARILI' if result2['status'] == 'different' else 'BAŞARISIZ'}")
    print(f"✅ Test 3 - Eksik/Fazla: {'BAŞARILI' if result3['status'] == 'different' else 'BAŞARISIZ'}")
    print(f"✅ Test 4 - Array: {'BAŞARILI' if result4['status'] == 'identical' else 'BAŞARISIZ'}")
    print(f"✅ Test 5 - Hata yönetimi: {'BAŞARILI' if result5['status'] == 'error' else 'BAŞARISIZ'}")
    print()


if __name__ == "__main__":
    main()
