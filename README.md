# 🔍 JSON Compare MCP Server

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Smithery](https://img.shields.io/badge/Smithery-Deploy%20Ready-orange.svg)

**Derinlemesine ve sıra-bağımsız JSON karşılaştırma MCP tool'u**

*İki JSON dosyasını akıllıca karşılaştırın, farklılıkları tespit edin!*

[🎯 Hızlı Başlangıç](#-hızlı-başlangıç) • [📦 Özellikler](#-özellikler) • [🚀 Kullanım](#-kullanım) • [🧪 Test](#-test)

</div>

---

## ✨ Özellikler

- 🔍 **Derinlemesine Karşılaştırma** - Nested objeler ve array'ler dahil tüm seviyeler
- 🔀 **Sıra-Bağımsız** - Property ve obje sıralaması önemli değil
- 📊 **Detaylı Raporlama** - Eksik, fazla ve farklı değerlerin detaylı raporu
- 🎯 **Path Tracking** - Her farkın tam konumu (örn: `root.user.settings.theme`)
- 🏷️ **Tip Kontrolü** - Değer tiplerini de karşılaştırır
- ⚡ **Hızlı ve Verimli** - Optimize edilmiş recursive algoritma

## 🎯 Hızlı Başlangıç

### 1. Kurulum

```bash
git clone https://github.com/yourusername/json-compare-mcp.git
cd json-compare-mcp
pip install -r requirements.txt
```

### 2. MCP Server'ı Başlat

```bash
python server.py
```

### 3. Test Et

```bash
python test_compare.py
```

## 📦 Ne İçeriyor?

```
json-compare-mcp/
├── 🐍 app.py              # JSON karşılaştırma implementasyonu
├── 🚀 server.py           # MCP server yapılandırması
├── 🧪 test_compare.py     # Test suite
├── 📋 requirements.txt    # Python bağımlılıkları
├── 🐳 Dockerfile          # Container yapılandırması
├── ⚙️ smithery.yaml       # Smithery deployment config
└── 📁 test_samples/       # Örnek JSON dosyaları
    ├── file1.json
    ├── file2.json
    └── file3_different.json
```

## 🚀 Kullanım

### MCP Tool: `compare_json`

```python
# İki JSON string'ini karşılaştır
compare_json(
    json1='{"name": "Ahmet", "age": 30, "city": "Istanbul"}',
    json2='{"age": 30, "city": "Istanbul", "name": "Ahmet"}'
)
```

**Not:** Artık dosya yolu değil, direkt JSON string kullanın!

### Çıktı Formatı

```json
{
  "status": "different",
  "total_differences": 11,
  "differences": [
    {
      "type": "missing_key",
      "path": "root.user.settings.language",
      "key": "language",
      "file1_value": "tr",
      "message": "Key 'language' exists in file1 but missing in file2"
    },
    {
      "type": "value_mismatch",
      "path": "root.user.name",
      "file1_value": "Ahmet Yılmaz",
      "file2_value": "Mehmet Demir",
      "message": "Value mismatch at 'root.user.name'"
    }
  ],
  "summary": {
    "missing_keys": 1,
    "extra_keys": 2,
    "value_mismatches": 8,
    "type_mismatches": 0
  }
}
```

## 🔍 Karşılaştırma Mantığı

### Seviye 1: Üst Seviye Obje Karşılaştırma

- ✅ Her iki JSON'daki üst seviye objeleri/anahtarları tespit et
- ✅ **SIRALAMA ÖNEMLİ DEĞİL** - Objeler farklı sırada olabilir
- ✅ Eksik/fazla objeleri tespit et ve uyar
- ✅ Eşleşen objeler için Seviye 2'ye geç

### Seviye 2: İç Nesne/Property Karşılaştırma

- ✅ Tüm property'leri karşılaştır
- ✅ **SIRALAMA ÖNEMLİ DEĞİL** - Property'ler farklı sırada olabilir
- ✅ Property varlığı, tip ve içerik kontrolü
- ✅ Array'ler için sıra-bağımsız karşılaştırma

### Fark Tipleri

| Tip | Açıklama |
|-----|----------|
| `missing_key` | Anahtar file1'de var, file2'de yok |
| `extra_key` | Anahtar file2'de var, file1'de yok |
| `value_mismatch` | Değerler farklı |
| `type_mismatch` | Veri tipleri farklı |

## 🧪 Test

### Test Suite'i Çalıştır

```bash
python test_compare.py
```

### Test Senaryoları

1. **Sıra-bağımsız test**: Aynı içerik, farklı sıralama → `identical`
2. **Farklılık tespiti**: Farklı değerler → detaylı fark raporu
3. **Kendisi ile**: Aynı dosya → `identical`

### Test Çıktısı

```
✅ Test 1 - Sıra-bağımsız: BAŞARILI
✅ Test 2 - Farklılık tespiti: BAŞARILI
✅ Test 3 - Aynı dosya: BAŞARILI

🔍 Test 2 Detayları:
   - Eksik anahtarlar: 1
   - Fazla anahtarlar: 2
   - Değer uyuşmazlıkları: 8
   - Tip uyuşmazlıkları: 0
   - Toplam fark: 11
```

## 🛠️ Geliştirme

### Yeni Tool Eklemek

[app.py](app.py) dosyasına yeni fonksiyon ekle:

```python
def myNewTool(param: str) -> str:
    # Your logic
    return result
```

[server.py](server.py) dosyasına MCP tool olarak kaydet:

```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Tool açıklaması"""
    return myNewTool(param)
```

## 🚀 Deployment

### Smithery Deployment

1. Repository'yi GitHub'a push et
2. Smithery'de repository'yi bağla
3. Tek tıkla deploy et! 🎉

### Docker Deployment

```bash
docker build -t json-compare-mcp .
docker run -p 8000:8000 json-compare-mcp
```

### Manuel Deployment

```bash
pip install -r requirements.txt
python server.py
```

## 📋 Gereksinimler

- Python 3.11+
- mcp
- requests

## 🤝 Katkıda Bulunma

1. 🍴 Fork et
2. 🌱 Feature branch oluştur
3. 💻 Değişiklikleri yap
4. 🧪 Test et
5. 📝 Pull request gönder

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

<div align="center">

**Made with ❤️ for better JSON comparison**

*Sıra-bağımsız, derinlemesine, güvenilir* 🚀

</div>
