# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío V — La albúmina bovina (4JK4A) y la inversión del sitio

> **Consigna original (resumida):** Analizar en CaviDB las cavidades de 4JK4A, su tamaño y su relación con residuos relevantes; comparar el sitio con HSA. También se propone investigar la inversión del sitio en albúminas y su posible relación evolutiva. [Fuente](https://github.com/AJVelezRueda/Introduccion_a_la_Bioinformatica/blob/master/Teorico_Practicos/Bioinform%C3%A1tica_Estructural/La_vida_en_tres_dimensiones.md).

**Estructura:** 4JK4, cadena A, albúmina sérica bovina (BSA) en complejo con ácido
3,5-diiodosalicílico, 2,65 Å. Se eliminaron los ligandos para el análisis.

| | Resultado |
|---|---|
| Cavidades predichas | **41** |
| Cavidades drogables | **3**: cavidad 1 (498 Å³, 0,952), cavidad 3 (436 Å³, 0,552), cavidad 5 (1350 Å³, 0,893) |
| Cavidad principal del sitio AII | **cavidad 5**, 1350 Å³, 33 residuos, druggability 0,893; contiene W213, R198, R217, K187, etc. |
| Cavidades que contienen K221 | cavidad 4 (364 Å³, 0,086) y cavidad 38 (566 Å³, 0,002); **no** la cavidad 5 |

**pKa en BSA**

| Residuo | pKa calculado | pKa esperado | Δ |
|---|---|---|---|
| K221 | **5,39** | 10,50 | **−5,11** |
| R198 | 9,07 | 12,50 | −3,43 |
| R217 | 10,48 | 12,50 | −2,02 |

K221 aparece en las cavidades 4 y 38; R217 aparece en las cavidades 4, 5 y 38.
Los archivos disponibles no incluyen el cálculo de la distancia de 2,9 Å ni el
término de desolvatación mencionado en borradores previos. Por eso informo el pKa
de 5,39 como una predicción y no le asigno una causa estructural única.

**La comparación con la HSA**

| | HSA (1AO6A) | BSA (4JK4A) |
|---|---|---|
| Par de residuos del sitio | K199 / R222 | R198 / K221 |
| Lisina destacada en la interpretación del sitio | **K199**, pKa 6,78 | **K221**, pKa 5,39 |
| Residuo equivalente al otro miembro del par | R222, pKa 9,16 | R198, pKa 9,07 |
| Cavidad que contiene la lisina destacada | cavidad 1 (2656 Å³, 0,955) | cavidad 4 (364 Å³, 0,086) |
| Cavidad principal del sitio AII | cavidad 1 (drogable) | cavidad 5 (1350 Å³, 0,893) |

La publicación comparativa de albúminas describe una inversión del par de residuos
de este sitio entre HSA y BSA. Mis resultados coinciden con esa interpretación,
aunque no la prueban por sí solos. En las posiciones reportadas, K199 de HSA y
K221 de BSA tienen pKa calculados menores que los valores de referencia. Sin un
alineamiento estructural y sin medir actividad, estos resultados no bastan para concluir que los
residuos hayan intercambiado su función ni que la evolución haya conservado un
mecanismo determinado.

En los resultados geométricos, K199 de HSA está en la cavidad 1 y K221 de BSA en
las cavidades 4 y 38, no en la cavidad principal 5. Esto muestra que fpocket dividió
las regiones de manera distinta en estas dos estructuras. No alcanza para concluir
que los sitios tengan diferente afinidad o que se puedan diseñar ligandos selectivos
entre especies.

**Comparación con la literatura.** El estudio de Velez Rueda et al. [14] propone una
inversión del sitio entre HSA y BSA y reporta pKa calculados aproximados de 7,51
(K199) y 9,49 (R222) para HSA, y 9,24 (R198) y 7,27 (K221) para BSA. Nuestros
valores de PROPKA son 6,78; 9,16; 9,07 y 5,39, respectivamente. Los valores
publicados también son predicciones, no mediciones. La diferencia, sobre todo para
K221, indica que estos cálculos dependen de la estructura y la preparación usadas;
no la considero una reproducción cuantitativa del estudio.

**Respuestas puntuales**

- *¿Cuántas cavidades tiene 4JK4A?* 41; 3 drogables.
- *¿Dónde está K221?* En las cavidades 4 (364 Å³, no drogable) y 38 (566 Å³, no
  drogable), no en la cavidad principal 5.
- *¿Cómo se compara con la HSA?* La literatura propone una inversión de los
  residuos del sitio entre las dos albúminas. En nuestros cálculos, K199 y K221
  tienen pKa predichos de 6,78 y 5,39. La cavidad que contiene cada residuo difiere,
  pero fpocket no permite por sí solo concluir qué efecto funcional tiene esa
  diferencia.

---
