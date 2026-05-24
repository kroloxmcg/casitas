# Calculadora de Compra de Vivienda — España

Calculadora interactiva para saber el **precio real** que vas a pagar al comprar una vivienda en España, incluyendo todos los impuestos, gastos de formalización y costes de hipoteca.

Pensada para gente que compra por primera vez y no sabe qué gastos se va a encontrar. Cada campo tiene una explicación en lenguaje sencillo.

## Usar

**Online:** [https://kroloxmcg.github.io/casitas/](https://kroloxmcg.github.io/casitas/) — funciona en móvil y escritorio.

**Local:** Abre `index.html` en cualquier navegador. No necesita servidor, instalación ni dependencias.

Todos los cálculos se actualizan en tiempo real.

## Comunidades autónomas soportadas

Todas las comunidades autónomas de España, cada una con sus tipos impositivos y bonificaciones específicas:

| Comunidad | ITP (2ª mano) | AJD (obra nueva) |
|---|---|---|
| Andalucía | 7% | 1,2% |
| Aragón | 8–10% (progresivo) | 1,5% |
| Asturias | 8% | 1,2% |
| Islas Baleares | 8–13% (progresivo) | 1,5% |
| Canarias | 6,5% (IGIC 7% en vez de IVA) | 0,75% |
| Cantabria | 10% | 1,5% |
| Castilla-La Mancha | 9% | 1,25% |
| Castilla y León | 8% | 1,5% |
| Cataluña | 10% (11% > 1M€) | 1,5% |
| Ceuta | 6% | 0,5% |
| Extremadura | 8% | 1,5% |
| Galicia | 10% | 1,5% |
| **Madrid** | **6%** | **0,75%** |
| Melilla | 6% | 0,5% |
| Murcia | 8% | 1,5% |
| Navarra | 6% | 0,5% |
| País Vasco | 4% | 0% |
| La Rioja | 7% | 1% |
| C. Valenciana | 10% (→9% desde jul. 2026) | 2% |

## Qué calcula

### Impuestos
- **Segunda mano**: ITP según la comunidad autónoma (sobre el mayor entre precio de compra y valor de referencia catastral)
  - Bonificaciones específicas por comunidad (jóvenes, familias numerosas, discapacidad, etc.)
- **Obra nueva**: IVA 10% + AJD según comunidad (IGIC 7% en Canarias)

### Gastos de formalización
Se calculan automáticamente según el precio del piso (tarifas reguladas por ley, iguales en toda España):

- **Notaría** (~600–1.200 €) — da fe pública de la compraventa
- **Registro de la Propiedad** (~250–700 €) — inscribe el piso a tu nombre
- **Gestoría** (~300–600 €) — tramita papeles e impuestos por ti (opcional pero recomendable)

### Hipoteca (opcional)
Activable con un toggle. Incluye:

- Capital financiado (% configurable, lo normal es 80%)
- Cuota mensual (sistema francés)
- Total de intereses a lo largo del plazo
- Total pagado al banco (capital + intereses)
- Comisión de apertura (muchos bancos ya la han eliminado)
- Tasación (300–600 €)
- Seguro de hogar anual (obligatorio con hipoteca)

### Aval ICO primera vivienda (programa temporal)
Checkbox dentro de la sección de hipoteca. Al activarlo:

- Sube el porcentaje financiado al 100%
- Muestra todos los requisitos (edad, ingresos, precio máximo, patrimonio, residencia)
- Muestra los bancos adheridos (67 entidades)
- Aviso de que es un **programa temporal hasta diciembre 2027**

Requisitos principales: menor de 35 años, primera vivienda, precio ≤ 325.000 €, ingresos ≤ 37.800 €/año, patrimonio ≤ 100.000 €, residencia en España los últimos 2 años.

### Vivienda habitual — obligaciones
Sección informativa que explica:

- **12 meses** para mudarse tras la compra
- **3 años mínimo** de residencia continuada
- Cómo lo comprueba Hacienda (no solo empadronamiento: facturas de suministros, DNI, etc.)
- Qué pasa si no cumples (reclamación de ITP + intereses)
- **Si vives en el extranjero**: no puedes aplicar bonificaciones de vivienda habitual salvo que te mudes en plazo; para el aval ICO necesitas 2 años de residencia previa en España

### Resultado
- Desglose completo de cada gasto
- Precio final (compra + gastos)
- Porcentaje extra sobre el precio de compra
- Dinero necesario en mano (entrada + gastos, desglosado)
- Barra visual de distribución de costes

## Valor de referencia catastral

El ITP no se calcula solo sobre el precio de compra, sino sobre el **mayor valor entre el precio y el valor de referencia catastral**. Este valor lo fija Hacienda cada año para cada inmueble.

Para consultarlo: [Sede Electrónica del Catastro](https://www.sedecatastro.gob.es/Accesos/SECAccvr.aspx) (necesitas certificado digital o Cl@ve).

## Fuentes

- [Aval ICO primera vivienda — ICO](https://www.ico.es/en/linea-avales-hipoteca-primera-vivienda)
- [Aval ICO requisitos y bancos 2026 — Housfy](https://housfy.com/blog/hipoteca-ico-bancos-adheridos-y-requisitos-en-2026/)
- [Concepto vivienda habitual — Agencia Tributaria](https://sede.agenciatributaria.gob.es/Sede/vivienda-otros-inmuebles/deduccion-inversion-vivienda-habitual/concepto-vivienda-habitual.html)
- [Acreditar vivienda habitual ante Hacienda](https://asesorexcelente.com/acreditar-vivienda-habitual/)
- [ITP por comunidades 2026 — Calcula España](https://calculaespana.com/blog/itp-por-comunidades-autonomas)
- [ITP por comunidades — Idealista](https://www.idealista.com/news/inmobiliario/vivienda/2024/09/18/819047-itp-por-comunidades-2024-conoce-los-tipos-aplicables)
- [AJD por comunidades — Rankia](https://www.rankia.com/blog/mejores-hipotecas/2574021-impuesto-actos-juridicos-documentados-ajd-segun-comunidad-autonoma)
- [Bonificaciones ITP jóvenes 2026 — GoHipoteca](https://gohipoteca.com/blog/bonificacion-del-itp-en-la-compra-de-viviendas-para-jovenes)
- [ITP reducido por comunidad — Taxfix](https://taxfix.com/es-es/otros/el-itp-reducido-de-cada-comunidad-autonoma/)
- [Gastos compra vivienda 2026 — Arquitasa](https://arquitasa.com/gastos-compra-vivienda/)
- [Gastos hipoteca — Comunidad de Madrid](https://www.comunidad.madrid/servicios/consumo/gastos-constitucion-hipoteca-puede-reclamar)
- [Valor de referencia catastral — Sede Electrónica del Catastro](https://www.sedecatastro.gob.es/Accesos/SECAccvr.aspx)
