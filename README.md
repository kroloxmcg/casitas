# Calculadora de Compra de Vivienda — España

Calculadora interactiva para saber el **precio real** que vas a pagar al comprar una vivienda en España, incluyendo todos los impuestos, gastos de formalización y costes de hipoteca.

Pensada para gente que compra por primera vez y no sabe qué gastos se va a encontrar. Cada campo tiene una explicación en lenguaje sencillo.

## Usar

**Online:** [https://kroloxmcg.github.io/casitas/](https://kroloxmcg.github.io/casitas/) — funciona en móvil y escritorio.

**Local:** Abre `index.html` en cualquier navegador. No necesita servidor, instalación ni dependencias.

Todos los cálculos se actualizan en tiempo real. La app tiene dos pestañas:

- **Calculadora**: gastos, impuestos, hipoteca, ICO, vivienda habitual
- **Mi situación**: comprar solo o en pareja, sueldos, si te lo puedes permitir

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

### Aval ICO primera vivienda (programa temporal hasta dic. 2027)

El Estado avala el 20% que los bancos normalmente no financian, permitiendo comprar con hipoteca al 100% **sin necesidad de entrada**. Solo necesitas tener ahorrado el ~10-12% del precio para gastos e impuestos.

No es una ayuda ni una subvención: si dejas de pagar, el Estado cubre al banco pero luego te reclama la deuda con intereses.

Checkbox dentro de la sección de hipoteca. Al activarlo sube la financiación al 100% y muestra los requisitos.

**Requisitos:**

| Requisito | Detalle |
|---|---|
| Edad | < 35 años (ambos compradores). Sin límite si tienes hijos menores |
| Vivienda | Primera vivienda (nunca haber sido propietario, ni herencia) |
| Precio máximo | 325.000 € |
| Ingresos | ≤ 37.800 €/año brutos por persona |
| Patrimonio | ≤ 100.000 € |
| Residencia | 2 años seguidos viviendo en España |
| Obligación | Vivir en la vivienda mínimo 10 años |
| Ahorros necesarios | ~10-12% del precio para gastos (el aval cubre la entrada, no los gastos) |

**Ejemplo práctico** — piso de 200.000 €, comprador de 30 años con 28.000 €/año:

| | Sin ICO | Con ICO |
|---|---|---|
| Entrada | 40.000 € (20%) | 0 € |
| Gastos e impuestos | ~12.500 € | ~12.500 € |
| **Total en mano** | **52.500 €** | **12.500 €** |

**Bancos adheridos (67):** BBVA, CaixaBank, Santander, Sabadell, Bankinter, Unicaja, Abanca, Kutxabank, Ibercaja, Cajamar y 57 cajas rurales más. Se tramita directamente en el banco, no hay que ir al ICO.

### Vivienda habitual — obligaciones
Sección informativa que explica:

- **12 meses** para mudarse tras la compra
- **3 años mínimo** de residencia continuada
- Cómo lo comprueba Hacienda (no solo empadronamiento: facturas de suministros, DNI, etc.)
- Qué pasa si no cumples (reclamación de ITP + intereses)
- **Si vives en el extranjero**: no puedes aplicar bonificaciones de vivienda habitual salvo que te mudes en plazo; para el aval ICO necesitas 2 años de residencia previa en España

### Mi situación (pestaña)
Permite simular si te puedes permitir el piso:

- **1 o 2 compradores** (solo o en pareja)
- **Sueldo bruto anual** por persona → calcula el neto estimado (IRPF por tramos + SS 6,35%)
- **Ratio de endeudamiento**: cuota vs. 35% del neto mensual
  - Verde (< 35%): te lo puedes permitir
  - Naranja (35-40%): justo, riesgo
  - Rojo (> 40%): no recomendable
- **Precio máximo recomendado** según tus ingresos y los parámetros de hipoteca
- **Dinero necesario en mano** (entrada + gastos)

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
