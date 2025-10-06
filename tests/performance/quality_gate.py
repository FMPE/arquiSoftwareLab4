"""
Quality Gate - Verificador de umbrales de rendimiento
Determina si la aplicación cumple con los estándares de performance
"""
import json
import os
import glob
from typing import Dict, List

class QualityGate:
    def __init__(self):
        self.thresholds = {
            "auth": {
                "good": {
                    "max_avg_latency_ms": 200,
                    "min_success_rate": 95,
                    "max_p95_latency_ms": 300
                },
                "ok": {
                    "max_avg_latency_ms": 400,
                    "min_success_rate": 90,
                    "max_p95_latency_ms": 600
                }
            },
            "search": {
                "good": {
                    "max_avg_latency_ms": 300,
                    "min_success_rate": 90,
                    "max_p95_latency_ms": 500
                },
                "ok": {
                    "max_avg_latency_ms": 500,
                    "min_success_rate": 85,
                    "max_p95_latency_ms": 800
                }
            }
        }
        
        self.failures = []
        self.warnings = []
        self.passed = []
    
    def load_test_results(self) -> Dict:
        """Cargar todos los resultados de pruebas"""
        results = {"auth": [], "search": []}
        
        # Cargar resultados de auth
        auth_files = glob.glob("reports/auth-performance-*/auth_performance_*.json")
        for file_path in auth_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    results["auth"].append(data["analysis"])
            except Exception as e:
                print(f"Warning: Could not load {file_path}: {e}")
        
        # Cargar resultados de search
        search_files = glob.glob("reports/search-performance-*/search_performance_*.json")
        for file_path in search_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    results["search"].append(data["analysis"])
            except Exception as e:
                print(f"Warning: Could not load {file_path}: {e}")
        
        return results
    
    def evaluate_test(self, test_result: Dict, component: str) -> Dict:
        """Evaluar un resultado de prueba individual"""
        scenario = test_result.get("scenario", "unknown")
        
        # Obtener umbrales para este componente y escenario
        if scenario in self.thresholds[component]:
            thresholds = self.thresholds[component][scenario]
        else:
            # Usar umbrales "ok" como fallback
            thresholds = self.thresholds[component]["ok"]
        
        evaluation = {
            "component": component,
            "scenario": scenario,
            "status": "PASS",
            "issues": [],
            "metrics": {
                "avg_latency_ms": test_result.get("avg_latency_ms", 0),
                "success_rate": test_result.get("success_rate", 0),
                "p95_latency_ms": test_result.get("p95_latency_ms", 0)
            },
            "thresholds": thresholds
        }
        
        # Verificar cada métrica
        if evaluation["metrics"]["avg_latency_ms"] > thresholds["max_avg_latency_ms"]:
            evaluation["issues"].append(
                f"Average latency too high: {evaluation['metrics']['avg_latency_ms']:.1f}ms > {thresholds['max_avg_latency_ms']}ms"
            )
        
        if evaluation["metrics"]["success_rate"] < thresholds["min_success_rate"]:
            evaluation["issues"].append(
                f"Success rate too low: {evaluation['metrics']['success_rate']:.1f}% < {thresholds['min_success_rate']}%"
            )
        
        if evaluation["metrics"]["p95_latency_ms"] > thresholds["max_p95_latency_ms"]:
            evaluation["issues"].append(
                f"P95 latency too high: {evaluation['metrics']['p95_latency_ms']:.1f}ms > {thresholds['max_p95_latency_ms']}ms"
            )
        
        # Determinar status final
        if evaluation["issues"]:
            # Si es escenario "good" y hay issues, es FAIL
            # Si es escenario "ok" y hay issues menores, es WARNING
            if scenario == "good" or evaluation["metrics"]["success_rate"] < 85:
                evaluation["status"] = "FAIL"
            else:
                evaluation["status"] = "WARNING"
        
        return evaluation
    
    def run_quality_gate(self) -> Dict:
        """Ejecutar quality gate completo"""
        print("🔍 Running Quality Gate evaluation...")
        
        # Cargar resultados
        test_results = self.load_test_results()
        
        if not test_results["auth"] and not test_results["search"]:
            return {
                "overall_status": "FAIL",
                "reason": "No test results found",
                "evaluations": [],
                "summary": {
                    "total_tests": 0,
                    "passed": 0,
                    "warnings": 0,
                    "failed": 0
                }
            }
        
        evaluations = []
        
        # Evaluar resultados de auth
        for test in test_results["auth"]:
            evaluation = self.evaluate_test(test, "auth")
            evaluations.append(evaluation)
            
            if evaluation["status"] == "PASS":
                self.passed.append(evaluation)
            elif evaluation["status"] == "WARNING":
                self.warnings.append(evaluation)
            else:
                self.failures.append(evaluation)
        
        # Evaluar resultados de search
        for test in test_results["search"]:
            evaluation = self.evaluate_test(test, "search")
            evaluations.append(evaluation)
            
            if evaluation["status"] == "PASS":
                self.passed.append(evaluation)
            elif evaluation["status"] == "WARNING":
                self.warnings.append(evaluation)
            else:
                self.failures.append(evaluation)
        
        # Determinar status general
        if self.failures:
            overall_status = "FAIL"
            reason = f"{len(self.failures)} test(s) failed quality gate"
        elif self.warnings:
            overall_status = "WARNING"
            reason = f"{len(self.warnings)} test(s) have warnings"
        else:
            overall_status = "PASS"
            reason = "All tests passed quality gate"
        
        summary = {
            "overall_status": overall_status,
            "reason": reason,
            "evaluations": evaluations,
            "summary": {
                "total_tests": len(evaluations),
                "passed": len(self.passed),
                "warnings": len(self.warnings),
                "failed": len(self.failures)
            }
        }
        
        return summary
    
    def generate_report(self, quality_gate_result: Dict):
        """Generar reporte del quality gate"""
        os.makedirs("reports/summary", exist_ok=True)
        
        # Guardar resultado JSON
        with open("reports/summary/quality_gate_result.json", "w") as f:
            json.dump(quality_gate_result, f, indent=2)
        
        # Generar reporte de texto
        report_lines = [
            "🚪 QUALITY GATE REPORT",
            "=" * 50,
            f"Overall Status: {quality_gate_result['overall_status']}",
            f"Reason: {quality_gate_result['reason']}",
            "",
            f"📊 Summary:",
            f"  Total Tests: {quality_gate_result['summary']['total_tests']}",
            f"  ✅ Passed: {quality_gate_result['summary']['passed']}",
            f"  ⚠️  Warnings: {quality_gate_result['summary']['warnings']}",
            f"  ❌ Failed: {quality_gate_result['summary']['failed']}",
            ""
        ]
        
        # Detalles de evaluaciones
        if quality_gate_result['evaluations']:
            report_lines.append("📋 Detailed Results:")
            report_lines.append("-" * 30)
            
            for eval_result in quality_gate_result['evaluations']:
                status_emoji = "✅" if eval_result['status'] == 'PASS' else "⚠️" if eval_result['status'] == 'WARNING' else "❌"
                
                report_lines.extend([
                    f"{status_emoji} {eval_result['component'].upper()} - {eval_result['scenario'].upper()}",
                    f"  Status: {eval_result['status']}",
                    f"  Avg Latency: {eval_result['metrics']['avg_latency_ms']:.1f}ms (max: {eval_result['thresholds']['max_avg_latency_ms']}ms)",
                    f"  Success Rate: {eval_result['metrics']['success_rate']:.1f}% (min: {eval_result['thresholds']['min_success_rate']}%)",
                    f"  P95 Latency: {eval_result['metrics']['p95_latency_ms']:.1f}ms (max: {eval_result['thresholds']['max_p95_latency_ms']}ms)"
                ])
                
                if eval_result['issues']:
                    report_lines.append("  Issues:")
                    for issue in eval_result['issues']:
                        report_lines.append(f"    - {issue}")
                
                report_lines.append("")
        
        # Guardar reporte de texto
        report_text = "\n".join(report_lines)
        with open("reports/summary/quality_gate_report.txt", "w") as f:
            f.write(report_text)
        
        # Si hay fallas, crear archivo especial para CI
        if quality_gate_result['overall_status'] == 'FAIL':
            with open("reports/summary/quality_gate_failed", "w") as f:
                f.write(f"Quality Gate Failed: {quality_gate_result['reason']}\n")
                f.write(f"Failed tests: {quality_gate_result['summary']['failed']}\n")
                
                for eval_result in quality_gate_result['evaluations']:
                    if eval_result['status'] == 'FAIL':
                        f.write(f"\n❌ {eval_result['component'].upper()} - {eval_result['scenario'].upper()}:\n")
                        for issue in eval_result['issues']:
                            f.write(f"  - {issue}\n")
        
        print(f"📁 Quality Gate report saved to reports/summary/")
        return report_text

def main():
    quality_gate = QualityGate()
    
    try:
        result = quality_gate.run_quality_gate()
        report = quality_gate.generate_report(result)
        
        print("\n" + "=" * 50)
        print(report)
        print("=" * 50)
        
        # Exit with appropriate code for CI
        if result['overall_status'] == 'FAIL':
            print("\n❌ Quality Gate FAILED!")
            exit(1)
        elif result['overall_status'] == 'WARNING':
            print("\n⚠️  Quality Gate passed with WARNINGS")
            exit(0)  # Warnings don't fail the build
        else:
            print("\n✅ Quality Gate PASSED!")
            exit(0)
    
    except Exception as e:
        print(f"❌ Quality Gate evaluation failed: {e}")
        
        # Crear archivo de error
        os.makedirs("reports/summary", exist_ok=True)
        with open("reports/summary/quality_gate_failed", "w") as f:
            f.write(f"Quality Gate evaluation failed: {str(e)}\n")
        
        exit(1)

if __name__ == "__main__":
    main()
