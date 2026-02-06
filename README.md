# propiedades_cpp
uso python para crear propiedades de c++

# cpp-config

Generador de `c_cpp_properties.json` para proyectos C++ en VS Code.

## Instalación
```bash
pip install .
```

## Uso rápido
```python
from cpp_config.cpp_config import Cpp_config, Cpp_config_auto

# Configuración automática (rutas estándar)
Cpp_config_auto().config_pybind()

# Configuración personalizada
Cpp_config(
    ruta_compilador="C:/.../cl.exe",
    python_dll="C:/.../Python312/include",
    pybind11_dll="C:/.../pybind11/include",
).config_pybind()
```
