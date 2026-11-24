# Diagnóstico de revisión — La vida en tres dimensiones

Revisé `informe.md`, las seis respuestas por desafío, el README, los scripts y los CSV/PDB incluidos. La corrección del documento se debe hacer con cuidado porque hay afirmaciones que no salen de los archivos presentes y una confusión sobre el modelo de E7. Este diagnóstico registra los hallazgos de la primera etapa, antes de aplicar las correcciones descritas en el informe revisado.

## Problemas críticos

1. **Desafío VI: origen del modelo analizado — error comprobado.** El texto y el README identifican `datos/AF-P03129.pdb` como un modelo de AlphaFold DB generado con ColabFold. El encabezado de ese PDB lo identifica como un modelo de ViRO3D (`AF-0000000365760270-MODEL_V1`) y cita su origen. En cambio, `datos/test_3b510.result.zip` contiene una corrida de ColabFold 1.6.3, con `use_templates: true`, `num_relax: 1`, cinco modelos y secuencia de 98 aa. Por lo tanto, los valores de `resultados/plddt_E7.csv` (81,3 global; 66,1 en 1–40; 95,4 en 61–98) describen el PDB de ViRO3D, no la corrida de ColabFold archivada. **Corrección necesaria:** tomar como resultado de ColabFold el modelo relajado rank 1 del ZIP, recalcular y actualizar gráfico y valores. Con ese modelo los promedios son 81,5 global; 66,3 en 1–40; 85,1 en 41–60 y 95,5 en 61–98. El JSON de configuración confirma ColabFold 1.6.3, no 1.5.2. La forma exacta de activar `pdb100` no figura en el `config.json`; el ZIP sí incluye nombres de plantillas usadas.

2. **Desafíos IV–V: causalidad atribuida a los pKa — interpretación no demostrada.** Los CSV respaldan los pKa calculados y los desplazamientos respecto de los valores de referencia. No demuestran que esos desplazamientos sean la causa de catálisis, ni que el microambiente descrito sea el mecanismo responsable. Frases como “es exactamente lo que se necesita”, “eso explica su pKa” y “la selección natural mantuvo” exceden lo que se puede concluir de PROPKA sobre una estructura aislada. **Corrección necesaria:** explicar que un pKa desplazado sugiere un entorno distinto y puede ser compatible con una función, pero que estos cálculos no prueban mecanismo ni adaptación. Los pKa extremos de PROPKA deben presentarse como predicciones, no valores experimentales.

## Problemas importantes

3. **Desafío I: datos de contactos con ligando y SASA sin trazabilidad local.** Las cifras de SASA, distancias del puente salino y la lista de residuos en contacto con el inhibidor no se producen con ninguno de los scripts incluidos y no hay tablas fuente para reproducirlas. Los CSV sí respaldan cantidades/volúmenes/druggability de cavidades. Además, la frase “los residuos que rodean al ligando coinciden con los que revisten la cavidad” es más fuerte que lo que demuestra el CSV: la cavidad 1 de 3W32 enumera una lista mucho más corta de residuos en `cavidades.csv`. **Corrección necesaria:** conservar como no verificadas las cifras externas o retirarlas del argumento; no usarlas como evidencia central sin una tabla/script de cálculo.

4. **Desafíos IV–V: cavidad geométrica y “sitio activo” se tratan como equivalentes.** La coincidencia de residuos en cavidades apoya una posible relación espacial, pero fpocket no determina por sí mismo que una cavidad sea catalítica. En 4JK4, K221 pertenece a las cavidades 4 y 38, mientras que el bolsillo principal 5 no la incluye; en HSA, la cavidad 1 sí contiene K199/R222. La conclusión de “inversión” y de conservación evolutiva necesita apoyarse en la referencia bioquímica y en una comparación estructural/alineamiento, no solo en esos resultados.

5. **Desafío III: pKa de H117 = 1,52.** El valor está en `pka.csv`, pero es extremo para una histidina y depende del modelo y de haber retirado NADP. Llamarlo simplemente “muy ácido” puede sugerir que es un valor fisiológico confirmado. **Corrección necesaria:** mantenerlo como salida de PROPKA y aclarar que no se interpreta como medición ni se usa para inferir por sí solo una función.

