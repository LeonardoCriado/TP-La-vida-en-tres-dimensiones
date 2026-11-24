#!/usr/bin/env python3
"""
Analisis de cavidades estilo CaviDB: fpocket + PROPKA.

Para cada estructura de datos/estructuras/*.pdb corre fpocket (deteccion de
cavidades) y PROPKA (pKa de residuos ionizables), y arma una tabla con:

  - descriptores de cada cavidad (score, druggability, volumen, residuos)
  - pKa de los residuos ionizables que la revisten y su corrimiento
    (pKa predicho - pKa esperado), que es la base de las "cavidades activadas"
    de CaviDB.

Uso:
    python src/03_analizar_cavidades.py --estructuras datos/estructuras \
        --salida resultados

Requiere fpocket y propka3 en el PATH (ver README).
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

# pKa esperados en solucion usados por PROPKA (modelo interno)
PKA_ESPERADO = {
    "ASP": 3.80,
    "GLU": 4.50,
    "HIS": 6.50,
    "CYS": 9.00,
    "TYR": 10.00,
    "LYS": 10.50,
    "ARG": 12.50,
}

RE_POCKET = re.compile(r"^Pocket (\d+) :\s*$")
RE_VALOR = re.compile(r"^\s*([^:]+?)\s*:\s*([-\d.]+)\s*$")
RE_PKA = re.compile(r"^([A-Z]{3})\s+(-?\d+)\s+([A-Z])\s+(-?\d+\.\d+)\s+\d+\s*%")
RE_ATOMO = re.compile(
    r"^ATOM.{9}(.{3}) (.)(.{3}) (.)(.{4}).{4}(.{8})(.{8})(.{8})"
)


def correr(cmd, cwd):
    """Corre un comando y devuelve su salida; corta si falla."""
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"Fallo {' '.join(map(str, cmd))}:\n{proc.stderr[-2000:]}")
    return proc.stdout + proc.stderr


def correr_fpocket(pdb, cwd):
    salida = Path(cwd) / f"{pdb.stem}_out"
    if salida.is_dir():
        return salida
    correr(["fpocket", "-f", pdb.name], cwd)
    return salida


def correr_propka(pdb, cwd):
    pka = Path(cwd) / f"{pdb.stem}.pka"
    if not pka.exists():
        correr(["propka3", pdb.name], cwd)
    return pka


def leer_pockets(info_txt):
    """Devuelve {nro_pocket: {descriptor: valor}} desde *_info.txt."""
    pockets, actual = {}, None
    for linea in info_txt.read_text().splitlines():
        m = RE_POCKET.match(linea)
        if m:
            actual = int(m.group(1))
            pockets[actual] = {}
            continue
        if actual is not None:
            m = RE_VALOR.match(linea)
            if m:
                pockets[actual][m.group(1).strip()] = float(m.group(2))
    return pockets


def residuos_pocket(atm_pdb):
    """Residuos (nombre, numero) que revisten la cavidad."""
    residuos = []
    for linea in atm_pdb.read_text().splitlines():
        if not linea.startswith("ATOM"):
            continue
        resname = linea[17:20].strip()
        resnum = int(linea[22:26])
        if (resname, resnum) not in residuos:
            residuos.append((resname, resnum))
    return residuos


def leer_pka(pka_txt):
    """Devuelve {(resname, resnum): pKa} de las lineas resumen de PROPKA."""
    valores = {}
    for linea in pka_txt.read_text().splitlines():
        m = RE_PKA.match(linea)
        if m:
            valores[(m.group(1), int(m.group(2)))] = float(m.group(4))
    return valores


def pka_valido(valor):
    """PROPKA usa 99.99 para residuos sin desprotonacion posible (pKa fuera de
    rango); no sirve para promediar, asi que lo excluyo de los estadisticos."""
    return 0.0 < valor < 20.0


def resumen_estructura(pdb, cwd, salida_dir):
    out = correr_fpocket(pdb, cwd)
    info = out / f"{pdb.stem}_info.txt"
    pka_txt = correr_propka(pdb, cwd)
    pka = leer_pka(pka_txt)
    pockets = leer_pockets(info)

    filas = []
    filas_pka = []
    for (resname, resnum), valor in pka.items():
        filas_pka.append(
            {
                "estructura": pdb.stem,
                "residuo": f"{resname}{resnum}",
                "pka": f"{valor:.2f}",
                "pka_esperado": f"{PKA_ESPERADO.get(resname, float('nan')):.2f}",
                "corrimiento": f"{valor - PKA_ESPERADO.get(resname, valor):.2f}",
                "valido": "si" if pka_valido(valor) else "no",
            }
        )

    for nro, desc in sorted(pockets.items()):
        atm = out / "pockets" / f"pocket{nro}_atm.pdb"
        residuos = residuos_pocket(atm) if atm.exists() else []
        ionizables = [(r, n, pka[(r, n)]) for r, n in residuos if (r, n) in pka]
        validos = [(r, n, v) for r, n, v in ionizables if pka_valido(v)]
        valores = [v for _, _, v in validos]
        corrimientos = [abs(v - PKA_ESPERADO[r]) for r, _, v in validos]
        etiquetas = ";".join(f"{r}{n}" for r, n, _ in ionizables)
        filas.append(
            {
                "estructura": pdb.stem,
                "cavidad": nro,
                "score": f"{desc.get('Score', float('nan')):.3f}",
                "druggability": f"{desc.get('Druggability Score', float('nan')):.3f}",
                "drogable": "si" if desc.get("Druggability Score", 0) > 0.5 else "no",
                "volumen": f"{desc.get('Volume', float('nan')):.1f}",
                "n_residuos": len(residuos),
                "residuos": " ".join(f"{r}{n}" for r, n in residuos),
                "n_ionizables": len(ionizables),
                "pka_medio": f"{sum(valores) / len(valores):.2f}" if valores else "",
                "pka_min": f"{min(valores):.2f}" if valores else "",
                "pka_max": f"{max(valores):.2f}" if valores else "",
                "corrimiento_neto": f"{sum(corrimientos):.2f}" if valores else "",
                "residuos_ionizables": etiquetas,
            }
        )
    return filas, filas_pka


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--estructuras", default="datos/estructuras")
    ap.add_argument("--salida", default="resultados")
    args = ap.parse_args()

    dir_est = Path(args.estructuras).resolve()
    dir_sal = Path(args.salida).resolve()
    dir_sal.mkdir(parents=True, exist_ok=True)
    pdbs = sorted(dir_est.glob("*.pdb"))
    if not pdbs:
        sys.exit(f"No hay PDB en {dir_est}")

    todas = []
    todos_pka = []
    for pdb in pdbs:
        print(f"[+] {pdb.stem}", flush=True)
        filas, filas_pka = resumen_estructura(pdb, dir_est, dir_sal)
        todas += filas
        todos_pka += filas_pka

    campos = list(todas[0].keys())
    with open(dir_sal / "cavidades.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(todas)

    with open(dir_sal / "pka.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(todos_pka[0].keys()))
        w.writeheader()
        w.writerows(todos_pka)

    with open(dir_sal / "cavidades_resumen.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["estructura", "n_cavidades", "n_drogables", "volumen_max",
                    "cavidad_mayor", "druggability_max"])
        for pdb in pdbs:
            filas = [f for f in todas if f["estructura"] == pdb.stem]
            mayor = max(filas, key=lambda f: float(f["volumen"]))
            w.writerow([
                pdb.stem,
                len(filas),
                sum(f["drogable"] == "si" for f in filas),
                mayor["volumen"],
                mayor["cavidad"],
                max(float(f["druggability"]) for f in filas),
            ])

    print(f"\nTablas en {dir_sal}/cavidades.csv y cavidades_resumen.csv")


if __name__ == "__main__":
    main()
