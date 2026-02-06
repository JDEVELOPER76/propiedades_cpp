import os
import json


class Cpp_config:
    """
    Configurador personalizado de C++ para Visual Studio Code.
    
    Permite crear archivos c_cpp_properties.json con rutas personalizadas para proyectos C++.
    Ideal para usuarios avanzados que necesitan configurar rutas específicas de compilador,
    Python y pybind11.
    
    Configuraciones estándar utilizadas:
        - cStandard: "c17"
        - cppStandard: "c++20"
        - intelliSenseMode: "windows-msvc-x64"
    
    Atributos:
        ruta_compilador (str | None): Ruta al compilador de MSVC (cl.exe).
        python_dll (str | None): Ruta al directorio include de Python.
        pybind11_dll (str | None): Ruta al directorio include de pybind11.
    
    Ejemplo:
        >>> # Configuración básica de C++ sin pybind11
        >>> config = Cpp_config(
        ...     ruta_compilador="C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe"
        ... )
        >>> config.config_estandar()  # Usa el directorio actual
        
        >>> # Configuración con pybind11
        >>> config = Cpp_config(
        ...     ruta_compilador="C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe",
        ...     python_dll="C:/Users/SZ/AppData/Local/Programs/Python/Python312/include",
        ...     pybind11_dll="C:/Users/SZ/AppData/Local/Programs/Python/Python312/Lib/site-packages/pybind11/include"
        ... )
        >>> config.config_pybind("C:/mi/proyecto")  # Ruta personalizada
    """
    def __init__(self, ruta_compilador: str | None = None, python_dll: str | None = None, pybind11_dll: str | None = None):
        """
        Inicializa el configurador con las rutas personalizadas.
        
        Args:
            ruta_compilador: Ruta completa al ejecutable del compilador cl.exe de MSVC.
            python_dll: Ruta al directorio include de Python (necesario para pybind11).
            pybind11_dll: Ruta al directorio include de pybind11 (necesario para pybind11).
        """
        self.ruta_compilador = ruta_compilador
        self.python_dll = python_dll
        self.pybind11_dll = pybind11_dll

    def _build_config_estandar(self) -> dict:
        """
        Construye la configuración estándar de C++ sin pybind11.
        
        Returns:
            dict: Diccionario con la configuración de c_cpp_properties.json.
        
        Raises:
            ValueError: Si ruta_compilador no está definida.
        """
        if not self.ruta_compilador:
            raise ValueError("ruta_compilador es requerido")

        return {
            "configurations": [
                {
                    "name": "MSVC",
                    "includePath": [
                        "${workspaceFolder}/**",
                    ],
                    "compilerPath": self.ruta_compilador,
                    "cStandard": "c17",
                    "cppStandard": "c++20",
                    "intelliSenseMode": "windows-msvc-x64",
                }
            ],
            "version": 4,
        }

    def _build_config_pybind(self) -> dict:
        """
        Construye la configuración de C++ con soporte para pybind11.
        
        Incluye las rutas de Python y pybind11 en includePath para permitir
        el desarrollo de extensiones de Python en C++.
        
        Returns:
            dict: Diccionario con la configuración de c_cpp_properties.json.
        
        Raises:
            ValueError: Si falta ruta_compilador, python_dll o pybind11_dll.
        """
        if not self.ruta_compilador:
            raise ValueError("ruta_compilador es requerido")
        if not self.python_dll:
            raise ValueError("python_dll es requerido")
        if not self.pybind11_dll:
            raise ValueError("pybind11_dll es requerido")

        return {
            "configurations": [
                {
                    "name": "MSVC",
                    "includePath": [
                        "${workspaceFolder}/**",
                        self.pybind11_dll,
                        self.python_dll,
                    ],
                    "compilerPath": self.ruta_compilador,
                    "cStandard": "c17",
                    "cppStandard": "c++20",
                    "intelliSenseMode": "windows-msvc-x64",
                }
            ],
            "version": 4,
        }

    def config_estandar(self, ruta: str | None = None) -> None:
        """
        Genera archivo c_cpp_properties.json con configuración estándar de C++.
        
        Crea el directorio .vscode si no existe y genera el archivo de configuración
        sin las rutas de pybind11. Ideal para proyectos C++ puros.
        
        Args:
            ruta: Ruta del proyecto donde crear .vscode/c_cpp_properties.json.
                  Si es None, usa el directorio actual (os.getcwd()).
        
        Ejemplo:
            >>> config = Cpp_config(ruta_compilador="C:/ruta/al/cl.exe")
            >>> config.config_estandar()  # Genera en directorio actual
            >>> config.config_estandar("C:/mi/proyecto")  # Genera en ruta específica
        """
        if ruta is None:
            ruta = os.getcwd()
        os.makedirs(f"{ruta}/.vscode", exist_ok=True)
        with open(f"{ruta}/.vscode/c_cpp_properties.json", "w") as f:
            json.dump(self._build_config_estandar(), f, indent=4)

    def config_pybind(self, ruta: str | None = None) -> None:
        """
        Genera archivo c_cpp_properties.json con soporte para pybind11.
        
        Crea el directorio .vscode si no existe y genera el archivo de configuración
        incluyendo las rutas de Python y pybind11. Necesario para desarrollar
        extensiones de Python en C++.
        
        Args:
            ruta: Ruta del proyecto donde crear .vscode/c_cpp_properties.json.
                  Si es None, usa el directorio actual (os.getcwd()).
        
        Raises:
            ValueError: Si faltan python_dll o pybind11_dll en la instancia.
        
        Ejemplo:
            >>> config = Cpp_config(
            ...     ruta_compilador="C:/ruta/al/cl.exe",
            ...     python_dll="C:/Python312/include",
            ...     pybind11_dll="C:/Python312/Lib/site-packages/pybind11/include"
            ... )
            >>> config.config_pybind()  # Genera en directorio actual
        """
        if ruta is None:
            ruta = os.getcwd()
        os.makedirs(f"{ruta}/.vscode", exist_ok=True)
        with open(f"{ruta}/.vscode/c_cpp_properties.json", "w") as f:
            json.dump(self._build_config_pybind(), f, indent=4)
    

