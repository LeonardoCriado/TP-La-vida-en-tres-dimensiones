# TP — La vida en tres dimensiones

Trabajo práctico de **bioinformática estructural**: ubiquitina, cavidades proteicas,
albúminas y predicción de estructura con AlphaFold2/ColabFold.

**Autor:** Leonardo Criado · **Fecha:** noviembre de 2026

El desarrollo está organizado por consigna en los informes de los [desafíos I](informe_desafio_I.md), [II](informe_desafio_II.md), [III](informe_desafio_III.md), [IV](informe_desafio_IV.md), [V](informe_desafio_V.md) y [VI](informe_desafio_VI.md).

---

## Resultados en una tabla

| Consigna | Resultado principal |
|---|---|
| 1UBQ | Difracción de rayos X a 1,8 Å, 76 aa, una cadena, 602 átomos, R = 0,176 |
| Desafío I — EGFR | fpocket reparte la región ATP entre cavidades en 1M14; detecta cavidad 1 de 710,7 Å³ y score 0,932 en 3W32 |
| Desafío II — AKR1C4 | UniProt P17516: Y55 sitio activo, K84 modula su pKa, tetrada D50/Y55/K84/H117; S145C se estudió en relación con progesterona y bipolaridad |
| Desafío III — 2FVLB | 21 cavidades, 1 drogable (988 Å³, druggability 0,85) que coincide con el sitio catalítico/NADP |
| Desafío IV — 1AO6A | 36 cavidades; PROPKA predice pKa 6,78 para K199 y 9,16 para R222 en la cavidad 1 |
| Desafío V — 4JK4A | 41 cavidades; PROPKA predice pKa 5,39 para K221; se discute la inversión propuesta en la literatura |
| Desafío VI — E7 | ColabFold 1.6.3, modelo que quedó primero: pLDDT medio 81,5; 61–98: 95,5; 1–40: 66,3 |

---

## Estructura del repositorio

```
.
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
│   ├── AF-P03129.pdb              # modelo ViRO3D de E7 (HPV16)
│   ├── PAE_P03129.json            # PAE de ese modelo
│   ├── test_3b510.result.zip      # corrida ColabFold usada en el desafío VI
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
    ├── fig_plddt_E7.png            # modelo ViRO3D anterior
    ├── fig_plddt_E7_colabfold.png  # modelo que quedó primero en la corrida de ColabFold
    ├── cavidades.csv
    ├── cavidades_resumen.csv
    ├── pka.csv
    ├── plddt_E7.csv                # modelo ViRO3D anterior
    └── plddt_E7_colabfold.csv      # modelo que quedó primero en la corrida de ColabFold
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
unzip -q datos/test_3b510.result.zip -d /tmp/tp-colabfold
python src/05_plddt.py /tmp/tp-colabfold/test_3b510/test_3b510_relaxed_rank_001_alphafold2_ptm_model_4_seed_000.pdb \
    --pae /tmp/tp-colabfold/test_3b510/test_3b510_predicted_aligned_error_v1.json \
    --salida resultados/fig_plddt_E7_colabfold.png \
    --csv resultados/plddt_E7_colabfold.csv
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
  respondía). Se hizo un análisis independiente con **fpocket 4.2.3** (cavidades)
  y **PROPKA 3.5.1** (pKa), herramientas que también usa la base. No se afirma que
  sea una réplica exacta de todos sus pasos.
- Las cavidades se calcularon sobre cadenas aisladas y **sin aguas ni ligandos**,
  para comparar conformeros en las mismas condiciones. Los volúmenes pueden variar
  levemente entre corridas de fpocket.
- El archivo `datos/AF-P03129.pdb` corresponde a ViRO3D, según su encabezado. Para
  el desafío VI analicé el modelo que quedó primero en la corrida de ColabFold
  (rank 1, modelo 4), guardado en `datos/test_3b510.result.zip`. La configuración
  indica ColabFold 1.6.3, que se usaron plantillas y `num_relax=1`. Los valores están en
  `resultados/plddt_E7_colabfold.csv` y la figura asociada. Los archivos anteriores
  de pLDDT se conservaron.

## Consigna original

[La vida en tres dimensiones](https://github.com/AJVelezRueda/Introduccion_a_la_Bioinformatica/blob/master/Teorico_Practicos/Bioinform%C3%A1tica_Estructural/La_vida_en_tres_dimensiones.md),
Dra. Ana Julia Velez Rueda y Nicolás Palopoli (CC BY-SA 4.0).
