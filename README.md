# 🔐 Proyecto de Seguridad en el Desarrollo de Software

![CI/CD Status](https://img.shields.io/badge/Pipeline-Passing-success?style=for-the-badge&logo=github-actions)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-ML_Analysis-red?style=for-the-badge&logo=security-scorecard)

## 📌 Pipeline CI/CD con Análisis de Vulnerabilidades mediante Machine Learning

Este proyecto implementa un pipeline completo de **Desarrollo Seguro (DevSecOps)** utilizando GitHub Actions, Machine Learning y reglas de protección de ramas.

El objetivo es garantizar que **cada cambio integrado** al repositorio cumpla con requisitos mínimos de seguridad, calidad y estabilidad.

---

## 🎯 Objetivo General

Implementar un pipeline automatizado que detecte vulnerabilidades en código C utilizando modelos de Machine Learning, y que controle el proceso de integración mediante pruebas, validaciones de seguridad y reglas estrictas en GitHub.

---

## 🧱 Arquitectura del Pipeline

El repositorio utiliza tres workflows principales orquestados para validar cada Pull Request:

### 1️⃣ Security Check (Análisis de Código con ML)
* **Archivo:** `.github/workflows/security-check.yml`
* **Función:** Detecta vulnerabilidades en código C utilizando un modelo entrenado con **Juliet Test Suite**.
* **Métrica:** Si encuentra vulnerabilidades con probabilidad **≥ 0.40**, marca el PR como fallido.
* **Detalle:** Analiza tokens, profundidad del AST y funciones peligrosas.

### 2️⃣ Unit Tests
* **Archivo:** `.github/workflows/unit-tests.yml`
* **Función:** Ejecuta pruebas simuladas para validar la integridad del proyecto.
* **Objetivo:** Garantizar que los cambios no rompan funcionalidades existentes.

### 3️⃣ Deploy / Build Simulation
* **Archivo:** `.github/workflows/deploy.yml`
* **Función:** Realiza una compilación simulada.
* **Objetivo:** Verificar que el proyecto se pueda construir (build) correctamente antes de integrar.

---

## 🛡️ Reglas de Protección de Ramas (Branch Protection)

La rama principal (`main` o `test`) está protegida bajo las siguientes reglas estrictas:

* 🔒 **Require a pull request before merging:** No se permite push directo.
* ✅ **Require status checks to pass:**
    * `security-check`
    * `unit-tests`
    * `deploy`
* 👀 **Review required:** Se requiere aprobación manual del PR antes del merge.

**Resultado:**
> No se puede integrar código vulnerable, que rompa la compilación o que no haya sido revisado.

---

## 🧠 Modelo de Machine Learning

Se entrenó un modelo con el dataset **Juliet Test Suite** (NIST), analizando miles de ejemplos de código vulnerable y no vulnerable.

### Características analizadas (Features):
* Tokenización del código.
* Profundidad del AST (Abstract Syntax Tree).
* Conteo de funciones peligrosas (`strcpy`, `gets`, `system`, etc.).
* Vectorización tipo *Bag-of-Words*.

### Métricas del Modelo:
* **Dataset:** 41,651 Vulnerables / 12,635 No vulnerables.
* **Accuracy promedio:** 85.73%

El modelo se encuentra serializado en:
* `/model/model.pkl`
* `/model/vectorizer.pkl`

---

## 🔍 Funcionamiento del Scanner (`scan.py`)

El escáner recibe los archivos modificados en el PR y calcula la probabilidad de vulnerabilidad.

**Salida JSON de ejemplo:**

```json
{
  "file": "test/example_vuln.c",
  "p_vulnerable": 0.43,
  "ast_depth": 12,
  "danger_count": 2
}
```

🚨 Criterio de Fallo: Si `p_vulnerable >= 0.40`, el pipeline falla y bloquea el merge.

## 🚀 Flujo de Trabajo del Desarrollador

1. Crear una rama nueva (feature/..., fix/...).
2. Realizar cambios en el código, commit y push.
3. Abrir Pull Request hacia la rama protegida.
4. Esperar ejecución automática de GitHub Actions:
5. Security Check
  5.1. Unit Tests
  5.2. Deploy

Si los tres checks pasan (✅), el PR puede ser aprobado y mergeado.

## 🧪 Evidencia del Funcionamiento

* ✔️ Se detectan vulnerabilidades reales en archivos .c.
* ✔️ Los cambios seguros pasan el pipeline automáticamente.
* ✔️ Los cambios peligrosos bloquean el botón de merge.
* ✔️ El pipeline fuerza la cultura de "Code Review".

## 📂 Estructura del Repositorio
```
Proyecto_SS_Pipeline/
│
├── model/
│   ├── model.pkl           # Modelo entrenado
│   └── vectorizer.pkl      # Vectorizador
│
├── scan.py                 # Script de análisis de seguridad
├── requirements.txt        # Dependencias de Python
├── test/
│   ├── example.c           # Archivo de prueba seguro
│   └── example_vuln.c      # Archivo de prueba vulnerable
│
└── .github/
    └── workflows/
        ├── security-check.yml
        ├── unit-tests.yml
        └── deploy.yml
```
## 🏁 Conclusión
Este proyecto implementa un pipeline completo y automatizado que:

1. Detecta vulnerabilidades en código C.
2. Automatiza el proceso de revisión.
3. Impide integrar código inseguro.
4. Mantiene buenas prácticas DevSecOps.

Es un ejemplo práctico de cómo aplicar Seguridad en el Desarrollo de Software utilizando herramientas modernas como GitHub Actions y Machine Learning.

##👤 Autores
Proyecto desarrollado para la materia de Desarrollo de Software Seguro Universidad de las Fuerzas Armadas ESPE

* 👨‍💻 Dylan G. Reinoso
* 👨‍💻 Kleber E. Chavez
* 👩‍💻 Pamela N. Chipe
