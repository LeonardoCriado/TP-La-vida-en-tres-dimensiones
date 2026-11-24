# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío III — Las cavidades de 2FVLB

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
N167). K84 no quedó asignada a la cavidad por fpocket, pero está a **2,89 Å** del
OH de Y55, en el borde del sitio; su función es justamente modular el pKa de la
tirosina. Es una cavidad grande, única y drogable: un bolsillo atractivo para
inhibidores, aunque la selectividad frente a las otras isoformas de AKR1C (muy
similares) es el problema central del diseño.

**pKa (PROPKA, sin NADP):** H117 1,52 (muy ácido), Y55 11,24, K84 12,27. Estos
valores no deben tomarse como los pKa fisiológicos definitivos: la ausencia del
cofactor y de hidrógenos explícitos afecta el cálculo. Lo robusto es la
identificación del sitio, no el valor absoluto.

**Cautela:** CaviDB puede reportar un número de cavidades algo distinto según cómo
separe el sitio del NADP y según la versión de fpocket. Nuestra corrida da 21 y una
sola cavidad drogable, que es la conclusión relevante.

---

El contexto general, la metodología y las referencias completas están en el [informe integral](informe.md).
