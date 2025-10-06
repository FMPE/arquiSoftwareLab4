"""
Generador de reporte resumen de todas las pruebas de rendimiento
"""
import json
import os
from datetime import datetime
from typing import Dict, List
import glob

def load_performance_results() -> Dict:
    """Cargar todos los resultados de rendimiento"""
    results = {
        "auth": [],
        "search": [],
        "summary": {
            "timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "warning_tests": 0
        }
    }
    
    # Buscar archivos de resultados
    auth_files = glob.glob("reports/auth-performance-*/auth_performance_*.json")
    search_files = glob.glob("reports/search-performance-*/search_performance_*.json")
    
    # Cargar resultados de auth
    for file_path in auth_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                results["auth"].append(data["analysis"])
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    # Cargar resultados de search
    for file_path in search_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                results["search"].append(data["analysis"])
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    # Calcular estadísticas
    all_tests = results["auth"] + results["search"]
    results["summary"]["total_tests"] = len(all_tests)
    
    for test in all_tests:
        status = test.get("status", "UNKNOWN")
        if status == "PASS":
            results["summary"]["passed_tests"] += 1
        elif status == "FAIL":
            results["summary"]["failed_tests"] += 1
        elif status == "WARNING":
            results["summary"]["warning_tests"] += 1
    
    return results

def generate_pr_comment(results: Dict) -> str:
    """Generar comentario para PR"""
    summary = results["summary"]
    
    # Determinar emoji y estado general
    if summary["failed_tests"] > 0:
        status_emoji = "❌"
        overall_status = "FAILED"
    elif summary["warning_tests"] > 0:
        status_emoji = "⚠️"
        overall_status = "WARNING"
    else:
        status_emoji = "✅"
        overall_status = "PASSED"
    
    comment = f"""## {status_emoji} Performance Tests Report

### Overall Status: **{overall_status}**

📊 **Summary:**
- Total Tests: {summary['total_tests']}
- ✅ Passed: {summary['passed_tests']}
- ❌ Failed: {summary['failed_tests']}
- ⚠️ Warnings: {summary['warning_tests']}

### 🔐 Authentication Performance

"""
    
    # Resultados de Auth
    if results["auth"]:
        for i, test in enumerate(results["auth"]):
            scenario = test.get("scenario", f"test_{i}")
            status = test.get("status", "UNKNOWN")
            avg_latency = test.get("avg_latency_ms", 0)
            success_rate = test.get("success_rate", 0)
            max_allowed = test.get("max_allowed_latency_ms", 0)
            
            status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            
            comment += f"""- **{scenario.upper()}** {status_emoji}
  - Status: {status}
  - Avg Latency: {avg_latency:.1f}ms (max: {max_allowed}ms)
  - Success Rate: {success_rate:.1f}%
"""
    else:
        comment += "- No authentication tests found\n"
    
    comment += "\n### 🔍 Search Performance\n\n"
    
    # Resultados de Search
    if results["search"]:
        for i, test in enumerate(results["search"]):
            scenario = test.get("scenario", f"test_{i}")
            status = test.get("status", "UNKNOWN")
            avg_latency = test.get("avg_latency_ms", 0)
            success_rate = test.get("success_rate", 0)
            max_allowed = test.get("max_allowed_latency_ms", 0)
            
            status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            
            comment += f"""- **{scenario.upper()}** {status_emoji}
  - Status: {status}
  - Avg Latency: {avg_latency:.1f}ms (max: {max_allowed}ms)
  - Success Rate: {success_rate:.1f}%
"""
    else:
        comment += "- No search tests found\n"
    
    comment += f"""
### 📈 Quality Gates

| Component | Good (≤200ms) | OK (≤400ms) | Status |
|-----------|---------------|-------------|---------|
| Auth | 300 concurrent users | 500 concurrent users | {status_emoji} |
| Search | 200 concurrent users | 400 concurrent users | {status_emoji} |

**Generated on:** {summary['timestamp']}
"""
    
    return comment

