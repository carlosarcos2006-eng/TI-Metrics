from abc import ABC, abstractmethod

class BaseLogParser(ABC):
    """Clase base abstracta para los lectores de logs."""

    def __init__(self, ruta_archivo: str):
        if not isinstance(ruta_archivo, str):
            raise TypeError("La ruta debe ser una cadena de texto.")

        if not ruta_archivo.strip():
            raise ValueError("La ruta del archivo no puede estar vacía.")

        self._ruta_archivo = ruta_archivo

    @property
    def ruta_archivo(self) -> str:
        """Devuelve la ruta del archivo."""
        return self._ruta_archivo

    @abstractmethod
    def leer(self):
        """Método que deben implementar las clases hijas."""
        pass