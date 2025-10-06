# 📊 Fitness Functions - Performance Testing

## Descripción General

Este sistema implementa **fitness functions** automatizadas para monitorear continuamente el rendimiento de los componentes críticos de Paperly.utec. Las fitness functions son pruebas automatizadas que verifican que la arquitectura mantenga las características de calidad deseadas.

## 🎯 Fitness Functions Implementadas

### 1. f(latencia) - Servicio de Login/Register + Auth

**Objetivo:** Medir el rendimiento del servicio de autenticación bajo solicitudes concurrentes.

**Importancia:** Es la puerta de entrada al sistema; si este servicio se degrada, los usuarios no pueden autenticarse, registrarse ni acceder a las funcionalidades.

#### Umbrales Definidos:
- **🟢 Good:** tiempo de respuesta ≤ 200ms con 300 solicitudes concurrentes
- **🟡 OK:** tiempo de respuesta ≤ 400ms con 500 solicitudes concurrentes  
- **🔴 Bad:** > 400ms o presencia de timeouts bajo concurrencia normal

#### Operaciones Medidas:
- Registro de nuevos usuarios
- Login con credenciales válidas
- Verificación de tokens JWT
- Manejo de errores de autenticación

### 2. f(latencia) - Flujo de Búsqueda de Papers

**Objetivo:** Medir la latencia end-to-end del proceso de búsqueda, desde la consulta hasta la entrega de resultados.

**Importancia:** La búsqueda es el núcleo del sistema; si el tiempo de respuesta es alto, la experiencia del usuario se degrada y puede provocar abandono.

#### Umbrales Definidos:
- **🟢 Good:** tiempo de respuesta ≤ 300ms con 200 solicitudes concurrentes
- **🟡 OK:** tiempo de respuesta ≤ 500ms con 400 solicitudes concurrentes
- **🔴 Bad:** > 500ms o experiencia de usuario degradada

#### Operaciones Medidas:
- Búsqueda de papers por título/contenido
- Búsqueda por autor
- Obtención de sugerencias
- Consulta a APIs externas (mock)

## 🚀 GitHub Actions Workflow

### Estructura del Pipeline

```yaml
1. setup-and-build          # Preparar aplicación
2. fitness-function-auth     # Pruebas de autenticación
3. fitness-function-search   # Pruebas de búsqueda  
4. performance-summary       # Quality Gate
```

### Triggers del Workflow:
- **Push** a `main` o `develop`
- **Pull Requests** a `main`
- **Schedule** diario a las 2 AM UTC
- **Manual** con diferentes intensidades de prueba

### Matrix Strategy:
Cada fitness function se ejecuta con múltiples escenarios:
- **good:** Umbrales estrictos para rendimiento óptimo
- **ok:** Umbrales relajados para rendimiento aceptable
- **stress:** Pruebas de límites del sistema

## 📁 Estructura de Archivos

```
tests/performance/
├── auth_fitness_function.py      # Fitness function de auth
├── search_fitness_function.py    # Fitness function de búsqueda
├── generate_summary.py           # Generador de reportes
├── quality_gate.py               # Verificador de quality gate
└── __init__.py

.github/workflows/
└── fitness-functions.yml         # Workflow de GitHub Actions

reports/                           # Generado automáticamente
├── auth-performance-*/           # Resultados de auth
├── search-performance-*/         # Resultados de búsqueda
└── summary/                      # Reportes consolidados
    ├── performance_summary.html
    ├── performance_summary.json
    ├── quality_gate_result.json
    └── pr_comment.md
```

## 🛠️ Uso Local

### Prerrequisitos:
1. Servidor ejecutándose: `run_server_v2.bat`
2. Dependencias instaladas: `pip install aiohttp locust`

### Ejecutar Todas las Fitness Functions:
```bash
test_fitness_functions.bat
```

### Ejecutar Fitness Functions Individuales:

#### Autenticación:
```bash
# Escenario GOOD (300 usuarios, ≤200ms)
python tests/performance/auth_fitness_function.py --users 300 --duration 30s --max-latency 200 --scenario good

# Escenario OK (500 usuarios, ≤400ms)
python tests/performance/auth_fitness_function.py --users 500 --duration 45s --max-latency 400 --scenario ok
```

