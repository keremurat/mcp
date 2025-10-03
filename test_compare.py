#!/usr/bin/env python3
"""
JSON Karşılaştırma MCP Tool Test Script
"""
import json
from app import compare_json_files

def print_result(title: str, result: dict):
    """Test sonucunu formatla ve yazdır"""
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print('='*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()


def main():
    print("🔍 JSON Karşılaştırma MCP Tool - Test Suite")
    print("=" * 60)

    # Test 1: İdentik dosyalar (farklı sıralamada)
    print("\n📋 Test 1: Aynı içerik, farklı sıralama")
    result1 = compare_json_files(
        "test_samples/file1.json",
        "test_samples/file2.json"
    )
    print_result("Sıra-bağımsız karşılaştırma (aynı olmalı)", result1)

    # Test 2: Farklı dosyalar
    print("\n📋 Test 2: Farklı içerik")
    result2 = compare_json_files(
        "test_samples/file1.json",
        "test_samples/file3_different.json"
    )
    print_result("Farklılıkları tespit etme", result2)

    # Test 3: Aynı dosyayla karşılaştırma
    print("\n📋 Test 3: Aynı dosya ile karşılaştırma")
    result3 = compare_json_files(
        "test_samples/file1.json",
        "test_samples/file1.json"
    )
    print_result("Kendisiyle karşılaştırma (identical olmalı)", result3)

    # Test Özeti
    print("\n" + "="*60)
    print("📊 TEST ÖZETİ")
    print("="*60)
    print(f"✅ Test 1 - Sıra-bağımsız: {'BAŞARILI' if result1['status'] == 'identical' else 'BAŞARISIZ'}")
    print(f"✅ Test 2 - Farklılık tespiti: {'BAŞARILI' if result2['status'] == 'different' and result2['total_differences'] > 0 else 'BAŞARISIZ'}")
    print(f"✅ Test 3 - Aynı dosya: {'BAŞARILI' if result3['status'] == 'identical' else 'BAŞARISIZ'}")
    print()

    if result2['status'] == 'different':
        print(f"\n🔍 Test 2 Detayları:")
        print(f"   - Eksik anahtarlar: {result2['summary']['missing_keys']}")
        print(f"   - Fazla anahtarlar: {result2['summary']['extra_keys']}")
        print(f"   - Değer uyuşmazlıkları: {result2['summary']['value_mismatches']}")
        print(f"   - Tip uyuşmazlıkları: {result2['summary']['type_mismatches']}")
        print(f"   - Toplam fark: {result2['total_differences']}")


if __name__ == "__main__":
    main()
