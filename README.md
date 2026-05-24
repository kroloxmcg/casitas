# Calculadora de Compra de Vivienda — Madrid

Calculadora interactiva para saber el **precio real** que vas a pagar al comprar una vivienda en la Comunidad de Madrid, incluyendo todos los impuestos, gastos de formalización y costes de hipoteca.

Pensada para gente que compra por primera vez y no sabe qué gastos se va a encontrar. Cada campo tiene una explicación en lenguaje sencillo.

## Usar

Abre `index.html` en cualquier navegador. No necesita servidor, instalación ni dependencias. Todos los cálculos se actualizan en tiempo real.

## Qué calcula

### Impuestos
- **Segunda mano**: ITP 6% (sobre el mayor entre precio de compra y valor de referencia catastral)
  - Bonificación vivienda habitual ≤ 250.000 € → tipo efectivo 5,4%
  - Tipo reducido familia numerosa → 4%
- **Obra nueva**: IVA 10% + AJD 0,75%

### Gastos de formalización
Se calculan automáticamente según el precio del piso (tarifas reguladas por ley). Se pueden ajustar manualmente si tienes un presupuesto concreto.

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

- [Gastos compra vivienda 2026 — Arquitasa](https://arquitasa.com/gastos-compra-vivienda/)
- [Impuestos compra vivienda Madrid 2026 — Mabelan](https://mabelan.es/que-debo-pagar-a-la-hora-de-comprar-una-vivienda/)
- [ITP por comunidades — Idealista](https://www.idealista.com/news/inmobiliario/vivienda/2024/09/18/819047-itp-por-comunidades-2024-conoce-los-tipos-aplicables)
- [Gastos hipoteca — Comunidad de Madrid](https://www.comunidad.madrid/servicios/consumo/gastos-constitucion-hipoteca-puede-reclamar)
- [Valor de referencia catastral — Sede Electrónica del Catastro](https://www.sedecatastro.gob.es/Accesos/SECAccvr.aspx)
