#!/usr/bin/env python3
"""
Grafica el pLDDT por posicion a partir de un PDB de AlphaFold2 / ColabFold.

En los modelos de AlphaFold2 y ColabFold el pLDDT de cada residuo queda
guardado en la columna B-factor del atomo CA (y de todos los atomos del
residuo). Este script lo lee, lo grafica coloreado por nivel de confianza y
escribe un CSV con los valores por residuo.

Uso:
    python src/05_plddt.py modelo.pdb
    python src/05_plddt.py resultados/*_relaxed_rank_001_*.pdb

Opcional:
    --pae archivo_predicted_aligned_error.json   (grafica tambien el PAE medio)
    --salida figura.png

Si faltan numpy o matplotlib, el script crea un entorno virtual .venv en la raiz
del repositorio, instala las dependencias y se vuelve a ejecutar solo.
"""

import argparse
import csv
import json
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

# Bandas de confianza de AlphaFold2 (pLDDT)
BANDAS = [
    (90, 100, "#0053D6", "Muy alta (>90)"),
    (70, 90, "#65CBF3", "Confiable (70-90)"),
    (50, 70, "#FFDB13", "Baja (50-70)"),
    (0, 50, "#FF7D45", "Muy baja (<50)"),
]


def leer_plddt(pdb):
    """Devuelve arrays (numero de residuo, pLDDT) usando los CA."""
    residuos, valores = [], []
    for linea in Path(pdb).read_text().splitlines():
        if linea.startswith("ENDMDL"):
            break  # si hay varios modelos, uso el primero
        if linea.startswith("ATOM") and linea[12:16].strip() == "CA":
            residuos.append(int(linea[22:26]))
            valores.append(float(linea[60:66]))
    if not valores:
        sys.exit(f"No encontre atomos CA en {pdb}")
    return np.array(residuos), np.array(valores)


def leer_pae(archivo):
    """PAE medio por residuo desde el JSON de ColabFold/AlphaFold."""
    datos = json.loads(Path(archivo).read_text())
    if isinstance(datos, list):
        datos = datos[0]
    pae = np.array(datos["predicted_aligned_error"])
    return pae.mean(axis=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdb", help="modelo PDB de AlphaFold2/ColabFold")
    ap.add_argument("--pae", help="JSON de PAE (opcional)")
    ap.add_argument("--salida", help="PNG de salida")
    ap.add_argument("--csv", help="CSV con pLDDT por residuo")
    args = ap.parse_args()

    pdb = Path(args.pdb)
    res, plddt = leer_plddt(pdb)
    salida = Path(args.salida) if args.salida else pdb.with_name(pdb.stem + "_plddt.png")
    csv_out = Path(args.csv) if args.csv else pdb.with_name(pdb.stem + "_plddt.csv")

    with open(csv_out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["residuo", "plddt"])
        w.writerows(zip(res.tolist(), plddt.tolist()))

    filas = 2 if args.pae else 1
    fig, axes = plt.subplots(filas, 1, figsize=(11, 3.6 * filas), sharex=True,
                             squeeze=False, constrained_layout=True)
    ax = axes[0, 0]

    # puntos coloreados por banda de confianza
    for desde, hasta, color, etiqueta in BANDAS:
        mask = (plddt > desde) & (plddt <= hasta)
        ax.scatter(res[mask], plddt[mask], s=18, color=color, label=etiqueta,
                   zorder=3, edgecolors="none")
    ax.plot(res, plddt, color="#444444", lw=0.8, zorder=2)

    for desde, hasta, color, _ in BANDAS:
        ax.axhspan(desde, hasta, color=color, alpha=0.10, zorder=1)

    ax.set_ylabel("pLDDT")
    ax.set_ylim(0, 100)
    ax.set_xlim(res.min() - 1, res.max() + 1)
    ax.set_title(f"pLDDT por posición — {pdb.name}")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.grid(axis="y", ls=":", alpha=0.4)

    if args.pae:
        pae = leer_pae(args.pae)
        ax2 = axes[1, 0]
        ax2.plot(res[: len(pae)], pae, color="#7B3294", lw=1)
        ax2.fill_between(res[: len(pae)], 0, pae, color="#7B3294", alpha=0.15)
        ax2.set_xlabel("Residuo")
        ax2.set_ylabel("PAE medio (Å)")
        ax2.set_title("Error alineado predicho (PAE) medio por residuo")
        ax2.grid(ls=":", alpha=0.4)
    else:
        ax.set_xlabel("Residuo")

    fig.savefig(salida, dpi=200)
    print(f"Figura: {salida}")
    print(f"CSV:    {csv_out}")
    print(f"pLDDT medio: {plddt.mean():.1f} | "
          f"muy alta: {np.mean(plddt > 90) * 100:.0f}% | "
          f"confiable: {np.mean((plddt > 70) & (plddt <= 90)) * 100:.0f}% | "
          f"baja/muy baja: {np.mean(plddt <= 70) * 100:.0f}%")


if __name__ == "__main__":
    main()
