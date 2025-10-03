from mcp.server.fastmcp import FastMCP
from app import dummyTool, compare_json_files
import json

# Initialize MCP server
mcp = FastMCP("json-compare-mcp")

@mcp.tool()
async def dummy_tool(param: str) -> str:
    """
    Definition of a tool here.
    """
    # Do some awsome processing here
    awsome_response = dummyTool(param)
    if not awsome_response:
        return "No awsome response found."

    return awsome_response


@mcp.tool()
async def compare_json(file1_path: str, file2_path: str) -> str:
    """
    İki JSON dosyasını derinlemesine ve sıra-bağımsız (order-agnostic) şekilde karşılaştırır.

    Bu tool:
    - Üst seviye objeleri/anahtarları karşılaştırır (sıralama önemli değil)
    - Her objenin içindeki property'leri derinlemesine kontrol eder
    - Eksik, fazla veya farklı anahtarları tespit eder
    - Değer tiplerini ve içeriklerini kontrol eder
    - Nested array'ler ve objeler için recursive karşılaştırma yapar

    Args:
        file1_path: İlk JSON dosyasının tam yolu
        file2_path: İkinci JSON dosyasının tam yolu

    Returns:
        Karşılaştırma sonuçlarını içeren detaylı JSON raporu:
        - status: "identical" veya "different"
        - total_differences: Toplam fark sayısı
        - differences: Tespit edilen tüm farkların listesi
        - summary: Fark tiplerinin özet istatistikleri
    """
    result = compare_json_files(file1_path, file2_path)
    return json.dumps(result, indent=2, ensure_ascii=False)


# Your another awsome tools can be added here
# @mcp.tool()
# async def another_awsome_tool(param: str) -> str:
#     """
#     Get better at AI.
#     """
#     # Do some awsome processing here
#     return "You are getting better at AI!"


if __name__ == "__main__":
    mcp.run(transport="stdio")