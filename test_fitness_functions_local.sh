#!/bin/bash
# Script para probar las fitness functions localmente

echo "🧪 Probando Fitness Functions Localmente"

# Verificar que FastAPI esté ejecutándose
echo "1. Verificando servidor..."
curl -f http://localhost:8000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Servidor está ejecutándose"
else
    echo "❌ Servidor no está ejecutándose. Iniciando..."
    cd .. && cd ..
    python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 &
    SERVER_PID=$!
    sleep 5
    echo "✅ Servidor iniciado (PID: $SERVER_PID)"
fi

# Crear directorio de reportes
mkdir -p reports

# Probar Auth Fitness Function
echo "2. Probando Auth Fitness Function..."
python tests/performance/auth_fitness_function.py --users 10 --duration 10s --max-latency 500 --scenario test
AUTH_RESULT=$?

if [ $AUTH_RESULT -eq 0 ]; then
    echo "✅ Auth Fitness Function: PASS"
elif [ $AUTH_RESULT -eq 2 ]; then
    echo "⚠️  Auth Fitness Function: WARNING"
else
    echo "❌ Auth Fitness Function: FAIL"
fi

# Probar Search Fitness Function
echo "3. Probando Search Fitness Function..."
python tests/performance/search_fitness_function.py --users 10 --duration 10s --max-latency 600 --scenario test
SEARCH_RESULT=$?

if [ $SEARCH_RESULT -eq 0 ]; then
    echo "✅ Search Fitness Function: PASS"
elif [ $SEARCH_RESULT -eq 2 ]; then
    echo "⚠️  Search Fitness Function: WARNING"
else
    echo "❌ Search Fitness Function: FAIL"
fi

# Generar resumen
echo "4. Generando resumen..."
python tests/performance/generate_summary.py

# Verificar Quality Gate
echo "5. Verificando Quality Gate..."
python tests/performance/quality_gate.py
GATE_RESULT=$?

if [ $GATE_RESULT -eq 0 ]; then
    echo "✅ Quality Gate: PASS"
else
    echo "❌ Quality Gate: FAIL"
fi

echo "🏁 Pruebas completadas!"
echo "📊 Reportes guardados en: ./reports/"

# Detener servidor si lo iniciamos nosotros
if [ ! -z "$SERVER_PID" ]; then
    echo "🔌 Deteniendo servidor..."
    kill $SERVER_PID
fi
