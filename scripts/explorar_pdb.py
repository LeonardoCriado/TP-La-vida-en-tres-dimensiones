#!/usr/bin/env python3
"""
Explora un archivo PDB "a mano": cuenta registros, cadenas, atomos, aguas,
heteroatomos y reconstruye la secuencia desde los registros ATOM y SEQRES.

Es el codigo que respalda la seccion "Un problema estructural" del informe.

Uso:
    python scripts/explorar_pdb.py data/1UBQ.pdb
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

TRES_A_UNO = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q",
    "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
    "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
    "TYR": "Y", "VAL": "V",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdb")
    args = ap.parse_args()
    lineas = Path(args.pdb).read_text().splitlines()

    registros = Counter(l[:6].strip() for l in lineas if l.strip())
    atomos = [l for l in lineas if l.startswith("ATOM")]
    het = [l for l in lineas if l.startswith("HETATM")]
    cadenas = sorted({l[21] for l in atomos})
    residuos = []
    for l in atomos:
        clave = (l[21], l[22:27])
        if not residuos or residuos[-1] != clave:
            if clave not in residuos:
                residuos.append(clave)

    print(f"Archivo: {args.pdb}")
    print(f"Lineas totales: {len(lineas)}")
    print(f"Registros: {dict(registros.most_common(8))}")
    print(f"Atomos ATOM: {len(atomos)} | HETATM: {len(het)}")
    print(f"Cadenas: {cadenas}")
    print(f"Residuos observados (ATOM): {len(residuos)}")

    agua = sum(1 for l in het if l[17:20] == "HOH")
    if agua:
        print(f"Moléculas de agua: {agua}")

    metales = sorted({l[17:20] for l in het if l[17:20] != "HOH"})
    if metales:
        print(f"Otros heteroatomos: {metales}")

    for l in lineas:
        if l.startswith("HEADER"):
            print(f"HEADER: {l[10:50].strip()} ({l[50:59].strip()})")
        if l.startswith("EXPDTA"):
            print(f"Metodo: {l[10:].strip()}")
        if l.startswith("REMARK   2 RESOLUTION"):
            print(f"Resolucion: {l[23:].strip()}")
        if l.startswith("REMARK   3   R VALUE            (WORKING SET)"):
            print(f"R-work: {l.split(':')[-1].strip()}")

    seq_atom = "".join(TRES_A_UNO.get(l[17:20], "X") for l in lineas
                       if l.startswith("ATOM") and l[12:16].strip() == "CA")
    print(f"\nSecuencia desde ATOM ({len(seq_atom)} aa):")
    print(seq_atom)

    seqres = "".join(
        l[19:].strip().replace(" ", "") for l in lineas if l.startswith("SEQRES")
    )
    secuencia = "".join(TRES_A_UNO.get(t, "X")
                        for t in [seqres[i:i + 3] for i in range(0, len(seqres), 3)])
    print(f"\nSecuencia desde SEQRES ({len(secuencia)} aa):")
    print(secuencia)

    if len(seq_atom) != len(secuencia):
        print("\nOjo: SEQRES y ATOM no coinciden (residuos no observados en el mapa "
              "de densidad electronica).")


if __name__ == "__main__":
    main()
