"""
Fitness Function para Latencia de Búsqueda
Objetivo: Medir latencia end-to-end del proceso de búsqueda de papers
"""
import asyncio
import aiohttp
import argparse
import time
import json
import statistics
from datetime import datetime
from typing import List, Dict
import random
import os

class SearchPerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.search_queries = [
            "machine learning", "deep learning", "computer vision", "natural language processing",
            "artificial intelligence", "neural networks", "data science", "algorithms",
            "cybersecurity", "blockchain", "quantum computing", "cloud computing",
            "software engineering", "database", "web development", "mobile apps",
            "internet of things", "big data", "data mining", "pattern recognition"
        ]
        self.author_queries = [
            "Smith", "Johnson", "García", "Chen", "López", "Wang", "Brown", "Davis",
            "Wilson", "Miller", "Taylor", "Anderson", "Thomas", "Jackson", "White"
        ]
    
    async def search_papers(self, session: aiohttp.ClientSession, query: str, limit: int = 10) -> Dict:
        """Buscar papers y medir latencia end-to-end"""
        start_time = time.time()
        
        params = {
            "q": query,
            "limit": limit,
            "offset": 0
        }
        
        try:
            async with session.get(
                f"{self.base_url}/api/v1/search/papers",
                params=params,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                
                response_data = await response.json() if response.status == 200 else {}
                
                return {
                    "operation": "search_papers",
                    "query": query,
                    "status_code": response.status,
                    "latency_ms": latency_ms,
                    "success": response.status == 200,
                    "results_count": len(response_data.get("results", [])),
                    "total_results": response_data.get("total", 0),
                    "timestamp": datetime.now().isoformat(),
                    "limit": limit
                }
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            return {
                "operation": "search_papers",
                "query": query,
                "status_code": 0,
                "latency_ms": latency_ms,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "limit": limit
            }
    
    async def search_authors(self, session: aiohttp.ClientSession, query: str, limit: int = 10) -> Dict:
        """Buscar por autor y medir latencia"""
        start_time = time.time()
        
        params = {
            "q": query,
            "limit": limit,
            "offset": 0
        }
        
        try:
            async with session.get(
                f"{self.base_url}/api/v1/search/authors",
                params=params,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                
                response_data = await response.json() if response.status == 200 else {}
                
                return {
                    "operation": "search_authors",
                    "query": query,
                    "status_code": response.status,
                    "latency_ms": latency_ms,
                    "success": response.status == 200,
                    "results_count": len(response_data.get("results", [])),
                    "total_results": response_data.get("total", 0),
                    "timestamp": datetime.now().isoformat(),
                    "limit": limit
                }
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            return {
                "operation": "search_authors",
                "query": query,
                "status_code": 0,
                "latency_ms": latency_ms,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "limit": limit
            }
    
    async def get_suggestions(self, session: aiohttp.ClientSession, query: str) -> Dict:
        """Obtener sugerencias de búsqueda"""
        start_time = time.time()
        
        params = {"q": query}
        
        try:
            async with session.get(
                f"{self.base_url}/api/v1/search/suggestions",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                
                response_data = await response.json() if response.status == 200 else []
                
                return {
                    "operation": "get_suggestions",
                    "query": query,
                    "status_code": response.status,
                    "latency_ms": latency_ms,
                    "success": response.status == 200,
                    "suggestions_count": len(response_data),
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            return {
                "operation": "get_suggestions",
                "query": query,
                "status_code": 0,
                "latency_ms": latency_ms,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def search_external_apis(self, session: aiohttp.ClientSession, query: str) -> Dict:
        """Buscar en APIs externas mock"""
        start_time = time.time()
        
        params = {
            "q": query,
            "limit_per_source": 3
        }
        
        try:
            async with session.get(
                f"{self.base_url}/api/v1/external/papers",
                params=params,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                
                response_data = await response.json() if response.status == 200 else []
                
                total_papers = sum(len(source.get("papers", [])) for source in response_data)
                
                return {
                    "operation": "search_external",
                    "query": query,
                    "status_code": response.status,
                    "latency_ms": latency_ms,
                    "success": response.status == 200,
                    "sources_count": len(response_data),
                    "total_papers": total_papers,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            return {
                "operation": "search_external",
                "query": query,
                "status_code": 0,
                "latency_ms": latency_ms,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def mixed_search_operations(self, session: aiohttp.ClientSession, user_id: int) -> List[Dict]:
        """Realizar operaciones mixtas de búsqueda (flujo completo)"""
        results = []
        
        # Seleccionar queries aleatorias
        paper_query = random.choice(self.search_queries)
        author_query = random.choice(self.author_queries)
        
        # 1. Búsqueda de papers
        paper_search = await self.search_papers(session, paper_query, random.randint(5, 15))
        results.append(paper_search)
        
        # 2. Búsqueda por autor
        author_search = await self.search_authors(session, author_query, random.randint(5, 10))
        results.append(author_search)
        
        # 3. Obtener sugerencias
        suggestions = await self.get_suggestions(session, paper_query[:5])
        results.append(suggestions)
        
        # 4. Búsqueda en APIs externas (ocasionalmente)
        if random.random() < 0.3:  # 30% de probabilidad
            external_search = await self.search_external_apis(session, paper_query)
            results.append(external_search)
        
        return results
    
    async def run_concurrent_test(self, concurrent_users: int, duration_seconds: int) -> List[Dict]:
        """Ejecutar prueba con usuarios concurrentes"""
        print(f"🔍 Iniciando prueba de búsqueda con {concurrent_users} usuarios concurrentes por {duration_seconds}s")
        
        connector = aiohttp.TCPConnector(limit=concurrent_users * 2)
        async with aiohttp.ClientSession(connector=connector) as session:
            start_time = time.time()
            all_results = []
            
            while time.time() - start_time < duration_seconds:
                # Crear tasks para usuarios concurrentes
                tasks = []
                for i in range(concurrent_users):
                    task = asyncio.create_task(
                        self.mixed_search_operations(session, i + int(time.time()))
                    )
                    tasks.append(task)
                
                # Ejecutar todas las tareas concurrentemente
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Procesar resultados
                for result in batch_results:
                    if isinstance(result, Exception):
                        error_result = {
                            "operation": "batch_error",
                            "status_code": 0,
                            "latency_ms": 0,
                            "success": False,
                            "error": str(result),
                            "timestamp": datetime.now().isoformat()
                        }
                        all_results.append(error_result)
                    else:
                        all_results.extend(result)
                
                # Pequeña pausa entre batches
                await asyncio.sleep(0.2)
        
        return all_results
    
    def analyze_results(self, results: List[Dict], max_latency_ms: int, scenario: str) -> Dict:
        """Analizar resultados y determinar si pasa el fitness function"""
        if not results:
            return {"status": "FAIL", "reason": "No results to analyze"}
        
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        if not successful_results:
            return {"status": "FAIL", "reason": "No successful operations"}
        
        latencies = [r["latency_ms"] for r in successful_results]
        
        # Análisis por tipo de operación
        operations_analysis = {}
        for op_type in ["search_papers", "search_authors", "get_suggestions", "search_external"]:
            op_results = [r for r in successful_results if r["operation"] == op_type]
            if op_results:
                op_latencies = [r["latency_ms"] for r in op_results]
                operations_analysis[op_type] = {
                    "count": len(op_results),
                    "avg_latency_ms": statistics.mean(op_latencies),
                    "p95_latency_ms": sorted(op_latencies)[int(len(op_latencies) * 0.95)] if op_latencies else 0,
                    "max_latency_ms": max(op_latencies)
                }
        
        analysis = {
            "total_operations": len(results),
            "successful_operations": len(successful_results),
            "failed_operations": len(failed_results),
            "success_rate": len(successful_results) / len(results) * 100,
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "avg_latency_ms": statistics.mean(latencies),
            "median_latency_ms": statistics.median(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0,
            "p99_latency_ms": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
            "max_allowed_latency_ms": max_latency_ms,
            "scenario": scenario,
            "operations_breakdown": operations_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        # Determinar status del fitness function
        if analysis["success_rate"] < 90:
            analysis["status"] = "FAIL"
            analysis["reason"] = f"Success rate too low: {analysis['success_rate']:.1f}%"
        elif analysis["p95_latency_ms"] > max_latency_ms * 1.5:  # Más tolerante para búsquedas
            analysis["status"] = "FAIL"
            analysis["reason"] = f"P95 latency too high: {analysis['p95_latency_ms']:.1f}ms > {max_latency_ms * 1.5}ms"
        elif analysis["avg_latency_ms"] > max_latency_ms:
            if scenario == "good":
                analysis["status"] = "FAIL"
                analysis["reason"] = f"Average latency too high: {analysis['avg_latency_ms']:.1f}ms > {max_latency_ms}ms"
            else:
                analysis["status"] = "WARNING"
                analysis["reason"] = f"Average latency acceptable for '{scenario}' scenario"
        else:
            analysis["status"] = "PASS"
            analysis["reason"] = "All metrics within acceptable limits"
        
        return analysis

def save_results(results: List[Dict], analysis: Dict, scenario: str):
    """Guardar resultados en archivos"""
    os.makedirs("reports", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Guardar resultados detallados
    with open(f"reports/search_performance_{scenario}_{timestamp}.json", "w") as f:
        json.dump({
            "analysis": analysis,
            "raw_results": results
        }, f, indent=2)
    
    # Guardar reporte HTML
    operations_html = ""
    for op, data in analysis.get("operations_breakdown", {}).items():
        operations_html += f"""
        <tr>
            <td>{op}</td>
            <td>{data['count']}</td>
            <td>{data['avg_latency_ms']:.1f} ms</td>
            <td>{data['p95_latency_ms']:.1f} ms</td>
            <td>{data['max_latency_ms']:.1f} ms</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Performance Report - {scenario}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .status-PASS {{ color: green; }}
            .status-FAIL {{ color: red; }}
            .status-WARNING {{ color: orange; }}
            table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>🔍 Search Performance Report</h1>
        <h2>Scenario: {scenario}</h2>
        <h3 class="status-{analysis['status']}">Status: {analysis['status']}</h3>
        <p><strong>Reason:</strong> {analysis['reason']}</p>
        
        <h3>📊 Overall Metrics</h3>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Operations</td><td>{analysis['total_operations']}</td></tr>
            <tr><td>Success Rate</td><td>{analysis['success_rate']:.1f}%</td></tr>
            <tr><td>Average Latency</td><td>{analysis['avg_latency_ms']:.1f} ms</td></tr>
            <tr><td>P95 Latency</td><td>{analysis['p95_latency_ms']:.1f} ms</td></tr>
            <tr><td>P99 Latency</td><td>{analysis['p99_latency_ms']:.1f} ms</td></tr>
            <tr><td>Max Allowed Latency</td><td>{analysis['max_allowed_latency_ms']} ms</td></tr>
        </table>
        
        <h3>🔧 Operations Breakdown</h3>
        <table>
            <tr><th>Operation</th><th>Count</th><th>Avg Latency</th><th>P95 Latency</th><th>Max Latency</th></tr>
            {operations_html}
        </table>
        
        <h3>📈 Latency Distribution</h3>
        <p>Min: {analysis['min_latency_ms']:.1f} ms | Max: {analysis['max_latency_ms']:.1f} ms | Median: {analysis['median_latency_ms']:.1f} ms</p>
        
        <p><em>Generated on {analysis['timestamp']}</em></p>
    </body>
    </html>
    """
    
    with open(f"reports/search_performance_{scenario}_{timestamp}.html", "w") as f:
        f.write(html_content)
    
    print(f"📊 Results saved to reports/search_performance_{scenario}_{timestamp}.*")

async def main():
    parser = argparse.ArgumentParser(description="Search Performance Fitness Function")
    parser.add_argument("--users", type=int, default=200, help="Number of concurrent users")
    parser.add_argument("--duration", type=str, default="30s", help="Test duration (e.g., 30s, 2m)")
    parser.add_argument("--max-latency", type=int, default=300, help="Maximum allowed latency in ms")
    parser.add_argument("--scenario", type=str, default="good", help="Test scenario name")
    parser.add_argument("--base-url", type=str, default="http://localhost:8000", help="Base URL")
    
    args = parser.parse_args()
    
    # Parse duration
    duration_str = args.duration.lower()
    if duration_str.endswith('s'):
        duration_seconds = int(duration_str[:-1])
    elif duration_str.endswith('m'):
        duration_seconds = int(duration_str[:-1]) * 60
    else:
        duration_seconds = int(duration_str)
    
    print(f"🔍 Search Fitness Function - Scenario: {args.scenario}")
    print(f"⚙️  Configuration:")
    print(f"   - Concurrent Users: {args.users}")
    print(f"   - Duration: {duration_seconds}s")
    print(f"   - Max Latency: {args.max_latency}ms")
    print(f"   - Base URL: {args.base_url}")
    
    tester = SearchPerformanceTester(args.base_url)
    
    try:
        results = await tester.run_concurrent_test(args.users, duration_seconds)
        analysis = tester.analyze_results(results, args.max_latency, args.scenario)
        
        print(f"\n📊 Results:")
        print(f"   Status: {analysis['status']}")
        print(f"   Reason: {analysis['reason']}")
        print(f"   Success Rate: {analysis['success_rate']:.1f}%")
        print(f"   Avg Latency: {analysis['avg_latency_ms']:.1f}ms")
        print(f"   P95 Latency: {analysis['p95_latency_ms']:.1f}ms")
        
        save_results(results, analysis, args.scenario)
        
        # Exit with appropriate code
        if analysis['status'] == 'FAIL':
            exit(1)
        elif analysis['status'] == 'WARNING':
            exit(2)
        else:
            exit(0)
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
