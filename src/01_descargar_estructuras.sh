#!/usr/bin/env bash
# Descarga las estructuras usadas en el TP y arma las cadenas que se analizan
# con fpocket (una cadena por archivo, sin aguas ni heteroatomos).
set -euo pipefail

mkdir -p datos/estructuras

# PDB ID:cadenas  (1UBQ es la ubiquitina; el resto, los casos de los desafios)
for entrada in 1UBQ:A 1M14:A 3W32:A 2FVL:B 1AO6:A 4JK4:A; do
  id="${entrada%%:*}"
  cadena="${entrada##*:}"
  if [ ! -f "datos/${id}.pdb" ]; then
    echo "Descargando ${id}..."
    curl -sL "https://files.rcsb.org/download/${id}.pdb" -o "datos/${id}.pdb"
  fi
  python3 - "$id" "$cadena" <<'PY'
import sys
from Bio.PDB import PDBIO, PDBParser, Select

pdb, cadena = sys.argv[1], sys.argv[2]

class Cadena(Select):
    def accept_chain(self, c):
        return c.id == cadena
    def accept_residue(self, r):
        return r.id[0] == " "      # solo aminoacidos, sin aguas ni ligandos

s = PDBParser(QUIET=True).get_structure(pdb, f"datos/{pdb}.pdb")
io = PDBIO()
io.set_structure(s)
io.save(f"datos/estructuras/{pdb}_{cadena}.pdb", Cadena())
PY
done

# Modelo de AlphaFold DB para E7 de HPV16 (misma secuencia del desafio VI)
if [ ! -f datos/AF-P03129.pdb ]; then
  curl -sL -H "User-Agent: Mozilla/5.0" \
    "https://alphafold.ebi.ac.uk/files/AF-0000000365760270-model_v1.pdb" \
    -o datos/AF-P03129.pdb
fi
if [ ! -f datos/PAE_P03129.json ]; then
  curl -sL -H "User-Agent: Mozilla/5.0" \
    "https://alphafold.ebi.ac.uk/files/AF-0000000365760270-predicted_aligned_error_v1.json" \
    -o datos/PAE_P03129.json
fi

echo "Listo. Estructuras en datos/ y datos/estructuras/"