def generate_html_report(results: Dict) -> str:
    """Generar reporte HTML completo"""
    summary = results["summary"]
    
    # Generar tablas de resultados
    auth_rows = ""
    for test in results["auth"]:
        status_class = f"status-{test.get('status', 'UNKNOWN')}"
        auth_rows += f"""
        <tr class="{status_class}">
            <td>{test.get('scenario', 'Unknown').upper()}</td>
            <td>{test.get('status', 'UNKNOWN')}</td>
            <td>{test.get('avg_latency_ms', 0):.1f} ms</td>
            <td>{test.get('p95_latency_ms', 0):.1f} ms</td>
            <td>{test.get('success_rate', 0):.1f}%</td>
            <td>{test.get('max_allowed_latency_ms', 0)} ms</td>
        </tr>
        """
    
    search_rows = ""
    for test in results["search"]:
        status_class = f"status-{test.get('status', 'UNKNOWN')}"
        search_rows += f"""
        <tr class="{status_class}">
            <td>{test.get('scenario', 'Unknown').upper()}</td>
            <td>{test.get('status', 'UNKNOWN')}</td>
            <td>{test.get('avg_latency_ms', 0):.1f} ms</td>
            <td>{test.get('p95_latency_ms', 0):.1f} ms</td>
            <td>{test.get('success_rate', 0):.1f}%</td>
            <td>{test.get('max_allowed_latency_ms', 0)} ms</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Paperly.utec - Performance Summary Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1, h2, h3 {{ color: #2c3e50; }}
            .summary-cards {{ display: flex; gap: 20px; margin: 20px 0; }}
            .card {{ flex: 1; padding: 20px; border-radius: 8px; text-align: center; }}
            .card-success {{ background: #d4edda; border: 1px solid #c3e6cb; }}
            .card-warning {{ background: #fff3cd; border: 1px solid #ffeaa7; }}
            .card-danger {{ background: #f8d7da; border: 1px solid #f5c6cb; }}
            .status-PASS {{ background-color: #d4edda; }}
            .status-FAIL {{ background-color: #f8d7da; }}
            .status-WARNING {{ background-color: #fff3cd; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f8f9fa; font-weight: bold; }}
            .metric {{ font-size: 2em; font-weight: bold; margin: 0; }}
            .metric-label {{ margin: 5px 0 0 0; color: #6c757d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Paperly.utec - Performance Summary Report</h1>
            
            <div class="summary-cards">
                <div class="card card-success">
                    <p class="metric">{summary['passed_tests']}</p>
                    <p class="metric-label">Passed Tests</p>
                </div>
                <div class="card card-warning">
                    <p class="metric">{summary['warning_tests']}</p>
                    <p class="metric-label">Warning Tests</p>
                </div>
                <div class="card card-danger">
                    <p class="metric">{summary['failed_tests']}</p>
                    <p class="metric-label">Failed Tests</p>
                </div>
            </div>
            
            <h2>🔐 Authentication Performance Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Status</th>
                        <th>Avg Latency</th>
                        <th>P95 Latency</th>
                        <th>Success Rate</th>
                        <th>Max Allowed</th>
                    </tr>
                </thead>
                <tbody>
                    {auth_rows if auth_rows else '<tr><td colspan="6">No authentication tests found</td></tr>'}
                </tbody>
            </table>
            
            <h2>🔍 Search Performance Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Status</th>
                        <th>Avg Latency</th>
                        <th>P95 Latency</th>
                        <th>Success Rate</th>
                        <th>Max Allowed</th>
                    </tr>
                </thead>
                <tbody>
                    {search_rows if search_rows else '<tr><td colspan="6">No search tests found</td></tr>'}
                </tbody>
            </table>
            
            <h2>📊 Fitness Functions Definition</h2>
            
            <h3>f(latencia) - Authentication Service</h3>
            <ul>
                <li><strong>Good:</strong> ≤ 200ms with 300 concurrent users</li>
                <li><strong>OK:</strong> ≤ 400ms with 500 concurrent users</li>
                <li><strong>Bad:</strong> > 400ms or timeouts under normal concurrency</li>
            </ul>
            
            <h3>f(latencia) - Search Flow</h3>
            <ul>
                <li><strong>Good:</strong> ≤ 300ms with 200 concurrent users</li>
                <li><strong>OK:</strong> ≤ 500ms with 400 concurrent users</li>
                <li><strong>Bad:</strong> > 500ms or degraded user experience</li>
            </ul>
            
            <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #6c757d; text-align: center;">
                <p>Generated on {summary['timestamp']}</p>
                <p>Paperly.utec Performance Monitoring System</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    return html_content

def main():
    print("📊 Generating performance summary report...")
    
    # Crear directorio de reportes
    os.makedirs("reports/summary", exist_ok=True)
    
    # Cargar resultados
    results = load_performance_results()
    
    # Generar comentario para PR
    pr_comment = generate_pr_comment(results)
    with open("reports/summary/pr_comment.md", "w") as f:
        f.write(pr_comment)
    
    # Generar reporte HTML
    html_report = generate_html_report(results)
    with open("reports/summary/performance_summary.html", "w") as f:
        f.write(html_report)
    
    # Guardar resultados JSON
    with open("reports/summary/performance_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Summary generated:")
    print(f"   - Total tests: {results['summary']['total_tests']}")
    print(f"   - Passed: {results['summary']['passed_tests']}")
    print(f"   - Failed: {results['summary']['failed_tests']}")
    print(f"   - Warnings: {results['summary']['warning_tests']}")
    
    print("\n📁 Files generated:")
    print("   - reports/summary/pr_comment.md")
    print("   - reports/summary/performance_summary.html")
    print("   - reports/summary/performance_summary.json")

if __name__ == "__main__":
    main()