#### Búsqueda:
```bash
# Escenario GOOD (200 usuarios, ≤300ms)
python tests/performance/search_fitness_function.py --users 200 --duration 30s --max-latency 300 --scenario good

# Escenario OK (400 usuarios, ≤500ms)
python tests/performance/search_fitness_function.py --users 400 --duration 45s --max-latency 500 --scenario ok
```

### Generar Reportes:
```bash
# Reporte resumen
python tests/performance/generate_summary.py

# Quality Gate
python tests/performance/quality_gate.py
```

## 📊 Interpretación de Resultados

### Estados de Fitness Functions:

#### ✅ PASS
- Todas las métricas dentro de los umbrales
- Tasa de éxito ≥ 95% (auth) / ≥ 90% (search)
- Latencia promedio y P95 aceptables

#### ⚠️ WARNING  
- Métricas en el límite de los umbrales
- Tasa de éxito entre 85-95%
- Posible degradación futura

#### ❌ FAIL
- Una o más métricas superan los umbrales
- Tasa de éxito < 85%
- Sistema no cumple requirements de rendimiento

### Métricas Monitoreadas:

1. **Latencia Promedio:** Tiempo medio de respuesta
2. **P95 Latency:** 95% de requests bajo este tiempo
3. **P99 Latency:** 99% de requests bajo este tiempo
4. **Success Rate:** Porcentaje de operaciones exitosas
5. **Throughput:** Operaciones por segundo
6. **Error Rate:** Porcentaje de errores

## 🚪 Quality Gate

El **Quality Gate** es el mecanismo que determina si el código puede ser desplegado:

### Criterios de Aprobación:
- **Auth Service:** P95 ≤ 300ms, Success Rate ≥ 95%
- **Search Service:** P95 ≤ 500ms, Success Rate ≥ 90%
- **Sin errores críticos** en ningún componente

### Acciones por Estado:
- **PASS:** ✅ Deployment permitido
- **WARNING:** ⚠️ Deployment con notificación
- **FAIL:** ❌ Bloqueo de deployment

## 🔄 Integración con CI/CD

### En Pull Requests:
- Ejecuta fitness functions automáticamente
- Comenta resultados directamente en el PR
- Bloquea merge si Quality Gate falla

### En Main Branch:
- Monitoreo continuo de rendimiento
- Alertas automáticas si se detecta degradación
- Reportes diarios de tendencias

### Notificaciones:
- **Slack/Teams:** Alertas de fallos críticos
- **Email:** Reportes semanales de tendencias
- **Dashboard:** Métricas en tiempo real

## 📈 Monitoreo de Tendencias

Las fitness functions permiten detectar:
- **Regresiones de rendimiento** en nuevos commits
- **Degradación gradual** del sistema
- **Impacto** de cambios específicos
- **Patrones** de uso y carga

## 🎛️ Configuración Avanzada

### Variables de Entorno:
```bash
PERFORMANCE_TEST_INTENSITY=normal    # light, normal, heavy
PERFORMANCE_BASE_URL=http://localhost:8000
PERFORMANCE_CONCURRENT_USERS=auto    # Calculado por escenario
PERFORMANCE_DURATION=30s             # Duración de pruebas
```

### Personalización de Umbrales:
Editar `tests/performance/quality_gate.py` para ajustar:
- Límites de latencia por componente
- Tasas de éxito mínimas
- Criterios de evaluación

## 🚀 Próximos Pasos

1. **Integración con APM:** New Relic, DataDog
2. **Métricas de negocio:** Papers descargados, búsquedas exitosas
3. **Pruebas de carga sostenida:** Tests de resistencia
4. **Fitness functions adicionales:** Disponibilidad, seguridad
5. **ML para predicción:** Detección proactiva de problemas

---

**¡Las fitness functions aseguran que Paperly.utec mantenga un rendimiento óptimo mientras evoluciona!** 🚀
