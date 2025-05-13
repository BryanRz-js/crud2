#!/bin/bash

# === Configuración ===
VENV_PATH="venv"
PROJECT_ROOT="/home/bryan/Documentos/flask/crud"
EXPECTED_INTERPRETER="$PROJECT_ROOT/venv/bin/python3"

# === Inicio del script ===
echo "🔍 Verificando configuración del entorno virtual..."

# 1. Verificar si se está usando el intérprete correcto
CURRENT_INTERPRETER=$(which python)
if [ "$CURRENT_INTERPRETER" == "$EXPECTED_INTERPRETER" ]; then
    echo "✅ Intérprete correcto: $CURRENT_INTERPRETER"
else
    echo "❌ Intérprete incorrecto. Debería ser: $EXPECTED_INTERPRETER"
    echo "💡 Activa tu entorno virtual con: source venv/bin/activate"
    exit 1
fi

# 2. Mostrar PYTHONPATH actual
echo -e "\n📂 Rutas de búsqueda de Python:"
python -c "import sys; print('\n'.join(sys.path))"

# 3. Mostrar ubicación de site-packages
SITE_PACKAGES=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
echo -e "\n📦 Ubicación de site-packages: $SITE_PACKAGES"

# 4. Verificar si las librerías necesarias están instaladas
echo -e "\n🧩 Comprobando librerías..."
for package in flask flask_cors mysql.connector cryptography; do
    if python -c "import $package" >/dev/null 2>&1; then
        echo "✅ Librería '$package' encontrada."
    else
        echo "❌ Librería '$package' NO encontrada. Instálala con pip."
    fi
done

# 5. Recomendación final
echo -e "\n💡 Acciones sugeridas si aún hay errores en VS Code:"
echo "1. Crea/edita el archivo .vscode/settings.json con estas líneas:"
echo '{
  "python.pythonPath": "'$EXPECTED_INTERPRETER'",
  "python.analysis.extraPaths": ["'$SITE_PACKAGES'"],
  "python.analysis.diagnosticMode": "workspace",
  "python.languageServer": "Pylance"
}'
echo "2. Reinicia Pylance: Ctrl + Shift + P → 'Python: Restart Language Server'"
echo "3. Reinicia VS Code completo."

exit 0