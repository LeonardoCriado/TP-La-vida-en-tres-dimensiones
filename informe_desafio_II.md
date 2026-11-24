# La vida en tres dimensiones

**Trabajo práctico de Bioinformática Estructural**  
Leonardo Criado · noviembre de 2026

### Desafío II — AKR1C4 en UniProt

**Proteína:** aldo-keto reductasa familia 1, miembro C4 (AKR1C4; UniProt
[P17516](https://www.uniprot.org/uniprotkb/P17516/entry)), 323 aminoácidos.
Es una enzima citosólica dependiente de NADPH que reduce cetosteroides a
hidroxiesteroides, con actividad 3α-hidroxiesteroide deshidrogenasa; participa en el
metabolismo de esteroides, ácidos biliares y fármacos.

**Sitios anotados en UniProt**

| Anotación | Posición | Relevancia |
|---|---|---|
| Sitio activo (dador de protones) | Y55 | Tirosina catalítica; su pKa determina la catálisis |
| Sitio que baja el pKa de Y55 | K84 | Lisina que estabiliza la tirosinato |
| Unión a cofactor/NADP | 20–24, 166–167, 190, 216–221, 270–280 | Bolsillo de NADP(H) |
| Unión a sustrato/esteroide | 50, 190, 216–221 | Contactos con el anillo esteroideo |
| Tetrada catalítica | D50, Y55, K84, H117 | Red de protones y estabilización |

Las variantes naturales anotadas son G135E (rs11253043), S145C (rs3829125),
C170Y (rs17851824), Q250R (rs4880718) y L311V (rs17134592). La variante **S145C**
se asoció con niveles bajos de progesterona y con historia de irritabilidad
maníaca/hipomaníaca en varones con trastorno bipolar (Johansson et al., 2011), y
otros polimorfismos de AKR1C4 se han estudiado en relación con ideación paranoide
durante episodios maníacos. Es importante notar que **S145 está lejos del sitio
activo** (~20 Å de Y55/H117/K84/D50 y del NADP en 2FVL): su efecto probablemente
no sea catalítico directo, sino de estabilidad, plegamiento o regulación. Es un
buen ejemplo de por qué anotar una variante no es lo mismo que entender su
mecanismo.

---

El contexto general, la metodología y las referencias completas están en el [informe integral](informe.md).
