# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**
Leonardo Criado · noviembre de 2026

> Consigna original: *La vida en tres dimensiones*, Dra. Ana Julia Velez Rueda y Nicolás Palopoli,
> [Introducción a la Bioinformática](https://github.com/AJVelezRueda/Introduccion_a_la_Bioinformatica/blob/master/Teorico_Practicos/Bioinform%C3%A1tica_Estructural/La_vida_en_tres_dimensiones.md) (CC BY-SA 4.0).

> **Nota metodológica.** Al momento de hacer este TP no se pudo consultar CaviDB.
> Por eso se analizaron las estructuras con fpocket y PROPKA, herramientas que
> también usa la base. Es una reproducción independiente con esos programas, no
> una réplica exacta de todos los pasos de CaviDB. Los parámetros y límites están
> detallados en la sección 2.1.

---

## Resumen

Se analizó la estructura de ubiquitina 1UBQ y el formato PDB; se compararon las
estructuras 1M14 y 3W32 del dominio quinasa de EGFR; se consultó la anotación de
AKR1C4 en UniProt y sus cavidades en 2FVL; se compararon cavidades y pKa de las
albúminas humana (1AO6) y bovina (4JK4); y se analizó una predicción de E7 del
VPH16 obtenida con ColabFold.

Los resultados principales:

- La ubiquitina es una proteína de 76 aminoácidos, resuelta por rayos X a 1,8 Å,
  con una sola cadena y 602 átomos.
- El sitio ATP de EGFR aparece fragmentado en 1M14 y como una cavidad detectada
  por fpocket en 3W32 (711 Å³; druggability 0,93). Estos resultados describen las
  estructuras analizadas y no, por sí solos, la actividad bioquímica de la proteína.
- La cavidad drogable de AKR1C4 (2FVL, cadena B; 988 Å³, druggability 0,85)
  coincide con el sitio catalítico y de unión a NADP.
- En la albúmina humana, la cavidad 1 (2656 Å³) incluye K199 y R222. PROPKA
  predice pKa de 6,78 y 9,16, respectivamente. Estos desplazamientos son indicios
  calculados y no prueban por sí mismos un mecanismo catalítico.
- En la albúmina bovina, K221 tiene un pKa calculado de 5,39 y aparece en las
  cavidades 4 y 38, no en la cavidad principal 5. La interpretación como inversión
  funcional se discute con cautela y en relación con la literatura.
- En el modelo rank 1 relajado de ColabFold, el pLDDT medio es 81,5; el tramo
  61–98 promedia 95,5 y el tramo 1–40 promedia 66,3. La baja confianza en parte
  del extremo N-terminal es compatible con flexibilidad o desorden, pero no lo
  demuestra por sí sola.

---

## 1. Un problema estructural

### 1.1 ¿Por qué una célula destruiría sus propias proteínas?

La célula no destruye proteínas "porque sí": las degrada de forma **regulada**. La
proteólisis selectiva cumple funciones esenciales:

- **Control de calidad:** elimina proteínas mal plegadas, dañadas o agregadas
  antes de que sean tóxicas.
- **Regulación:** muchas proteínas reguladoras (ciclinas, factores de
  transcripción, inhibidores) deben desaparecer en un momento preciso del ciclo
  celular o de una vía de señalización.
- **Reciclado:** libera aminoácidos para sintetizar otras proteínas, sobre todo en
  situaciones de estrés o ayuno.
- **Presentación de antígenos:** los péptidos degradados por el proteasoma se
  presentan en el MHC-I al sistema inmune.
- **Defensa y homeostasis:** elimina proteínas virales o bacterianas y controla la
  abundancia de proteínas de respuesta inmune.

La **ubiquitina** es la etiqueta clásica de este sistema. Es una proteína pequeña
(76 aminoácidos, ~8,6 kDa) que se une covalentemente a las proteínas sustrato
mediante una cascada de enzimas E1–E2–E3. La cadena de poliubiquitina unida por
lisinas K48 es la señal clásica de degradación por el proteasoma 26S; otras
modificaciones (K63, monoubiquitina) participan en señalización, tráfico
vesicular, reparación del ADN, autofagia e inflamación. Por eso el sistema
ubiquitina–proteasoma no es solo una "máquina de destrucción": es un sistema de
información y control.

### 1.2 La ubiquitina en el PDB

La entrada **1UBQ** de la ubiquitina humana tiene estos datos:

| Dato | Valor |
|---|---|
| Entrada | 1UBQ |
| Proteína | Ubiquitina (Homo sapiens) |
| Método | Difracción de rayos X |
| Resolución | 1,80 Å |
| Factor R (working + test) | 0,176 |
| Cadenas | 1 (A) |
| Residuos | 76 |
| Átomos | 602 sin hidrógenos + 58 aguas |
| Fecha de depósito | 02-01-1987 |
| Artículo | Vijay-Kumar, Bugg & Cook, *J. Mol. Biol.* (1987) |

**¿Qué información nos provee la página del PDB?**
La ficha (*Structure Summary*) reúne: identificador y título de la entrada; autores
y fechas; método experimental y resolución; estadísticas de refinamiento
(R y R-free); grupo espacial y celda unidad; la **asamblea biológica**; las
cadenas con su secuencia; ligandos, cofactores, iones y aguas; enlaces a bases de
datos (UniProt, Pfam, GO, CATH, SCOP); la citación; métricas de validación
(Ramachandran, choques estéricos, rotámeros); el visor 3D; y las opciones de
descarga (PDB, mmCIF, FASTA, factores de estructura).

**¿Cómo se determinó la estructura de esta proteína?**
Por **cristalografía de rayos X**. El procedimiento, en grandes pasos: se purifica
la proteína, se cristaliza, se difracta con rayos X (en un tubo o en un
sincrotrón), se indexan e integran las reflexiones, se escalan los datos, se
obtienen las fases (por reemplazo molecular, dispersión anómala o métodos
experimentales), se calcula el mapa de densidad electrónica, se construye el
modelo atómico y se refina contra los datos hasta que el modelo explica el mapa.
La 1UBQ se refinó a 1,8 Å, lo que permite ubicar bien el esqueleto y la mayoría de
las cadenas laterales.

**¿Qué significan las cintas, las flechas y las regiones angostas?**
Es una representación **cartoon** de la estructura secundaria, no de los átomos:
las **flechas** son hebras β (en la ubiquitina hay cinco, que forman el plegamiento
β-grasp); las **cintas/espirales** son hélices α (la ubiquitina tiene una hélice
α principal, entre los residuos 23 y 34, y una hélice 3₁₀ corta); y las **regiones
angostas** son *loops* o giros que conectan los elementos de estructura secundaria.
Las flechas suelen indicar la dirección N→C de la hebra.

**¿Representa esa imagen la realidad del sistema biológico?**
No literalmente. La imagen es un **modelo**, no una fotografía: muestra una sola
conformación (o un promedio) de las moléculas presentes en el cristal, sin
hidrógenos, sin la mayoría de las aguas y sin las regiones flexibles que no se ven
en el mapa de densidad. Tampoco muestra la dinámica, las modificaciones
postraduccionales, el entorno celular ni los ligandos que la proteína encuentra in
vivo. Es una excelente aproximación al plegamiento y a la arquitectura de la
proteína, pero no es "la proteína real" en toda su complejidad. En palabras
habituales: el mapa no es el territorio.

**Sobre la resolución de 1,8 Å.**
La resolución nominal es la distancia mínima entre planos cristalinos para la que
se midieron reflexiones; se expresa en Å. **Cuanto menor es el número, mayor es la
resolución** y menor la incertidumbre de las posiciones atómicas. Un valor de
1,8 Å es bueno para una proteína de 76 aminoácidos: permite trazar el esqueleto,
asignar la estructura secundaria y ubicar la mayoría de las cadenas laterales; no
permite ver hidrógenos y las zonas con alta movilidad tienen factores B altos o
directamente no se observan. La resolución no es exactamente "el error", pero sí
una medida del nivel de detalle y de la incertidumbre asociada.

**¿Cuál es la utilidad y los condicionamientos de usar un modelo inexacto?**
La utilidad es enorme: un modelo permite formular hipótesis mecanísticas, diseñar
mutantes, interpretar mutaciones patogénicas, comparar conformeros, buscar sitios
de unión y hacer diseño de fármacos. El condicionamiento es usarlo **con su
incertidumbre**: no sobreinterpretar contactos de cadenas laterales, comparar
varias conformaciones, mirar los factores B y las métricas de validación, y
recordar que el modelo es una interpretación de los datos, no un hecho desnudo.
La ciencia trabaja siempre con modelos aproximados; la diferencia entre un buen y
un mal uso no es la ausencia de error, sino la conciencia de ese error.

### 1.3 Del visor 3D al archivo PDB

**¿Qué diferencias y similitudes hay entre la representación inicial y el visor 3D?**
Ambas usan las **mismas coordenadas** de la misma entrada, así que el plegamiento
es idéntico. La diferencia es la interfaz y el nivel de detalle: la imagen inicial
es una vista pre-renderizada, estática y curada; el visor 3D es interactivo,
permite rotar, hacer zoom, desplazar, cambiar la representación (cartoon, sticks,
esferas, superficie), colorear por cadena, estructura secundaria, factor B,
hidrofobicidad o tipo de residuo, y seleccionar ligandos o residuos concretos.

**¿Para qué sirve visualizar lo mismo de distintas maneras?**
Cada representación responde a una pregunta distinta. El cartoon sirve para ver el
plegamiento; los *sticks* para ver interacciones y contactos; la superficie para
ver la forma, las cavidades y la complementariedad; el coloreado por factor B para
ver flexibilidad; el coloreado por cadena para ver la ensambladura; el coloreado
por conservación o por mutaciones para ver relaciones evolutivas o clínicas. Una
representación es siempre una elección: muestra algo y esconde otra cosa.

**¿Qué información esperaría encontrar como resultado de un experimento
estructural?**
Coordenadas atómicas en Å; método y resolución; medidas de calidad (R, R-free,
validación); secuencia cubierta y residuos no observados; ligandos, cofactores,
iones y aguas; factores B; la asamblea biológica; y los datos experimentales
asociados. Para NMR o criomicroscopía electrónica se esperan, además, múltiples
modelos o mapas de densidad, respectivamente.

**¿En qué consiste un archivo PDB?**
Es un archivo de **texto plano con columnas fijas** (80 caracteres por línea) que
describe la estructura. Cada línea es un **registro** con un formato definido:

| Registro | Contenido |
|---|---|
| `HEADER`, `TITLE`, `COMPND`, `SOURCE` | Identificación, nombre, composición y origen |
| `EXPDTA`, `REMARK` | Método experimental, resolución, refinamiento, validación |
| `SEQRES` | Secuencia completa de cada cadena (en código de 3 letras) |
| `DBREF` | Correspondencia con bases de datos (UniProt, etc.) |
| `HELIX`, `SHEET`, `SSBOND` | Estructura secundaria y puentes disulfuro |
| `CRYST1`, `ORIGX`, `SCALE` | Celda unidad y transformaciones de coordenadas |
| `ATOM` | Átomos de la macromolécula, con coordenadas |
| `HETATM` | Ligandos, cofactores, iones, aguas |
| `TER`, `CONECT`, `MASTER`, `END` | Fin de cadena, conectividad, control y fin de archivo |

**La sección ATOM.**
Cada línea `ATOM` describe un átomo:

| Columnas | Campo | Ejemplo (primer átomo de 1UBQ) |
|---|---|---|
| 1–6 | Registro | `ATOM` |
| 7–11 | Número de serie | `1` |
| 13–16 | Nombre del átomo | `N` |
| 17 | Conformación alterna | ` ` |
| 18–20 | Residuo (3 letras) | `MET` |
| 22 | Cadena | `A` |
| 23–26 | Número de residuo | `1` |
| 27 | Código de inserción | ` ` |
| 31–38 | Coordenada x (Å) | `27.340` |
| 39–46 | Coordenada y (Å) | `24.430` |
| 47–54 | Coordenada z (Å) | `2.614` |
| 55–60 | Ocupancia | `1.00` |
| 61–66 | Factor B (Å²) | `9.67` |
| 77–78 | Elemento | `N` |
| 79–80 | Carga | ` ` |

La sección `ATOM` da, entonces, la identidad química de cada átomo, el residuo y la
cadena a la que pertenece, su número, sus coordenadas tridimensionales, su
ocupancia (cuántas veces aparece esa conformación) y su factor B (movilidad o
incertidumbre). Es una **tabla de coordenadas**, no una secuencia.

**¿Podemos extraer la estructura primaria del archivo?**
Sí, por dos vías complementarias:

- `SEQRES` da la secuencia **completa** de cada cadena, en código de tres letras;
  pasándola a una letra se obtiene la secuencia primaria.
- `ATOM` da los residuos **observados** en el mapa, en orden; puede faltar alguno
  (regiones desordenadas, extremos flexibles) y puede haber microheterogeneidad.

Desde el punto de vista computacional, `SEQRES` es una **cadena de caracteres**
(una lista de símbolos), mientras que `ATOM` es una **tabla de registros** con
números reales (las coordenadas) y enteros (residuo, cadena). La secuencia es el
orden de los residuos; las coordenadas son la geometría. En 1UBQ ambas coinciden:
`MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG`
(76 aa). En muchas estructuras no coinciden exactamente, y ahí está la información
de qué partes del modelo están resueltas y cuáles no.

**¿Es útil el formato PDB para presentar los resultados del experimento?**
Es útil y fue durante décadas el estándar de facto, pero tiene límites claros.

*Ventajas:* es simple, de texto, legible por humanos y por casi cualquier
programa; contiene coordenadas y metadatos en el mismo archivo; fue adoptado por
toda la comunidad; permite reconstruir la estructura y compararla.

*Limitaciones:* las columnas fijas de 80 caracteres obligan a abreviar y a veces
pierden información; el formato no tiene un diccionario de datos formal tan
estricto como mmCIF; la precisión de las coordenadas es limitada; las estructuras
grandes o con muchos modelos se vuelven incómodas; la anotación es heterogénea; y
el PDB "clásico" fue reemplazado como formato maestro por **PDBx/mmCIF**, que es
más expresivo y escalable. Para *presentar* resultados, el PDB es necesario pero
no suficiente: sin resolución, R, validación y factores B, las coordenadas solas
pueden dar una falsa sensación de exactitud.

**Beneficios y limitaciones de imponer una estructura para comunicar resultados.**
*Beneficios:* interoperabilidad (todos leen lo mismo), automatización, validación
cruzada, comparabilidad entre experimentos, posibilidad de construir bases de
datos y de reproducir análisis, y claridad semántica sobre qué es cada campo.
*Limitaciones:* todo esquema pierde matices; lo que no entra en el formato se
pierde o se anota mal; los formatos envejecen; la rigidez puede forzar
interpretaciones; y la existencia de un campo no garantiza que su contenido sea
correcto. Un estándar es una convención social y técnica, no una verdad natural:
hay que usarlo sabiendo qué deja afuera.

### 1.4 ¿Y los ácidos nucleicos?

Sí: los ácidos nucleicos también tienen estructura tridimensional y se estudian
con la misma lógica. El ADN forma una doble hélice con dos cadenas antiparalelas
unidas por puentes de hidrógeno entre bases complementarias (A–T, G–C) y apiladas
en el interior; el esqueleto de azúcar–fosfato queda afuera. Hay varias formas:
**B-DNA** (la clásica, ~10 pb/vuelta, paso de 34 Å, diámetro ~20 Å), **A-DNA**
(~11 pb/vuelta, más compacta) y **Z-DNA** (levógira, ~12 pb/vuelta). El ARN suele
ser monocatenario y se pliega sobre sí mismo: horquillas, tRNAs con forma de L,
ribozimas, riboswitches y aptámeros, con apareamientos canónicos y no canónicos,
apilamiento de bases e iones que estabilizan la estructura.

El PDB contiene estructuras de ADN, ARN y complejos proteína–ácido nucleico, y el
formato es el mismo (ATOM/HETATM). Las diferencias están en la química: el ARN
tiene 2'-OH, uracilo en lugar de timina, y una geometría de azúcar distinta; es más
flexible y depende más de iones y de proteínas. Por eso la predicción de estructura
de ácidos nucleicos es más difícil que la de proteínas, y los métodos actuales
(AlphaFold3, RoseTTAFold NA, etc.) todavía están menos maduros que AlphaFold2 para
proteínas.

### 1.5 Rosalind Franklin

Rosalind Elsie Franklin (1920–1958) fue una química y cristalógrafa británica. Se
formó en Cambridge, trabajó en París con Jacques Mering en la difracción de rayos X
de carbones y materiales desordenados, y en 1951 se incorporó al King's College de
Londres para estudiar la estructura del ADN con Maurice Wilkins.

Sus **procedimientos** fueron experimentales y cuantitativos:

- Preparaba **fibras de ADN** orientadas y controlaba con precisión la humedad
  relativa, lo que le permitió distinguir dos formas: la **A** (más seca) y la
  **B** (más hidratada).
- Obtenía **patrones de difracción de rayos X** de esas fibras, con exposiciones
  largas y cámaras especiales; la famosa **Foto 51** (tomada con Raymond Gosling en
  1952) es un patrón de la forma B.
- Analizaba los patrones midiendo las posiciones e intensidades de las capas y
  aplicando la teoría de difracción helicoidal para inferir parámetros: período de
  la hélice, número de bases por vuelta, radio, simetría y orientación de las bases.
- Construía y contrastaba modelos con esos datos, y fue muy cuidadosa en distinguir
  lo que los datos permitían afirmar de lo que era especulación.

A partir de sus medidas se establecieron parámetros de la forma B (alrededor de
10 pb por vuelta, paso de ~34 Å, diámetro de ~20 Å, bases hacia adentro). Sus datos
fueron mostrados a James Watson sin su consentimiento por Wilkins, y fueron
centrales para el modelo de la doble hélice publicado por Watson y Crick en 1953.
Ese mismo año salieron tres artículos en *Nature*: el de Franklin y Gosling sobre
la forma B, el de Wilkins y colaboradores, y el de Watson y Crick. Franklin no
publicó una "foto" y nada más: produjo un cuerpo de mediciones y un análisis
cuantitativo sin el cual el modelo no se sostenía.

Después se mudó al Birkbeck College, donde estudió la estructura del virus del
mosaico del tabaco (TMV) y de otros virus, y siguió trabajando hasta su muerte por
cáncer de ovario en 1958, a los 37 años. El Premio Nobel de 1962 fue para Watson,
Crick y Wilkins; Franklin había muerto y el Nobel no se otorga póstumamente. Su
reconocimiento llegó tarde, y hoy es un caso emblemático de cómo la ciencia también
se escribe con jerarquías, acceso a datos y crédito desigual.

---

## 2. Una solución en el bolsillo

Las proteínas no son ovillos: adoptan estructuras definidas que se describen en
cuatro niveles (primaria, secundaria, terciaria y cuaternaria). Desde Anfinsen
sabemos que la secuencia contiene la información para el plegamiento, aunque in
vivo el plegamiento ocurre en un entorno celular complejo y con ayuda de
chaperonas. Además, las proteínas no están quietas: son **ensambles
conformacionales** que se mueven, y esa dinámica es parte de la función.

En la superficie, una proteína tiene cavidades, canales y protuberancias que crean
microambientes para unir ligandos o catalizar reacciones. La forma y las
propiedades fisicoquímicas de esas cavidades (volumen, hidrofobicidad, carga,
residuos ionizables, pKa) determinan si un ligando puede unirse y si la cavidad es
"drogable". De ahí el interés en detectarlas computacionalmente: fpocket, CaviDB,
PocketFinder, DoGSiteScorer, etc.

### 2.1 Cómo se analizaron las cavidades en este TP

Como CaviDB no estaba disponible, se hizo un análisis independiente sobre las
cadenas indicadas por la consigna, con herramientas también usadas por esa base:

1. **Descarga y preparación:** estructuras del RCSB PDB; se aisló la cadena de
   interés con Biopython y se eliminaron aguas y heteroatomos (ligandos,
   cofactores, iones) para comparar todas las estructuras en las mismas
   condiciones. Las cadenas usadas fueron 1M14:A, 3W32:A, 2FVL:B, 1AO6:A y 4JK4:A.
2. **Detección de cavidades:** **fpocket 4.2.3** (conda-forge) con parámetros por defecto. Se
   consideró **drogable** una cavidad con *druggability score* > 0,5, el mismo
   criterio que usa CaviDB.
3. **pKa:** **PROPKA 3.5.1** sobre cada cadena, con las opciones por defecto del
   comando (pH 7 para los cálculos que dependen de pH). Se tomó la predicción de
   pKa de cada grupo ionizable y se calculó el corrimiento respecto de los valores
   de referencia usados por PROPKA (Asp 3,8; Glu 4,5; His 6,5;
   Cys 9,0; Tyr 10,0; Lys 10,5; Arg 12,5) y el corrimiento neto por cavidad. Los
   valores 99,99 que PROPKA usa para residuos sin desprotonación posible se
   excluyeron de los promedios.
4. **Análisis:** se compararon los residuos incluidos en cada cavidad con los
   sitios de interés y se calcularon estadísticas descriptivas de pKa.

El *druggability score* de fpocket es un indicador computacional basado en las
características de una cavidad. En este informe se usa el corte > 0,5 para resumir
los resultados; no es una probabilidad de unión ni confirma que una molécula pueda
ser un fármaco. Del mismo modo, el volumen estima el tamaño geométrico del bolsillo,
pero no alcanza para decidir si es funcional o si un ligando se unirá.

**Límites de esta reproducción.** Se analiza una sola conformación por estructura,
sin hidrógenos explícitos ni cofactores, y fpocket puede fragmentar cavidades
abiertas o dividir un sitio grande en subcavidades. Los volúmenes pueden variar
levemente entre corridas. Por eso los números deben leerse como una estimación
consistente, no como un valor único y absoluto. Cuando existen, se comparan con los
valores publicados de CaviDB y del trabajo de albúminas del grupo de la UNQ.

---

## 3. Desafíos

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

| | 1M14 (conformación activa, sin ligando, 2,6 Å) | 3W32 (conformación inactiva, con inhibidor W32, 1,8 Å) |
|---|---|---|
| Cavidades predichas | 24 | 21 |
| Cavidades drogables | 1 (cavidad 1, 1071 Å³, 0,60) | 1 (cavidad 1, 711 Å³, 0,93) |
| Cavidades asignadas a la región del sitio ATP | fragmentada: cavidad 18 (586 Å³, 0,25), 19 (297 Å³), 24 (256 Å³); C797 no pertenece a ninguna | cavidad 1 (710,7 Å³, 0,932) |
| Cavidad que contiene Asp837 | cavidad 2 (112 Å³, 0,001); Asp837 = **Asp813** local | cavidad 7 (369 Å³, 0,001) |
| Residuos del motivo HRD relevantes para la consigna | Asp837 corresponde a Asp813 en la numeración de 1M14 | Asp837 |

![Cavidades de EGFR en los dos conformeros](resultados/fig_cavidades_egfr.png)

**¿Qué se observa?**

1. **Las cavidades difieren entre las estructuras.** En 1M14, fpocket predice 24
   cavidades y separa la zona del sitio ATP entre varias de ellas. En 3W32 predice
   21, incluida una cavidad de 710,7 Å³ con druggability 0,932. El score resume
   rasgos geométricos de la cavidad; no mide directamente la afinidad del inhibidor.
2. **La numeración del Asp importa.** En la cadena de 1M14, el Asp del motivo HRD
   se numera 813, aunque corresponde al Asp837 de la numeración canónica. En 3W32
   aparece como Asp837. Comparar las cifras sin convertir la numeración llevaría a
   seleccionar residuos distintos.
3. **El tamaño no determina por sí solo la calidad del bolsillo.** La cavidad más
   grande de 1M14 mide 1070,6 Å³ (score 0,597), mientras que la cavidad 1 de 3W32
   mide 710,7 Å³ (score 0,932). Esto muestra que el volumen y el score describen
   propiedades distintas. La fragmentación observada también depende del método
   con que se define una cavidad.

**Interpretación.** La comparación muestra que cambios de conformación pueden
cambiar la forma y la partición geométrica del sitio de unión. Los datos de fpocket
son compatibles con una cavidad más definida en 3W32, estructura que contiene el
inhibidor W32. Como no se recalcularon aquí contactos ni accesibilidad al solvente,
no se puede atribuir el cambio observado a un mecanismo único ni concluir que una
conformación tenga mayor actividad a partir de estos scores.

**Cautelas.** Los ligandos y las aguas se retiraron para correr fpocket, aunque las
estructuras de origen no tienen el mismo estado de unión: 1M14 no contiene ligando
y 3W32 está asociada al inhibidor W32. Las resoluciones también difieren (2,6 y
1,8 Å). La SASA, las distancias de contacto y los puentes salinos mencionados en
borradores previos no tienen archivos de cálculo incluidos y por eso no se usan
como resultados verificados en esta versión.

### Desafío II — AKR1C4 en UniProt

**Proteína:** aldo-keto reductasa familia 1, miembro C4 (AKR1C4; UniProt
[P17516](https://www.uniprot.org/uniprotkb/P17516/entry)), 323 aminoácidos.
Es una enzima citosólica dependiente de NADPH que reduce cetosteroides a
hidroxiesteroides, con actividad 3α-hidroxiesteroide deshidrogenasa; participa en el
metabolismo de esteroides, ácidos biliares y fármacos.

**Sitios anotados en UniProt**

| Anotación | Posición | Relevancia |
|---|---|---|
| Sitio activo (dador de protones) | Y55 | Tirosina catalítica; su pKa influye en la transferencia de protones |
| Sitio que baja el pKa de Y55 | K84 | Lisina que estabiliza la tirosinato |
| Unión a cofactor/NADP | 20–24, 166–167, 190, 216–221, 270–280 | Bolsillo de NADP(H) |
| Unión a sustrato/esteroide | 50, 190, 216–221 | Contactos con el anillo esteroideo |
| Tetrada catalítica | D50, Y55, K84, H117 | Red de protones y estabilización |

Las variantes naturales anotadas son G135E (rs11253043), S145C (rs3829125),
C170Y (rs17851824), Q250R (rs4880718) y L311V (rs17134592). La variante **S145C**
se asoció con niveles bajos de progesterona y con historia de irritabilidad
maníaca/hipomaníaca en varones con trastorno bipolar (Johansson et al., 2011), y
otros polimorfismos de AKR1C4 se han estudiado en relación con ideación paranoide
durante episodios maníacos. S145 no forma parte de la tetrada catalítica anotada.
La asociación reportada no permite establecer qué efecto estructural o funcional
tendría la variante; para eso harían falta análisis adicionales.

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
N167). K84 no quedó asignada a la cavidad por fpocket, pero está cerca del OH de
Y55 en la estructura (distancia entre NZ de K84 y OH de Y55: 2,89 Å); UniProt la
anota como residuo que modula el pKa de la tirosina. Es una cavidad grande, única y
con druggability > 0,5, que podría estudiarse para inhibidores. La selectividad
frente a las otras isoformas de AKR1C sería una dificultad a considerar.

**pKa (PROPKA, sin NADP):** H117 1,52 (muy ácido), Y55 11,24, K84 12,27. Estos
valores no deben tomarse como los pKa fisiológicos definitivos: la ausencia del
cofactor y de hidrógenos explícitos afecta el cálculo. Lo robusto es la
identificación del sitio, no el valor absoluto.

**Cautela:** CaviDB puede reportar un número de cavidades algo distinto según cómo
separe el sitio del NADP y según la versión de fpocket. Nuestra corrida da 21 y una
sola cavidad drogable, que es la conclusión relevante.

### Desafío IV — La albúmina humana (1AO6A)

**Estructura:** 1AO6, cadena A, albúmina sérica humana (HSA), 2,5 Å, sin ligandos
(albúmina "defatted"). La HSA tiene tres dominios homólogos (I, II y III), cada uno
con dos subdominios (A y B); los sitios de unión a fármacos más importantes son el
**sitio I** (subdominio IIA, Sudlow I) y el **sitio II** (subdominio IIIA,
Sudlow II).

| | Resultado |
|---|---|
| Cavidades predichas | **36** |
| Cavidades con druggability > 0,5 | **2** (cavidad 1: 2656,5 Å³, 0,955; cavidad 2: 325,6 Å³, 0,675) |
| Cavidades más grandes | 36 (2713 Å³, 0,36), 1 (2656 Å³, 0,955), 30 (1388 Å³, 0,05), 18 (1197 Å³, 0,02) |
| Cavidad del sitio I (AII) | **cavidad 1**, 2656 Å³, 65 residuos, druggability 0,955 |
| Cavidad del sitio II (AIII) | **cavidad 2**, 326 Å³, druggability 0,675 |

![Cavidades de HSA y BSA](resultados/fig_cavidades_albuminas.png)

**¿Se solapan las cavidades con los residuos relevantes?**

- **K195, K199, R222, W214, R218 y H242** están en la **cavidad 1** (zona AII).
  La cavidad 1 es la segunda más grande de la proteína (la 36 es apenas mayor pero
  no es drogable), lo que coincide con la descripción del sitio AII como una de las
  cavidades principales.
- **R410 y Y411** están en la **cavidad 2** (zona AIII).
- **C34** no aparece entre los residuos de las cavidades de fpocket. Esto no permite
  concluir por sí solo cuál es su accesibilidad o función química.

**pKa y posibles cavidades activadas**

| Residuo | pKa calculado | pKa esperado | Δ |
|---|---|---|---|
| K199 | 6,78 | 10,50 | **−3,72** |
| R222 | 9,16 | 12,50 | **−3,34** |
| R218 | 10,84 | 12,50 | −1,66 |
| K195 | 9,99 | 10,50 | −0,51 |
| R410 (cavidad 2) | 11,99 | 12,50 | −0,51 |
| Y411 (cavidad 2) | 11,19 | 10,00 | +1,19 |

La **cavidad 1** tiene 27 residuos ionizables. Sus pKa calculados van de 1,31 a
14,12 y el promedio es 8,43. La suma de los valores absolutos de los corrimientos
respecto de los valores de referencia es 40,57; no es un pKa ni una medida directa
de actividad. En particular, PROPKA predice valores menores que los de referencia
para K199 (6,78) y R222 (9,16). Un pKa desplazado indica que el entorno estructural
podría modificar su protonación. CaviDB usa estos desplazamientos para señalar
cavidades potencialmente activadas, pero este cálculo por sí solo no prueba que
K199 o R222 catalicen una reacción ni explica el mecanismo.

La **cavidad 2** (zona AIII) tiene 6 residuos ionizables, rango 11,19–13,51,
promedio 12,23 y suma absoluta de corrimientos 2,71. En los residuos de interés,
los desplazamientos calculados son menores que los de K199 y R222; con estos
resultados no la clasificamos como potencialmente activada.

**Comparación con CaviDB.** Para HSA, la publicación de CaviDB [13] informa pKa calculados
aproximados de 7,51 para K199 y 9,49 para R222. En esta corrida obtuvimos 6,78 y
9,16. Son predicciones calculadas, no mediciones experimentales; la diferencia es
posible porque no se reprodujeron el mismo conjunto de conformaciones y todos los
parámetros del análisis publicado.

**Respuestas puntuales**

- *¿Cuántas cavidades fueron predichas?* 36.
- *¿Cuáles son las principales por tamaño?* 36 (2713 Å³), 1 (2656 Å³), 30
  (1388 Å³), 18 (1197 Å³); la más relevante funcionalmente es la 1.
- *¿Hay cavidades que se solapen con los residuos relevantes?* Sí: cavidad 1 con
  K195/K199/R222/W214; cavidad 2 con R410/Y411; C34 no está en ninguna.
- *¿Hay una cavidad con residuos que muestran desplazamientos de pKa?* Sí, en la
  cavidad 1 se predicen desplazamientos para K199 y R222. Esto es una pista para
  investigar, no una demostración de catálisis.
- *¿Qué rangos de pKa se observan?* En la cavidad 1, 1,31–14,12 (promedio 8,43);
  los residuos destacados, 6,78 (K199) y 9,16 (R222). En la cavidad 2,
  11,19–13,51 (promedio 12,23).

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

K221 aparece en las cavidades 4 y 38, mientras que R217 aparece en la cavidad 5,
4 y 38. El CSV no incluye distancias atómicas ni componentes energéticos de
PROPKA, así que no puedo verificar con los archivos disponibles la distancia de
2,9 Å ni el término de desolvatación citado en borradores previos. Por ese motivo,
el pKa calculado de 5,39 se informa como predicción, sin asignarle aquí una causa
estructural única.

**La comparación con la HSA**

| | HSA (1AO6A) | BSA (4JK4A) |
|---|---|---|
| Par de residuos del sitio | K199 / R222 | R198 / K221 |
| Lisina destacada en la interpretación del sitio | **K199**, pKa 6,78 | **K221**, pKa 5,39 |
| Residuo equivalente al otro miembro del par | R222, pKa 9,16 | R198, pKa 9,07 |
| Cavidad que contiene la lisina destacada | cavidad 1 (2656 Å³, 0,955) | cavidad 4 (364 Å³, 0,086) |
| Cavidad principal del sitio AII | cavidad 1 (drogable) | cavidad 5 (1350 Å³, 0,893) |

La publicación comparativa de albúminas describe una inversión del par de residuos
de este sitio entre HSA y BSA. Los resultados de esta corrida son compatibles con
esa interpretación: en las posiciones reportadas, K199 de HSA y K221 de BSA tienen
pKa calculados menores que los valores de referencia. Sin un alineamiento
estructural y sin medir actividad, estos resultados no bastan para concluir que los
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
no conviene presentarla como una reproducción cuantitativa del estudio.

**Respuestas puntuales**

- *¿Cuántas cavidades tiene 4JK4A?* 41; 3 drogables.
- *¿Dónde está K221?* En las cavidades 4 (364 Å³, no drogable) y 38 (566 Å³, no
  drogable), no en la cavidad principal 5.
- *¿Cómo se compara con la HSA?* La literatura propone una inversión de los
  residuos del sitio entre las dos albúminas. En nuestros cálculos, K199 y K221
  tienen pKa predichos de 6,78 y 5,39. La cavidad que contiene cada residuo difiere,
  pero fpocket no permite por sí solo concluir qué efecto funcional tiene esa
  diferencia.

### Para investigar — Docking

El **docking molecular** propone cómo podría ubicarse una molécula pequeña dentro
de una cavidad. El programa prueba distintas posiciones y las ordena mediante un
*score* aproximado. Ese score puede ayudar a priorizar moléculas, pero no equivale
a una medición de afinidad ni demuestra que un compuesto funcione en un experimento.

Para AKR1C4, se podría explorar el sitio catalítico o el bolsillo de NADP. Una
limitación sería distinguir AKR1C4 de otras proteínas AKR1C parecidas. En este
trabajo no se realizó docking, así que queda como una propuesta de análisis futuro.

---

## 4. Un modelo a seguir

Predecir la estructura tridimensional a partir de la secuencia fue un problema
abierto durante más de 50 años. Los métodos computacionales se agrupan en tres
familias:

1. **Ab initio / de novo:** usan la física y la búsqueda conformacional (dinámica
   molecular, Monte Carlo, optimización) sin depender de estructuras homólogas.
   Son costosos y propensos a imprecisiones, pero pueden explorar plegamientos
   nuevos.
2. **Modelado por homología:** usan una proteína con estructura conocida
   ("plantilla") y la secuencia de la proteína objetivo; funcionan muy bien cuando
   hay un homólogo cercano, y se basan en alineamientos y en la conservación del
   esqueleto.
3. **Aprendizaje automático:** aprenden patrones de grandes conjuntos de
   estructuras. AlphaFold2 es el ejemplo más conocido: usa alineamientos múltiples
   de secuencias (MSAs) y una representación de pares de residuos, con una red
   neuronal (Evoformer + módulo estructural) que predice coordenadas y confianza.

AlphaFold2 reporta dos métricas de confianza:

- **pLDDT** (*predicted local distance difference test*): confianza local por
  residuo, de 0 a 100. >90 muy alta, 70–90 confiable, 50–70 baja y <50 muy baja
  (a menudo en regiones desordenadas).
- **PAE** (*predicted aligned error*): error esperado entre pares de residuos
  cuando se alinean las estructuras predicha y real sobre un residuo; en Å. Un PAE
  bajo entre dos dominios indica que su orientación relativa está bien predicha;
  un PAE alto indica incertidumbre en la disposición relativa.

### Desafío VI — E7 del VPH16 con ColabFold

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
secuencia de 98 aminoácidos. Usé el modelo relajado rank 1, que corresponde al
modelo 4 de esa corrida. El archivo de configuración registra ColabFold 1.6.3,
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

**Archivos de esta corrida.** El ZIP contiene el alineamiento, los nombres de las
plantillas, la configuración, los cinco modelos y sus métricas. Para estos
resultados se tomó el modelo relajado rank 1 y el JSON de PAE correspondiente. La
relajación busca mejorar la geometría local; no vuelve experimental la estructura
ni garantiza que represente el estado funcional de E7.

---

## 5. Conclusiones

- La estructura tridimensional no es un adorno: es la base física de la función.
  Un archivo PDB es una representación parcial y modelada de esa realidad, y leerlo
  críticamente (resolución, R, B-factors, residuos faltantes) es parte del trabajo
  bioinformático.
- Las cavidades permiten describir partes de una estructura y comparar modelos.
  Sus volúmenes y scores dependen de la estructura y del método usado; no indican
  por sí solos que un sitio se una a un fármaco.
- PROPKA predice desplazamientos de pKa para algunos residuos de las albúminas.
  Estos valores sirven para proponer preguntas sobre el entorno químico, pero no
  demuestran actividad catalítica ni explican por sí solos un mecanismo.
- En la corrida de ColabFold analizada, el extremo C-terminal de E7 tiene pLDDT
  alto y una parte del extremo N-terminal tiene valores bajos. Son estimaciones de
  confianza del modelo; para confirmar estructura, desorden o función se necesitan
  otras evidencias.
- La biología estructural computacional no reemplaza al experimento: lo orienta, lo
  interpreta y lo complementa.

---

## 6. Referencias

1. Vijay-Kumar S, Bugg CE, Cook WJ. *Structure of ubiquitin refined at 1.8 Å
   resolution.* J Mol Biol. 1987;194(3):531–544. PDB: [1UBQ](https://www.rcsb.org/structure/1UBQ).
2. Berman HM et al. *The Protein Data Bank.* Nucleic Acids Res. 2000;28:235–242.
   [PDB](https://www.rcsb.org/).
3. wwPDB. *PDB file format documentation.*
   [https://www.wwpdb.org/documentation/file-format](https://www.wwpdb.org/documentation/file-format)
4. wwPDB. *PDBx/mmCIF.* [https://mmcif.wwpdb.org/](https://mmcif.wwpdb.org/)
5. Franklin RE, Gosling RG. *Molecular configuration in sodium thymonucleate.*
   Nature. 1953;171:740–741. doi:10.1038/171740a0.
6. Watson JD, Crick FHC. *Molecular structure of nucleic acids.* Nature.
   1953;171:737–738. doi:10.1038/171737a0.
7. Wilkins MHF, Stokes AR, Wilson HR. *Molecular structure of deoxypentose nucleic
   acids.* Nature. 1953;171:738–740. doi:10.1038/171738a0.
8. Maddox B. *Rosalind Franklin: The Dark Lady of DNA.* HarperCollins, 2002.
9. Anfinsen CB. *Principles that govern the folding of protein chains.* Science.
   1973;181:223–230.
10. Le Guilloux V, Schmidtke P, Tufféry P. *Fpocket: an open source platform for
    ligand pocket detection.* BMC Bioinformatics. 2009;10:168.
11. Olsson MHM, Søndergaard CR, Rostkowski M, Jensen JH. *PROPKA3: consistent
    treatment of internal and surface residues in empirical pKa predictions.*
    J Chem Theory Comput. 2011;7(2):525–537.
12. Schmidtke P, Barril X. *Understanding and predicting druggability.* J Med
    Chem. 2010;53:5858–5867.
13. Velez Rueda AJ et al. *CaviDB: a database of cavities and their features in the
    structural and conformational space of proteins.* Database. 2023;baad010.
    doi:10.1093/database/baad010.
    [Artículo](https://academic.oup.com/database/article/7159200)
14. *Structural and evolutionary analysis unveil functional adaptations in the
    promiscuous behavior of serum albumins.* Biochimie. 2022.
    doi:10.1016/j.biochi.2022.02.004.
15. Johansson AGM et al. *AKR1C4 gene variant associated with low euthymic serum
    progesterone and a history of mood irritability in males with bipolar disorder.*
    J Affect Disord. 2011;133(1–2):346–351.
    [PubMed 21570127](https://pubmed.ncbi.nlm.nih.gov/21570127/)
16. UniProt Consortium. *UniProt: the universal protein knowledgebase.*
    [P17516](https://www.uniprot.org/uniprotkb/P17516/entry).
17. Jumper J et al. *Highly accurate protein structure prediction with AlphaFold.*
    Nature. 2021;596:583–589. doi:10.1038/s41586-021-03819-2.
18. Mirdita M et al. *ColabFold: making protein folding accessible to all.*
    Nat Methods. 2022;19:679–682. doi:10.1038/s41592-022-01488-1.
19. Varadi M et al. *AlphaFold Protein Structure Database.* Nucleic Acids Res.
    2022;50:D439–D444.
20. ColabFold. *AlphaFold2.ipynb.*
    [Notebook](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb)
21. Trott O, Olson AJ. *AutoDock Vina: improving the speed and accuracy of docking
    with a new scoring function, efficient optimization and multithreading.*
    J Comput Chem. 2010;31:455–461.
22. PDB entries: [1M14](https://www.rcsb.org/structure/1M14),
    [3W32](https://www.rcsb.org/structure/3W32),
    [2FVL](https://www.rcsb.org/structure/2FVL),
    [1AO6](https://www.rcsb.org/structure/1AO6),
    [4JK4](https://www.rcsb.org/structure/4JK4).

---

## 7. Cómo reproducir este informe

```bash
# entorno
conda env create -f environment.yml
conda activate tp-estructural

# estructuras y cadenas
bash src/01_descargar_estructuras.sh

# cavidades + pKa
python src/03_analizar_cavidades.py

# figuras
python src/04_figuras_cavidades.py
unzip -q datos/test_3b510.result.zip -d /tmp/tp-colabfold
python src/05_plddt.py /tmp/tp-colabfold/test_3b510/test_3b510_relaxed_rank_001_alphafold2_ptm_model_4_seed_000.pdb \
    --pae /tmp/tp-colabfold/test_3b510/test_3b510_predicted_aligned_error_v1.json \
    --salida resultados/fig_plddt_E7_colabfold.png \
    --csv resultados/plddt_E7_colabfold.csv

# exploración de 1UBQ
python src/02_explorar_pdb.py datos/1UBQ.pdb
```

Los análisis de cavidades escriben sus tablas en `resultados/`. La figura y la
tabla de pLDDT de la corrida ColabFold se guardan con el sufijo `_colabfold` para
distinguirlas de los archivos anteriores basados en el modelo de ViRO3D.
