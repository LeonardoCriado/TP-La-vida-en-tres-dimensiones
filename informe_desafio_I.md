# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío I — El sitio activo de EGFR en dos conformeros

**Consigna:** comparar el sitio activo de los conformeros 1M14 (activo) y 3W32
(inactivo) en la posición 837 y comparar los tamaños de las cavidades.

**Un detalle de numeración que cambia la respuesta.** La 1M14 numera la cadena A
con un corrimiento de −24 respecto de la numeración canónica de EGFR (DBREF:
671–998 en el PDB ↔ 695–1022 en UniProt P00533). Por eso:

- En **1M14**, el residuo 837 es **Leu861**, y el **Asp837 catalítico** es el
  residuo local **813**.
- En **3W32**, la numeración es canónica y el **Asp837** es el 837.

Comparar "el residuo 837" sin corregir esto lleva a conclusiones falsas.

**Resultados de fpocket y de accesibilidad**

| | 1M14 (activo, apo, 2,6 Å) | 3W32 (inactivo, con inhibidor W32, 1,8 Å) |
|---|---|---|
| Cavidades predichas | 24 | 21 |
| Cavidades drogables | 1 (cavidad 1, 1071 Å³, 0,60) | 1 (cavidad 1, 711 Å³, 0,93) |
| Cavidad del sitio ATP | fragmentada: cavidad 18 (586 Å³, 0,25), 19 (297 Å³), 24 (256 Å³); C797 no pertenece a ninguna | cavidad 1 (711 Å³, 0,93), única y bien definida |
| Cavidad que contiene Asp837 | cavidad 2 (112 Å³, 0,001); Asp837 = **Asp813** local | cavidad 7 (369 Å³, 0,001) |
| SASA de Asp837 | 15,4 Å² | 6,4 Å² |
| SASA de K745 / T790 / M793 / D855 / F856 / L858 | 43,0 / 9,3 / 15,2 / 34,7 / 4,3 / 32,6 Å² | 0,0 / 0,0 / 6,0 / 0,0 / 0,0 / 0,0 Å² |
| Puente salino K745–E762 | 3,8 Å (presente) | 13,6 Å (roto) |

![Cavidades de EGFR en los dos conformeros](resultados/fig_cavidades_egfr.png)

**¿Qué se observa?**

1. **La conformación activa tiene el sitio ATP abierto.** En 1M14, el puente
   salino K745–E762 (marca de la hélice αC "adentro", conformación activa) está
   presente (3,8 Å), y los residuos del sitio ATP están mucho más expuestos al
   solvente: K745, T790, D855, F856 y L858 pasan de SASA ~0 en 3W32 a 9–43 Å² en
   1M14. fpocket no encuentra una única cavidad cerrada: el sitio está abierto y se
   fragmenta en varias subcavidades (18, 19, 24).
2. **La conformación inactiva tiene el sitio cerrado y drogable.** En 3W32 el
   puente salino está roto (13,6 Å) y el sitio ATP es una cavidad única, profunda y
   con druggability 0,93, que alojaba al inhibidor W32. Los 21 residuos que rodean
   al ligando (L718, G719, S720, V726, A743, K745, M766, C775, R776, L777, L788,
   T790, Q791, L792, M793, G796, L844, T854, D855, F856, F997) coinciden con los
   que revisten la cavidad 1. El inhibidor estabiliza la conformación inactiva.
3. **El Asp837 catalítico no está en la cavidad principal del ATP.** Es el aspartato
   del motivo HRD (835–837), en el *loop* catalítico, y está en el borde del sitio.
   En la conformación inactiva está más enterrado (SASA 6,4 Å²) y reviste una
   subcavidad más grande (369 Å³) que en la activa (112 Å³, SASA 15,4 Å²). Es decir:
   el cambio conformacional no solo agranda o achica un bolsillo, sino que
   **reorganiza** el sitio y cambia la exposición de los residuos catalíticos.

**Interpretación.** El sitio ATP de EGFR es un ejemplo de **selección
conformacional**: la proteína activa tiene un sitio abierto y accesible, mientras
que la inactiva tiene un bolsillo cerrado y complementario a inhibidores. Los
inhibidores de tipo "DFG-out" o los alostéricos aprovechan justamente esa
conformación. La comparación también muestra que "tamaño de la cavidad" no es
sinónimo de "druggability": la cavidad 1 de 1M14 es más grande (1071 Å³) pero
mucho menos drogable (0,60) que la de 3W32 (711 Å³, 0,93), porque su forma es más
abierta y menos complementaria.

**Cautelas.** 1M14 es *apo* y 3W32 es *holo* (aunque el ligando se eliminó para el
análisis); las resoluciones difieren (2,6 vs 1,8 Å); y fpocket está sesgado hacia
cavidades cerradas, por lo que un sitio abierto puede aparecer fragmentado. La
dirección de los cambios (más exposición en el activo, más bury en el inactivo) es
robusta y coincide con los indicadores estructurales independientes (puente salino
y contactos del ligando).

---

El contexto general, la metodología y las referencias completas están en el [informe integral](informe.md).
