# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío VI — E7 del VPH16 con ColabFold

> **Consigna original (resumida):** Predecir la estructura de E7 con ColabFold usando una plantilla de PDB y una relajación; explicar las opciones utilizadas, identificar las regiones de mayor confianza y describir el script para analizar pLDDT. [Fuente](https://github.com/AJVelezRueda/Introduccion_a_la_Bioinformatica/blob/master/Teorico_Practicos/Bioinform%C3%A1tica_Estructural/La_vida_en_tres_dimensiones.md).

**Procedimiento en ColabFold.** Se abre el notebook
[AlphaFold2.ipynb](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb),
se pega la secuencia de E7 en `query_sequence`, se elige un `jobname` y se ejecuta
la predicción con plantillas. La consigna propone `num_relax = 1` y
`template_mode = "pdb100"`. El ZIP de esta corrida confirma `num_relax = 1` y que
se usaron plantillas, aunque su `config.json` no guarda literalmente el valor
elegido en el selector `template_mode`. La secuencia es:

```
MHGDTPTLHEYMLDLQPETTDLYCYEQLNDSSEEEDEIDGPAGQAEPDRAHYNIVTFCCKCDSTLRLCVQSTHVDIRTLEDLLMGTLGIVCPICSQKP
```

**¿Qué es `template_mode` y qué opciones acepta?**
Controla si ColabFold usa plantillas estructurales para la predicción:

- `"none"`: no usa plantillas; predice solo a partir de la secuencia y del MSA.
- `"pdb100"`: busca estructuras del PDB en la base de plantillas y las usa como
  información estructural. Es útil cuando hay estructuras homólogas disponibles.
- `"custom"`: permite subir plantillas propias en formato PDB o mmCIF (nombres de
  cuatro letras en minúscula); el notebook las usa para la búsqueda.

**Resultados.** El repositorio incluye un ZIP con una corrida de ColabFold para la
secuencia de 98 aminoácidos. Analicé el modelo que quedó primero en la clasificación
de la corrida (rank 1, modelo 4). El archivo de configuración registra ColabFold 1.6.3,
plantillas activadas y `num_relax = 1`; el ZIP también guarda los nombres de las
plantillas encontradas. No atribuyo esta corrida a la versión 1.5.2 ni a AlphaFold
DB. El PDB suelto `datos/AF-P03129.pdb` es otro modelo: su encabezado lo identifica
como ViRO3D, así que no lo usé para los valores de esta sección.

![pLDDT y PAE de E7](resultados/fig_plddt_E7_colabfold.png)

| Región | pLDDT medio | Interpretación |
|---|---|---|
| 1–40 | 66,3 | Baja/media; 32–40 queda por debajo de 50 |
| 41–60 | 85,1 | Confiable en promedio |
| 61–98 | **95,5** | Muy alta en promedio; 49–96 tienen pLDDT > 90 |

**¿Qué regiones tienen mayor confianza?**
El **dominio C-terminal** (aproximadamente 61–98) tiene el pLDDT más alto, con un
promedio de 95,5. La región **N-terminal** (1–40) tiene menor confianza y las
posiciones 32–40 quedan por debajo de 50. Esto es compatible con mayor flexibilidad
o desorden en ese tramo, pero el pLDDT mide la confianza del modelo y no es una
medición experimental de desorden. La secuencia de E7 contiene motivos ricos en
cisteína en el extremo C-terminal, asociados con el dominio de unión a zinc; el
PDB modelado no incluye un ion zinc, por lo que esta predicción no verifica su
coordinación. El PAE informa sobre la incertidumbre en la posición relativa entre
residuos; la curva media mostrada no alcanza para afirmar por sí sola que la
orientación global de los dominios sea correcta.

**El script `src/05_plddt.py`**

- Lee el archivo PDB y toma el pLDDT de la columna B-factor de los átomos CA.
- Grafica el pLDDT por número de residuo, coloreado por banda de confianza
  (>90, 70–90, 50–70, <50).
- Opcionalmente grafica el PAE medio por residuo a partir del JSON de PAE.
- Escribe un CSV con `residuo,plddt` y la figura PNG.
- Uso:

```bash
python src/05_plddt.py modelo_relajado_rank_001.pdb \
    --pae archivo_predicted_aligned_error_v1.json \
    --salida resultados/fig_plddt_E7_colabfold.png \
    --csv resultados/plddt_E7_colabfold.csv
```

**Archivos de la corrida.** El ZIP contiene el alineamiento, los nombres de las
plantillas, la configuración, los cinco modelos y sus métricas. Para estos
resultados usé el modelo que quedó primero en la clasificación (rank 1) y el JSON
de PAE correspondiente. La relajación busca mejorar la geometría local, pero no
convierte la predicción en una estructura experimental ni garantiza que represente
el estado funcional de E7.

---