6. **Desafío VI: lectura del PAE.** El texto atribuye al PAE alto/bajo una orientación relativa del dominio C. La figura y el script resumen PAE por residuo promediando una dimensión; esa curva no justifica una afirmación detallada sobre orientación de dominios. **Corrección necesaria:** limitar la conclusión a confianza local alta en el dominio C y mayor incertidumbre en la posición relativa del segmento N-terminal, distinguiendo pLDDT de PAE.

7. **Sección de reproducibilidad: rutas incompatibles con el repositorio.** El informe indica `scripts/`, `data/`, `resultados/figuras/` y `resultados/tablas/`, pero el repositorio usa `src/`, `datos/` y archivos directamente dentro de `resultados/`. Los enlaces a las figuras del informe también usan rutas inexistentes. **Corrección necesaria:** usar las rutas reales y dar comandos reproducibles con los scripts presentes.

8. **README: datos de portada y resumen no coinciden completamente con el documento o los CSV.** Ejemplos: README atribuye a 3W32 una cavidad de 711 Å³ (CSV: 710,7, redondeo aceptable), a HSA cavidad 1 de 2656 Å³ (CSV: 2656,5, redondeo aceptable), pero describe el modelo E7 y la versión de ColabFold incorrectamente. El pKa de K221 concuerda con el CSV. La portada debe alinearse con el modelo del ZIP después de corregir el informe.

## Problemas menores de redacción y consistencia

9. Se repite K195 en la lista de solapamiento de HSA; hay conclusiones duplicadas en las respuestas puntuales y el resumen. Algunas palabras (“drogable”, “activada”, “selección conformacional”) aparecen sin explicación breve en su primera mención.

10. El informe alterna `Å³` y “A3”, `pKa`/`pKa esperado`, y los identificadores `1AO6A`, `1AO6_A` y `1AO6`; se recomienda normalizar unidades, nombres y separadores decimales.

11. El texto mezcla resultados propios, información del PDB/UniProt y literatura sin marcar siempre de qué fuente proviene cada afirmación. Se recomienda agregar referencias junto a afirmaciones que no salen de los archivos generados.

## Cálculos y datos que sí coinciden con los archivos

- Los conteos de cavidades (`1M14_A`: 24; `3W32_A`: 21; `2FVL_B`: 21; `1AO6_A`: 36; `4JK4_A`: 41) y los conteos drogables coinciden con `cavidades_resumen.csv` bajo el corte indicado de druggability > 0,5.
- Los volúmenes/druggability destacados de 2FVL, 1AO6 y 4JK4 son redondeos coherentes de `cavidades.csv`; 1AO6 tiene 2 cavidades sobre el corte y 4JK4 tiene 3.
- Los valores reportados para K199, R222, R218, K195, R410, Y411, K221, R198 y R217 aparecen en `pka.csv`.
- Los tramos de pLDDT y medias del informe corresponden al CSV de ViRO3D, según cálculo directo. No corresponden al ZIP de ColabFold, que ofrece una segunda fuente para corregir esa sección.

## Pendientes de verificación manual

- Recalcular o documentar SASA, distancias de contactos y los términos de desolvatación usados en los desafíos I y V. No están respaldados por scripts ni tablas en el repositorio.
- Confirmar si la consigna exige expresamente guardar la corrida original de ColabFold en la entrega y si el modelo rank 1 relajado del ZIP es la corrida que se desea reportar. El ZIP es evidencia directa de una ejecución, pero su configuración indica versión 1.6.3.
- Verificar la numeración de residuos canónica frente a numeración PDB en los casos donde se comparan especies o estructuras. En el texto se mezclan posiciones de UniProt, de la cadena PDB y etiquetas históricas de la literatura.

**Estado:** la etapa 1 se documenta en este archivo. Las correcciones de la etapa 2 están aplicadas en [TP_revisado.md](TP_revisado.md); el documento original `informe.md` se conserva.
