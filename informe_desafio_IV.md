# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío IV — La albúmina humana (1AO6A)

**Estructura:** 1AO6, cadena A, albúmina sérica humana (HSA), 2,5 Å, sin ligandos
(albúmina "defatted"). La HSA tiene tres dominios homólogos (I, II y III), cada uno
con dos subdominios (A y B); los sitios de unión a fármacos más importantes son el
**sitio I** (subdominio IIA, Sudlow I) y el **sitio II** (subdominio IIIA,
Sudlow II).

| | Resultado |
|---|---|
| Cavidades predichas | **36** |
| Cavidades drogables | **2** (cavidad 1: 2656 Å³, 0,955; cavidad 2: 326 Å³, 0,675) |
| Cavidades más grandes | 36 (2713 Å³, 0,36), 1 (2656 Å³, 0,955), 30 (1388 Å³, 0,05), 18 (1197 Å³, 0,02) |
| Cavidad del sitio I (AII) | **cavidad 1**, 2656 Å³, 65 residuos, druggability 0,955 |
| Cavidad del sitio II (AIII) | **cavidad 2**, 326 Å³, druggability 0,675 |

![Cavidades de HSA y BSA](resultados/fig_cavidades_albuminas.png)

**¿Se solapan las cavidades con los residuos relevantes?**

- **K195, K199, R222, W214, R218, H242** están en la **cavidad 1** (sitio AII).
  La cavidad 1 es la segunda más grande de la proteína (la 36 es apenas mayor pero
  no es drogable), lo que coincide con la descripción del sitio AII como una de las
  cavidades principales.
- **R410 y Y411** están en la **cavidad 2** (sitio AIII).
- **C34** no pertenece a ninguna cavidad predicha: está en una grieta superficial,
  accesible, consistente con su papel de tiol libre reactivo y con su participación
  en reacciones redox/antioxidantes.
- **K195** también está en la cavidad 1, junto con K199 y R222.

**pKa y cavidades activadas**

| Residuo | pKa calculado | pKa esperado | Δ |
|---|---|---|---|
| K199 | 6,78 | 10,50 | **−3,72** |
| R222 | 9,16 | 12,50 | **−3,34** |
| R218 | 10,84 | 12,50 | −1,66 |
| K195 | 9,99 | 10,50 | −0,51 |
| R410 (cavidad 2) | 11,99 | 12,50 | −0,51 |
| Y411 (cavidad 2) | 11,19 | 10,00 | +1,19 |

La **cavidad 1** tiene 27 residuos ionizables, con un rango de pKa de 1,31 a 14,12
y un promedio de 8,43; el corrimiento neto absoluto es 40,6. Lo importante no es el
promedio (la cavidad es enorme y heterogénea) sino que **K199 y R222 están
anormalmente acidificados**. Esa acidificación es la firma de una cavidad
"activada": un ambiente hidrofóbico con residuos básicos cercanos (R218, R222,
K195) que desestabiliza la forma protonada de la lisina y de la arginina y baja su
pKa. Es exactamente lo que se necesita para una catálisis promiscua: una lisina que
pueda actuar como base/nucleófilo a pH fisiológico.

La **cavidad 2** (sitio AIII) tiene 6 residuos ionizables, rango 11,19–13,51,
promedio 12,23 y corrimiento neto 2,7: **no** está activada. R410 y Y411 no muestran
un corrimiento fuerte.

**Comparación con CaviDB.** El trabajo de CaviDB reporta para 1AO6A una Lys199 con
pKa ~7,51 y una Arg222 ~9,49, y describe la cavidad 1 como la cavidad grande del
sitio AII con esas dos "residuos activados". Nuestros valores (6,78 y 9,16) son
algo más ácidos, pero reproducen el mismo fenómeno y el mismo ordenamiento. Las
diferencias son esperables: una sola conformación, sin hidrógenos explícitos, sin
ligandos, y una versión de PROPKA distinta.

**Respuestas puntuales**

- *¿Cuántas cavidades fueron predichas?* 36.
- *¿Cuáles son las principales por tamaño?* 36 (2713 Å³), 1 (2656 Å³), 30
  (1388 Å³), 18 (1197 Å³); la más relevante funcionalmente es la 1.
- *¿Hay cavidades que se solapen con los residuos relevantes?* Sí: cavidad 1 con
  K195/K199/R222/W214; cavidad 2 con R410/Y411; C34 no está en ninguna.
- *¿Alguna cavidad catalíticamente activa está activada?* Sí, la cavidad 1 (sitio
  AII): K199 y R222 tienen pKa anormalmente ácidos.
- *¿Qué rangos de pKa se observan?* En la cavidad 1, 1,31–14,12 (promedio 8,43);
  los residuos catalíticos, 6,78 (K199) y 9,16 (R222). En la cavidad 2,
  11,19–13,51 (promedio 12,23).

---

El contexto general, la metodología y las referencias completas están en el [informe integral](informe.md).
