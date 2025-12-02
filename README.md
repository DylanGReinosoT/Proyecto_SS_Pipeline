# 🔐 Proyecto de Seguridad en el Desarrollo de Software  
## Pipeline CI/CD con Análisis de Vulnerabilidades mediante Machine Learning

Este proyecto implementa un pipeline completo de **Desarrollo Seguro (DevSecOps)** utilizando GitHub Actions, Machine Learning y reglas de protección de ramas.  
El objetivo es garantizar que cada cambio integrado al repositorio cumpla con requisitos mínimos de seguridad, calidad y estabilidad.

---

## 📌 Objetivo General

Implementar un pipeline automatizado que detecte vulnerabilidades en código C utilizando modelos de Machine Learning, y que controle el proceso de integración mediante pruebas, validaciones de seguridad y reglas estrictas en GitHub.

---

## 🧱 Arquitectura del Pipeline

El repositorio utiliza tres workflows principales:

### 1️⃣ **Security Check (Análisis de Código con ML)**
Ubicación: `.github/workflows/security-check.yml`

- Detecta vulnerabilidades en código C utilizando un modelo entrenado con **Juliet Test Suite**.  
- Extrae tokens, profundidad del AST y funciones peligrosas.
- Si encuentra vulnerabilidades con probabilidad ≥ **0.40**, marca el PR como fallido.
- Evita que código inseguro sea integrado a ramas protegidas.

---

### 2️⃣ **Unit Tests**
Ubicación: `.github/workflows/unit-tests.yml`

- Ejecuta pruebas (simuladas) para validar integridad del proyecto.
- Garantiza que los cambios no rompan funcionalidades existentes.

---

### 3️⃣ **Deploy / Build Simulation**
Ubicación: `.github/workflows/deploy.yml`

- Realiza una compilación simulada.
- Verifica que el proyecto se pueda construir correctamente.

---

## 🛡️ Reglas de Protección de Ramas (Branch Protection Rules)

La rama principal (`main` o `test`, según el flujo de trabajo) está protegida con los siguientes requisitos:

- **Require a pull request before merging**
- **Require status checks to pass before merging**
  - ✔️ security-check  
  - ✔️ unit-tests  
  - ✔️ deploy  
- **No se permite hacer push directo a la rama protegida**
- **Se requiere aprobación del PR antes de merge**

Esto garantiza que:

- No se puede integrar código vulnerable
- No se puede integrar código que falle la construcción
- No se puede integrar código sin revisiones previas

---

## 🧠 Modelo de Machine Learning

Se entrenó un modelo con el dataset **Juliet Test Suite**, el cual contiene miles de ejemplos de código vulnerable y no vulnerable.

### Características analizadas:
- Tokenización del código
- Profundidad del AST (Abstract Syntax Tree)
- Conteo de funciones peligrosas (`strcpy`, `gets`, `system`, etc.)
- Vectorización tipo Bag-of-Words

### Resultado del entrenamiento:
- **Distribución:**  
  - Vulnerable: 41,651  
  - No vulnerable: 12,635  
- **Accuracy promedio:** 0.8573 (85.7%)

El modelo se guarda en:

/model/model.pkl
/model/vectorizer.pkl

y es utilizado por el script:

scan.py


---

## 🔍 Funcionamiento del Scanner (`scan.py`)

El escáner recibe los archivos modificados en el PR y calcula:

- Tokens del código
- Profundidad del AST
- Uso de funciones peligrosas
- Probabilidad de vulnerabilidad

Ejemplo de salida:

```json
{
  "file": "test/example_vuln.c",
  "p_vulnerable": 0.43,
  "ast_depth": 12,
  "danger_count": 2
}
```
Si p_vulnerable ≥ 0.40, el pipeline falla.

🚀 Flujo de Trabajo del Desarrollador

Crear una rama nueva (feature/..., fix/..., etc.)

1. Realizar cambios en el código
2. Hacer commit y push
3. Abrir Pull Request hacia la rama protegida
4. Esperar ejecución automática de:
5. Security Check
  5.1. Unit Tests
  5.2.Deploy
6. Si los tres checks pasan, el PR puede ser aprobado y mergeado

🧪 Evidencia del Funcionamiento

- ✔️ Se detectan vulnerabilidades en archivos .c
- ✔️ Los cambios seguros pasan el pipeline
- ✔️ Los cambios peligrosos bloquean el merge
- ✔️ El pipeline obliga a trabajar con PR y revisiones

📂 Estructura del Repositorio

Proyecto_SS_Pipeline/
│
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── scan.py
├── requirements.txt
├── test/
│   ├── example.c
│   └── example_vuln.c
│
└── .github/
    └── workflows/
        ├── security-check.yml
        ├── unit-tests.yml
        └── deploy.yml

🏁 Conclusión

Este proyecto implementa un pipeline completo y automatizado de seguridad que:

- Detecta vulnerabilidades reales en código C
- Automatiza el proceso de revisión
- Impide integrar código inseguro
- Mantiene buenas prácticas DevSecOps

Es un ejemplo práctico y realista de cómo aplicar Seguridad en el Desarrollo de Software utilizando herramientas modernas como GitHub Actions y Machine Learning.

👤 Autor

Proyecto desarrollado por Dylan G. Reinoso, Kleber E. Chanvez, Pamela N. Chipe
Materia: Desarrollo de Software Seguro
Institución: Universidad de las Fuerzas Armadas ESPE
