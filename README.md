# Calculadora de Compra de Vivienda — España

Calculadora interactiva para saber el **precio real** que vas a pagar al comprar una vivienda en España, incluyendo todos los impuestos, gastos de formalización y costes de hipoteca.

Pensada para gente que compra por primera vez y no sabe qué gastos se va a encontrar. Cada campo tiene una explicación en lenguaje sencillo.

## Usar

**Online:** [https://kroloxmcg.github.io/casitas/](https://kroloxmcg.github.io/casitas/) — funciona en móvil y escritorio.

**Local:** Abre `index.html` en cualquier navegador. No necesita servidor, instalación ni dependencias.

Todos los cálculos se actualizan en tiempo real. La app tiene tres pestañas:

- **Calculadora**: gastos, impuestos, hipoteca, ICO, vivienda habitual + guardar/cargar escenarios
- **Mi situación**: comprar solo o en pareja, sueldos, si te lo puedes permitir
- **Comparar**: subir varios escenarios guardados (.json) y verlos lado a lado en tabla

## Comunidades autónomas

Todas las CCAA con sus tipos impositivos, escalas progresivas y bonificaciones auditadas una a una:

| Comunidad | ITP (2ª mano) | AJD (obra nueva) | Bonificaciones disponibles |
|---|---|---|---|
| Andalucía | 7% | 1,2% | Habitual 6%, jóvenes/familias/discapacidad ≥33%/víctimas 3,5%, VPO 3,5% |
| Aragón | 8–10% (progresivo) | 1,5% | Familias 50% bonif. cuota, jóvenes/discapacidad/víctimas 12,5% bonif. (<100k) |
| Asturias | 8–10% (progresivo) | 1,2% | Jóvenes 4% (<150k), familias/monop./discapacidad ≥65%/víctimas 4%, VPO 3% |
| Islas Baleares | 8–13% (progresivo) | 1,5% | Primera vivienda 4%, jóvenes <36 2%, <30 años/discap. ≥33% 0%, familias 2% |
| Canarias | 6,5% (IGIC 7%) | 0,75% | Habitual 5% (<150k), jóvenes/familias 4%, discapacidad ≥65% 1% |
| Cantabria | 10% | 1,5% | Jóvenes/familias 5%, discap. 33-64% 4%, discap. ≥65% 3% (todo <300k) |
| Castilla-La Mancha | 9% | 1,25% | Habitual 6%, jóvenes 3% (Ley 1/2026), familias/discap. 5% (todo <240k) |
| Castilla y León | 8% | 1,5% | Jóvenes/familias/discap. 4%, jóvenes rural <10k hab. 0,01% |
| Cataluña | 10% (11% >1M€) | 1,5% | Jóvenes <32/familias/monop./discap. ≥33% 5% |
| Ceuta | 6% | 0,5% | — |
| Extremadura | 8% | 1,5% | Jóvenes/familias/VPO/discap. ≥65% 4%, discap. ≥33% 5% (<300k) |
| Galicia | 8–10% (progresivo) | 1,5% | Habitual 7%, jóvenes/familias/monop./discap./víctimas 3%, VPO 4%, rural 0% |
| **Madrid** | **6%** | **0,75%** | **Habitual 5,4% (≤250k), familias 4%, discap. ≥33% 3,5% (≤130k), joven rural 0%** |
| Melilla | 6% | 0,5% | — |
| Murcia | 7,75% | 1,5% | Jóvenes/familias/discap. ≥65% 3%, VPO 4% |
| Navarra | 6% | 0,5% | — |
| País Vasco | 4% | 0% | Familias Bizkaia 2,5% |
| La Rioja | 7% | 1% | Jóvenes/familias/discap. ≥33% 5% |
| C. Valenciana | 10% (→9% jun. 2026) | 2% | Jóvenes 6% (<180k), familias/discap. 3-4%, VPO 4% |

## Qué calcula

### Impuestos
- **Segunda mano**: ITP según CCAA (sobre el mayor entre precio y valor de referencia catastral)
  - Bonificaciones por comunidad: jóvenes, familias numerosas, monoparentales, discapacidad (≥33% o ≥65%), víctimas de violencia, VPO, zonas rurales despobladas
- **Obra nueva**: IVA 10% + AJD según comunidad (IGIC 7% en Canarias)
- **No hay beneficios fiscales por ser funcionario** — solo mejores condiciones hipotecarias bancarias
- **Sobre plano**: mismos impuestos que obra nueva (IVA + AJD). El aval ICO excluye viviendas sobre plano

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

**Bancos adheridos (67):** BBVA, CaixaBank, Santander, Sabadell, Bankinter, Unicaja, Abanca, Kutxabank, Ibercaja, Cajamar y 57 cajas rurales más.

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
- **Dinero necesario en mano** con desglose real (mismos datos que la calculadora)

### Guardar y cargar escenarios
Botones en la pestaña Calculadora:

- **Guardar escenario**: descarga un archivo `.json` con todos los datos y resultados. Le pones un nombre (ej: "Piso Deva 4") y se descarga como `casitas-piso-deva-4.json`
- **Cargar escenario**: sube un `.json` guardado y rellena automáticamente todos los campos (incluida la pestaña Mi situación). Puedes modificar valores y volver a guardar

Los archivos se pueden compartir por WhatsApp, email, Drive... Cualquiera puede cargarlos en la calculadora.

### Comparar escenarios (pestaña)
Sube varios archivos `.json` de escenarios guardados y compáralos lado a lado en una tabla:

- Precio, impuestos, gastos, precio final
- Cuota mensual, dinero en mano
- Hipoteca, ICO, sueldos, neto mensual, ratio de endeudamiento
- Pulsa en el nombre de un escenario para cargarlo en la calculadora y modificarlo

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
- [Tipos reducidos Andalucía — Junta de Andalucía](https://www.juntadeandalucia.es/organismos/economiahaciendayfondoseuropeos/areas/tributos-juego/tributos/paginas/polit-social.html)
- [ITP Aragón 2026 — ForoHipotecario](https://forohipotecario.es/bonificaciones-fiscales-en-el-itp-por-compra-de-vivienda-en-aragon-actualizado-2026/)
- [ITP Asturias 2026 — Hipotecas.me](https://www.hipotecas.me/itp/asturias)
- [ITP Baleares 2026 — ForoHipotecario](https://forohipotecario.es/bonificaciones-fiscales-en-el-itp-por-compra-de-vivienda-en-islas-baleares-actualizado-2026/)
- [ITP Galicia 2026 — GuíaFiscal](https://guiafiscal.es/itp/galicia/)
- [Ley 1/2026 Castilla-La Mancha — Portal Tributario CLM](https://portaltributario.jccm.es/avisos/entrada-en-vigor-de-la-ley-12026-de-26-de-marzo-de-medidas-administrativas-y-tributarias-de)
- [ITP Madrid — Comunidad de Madrid](https://www.comunidad.madrid/atencion-contribuyente/transmisiones-patrimoniales-onerosas)
- [ITP Valencia 2026 — GoHipoteca](https://gohipoteca.com/blog/itp-comunidad-valenciana)
- [ITP Murcia 2026 — Hipotecas.me](https://www.hipotecas.me/itp/murcia)
- [Gastos compra vivienda 2026 — Arquitasa](https://arquitasa.com/gastos-compra-vivienda/)
- [Gastos hipoteca — Comunidad de Madrid](https://www.comunidad.madrid/servicios/consumo/gastos-constitucion-hipoteca-puede-reclamar)
- [Valor de referencia catastral — Sede Electrónica del Catastro](https://www.sedecatastro.gob.es/Accesos/SECAccvr.aspx)
