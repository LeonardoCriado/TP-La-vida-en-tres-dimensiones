#!/usr/bin/env python3
"""
Graficos de cavidades a partir de resultados/cavidades.csv.

Genera dos figuras:
  - fig_cavidades_egfr.png      (1M14 vs 3W32)
  - fig_cavidades_albuminas.png (1AO6 vs 4JK4)

Las barras se colorean por druggability (rojo > 0.5) y se marcan las cavidades
que contienen los residuos de interes.

Uso:
    python src/04_figuras_cavidades.py

Si faltan numpy o matplotlib, el script crea un entorno virtual .venv en la raiz
del repositorio, instala las dependencias y se vuelve a ejecutar solo.
"""

import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path

DEPENDENCIAS = ("numpy", "matplotlib")


def asegurar_dependencias():
    """Instala numpy y matplotlib en un .venv local si no estan disponibles."""
    try:
        import matplotlib  # noqa: F401
        import numpy  # noqa: F401
        return
    except ImportError:
        pass

    venv = Path(__file__).resolve().parent.parent / ".venv"
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    script = str(Path(__file__).resolve())

    # si el .venv ya tiene las dependencias, reejecutar sin instalar nada
    if python.exists():
        listo = subprocess.run([str(python), "-c", "import numpy, matplotlib"],
                               capture_output=True).returncode == 0
        if listo:
            os.execv(str(python), [str(python), script, *sys.argv[1:]])

    if not python.exists():
        print("Faltan numpy y/o matplotlib: creando entorno virtual en .venv ...",
              flush=True)
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    print("Instalando numpy y matplotlib en .venv ...", flush=True)
    subprocess.run([str(python), "-m", "pip", "install", "--quiet",
                    "--disable-pip-version-check", *DEPENDENCIAS], check=True)

    listo = subprocess.run([str(python), "-c", "import numpy, matplotlib"],
                           capture_output=True).returncode == 0
    if not listo:
        sys.exit("No pude importar numpy y matplotlib desde .venv; "
                 "revisa el error de pip de arriba.")
    print("Reejecutando el script con el entorno nuevo ...", flush=True)
    os.execv(str(python), [str(python), script, *sys.argv[1:]])


asegurar_dependencias()

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GRUPOS = [
    {
        "archivo": "fig_cavidades_egfr.png",
        "titulo": "EGFR: conformero activo (1M14) vs inactivo (3W32)",
        "estructuras": [
            ("1M14_A", "1M14 (activo, apo)", {18: "sitio ATP", 2: "D837 (D813)"}),
            ("3W32_A", "3W32 (inactivo, con inhibidor)", {1: "sitio ATP", 7: "D837"}),
        ],
    },
    {
        "archivo": "fig_cavidades_albuminas.png",
        "titulo": "Albúminas: HSA (1AO6) vs BSA (4JK4)",
        "estructuras": [
            ("1AO6_A", "HSA 1AO6 (cadena A)", {1: "K199/R222", 2: "R410/Y411"}),
            ("4JK4_A", "BSA 4JK4 (cadena A)", {5: "cavidad principal", 4: "K221"}),
        ],
    },
]


def leer_tabla(ruta):
    with open(ruta) as fh:
        return list(csv.DictReader(fh))


def graficar(ax, filas, etiqueta, resaltadas):
    top = sorted(filas, key=lambda f: float(f["volumen"]), reverse=True)[:7]
    incluir = {int(f["cavidad"]) for f in top} | set(resaltadas)
    filas = sorted([f for f in filas if int(f["cavidad"]) in incluir],
                   key=lambda f: float(f["volumen"]))
    y = np.arange(len(filas))
    vol = [float(f["volumen"]) for f in filas]
    drug = [float(f["druggability"]) for f in filas]
    colores = plt.cm.RdYlBu_r(np.array(drug))
    barras = ax.barh(y, vol, color=colores, edgecolor="#333333", linewidth=0.5)

    etiquetas = []
    for i, f in enumerate(filas):
        n = int(f["cavidad"])
        txt = f"Cavidad {n}"
        if n in resaltadas:
            txt += f"  ({resaltadas[n]})"
            barras[i].set_edgecolor("black")
            barras[i].set_linewidth(2)
        etiquetas.append(txt)
    ax.set_yticks(y, etiquetas, fontsize=8)
    ax.set_xlabel("Volumen (Å³)")
    ax.set_title(etiqueta, fontsize=10)
    ax.grid(axis="x", ls=":", alpha=0.4)

    for yy, v, d in zip(y, vol, drug):
        ax.text(v + 25, yy, f"{v:.0f} Å³ · {d:.2f}", va="center", fontsize=7)
    ax.set_xlim(0, max(vol) * 1.28)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tabla", default="resultados/cavidades.csv")
    ap.add_argument("--salida", default="resultados")
    args = ap.parse_args()
    filas = leer_tabla(args.tabla)
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    for grupo in GRUPOS:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), constrained_layout=True)
        for ax, (est, etiqueta, resaltadas) in zip(axes, grupo["estructuras"]):
            graficar(ax, [f for f in filas if f["estructura"] == est],
                     etiqueta, resaltadas)
        sm = plt.cm.ScalarMappable(cmap="RdYlBu_r", norm=plt.Normalize(0, 1))
        fig.colorbar(sm, ax=axes, label="Druggability (fpocket)", shrink=0.85)
        fig.suptitle(grupo["titulo"], fontsize=12)
        ruta = salida / grupo["archivo"]
        fig.savefig(ruta, dpi=200)
        print("Figura:", ruta)


if __name__ == "__main__":
    main()