class Cpp_config_auto:
    """
    Configurador automático de C++ para Visual Studio Code.
    
    Utiliza rutas predefinidas para el compilador MSVC, Python y pybind11.
    Ideal para usuarios con instalaciones estándar que no necesitan personalización.
    
    Rutas predefinidas:
        - Compilador: C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe
        - Python include: C:/Users/SZ/AppData/Local/Programs/Python/Python312/include
        - pybind11 include: C:/Users/SZ/AppData/Local/Programs/Python/Python312/Lib/site-packages/pybind11/include
    
    Nota:
        Si tus instalaciones están en rutas diferentes, usa la clase Cpp_config en su lugar.
    
    Ejemplo:
        >>> # Configuración rápida sin parámetros
        >>> config = Cpp_config_auto()
        >>> config.config_pybind()  # Genera en directorio actual
        >>> config.config_estandar("C:/mi/proyecto")  # Genera en ruta específica
    """
    def __init__(self):
        """
        Inicializa el configurador automático.
        
        No requiere parámetros ya que utiliza rutas predefinidas.
        """
        pass

    def config_estandar(self, ruta: str | None = None):
        """
        Genera archivo c_cpp_properties.json con configuración predefinida.
        
        Usa rutas estándar para el compilador MSVC sin incluir pybind11.
        
        Args:
            ruta: Ruta del proyecto donde crear .vscode/c_cpp_properties.json.
                  Si es None, usa el directorio actual (os.getcwd()).
        
        Ejemplo:
            >>> config = Cpp_config_auto()
            >>> config.config_estandar()  # Genera en directorio actual
        """
        if ruta is None:
            ruta = os.getcwd()
        os.makedirs(f"{ruta}/.vscode", exist_ok=True)
        with open(f"{ruta}/.vscode/c_cpp_properties.json", "w") as f:
            json.dump(estandar_1, f, indent=4)

    def config_pybind(self, ruta: str | None = None):
        """
        Genera archivo c_cpp_properties.json con soporte pybind11 predefinido.
        
        Usa rutas estándar para el compilador MSVC, Python y pybind11.
        
        Args:
            ruta: Ruta del proyecto donde crear .vscode/c_cpp_properties.json.
                  Si es None, usa el directorio actual (os.getcwd()).
        
        Ejemplo:
            >>> config = Cpp_config_auto()
            >>> config.config_pybind()  # Genera en directorio actual con pybind11
        """
        if ruta is None:
            ruta = os.getcwd()
        os.makedirs(f"{ruta}/.vscode", exist_ok=True)
        with open(f"{ruta}/.vscode/c_cpp_properties.json", "w") as f:
            json.dump(pybind_2, f, indent=4)


estandar_1 = {
    "configurations": [
        {
            "name": "MSVC",
            "includePath": [
                "${workspaceFolder}/**",
                "C:/Users/SZ/AppData/Local/Programs/Python/Python312/Lib/site-packages/pybind11/include",
                "C:/Users/SZ/AppData/Local/Programs/Python/Python312/include"
            ],
            "compilerPath": "C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe",
            "cStandard": "c17",
            "cppStandard": "c++20",
            "intelliSenseMode": "windows-msvc-x64"
        }
    ],
    "version": 4
}

pybind_2 = {
    "configurations": [
        {
            "name": "MSVC",
            "includePath": [
                "${workspaceFolder}/**",
                "C:/Users/SZ/AppData/Local/Programs/Python/Python312/Lib/site-packages/pybind11/include",
                "C:/Users/SZ/AppData/Local/Programs/Python/Python312/include"
            ],
            "compilerPath": "C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe",
            "cStandard": "c17",
            "cppStandard": "c++20",
            "intelliSenseMode": "windows-msvc-x64"
        }
    ],
    "version": 4
}

