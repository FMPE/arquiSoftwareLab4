"""
Fitness Function para Latencia de Autenticación
Objetivo: Medir rendimiento del servicio de auth bajo solicitudes concurrentes
"""
import asyncio
import aiohttp
import argparse
import time
import json
import statistics
from datetime import datetime
from typing import List, Dict
import os
import sys

# Asegurar que el directorio reports existe
os.makedirs("reports", exist_ok=True)

class AuthPerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        
    async def register_user(self, session: aiohttp.ClientSession, user_id: int) -> Dict:
        """Registrar un usuario y medir latencia"""
        start_time = time.time()
        
        user_data = {
            "username": f"testuser_{user_id}_{int(time.time())}",
            "email": f"test_{user_id}_{int(time.time())}@example.com",
            "password": "testpass123",
            "full_name": f"Test User {user_id}"
        }
        
        try:
            async with session.post(
                f"{self.base_url}/api/v1/auth/register",
                json=user_data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                
                # Get response details for debugging
                response_text = await response.text()
                
                result = {
                    "operation": "register",
                    "status_code": response.status,
                    "latency_ms": latency_ms,
                    "success": response.status == 201,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": user_id
                }
                
                # Add error details if failed
                if response.status != 201:
                    result["error_detail"] = response_text
                    result["headers"] = dict(response.headers)
                
                return result
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            return {
                "operation": "register",
                "status_code": 0,
                "latency_ms": latency_ms,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id
            }
    
    async def login_user(self, session: aiohttp.ClientSession, username: str, password: str) -> Dict:
        """Hacer login y medir latencia"""
        start_time = time.time()
        
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            async with session.post(
                f"{self.base_url}/api/v1/auth/login-json",
                json=login_data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000
                
                return {
                    "operation": "login",
                    "status_code": response.status,
                    "latency_ms": latency_ms,
                    "success": response.status == 200,
                    "timestamp": datetime.now().isoformat(),
                    "username": username
                }
        except Exception as e:
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000
            return {
                "operation": "login",
                "status_code": 0,
                "latency_ms": latency_ms,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "username": username
            }
    
    async def mixed_auth_operations(self, session: aiohttp.ClientSession, user_id: int) -> List[Dict]:
        """Realizar operaciones mixtas de auth"""
        results = []
        
        # 1. Registrar usuario
        register_result = await self.register_user(session, user_id)
        results.append(register_result)
        
        # 2. Hacer login si el registro fue exitoso
        if register_result["success"]:
            username = f"testuser_{user_id}_{int(time.time() - 1)}"
            login_result = await self.login_user(session, username, "testpass123")
            results.append(login_result)
        
        # 3. Intentar login con usuario existente (admin)
        admin_login = await self.login_user(session, "admin", "admin123")
        results.append(admin_login)
        
        return results
    
    async def run_concurrent_test(self, concurrent_users: int, duration_seconds: int) -> List[Dict]:
        """Ejecutar prueba con usuarios concurrentes"""
        print(f"🚀 Iniciando prueba con {concurrent_users} usuarios concurrentes por {duration_seconds}s")
        
        # First, test if endpoints are reachable
        await self.test_endpoints_availability()
        
        connector = aiohttp.TCPConnector(limit=concurrent_users * 2)
        async with aiohttp.ClientSession(connector=connector) as session:
            start_time = time.time()
            all_results = []
            
            while time.time() - start_time < duration_seconds:
                # Crear tasks para usuarios concurrentes
                tasks = []
                for i in range(concurrent_users):
                    task = asyncio.create_task(
                        self.mixed_auth_operations(session, i + int(time.time()))
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
                await asyncio.sleep(0.1)
        
        # Print some debug info
        success_count = len([r for r in all_results if r.get("success", False)])
        print(f"📊 Debug: {success_count}/{len(all_results)} operations successful")
        
        # Print first few failures for debugging
        failures = [r for r in all_results if not r.get("success", False)]
        if failures:
            print(f"🔍 First failure example: {failures[0]}")
        
        return all_results
    
    async def test_endpoints_availability(self):
        """Test basic endpoint availability before load testing"""
        print("🔍 Testing endpoint availability...")
        
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            try:
                async with session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    print(f"   Health endpoint: {response.status}")
            except Exception as e:
                print(f"   Health endpoint error: {e}")
                
            # Test simple register
            test_user = {
                "username": f"test_endpoint_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "test123",
                "full_name": "Test User"
            }
            
            try:
                async with session.post(
                    f"{self.base_url}/api/v1/auth/register",
                    json=test_user,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    print(f"   Register endpoint: {response.status}")
                    if response.status != 201:
                        text = await response.text()
                        print(f"   Register error: {text[:200]}...")
            except Exception as e:
                print(f"   Register endpoint error: {e}")
    
    def analyze_results(self, results: List[Dict], max_latency_ms: int, scenario: str) -> Dict:
        """Analizar resultados y determinar si pasa el fitness function"""
        if not results:
            return {
                "status": "FAIL", 
                "reason": "No results to analyze",
                "total_operations": 0,
                "successful_operations": 0,
                "failed_operations": 0,
                "success_rate": 0.0,
                "min_latency_ms": 0,
                "max_latency_ms": 0,
                "avg_latency_ms": 0,
                "median_latency_ms": 0,
                "p95_latency_ms": 0,
                "p99_latency_ms": 0,
                "max_allowed_latency_ms": max_latency_ms,
                "scenario": scenario,
                "timestamp": datetime.now().isoformat()
            }
        
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]
        
        if not successful_results:
            return {
                "status": "FAIL", 
                "reason": "No successful operations",
                "total_operations": len(results),
                "successful_operations": 0,
                "failed_operations": len(failed_results),
                "success_rate": 0.0,
                "min_latency_ms": 0,
                "max_latency_ms": 0,
                "avg_latency_ms": 0,
                "median_latency_ms": 0,
                "p95_latency_ms": 0,
                "p99_latency_ms": 0,
                "max_allowed_latency_ms": max_latency_ms,
                "scenario": scenario,
                "timestamp": datetime.now().isoformat()
            }
        
        latencies = [r["latency_ms"] for r in successful_results]
        
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
            "timestamp": datetime.now().isoformat()
        }
        
        # Determinar status del fitness function
        if analysis["success_rate"] < 95:
            analysis["status"] = "FAIL"
            analysis["reason"] = f"Success rate too low: {analysis['success_rate']:.1f}%"
        elif analysis["p95_latency_ms"] > max_latency_ms:
            analysis["status"] = "FAIL" 
            analysis["reason"] = f"P95 latency too high: {analysis['p95_latency_ms']:.1f}ms > {max_latency_ms}ms"
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
    with open(f"reports/auth_performance_{scenario}_{timestamp}.json", "w") as f:
        json.dump({
            "analysis": analysis,
            "raw_results": results
        }, f, indent=2)
    
    # Guardar reporte HTML simple
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auth Performance Report - {scenario}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .status-PASS {{ color: green; }}
            .status-FAIL {{ color: red; }}
            .status-WARNING {{ color: orange; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>🔐 Authentication Performance Report</h1>
        <h2>Scenario: {scenario}</h2>
        <h3 class="status-{analysis['status']}">Status: {analysis['status']}</h3>
        <p><strong>Reason:</strong> {analysis['reason']}</p>
        
        <h3>📊 Metrics</h3>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Operations</td><td>{analysis['total_operations']}</td></tr>
            <tr><td>Success Rate</td><td>{analysis['success_rate']:.1f}%</td></tr>
            <tr><td>Average Latency</td><td>{analysis['avg_latency_ms']:.1f} ms</td></tr>
            <tr><td>P95 Latency</td><td>{analysis['p95_latency_ms']:.1f} ms</td></tr>
            <tr><td>P99 Latency</td><td>{analysis['p99_latency_ms']:.1f} ms</td></tr>
            <tr><td>Max Allowed Latency</td><td>{analysis['max_allowed_latency_ms']} ms</td></tr>
        </table>
        
        <h3>📈 Latency Distribution</h3>
        <p>Min: {analysis['min_latency_ms']:.1f} ms | Max: {analysis['max_latency_ms']:.1f} ms | Median: {analysis['median_latency_ms']:.1f} ms</p>
        
        <p><em>Generated on {analysis['timestamp']}</em></p>
    </body>
    </html>
    """
    
    with open(f"reports/auth_performance_{scenario}_{timestamp}.html", "w") as f:
        f.write(html_content)
    
    print(f"📊 Results saved to reports/auth_performance_{scenario}_{timestamp}.*")

async def main():
    parser = argparse.ArgumentParser(description="Auth Performance Fitness Function")
    parser.add_argument("--users", type=int, default=300, help="Number of concurrent users")
    parser.add_argument("--duration", type=str, default="30s", help="Test duration (e.g., 30s, 2m)")
    parser.add_argument("--max-latency", type=int, default=200, help="Maximum allowed latency in ms")
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
    
    print(f"🔐 Auth Fitness Function - Scenario: {args.scenario}")
    print(f"⚙️  Configuration:")
    print(f"   - Concurrent Users: {args.users}")
    print(f"   - Duration: {duration_seconds}s")
    print(f"   - Max Latency: {args.max_latency}ms")
    print(f"   - Base URL: {args.base_url}")
    
    tester = AuthPerformanceTester(args.base_url)
    
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
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
