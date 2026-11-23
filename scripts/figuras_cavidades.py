#!/usr/bin/env python3
"""
Graficos de cavidades a partir de resultados/tablas/cavidades.csv.

Genera dos figuras:
  - cavidades_egfr.png      (1M14 vs 3W32)
  - cavidades_albuminas.png (1AO6 vs 4JK4)

Las barras se colorean por druggability (rojo > 0.5) y se marcan las cavidades
que contienen los residuos de interes.

Uso:
    python scripts/figuras_cavidades.py
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GRUPOS = [
    {
        "archivo": "cavidades_egfr.png",
        "titulo": "EGFR: conformero activo (1M14) vs inactivo (3W32)",
        "estructuras": [
            ("1M14_A", "1M14 (activo, apo)", {18: "sitio ATP", 2: "D837 (D813)"}),
            ("3W32_A", "3W32 (inactivo, con inhibidor)", {1: "sitio ATP", 7: "D837"}),
        ],
    },
    {
        "archivo": "cavidades_albuminas.png",
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
    ap.add_argument("--tabla", default="resultados/tablas/cavidades.csv")
    ap.add_argument("--salida", default="resultados/figuras")
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
