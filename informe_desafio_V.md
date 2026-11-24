# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío V — La albúmina bovina (4JK4A) y la inversión del sitio

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

K221 está a **2,9 Å** de R217, una repulsión electrostática fuerte, y además está
poco solvatada (el término de desolvatación es −2,69 kcal/mol): eso explica su pKa
tan bajo. Es el mismo tipo de mecanismo que acidifica a R222 en la HSA, donde R222
está a 4,3 Å de R218.

**La comparación con la HSA**

| | HSA (1AO6A) | BSA (4JK4A) |
|---|---|---|
| Par de residuos del sitio | K199 / R222 | R198 / K221 |
| Lisina catalítica (ácida) | **K199**, pKa 6,78 | **K221**, pKa 5,39 |
| Residuo equivalente al otro miembro del par | R222, pKa 9,16 | R198, pKa 9,07 |
| Cavidad que contiene la lisina catalítica | cavidad 1 (2656 Å³, 0,955) | cavidad 4 (364 Å³, 0,086) |
| Cavidad principal del sitio AII | cavidad 1 (drogable) | cavidad 5 (1350 Å³, 0,893) |

La conclusión es que el sitio activo de la albúmina **no está simplemente
"corrido"**: está **invertido**. En la HSA el par es Lys/Arg (K199/R222) y la lisina
ácida es K199; en la BSA el par es Arg/Lys (R198/K221) y la lisina ácida es K221.
Los dos residuos intercambiaron sus posiciones funcionales, y la selección natural
mantuvo un par ácido/base con pKa anómalos en ambos casos. Es una adaptación
interesante: lo que se conserva no es la identidad de los residuos, sino la
**propiedad fisicoquímica** (un residuo básico con pKa bajo) y la geometría de la
cavidad.

Las diferencias de drogabilidad también son sugerentes: en la HSA la lisina
catalítica está dentro de la cavidad principal, grande y drogable; en la BSA está
en una subcavidad más pequeña y no drogable, en el borde de la cavidad principal.
Eso podría explotarse para diseñar ligandos selectivos de especie, aunque hay que
tomarlo con cautela porque fpocket puede partir un sitio grande en subcavidades
según la forma del bolsillo.

**Comparación con la literatura.** El trabajo del grupo de la UNQ (Biochimie, 2022)
describe exactamente esta inversión y reporta pKa promedio de ~7,51 para K199 y
~9,49 para R222 en HSA, y ~9,24 para R198 y ~7,27 para K221 en BSA. Nuestros
valores son más ácidos (6,78; 9,16; 9,07; 5,39), pero la tendencia y la inversión
se reproducen. La diferencia cuantitativa es esperable por la metodología (una
conformación, sin hidrógenos, PROPKA 3.5.1).

**Respuestas puntuales**

- *¿Cuántas cavidades tiene 4JK4A?* 41; 3 drogables.
- *¿Dónde está K221?* En las cavidades 4 (364 Å³, no drogable) y 38 (566 Å³, no
  drogable), no en la cavidad principal 5.
- *¿Cómo se compara con la HSA?* El sitio está invertido: la lisina catalítica es
  K221 en BSA y K199 en HSA; ambas tienen pKa anormalmente bajos (5,39 y 6,78),
  pero la de BSA está en una subcavidad pequeña y no drogable, mientras que la de
  HSA está en la cavidad principal drogable.

---

El contexto general, la metodología y las referencias completas están en el [informe integral](informe.md).
