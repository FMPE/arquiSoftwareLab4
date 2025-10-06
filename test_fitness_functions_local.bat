@echo off
echo 🧪 Probando Fitness Functions Localmente

echo 1. Verificando servidor...
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Servidor está ejecutándose
) else (
    echo ❌ Servidor no está ejecutándose. Iniciando...
    start /B python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
    timeout /t 5 >nul
    echo ✅ Servidor iniciado
)

echo 2. Creando directorio de reportes...
mkdir reports 2>nul

echo 3. Probando Auth Fitness Function...
python tests\performance\auth_fitness_function.py --users 10 --duration 10s --max-latency 500 --scenario test
set AUTH_RESULT=%errorlevel%

if %AUTH_RESULT%==0 (
    echo ✅ Auth Fitness Function: PASS
) else if %AUTH_RESULT%==2 (
    echo ⚠️ Auth Fitness Function: WARNING
) else (
    echo ❌ Auth Fitness Function: FAIL
)

echo 4. Probando Search Fitness Function...
python tests\performance\search_fitness_function.py --users 10 --duration 10s --max-latency 600 --scenario test
set SEARCH_RESULT=%errorlevel%

if %SEARCH_RESULT%==0 (
    echo ✅ Search Fitness Function: PASS
) else if %SEARCH_RESULT%==2 (
    echo ⚠️ Search Fitness Function: WARNING
) else (
    echo ❌ Search Fitness Function: FAIL
)

echo 5. Generando resumen...
python tests\performance\generate_summary.py

echo 6. Verificando Quality Gate...
python tests\performance\quality_gate.py
set GATE_RESULT=%errorlevel%

if %GATE_RESULT%==0 (
    echo ✅ Quality Gate: PASS
) else (
    echo ❌ Quality Gate: FAIL
)

echo 🏁 Pruebas completadas!
echo 📊 Reportes guardados en: .\reports\

pause
