#!/usr/bin/env python3
"""
FlockLedger - Punto de entrada de la aplicación
"""

import sys
import os

# Agregar la carpeta src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import FlockLedgerApp
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    app = FlockLedgerApp(root)
    root.mainloop()
