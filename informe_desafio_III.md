# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío III — Las cavidades de 2FVLB

> **Consigna original (resumida):** Analizar las cavidades de 2FVLB, indicar cuántas se predijeron, si hay alguna drogable y si coincide con un sitio biológicamente relevante. También se propone investigar el docking y su posible aplicación al trastorno mencionado. [Fuente](https://github.com/AJVelezRueda/Introduccion_a_la_Bioinformatica/blob/master/Teorico_Practicos/Bioinform%C3%A1tica_Estructural/La_vida_en_tres_dimensiones.md).

**Estructura:** 2FVL, cadena B (2FVLB), AKR1C4 unida a NADP⁺, difracción de rayos X
a 2,4 Å. Se eliminó el NADP para el análisis, de modo que el bolsillo del cofactor
queda vacío.

| | Resultado |
|---|---|
| Cavidades predichas | **21** |
| Cavidades drogables (druggability > 0,5) | **1** |
| Cavidad drogable | cavidad 1: 988 Å³, druggability 0,851 |
| Residuos de la cavidad 1 | Y55, H117, D50, G22, T23, S217, R223, N167, S166, W227, etc. |
| ¿Coincide con un sitio relevante? | **Sí**: es el sitio catalítico y de unión a NADP |

La cavidad 1 contiene tres de los cuatro residuos de la tetrada catalítica
(D50, Y55, H117) y varios residuos que contactan el NADP (G22, T23, S217, R223,
N167). K84 no quedó asignada a la cavidad por fpocket, pero está cerca del OH de
Y55 en la estructura (distancia entre NZ de K84 y OH de Y55: 2,89 Å); UniProt la
anota como residuo que modula el pKa de la tirosina. Es una cavidad grande, única y
con druggability > 0,5. Esto podría servir como punto de partida para buscar
inhibidores. Una dificultad sería distinguir AKR1C4 de las otras isoformas AKR1C.

**pKa (PROPKA, sin NADP):** H117 1,52 (muy ácido), Y55 11,24, K84 12,27. Estos
valores no deben tomarse como los pKa fisiológicos definitivos: la ausencia del
cofactor y de hidrógenos explícitos afecta el cálculo. Lo robusto es la
identificación del sitio, no el valor absoluto.

**Cautela:** CaviDB puede reportar un número de cavidades algo distinto según cómo
separe el sitio del NADP y según la versión de fpocket. Nuestra corrida da 21 y una
sola cavidad supera el corte de druggability > 0,5.

---
