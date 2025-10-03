import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from middleware import SmitheryConfigMiddleware
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
async def compare_json(json1: str, json2: str) -> str:
    """
    İki JSON'u derinlemesine ve sıra-bağımsız (order-agnostic) şekilde karşılaştırır.

    Bu tool:
    - Üst seviye objeleri/anahtarları karşılaştırır (sıralama önemli değil)
    - Her objenin içindeki property'leri derinlemesine kontrol eder
    - Eksik, fazla veya farklı anahtarları tespit eder
    - Değer tiplerini ve içeriklerini kontrol eder
    - Nested array'ler ve objeler için recursive karşılaştırma yapar

    Args:
        json1: İlk JSON string (örn: '{"name": "John", "age": 30}')
        json2: İkinci JSON string (örn: '{"age": 30, "name": "John"}')

    Returns:
        Karşılaştırma sonuçlarını içeren detaylı JSON raporu:
        - status: "identical" veya "different"
        - total_differences: Toplam fark sayısı
        - differences: Tespit edilen tüm farkların listesi
        - summary: Fark tiplerinin özet istatistikleri

    Example:
        compare_json('{"a": 1}', '{"a": 2}')
        # Returns: differences showing value mismatch at "root.a"
    """
    from app import compare_json_strings
    result = compare_json_strings(json1, json2)
    return json.dumps(result, indent=2, ensure_ascii=False)


# Your another awsome tools can be added here
# @mcp.tool()
# async def another_awsome_tool(param: str) -> str:
#     """
#     Get better at AI.
#     """
#     # Do some awsome processing here
#     return "You are getting better at AI!"


def main():
    """Main entry point supporting both HTTP and stdio transports"""
    transport_mode = os.getenv("TRANSPORT", "stdio")

    if transport_mode == "http":
        # HTTP transport for Smithery deployment
        app = mcp.streamable_http_app()

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )

        # Add Smithery config middleware
        app = SmitheryConfigMiddleware(app)

        # Start HTTP server
        port = int(os.environ.get("PORT", 8081))
        print(f"Starting HTTP server on port {port}...")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")

    else:
        # STDIO transport for local development
        print("Starting STDIO server...")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()