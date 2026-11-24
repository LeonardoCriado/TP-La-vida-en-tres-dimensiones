# TP — La vida en tres dimensiones

Trabajo práctico de **bioinformática estructural**: ubiquitina, cavidades proteicas,
albúminas y predicción de estructura con AlphaFold2/ColabFold.

**Autor:** Leonardo Criado · **Fecha:** noviembre de 2026

El [informe integral](informe.md) reúne el desarrollo completo. Para leer cada consigna por separado, están los informes de los [desafíos I](informe_desafio_I.md), [II](informe_desafio_II.md), [III](informe_desafio_III.md), [IV](informe_desafio_IV.md), [V](informe_desafio_V.md) y [VI](informe_desafio_VI.md).

---

## Resultados en una tabla

| Consigna | Resultado principal |
|---|---|
| 1UBQ | X-ray 1,8 Å, 76 aa, una cadena, 602 átomos, R = 0,176 |
| Desafío I — EGFR | 1M14 (activo): sitio ATP abierto y fragmentado; 3W32 (inactivo): cavidad única de 711 Å³, druggability 0,93 |
| Desafío II — AKR1C4 | UniProt P17516: Y55 sitio activo, K84 modula su pKa, tetrada D50/Y55/K84/H117; variante S145C asociada a bipolaridad |
| Desafío III — 2FVLB | 21 cavidades, 1 drogable (988 Å³, druggability 0,85) que coincide con el sitio catalítico/NADP |
| Desafío IV — 1AO6A | 36 cavidades, 2 drogables; cavidad 1 = sitio AII (K199/R222), activada (K199 pKa 6,78) |
| Desafío V — 4JK4A | 41 cavidades, 3 drogables; K221 tiene pKa 5,39 y el sitio está invertido respecto de HSA |
| Desafío VI — E7 | pLDDT medio 81,3; dominio C-terminal 95,4; región N-terminal desordenada (32–40 < 50) |

---

## Estructura del repositorio

```
.
├── informe.md                     # informe integral
├── informe_desafio_I.md           # EGFR en dos conformeros
├── informe_desafio_II.md          # AKR1C4 en UniProt
├── informe_desafio_III.md         # cavidades de AKR1C4
├── informe_desafio_IV.md          # albúmina humana
├── informe_desafio_V.md           # albúmina bovina
├── informe_desafio_VI.md          # E7 del VPH16
├── README.md
├── environment.yml                # entorno con fpocket, PROPKA y Python
├── datos/
│   ├── 1UBQ.pdb                   # ubiquitina
│   ├── AF-P03129.pdb              # modelo AlphaFold DB de E7 (HPV16)
│   ├── PAE_P03129.json            # PAE del mismo modelo
│   └── estructuras/               # cadenas usadas en el análisis de cavidades
├── src/
│   ├── 01_descargar_estructuras.sh   # baja los PDB y arma las cadenas
│   ├── 02_explorar_pdb.py            # anatomía de un archivo PDB (1UBQ)
│   ├── 03_analizar_cavidades.py      # fpocket + PROPKA -> tablas
│   ├── 04_figuras_cavidades.py       # gráficos de cavidades
│   └── 05_plddt.py              # pLDDT (y PAE) por posición
└── resultados/
    ├── fig_cavidades_albuminas.png
    ├── fig_cavidades_egfr.png
    ├── fig_plddt_E7.png
    ├── cavidades.csv
    ├── cavidades_resumen.csv
    ├── pka.csv
    └── plddt_E7.csv
```

---

## Cómo reproducir

```bash
# 1) entorno (conda/mamba)
conda env create -f environment.yml
conda activate tp-estructural

# 2) estructuras
bash src/01_descargar_estructuras.sh

# 3) análisis de cavidades y pKa
python src/03_analizar_cavidades.py

# 4) gráficos
python src/04_figuras_cavidades.py
python src/05_plddt.py datos/AF-P03129.pdb \
    --pae datos/PAE_P03129.json \
    --salida resultados/fig_plddt_E7.png \
    --csv resultados/plddt_E7.csv
```

El análisis de cavidades tarda unos minutos: fpocket corre sobre cada cadena y
PROPKA calcula los pKa. Los resultados quedan en `resultados/`.

Si no tenés `numpy`/`matplotlib` instalados, los scripts de gráficos
(`04_figuras_cavidades.py` y `05_plddt.py`) crean un entorno virtual `.venv` en
la raíz del repositorio, instalan las dependencias y se vuelven a ejecutar solos
(la primera vez necesitan conexión a internet).

---

## Notas metodológicas

- **CaviDB** no estaba disponible al momento de hacer el TP (el dominio no
  respondía). Para no dejar los desafíos sin datos, se reprodujo su pipeline con
  las mismas herramientas que documenta la base: **fpocket 4.2.3** (cavidades) y
  **PROPKA 3.5.1** (pKa). Los valores publicados de CaviDB se citan en el informe
  para comparar.
- Las cavidades se calcularon sobre cadenas aisladas y **sin aguas ni ligandos**,
  para comparar conformeros en las mismas condiciones. Los volúmenes pueden variar
  levemente entre corridas de fpocket.
- El modelo de E7 incluido es el de **AlphaFold DB** (`AF-P03129-F1`, generado con
  ColabFold 1.5.2). La corrida de ColabFold con `num_relax=1` y
  `template_mode="pdb100"` se hace en el notebook de ColabFold; el script
  `05_plddt.py` se aplica directamente al archivo
  `*_relaxed_rank_001_*.pdb` que devuelve esa corrida.

## Consigna original

[La vida en tres dimensiones](https://github.com/AJVelezRueda/Introduccion_a_la_Bioinformatica/blob/master/Teorico_Practicos/Bioinform%C3%A1tica_Estructural/La_vida_en_tres_dimensiones.md),
Dra. Ana Julia Velez Rueda y Nicolás Palopoli (CC BY-SA 4.0).
