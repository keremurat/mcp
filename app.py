import requests
import json
from typing import Dict, List, Any, Tuple

def dummyTool(param: str) -> str:
    """
    Method description here.
    """
    # Do Some Processing Here
    return f"Your tool will return processed {param}"


def compare_json_files(file1_path: str, file2_path: str) -> Dict[str, Any]:
    """
    İki JSON dosyasını derinlemesine ve sıra-bağımsız şekilde karşılaştırır.

    Args:
        file1_path: İlk JSON dosyasının yolu
        file2_path: İkinci JSON dosyasının yolu

    Returns:
        Karşılaştırma sonuçlarını içeren detaylı rapor
    """
    try:
        # JSON dosyalarını oku
        with open(file1_path, 'r', encoding='utf-8') as f1:
            json1 = json.load(f1)

        with open(file2_path, 'r', encoding='utf-8') as f2:
            json2 = json.load(f2)

        # Karşılaştırmayı gerçekleştir
        differences = []
        compare_objects(json1, json2, "", differences)

        # Sonuç raporunu oluştur
        result = {
            "status": "identical" if len(differences) == 0 else "different",
            "total_differences": len(differences),
            "differences": differences,
            "summary": {
                "missing_keys": sum(1 for d in differences if d["type"] == "missing_key"),
                "extra_keys": sum(1 for d in differences if d["type"] == "extra_key"),
                "value_mismatches": sum(1 for d in differences if d["type"] == "value_mismatch"),
                "type_mismatches": sum(1 for d in differences if d["type"] == "type_mismatch")
            }
        }

        return result

    except FileNotFoundError as e:
        return {
            "status": "error",
            "error": f"Dosya bulunamadı: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"JSON parse hatası: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Beklenmeyen hata: {str(e)}"
        }


def compare_objects(obj1: Any, obj2: Any, path: str, differences: List[Dict]) -> None:
    """
    İki objeyi derinlemesine karşılaştırır (sıra-bağımsız).

    Args:
        obj1: İlk obje
        obj2: İkinci obje
        path: Mevcut obje yolu (örn: "root.user.name")
        differences: Tespit edilen farkların listesi
    """
    current_path = path if path else "root"

    # Tip kontrolü
    if type(obj1) != type(obj2):
        differences.append({
            "type": "type_mismatch",
            "path": current_path,
            "file1_type": type(obj1).__name__,
            "file2_type": type(obj2).__name__,
            "file1_value": str(obj1),
            "file2_value": str(obj2)
        })
        return

    # Dictionary karşılaştırması
    if isinstance(obj1, dict):
        # Dosya 1'deki anahtarlar
        keys1 = set(obj1.keys())
        keys2 = set(obj2.keys())

        # Eksik anahtarlar (dosya 2'de yok)
        missing_keys = keys1 - keys2
        for key in missing_keys:
            differences.append({
                "type": "missing_key",
                "path": f"{current_path}.{key}",
                "key": key,
                "file1_value": obj1[key],
                "message": f"Key '{key}' exists in file1 but missing in file2"
            })

        # Fazla anahtarlar (dosya 1'de yok)
        extra_keys = keys2 - keys1
        for key in extra_keys:
            differences.append({
                "type": "extra_key",
                "path": f"{current_path}.{key}",
                "key": key,
                "file2_value": obj2[key],
                "message": f"Key '{key}' exists in file2 but missing in file1"
            })

        # Ortak anahtarları karşılaştır
        common_keys = keys1 & keys2
        for key in common_keys:
            new_path = f"{current_path}.{key}"
            compare_objects(obj1[key], obj2[key], new_path, differences)

    # List karşılaştırması (içerik bazlı, sıra-bağımsız)
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            differences.append({
                "type": "value_mismatch",
                "path": current_path,
                "detail": "array_length_mismatch",
                "file1_length": len(obj1),
                "file2_length": len(obj2),
                "file1_value": obj1,
                "file2_value": obj2
            })
            return

        # Eğer liste primitive değerler içeriyorsa, sıra-bağımsız karşılaştır
        if obj1 and not isinstance(obj1[0], (dict, list)):
            if sorted(obj1) != sorted(obj2):
                differences.append({
                    "type": "value_mismatch",
                    "path": current_path,
                    "detail": "array_content_mismatch",
                    "file1_value": obj1,
                    "file2_value": obj2
                })
        else:
            # Nested objeler için sıralı karşılaştırma (her eleman için)
            for idx, (item1, item2) in enumerate(zip(obj1, obj2)):
                new_path = f"{current_path}[{idx}]"
                compare_objects(item1, item2, new_path, differences)

    # Primitive değer karşılaştırması
    else:
        if obj1 != obj2:
            differences.append({
                "type": "value_mismatch",
                "path": current_path,
                "file1_value": obj1,
                "file2_value": obj2,
                "message": f"Value mismatch at '{current_path}'"
            })