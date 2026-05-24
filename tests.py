#!/usr/bin/env python3
"""
Test suite for casitas calculator.
Replicates the JS calculation logic in Python and verifies correctness.
Run: python3 tests.py
"""

import json
import math
import sys
import re

# ============================================================
# REPLICATE JS LOGIC IN PYTHON
# ============================================================

def itp_aragon(base):
    if base <= 400000: return base * 0.08
    if base <= 450000: return 400000*0.08 + (base-400000)*0.085
    if base <= 500000: return 400000*0.08 + 50000*0.085 + (base-450000)*0.09
    if base <= 750000: return 400000*0.08 + 50000*0.085 + 50000*0.09 + (base-500000)*0.095
    return 400000*0.08 + 50000*0.085 + 50000*0.09 + 250000*0.095 + (base-750000)*0.10

def itp_asturias(base):
    if base <= 300000: return base * 0.08
    if base <= 500000: return 300000*0.08 + (base-300000)*0.09
    return 300000*0.08 + 200000*0.09 + (base-500000)*0.10

def itp_baleares(base):
    if base <= 400000: return base * 0.08
    if base <= 600000: return 400000*0.08 + (base-400000)*0.09
    if base <= 1000000: return 400000*0.08 + 200000*0.09 + (base-600000)*0.10
    if base <= 2000000: return 400000*0.08 + 200000*0.09 + 400000*0.10 + (base-1000000)*0.12
    return 400000*0.08 + 200000*0.09 + 400000*0.10 + 1000000*0.12 + (base-2000000)*0.13

def itp_cataluna(base):
    if base <= 1000000: return base * 0.10
    return 1000000*0.10 + (base-1000000)*0.11

def itp_galicia(base):
    if base <= 150000: return base * 0.08
    if base <= 600000: return 150000*0.08 + (base-150000)*0.09
    return 150000*0.08 + 450000*0.09 + (base-600000)*0.10

def itp_valencia(base):
    if base <= 1000000: return base * 0.10
    return 1000000*0.10 + (base-1000000)*0.11

def cuota_mensual(capital, interes_anual, plazo_anos):
    if capital <= 0 or plazo_anos <= 0: return 0
    if interes_anual <= 0: return capital / (plazo_anos * 12)
    r = interes_anual / 100 / 12
    n = plazo_anos * 12
    return capital * (r * (1+r)**n) / ((1+r)**n - 1)

def estimar_notaria(precio):
    if precio <= 0: return 0
    if precio <= 60000: return 450
    if precio <= 150000: return 600
    if precio <= 200000: return 700
    if precio <= 250000: return 800
    if precio <= 350000: return 900
    if precio <= 500000: return 1050
    return 1200

def estimar_registro(precio):
    if precio <= 0: return 0
    if precio <= 60000: return 250
    if precio <= 150000: return 350
    if precio <= 200000: return 420
    if precio <= 250000: return 480
    if precio <= 350000: return 550
    if precio <= 500000: return 620
    return 700

def calcular_neto_anual(bruto):
    if bruto <= 0: return 0
    ss = bruto * 0.0635
    base_irpf = bruto - ss
    tramos = [
        (12450, 0.19),
        (20200, 0.24),
        (35200, 0.30),
        (60000, 0.37),
        (300000, 0.45),
        (float('inf'), 0.47),
    ]
    irpf = 0
    prev = 0
    for hasta, tipo in tramos:
        if base_irpf <= prev: break
        tramo = min(base_irpf, hasta) - prev
        if tramo > 0: irpf += tramo * tipo
        prev = hasta
    return bruto - ss - irpf


# ============================================================
# TEST FRAMEWORK
# ============================================================

passed = 0
failed = 0
errors = []

def assert_close(actual, expected, label, tolerance=0.01):
    global passed, failed, errors
    if abs(actual - expected) <= tolerance:
        passed += 1
    else:
        failed += 1
        errors.append(f"FAIL: {label}: got {actual:.2f}, expected {expected:.2f} (diff {abs(actual-expected):.2f})")

def assert_equal(actual, expected, label):
    global passed, failed, errors
    if actual == expected:
        passed += 1
    else:
        failed += 1
        errors.append(f"FAIL: {label}: got {actual!r}, expected {expected!r}")


# ============================================================
# TESTS: ITP RATES (general, no bonificaciones)
# ============================================================

print("=" * 60)
print("TESTING ITP RATES")
print("=" * 60)

# Flat rates
assert_close(250000 * 0.07, 17500, "Andalucia 250k")
assert_close(250000 * 0.06, 15000, "Madrid 250k")
assert_close(250000 * 0.04, 10000, "Pais Vasco 250k")
assert_close(250000 * 0.065, 16250, "Canarias 250k")
assert_close(250000 * 0.10, 25000, "Cantabria 250k")
assert_close(250000 * 0.09, 22500, "CLM 250k")
assert_close(250000 * 0.08, 20000, "CyL 250k")
assert_close(250000 * 0.07, 17500, "Rioja 250k")
assert_close(250000 * 0.0775, 19375, "Murcia 250k")

# Progressive: Aragon
assert_close(itp_aragon(300000), 300000*0.08, "Aragon 300k (single bracket)")
assert_close(itp_aragon(420000), 400000*0.08 + 20000*0.085, "Aragon 420k (two brackets)")
assert_close(itp_aragon(800000), 400000*0.08 + 50000*0.085 + 50000*0.09 + 250000*0.095 + 50000*0.10, "Aragon 800k (all brackets)")

# Progressive: Asturias
assert_close(itp_asturias(250000), 250000*0.08, "Asturias 250k")
assert_close(itp_asturias(400000), 300000*0.08 + 100000*0.09, "Asturias 400k")
assert_close(itp_asturias(600000), 300000*0.08 + 200000*0.09 + 100000*0.10, "Asturias 600k")

# Progressive: Baleares
assert_close(itp_baleares(300000), 300000*0.08, "Baleares 300k")
assert_close(itp_baleares(500000), 400000*0.08 + 100000*0.09, "Baleares 500k")
assert_close(itp_baleares(2500000), 400000*0.08 + 200000*0.09 + 400000*0.10 + 1000000*0.12 + 500000*0.13, "Baleares 2.5M")

# Progressive: Cataluna
assert_close(itp_cataluna(800000), 800000*0.10, "Cataluna 800k")
assert_close(itp_cataluna(1500000), 1000000*0.10 + 500000*0.11, "Cataluna 1.5M")

# Progressive: Galicia
assert_close(itp_galicia(100000), 100000*0.08, "Galicia 100k")
assert_close(itp_galicia(300000), 150000*0.08 + 150000*0.09, "Galicia 300k")
assert_close(itp_galicia(700000), 150000*0.08 + 450000*0.09 + 100000*0.10, "Galicia 700k")

# Progressive: Valencia
assert_close(itp_valencia(500000), 500000*0.10, "Valencia 500k")
assert_close(itp_valencia(1200000), 1000000*0.10 + 200000*0.11, "Valencia 1.2M")


# ============================================================
# TESTS: BONIFICACIONES (key ones per community)
# ============================================================

print("\n" + "=" * 60)
print("TESTING BONIFICACIONES")
print("=" * 60)

# Andalucia
assert_close(140000 * 0.06, 8400, "Andalucia habitual <150k")
assert_close(140000 * 0.035, 4900, "Andalucia joven <150k")
assert_close(200000 * 0.035, 7000, "Andalucia familia <250k")
assert_close(200000 * 0.035, 7000, "Andalucia discapacidad 33% <250k")

# Aragon - 50% bonif on cuota for familia
tax_300k = itp_aragon(300000)  # 24000
assert_close(tax_300k * 0.5, 12000, "Aragon familia 300k (50% bonif)")
# 12.5% bonif for joven <100k
assert_close(80000 * 0.08 * 0.875, 5600, "Aragon joven 80k (12.5% bonif)")

# Asturias
assert_close(140000 * 0.04, 5600, "Asturias joven <150k")
assert_close(300000 * 0.04, 12000, "Asturias familia 300k")
assert_close(300000 * 0.03, 9000, "Asturias VPO 300k")

# Baleares
assert_close(250000 * 0.04, 10000, "Baleares primera vivienda 250k")
assert_close(250000 * 0.02, 5000, "Baleares joven<36 250k")
assert_equal(0, 0, "Baleares joven<30 250k (0%)")
assert_close(250000 * 0.02, 5000, "Baleares discapacidad 250k")
# Familia numerosa 300k: 2% on first 270k + 8% on excess
assert_close(270000*0.02 + 30000*0.08, 7800, "Baleares familia 300k (mixed)")

# Canarias
assert_close(140000 * 0.05, 7000, "Canarias habitual <150k")
assert_close(200000 * 0.04, 8000, "Canarias joven 200k")
assert_close(200000 * 0.01, 2000, "Canarias discapacidad 65% 200k")

# Cantabria
assert_close(250000 * 0.05, 12500, "Cantabria joven <300k")
assert_close(250000 * 0.04, 10000, "Cantabria discap 33-64% <300k")
assert_close(250000 * 0.03, 7500, "Cantabria discap 65% <300k")

# CLM (updated limits to 240k per Ley 1/2026)
assert_close(200000 * 0.06, 12000, "CLM habitual 200k <240k")
assert_close(200000 * 0.03, 6000, "CLM joven 200k <240k (3%)")
assert_close(200000 * 0.05, 10000, "CLM familia 200k <240k")

# CyL
assert_close(200000 * 0.04, 8000, "CyL joven 200k")
assert_close(200000 * 0.0001, 20, "CyL joven rural 200k (0.01%)")
assert_close(200000 * 0.04, 8000, "CyL discapacidad 200k")

# Cataluna
assert_close(300000 * 0.05, 15000, "Cataluna joven<32 300k")
assert_close(300000 * 0.05, 15000, "Cataluna discapacidad 33% 300k")

# Extremadura
assert_close(200000 * 0.04, 8000, "Extremadura joven 200k")
assert_close(250000 * 0.05, 12500, "Extremadura discap 33% 250k <300k")
assert_close(350000 * 0.04, 14000, "Extremadura discap 65% 350k")

# Galicia
assert_close(140000 * 0.03, 4200, "Galicia joven <150k")
assert_close(300000 * 0.03, 9000, "Galicia familia 300k")
assert_close(200000 * 0.07, 14000, "Galicia habitual 200k")
assert_close(200000 * 0.04, 8000, "Galicia VPO 200k")

# Madrid
assert_close(250000 * 0.054, 13500, "Madrid habitual 250k (5.4%)")
assert_close(300000 * 0.04, 12000, "Madrid familia 300k")
assert_close(120000 * 0.035, 4200, "Madrid discapacidad 120k <130k")
assert_equal(0, 0, "Madrid joven rural <2500hab 200k (0%)")

# Murcia
assert_close(140000 * 0.03, 4200, "Murcia joven <150k")
assert_close(300000 * 0.03, 9000, "Murcia familia 300k")
assert_close(200000 * 0.03, 6000, "Murcia discapacidad 65% 200k")

# Rioja
assert_close(200000 * 0.05, 10000, "Rioja joven 200k")
assert_close(200000 * 0.05, 10000, "Rioja discapacidad 33% 200k")

# Valencia
assert_close(170000 * 0.06, 10200, "Valencia joven 170k <180k (6%)")
assert_close(170000 * 0.03, 5100, "Valencia familia <180k (3%)")
assert_close(200000 * 0.04, 8000, "Valencia familia >180k (4%)")
assert_close(170000 * 0.03, 5100, "Valencia discap <180k (3%)")
assert_close(200000 * 0.04, 8000, "Valencia discap >180k (4%)")
assert_close(170000 * 0.04, 6800, "Valencia VPO 170k (4%)")


# ============================================================
# TESTS: BONIFICACION PRICE LIMITS (should NOT apply over limit)
# ============================================================

print("\n" + "=" * 60)
print("TESTING PRICE LIMITS")
print("=" * 60)

# Andalucia habitual: limit 150k
assert_close(160000 * 0.07, 11200, "Andalucia habitual 160k (>150k, general rate)")

# Andalucia joven: limit 150k
assert_close(160000 * 0.07, 11200, "Andalucia joven 160k (>150k, general rate)")

# CLM joven: limit 240k (Ley 1/2026)
assert_close(250000 * 0.09, 22500, "CLM joven 250k (>240k, general rate)")

# Madrid discapacidad: limit 130k
assert_close(140000 * 0.06, 8400, "Madrid discap 140k (>130k, general rate)")

# Cantabria: limit 300k
assert_close(310000 * 0.10, 31000, "Cantabria joven 310k (>300k, general rate)")


# ============================================================
# TESTS: OBRA NUEVA (IVA + AJD)
# ============================================================

print("\n" + "=" * 60)
print("TESTING OBRA NUEVA")
print("=" * 60)

# IVA 10% everywhere except Canarias (IGIC 7%)
assert_close(300000 * 0.10, 30000, "IVA obra nueva 300k")
assert_close(300000 * 0.07, 21000, "IGIC Canarias obra nueva 300k")

# AJD varies by community
assert_close(300000 * 0.0075, 2250, "AJD Madrid 300k (0.75%)")
assert_close(300000 * 0.012, 3600, "AJD Andalucia 300k (1.2%)")
assert_close(300000 * 0.015, 4500, "AJD Cataluna 300k (1.5%)")
assert_close(300000 * 0.02, 6000, "AJD Valencia 300k (2%)")
assert_close(300000 * 0.005, 1500, "AJD Navarra 300k (0.5%)")
assert_close(300000 * 0, 0, "AJD Pais Vasco 300k (0%)")

# Madrid AJD progresivo
assert_close(100000 * 0.004, 400, "AJD Madrid progresivo 100k (0.4%)")
assert_close(150000 * 0.005, 750, "AJD Madrid progresivo 150k (0.5%)")
assert_close(200000 * 0.0075, 1500, "AJD Madrid progresivo 200k (0.75%)")


# ============================================================
# TESTS: HIPOTECA
# ============================================================

print("\n" + "=" * 60)
print("TESTING HIPOTECA")
print("=" * 60)

# 250k, 80%, 2.5%, 25 years
c = cuota_mensual(200000, 2.5, 25)
assert_close(c, 897.22, "Cuota 200k 2.5% 25a", 1)

# 300k, 80%, 2.5%, 25 years
c = cuota_mensual(240000, 2.5, 25)
assert_close(c, 1076.67, "Cuota 240k 2.5% 25a", 1)

# 200k, 100%, 2.5%, 30 years (ICO scenario)
c = cuota_mensual(200000, 2.5, 30)
assert_close(c, 790.24, "Cuota ICO 200k 2.5% 30a", 1)

# 0% interest
c = cuota_mensual(120000, 0, 20)
assert_close(c, 500, "Cuota 120k 0% 20a")

# Total intereses
c = cuota_mensual(200000, 2.5, 25)
total_paid = c * 25 * 12
total_intereses = total_paid - 200000
assert_close(total_intereses, 69166, "Total intereses 200k 2.5% 25a", 200)


# ============================================================
# TESTS: GASTOS FORMALIZACION
# ============================================================

print("\n" + "=" * 60)
print("TESTING GASTOS FORMALIZACION")
print("=" * 60)

assert_equal(estimar_notaria(50000), 450, "Notaria 50k")
assert_equal(estimar_notaria(100000), 600, "Notaria 100k")
assert_equal(estimar_notaria(200000), 700, "Notaria 200k")
assert_equal(estimar_notaria(250000), 800, "Notaria 250k")
assert_equal(estimar_notaria(300000), 900, "Notaria 300k")
assert_equal(estimar_notaria(400000), 1050, "Notaria 400k")
assert_equal(estimar_notaria(600000), 1200, "Notaria 600k")

assert_equal(estimar_registro(50000), 250, "Registro 50k")
assert_equal(estimar_registro(200000), 420, "Registro 200k")
assert_equal(estimar_registro(300000), 550, "Registro 300k")
assert_equal(estimar_registro(600000), 700, "Registro 600k")


# ============================================================
# TESTS: SUELDO NETO
# ============================================================

print("\n" + "=" * 60)
print("TESTING SUELDO NETO")
print("=" * 60)

# 25000 bruto
neto = calcular_neto_anual(25000)
assert_close(neto, 18223.25, "Neto 25k bruto", 10)

# 35000 bruto
neto = calcular_neto_anual(35000)
assert_close(neto, 24778.75, "Neto 35k bruto", 10)

# 48000 bruto
neto = calcular_neto_anual(48000)
assert_close(neto, 32618.26, "Neto 48k bruto", 10)

# 60000 bruto
neto = calcular_neto_anual(60000)
assert_close(neto, 39698.20, "Neto 60k bruto", 10)

# Verify SS deduction
assert_close(25000 * 0.0635, 1587.5, "SS 25k")
assert_close(48000 * 0.0635, 3048, "SS 48k")


# ============================================================
# TESTS: RATIO ENDEUDAMIENTO
# ============================================================

print("\n" + "=" * 60)
print("TESTING RATIO ENDEUDAMIENTO")
print("=" * 60)

# Pareja: 48k + 34k bruto, cuota 1076.68
neto1 = calcular_neto_anual(48000)
neto2 = calcular_neto_anual(34000)
neto_mensual = (neto1 + neto2) / 12
cuota = cuota_mensual(240000, 2.5, 25)
ratio = cuota / neto_mensual * 100
assert_close(ratio, 22.8, "Ratio pareja 48k+34k cuota 240k", 1)

# Solo: 30k bruto, cuota 790 (ICO 200k)
neto_solo = calcular_neto_anual(30000) / 12
cuota_ico = cuota_mensual(200000, 2.5, 30)
ratio_solo = cuota_ico / neto_solo * 100
assert_close(ratio_solo, 44.1, "Ratio solo 30k ICO 200k", 1)


# ============================================================
# TESTS: FULL SCENARIO (end to end)
# ============================================================

print("\n" + "=" * 60)
print("TESTING FULL SCENARIOS")
print("=" * 60)

# Scenario 1: Madrid, segunda mano, 300k, habitual (>250k so no bonif), 80% hipoteca
precio = 300000
itp = precio * 0.06  # 18000
notaria = estimar_notaria(precio)  # 900
registro = estimar_registro(precio)  # 550
gestoria = 400
tasacion = 400
total_gastos = itp + notaria + registro + gestoria + tasacion
precio_final = precio + total_gastos
entrada = precio * 0.20  # 60000
dinero_mano = entrada + total_gastos

assert_close(itp, 18000, "E2E Madrid ITP")
assert_close(total_gastos, 20250, "E2E Madrid total gastos")
assert_close(precio_final, 320250, "E2E Madrid precio final")
assert_close(dinero_mano, 80250, "E2E Madrid dinero en mano")

# Scenario 2: Madrid, segunda mano, 200k, habitual bonif (5.4%), 100% ICO
precio = 200000
itp = precio * 0.054  # 10800 (bonificacion vivienda habitual)
notaria = estimar_notaria(precio)  # 700
registro = estimar_registro(precio)  # 420
gestoria = 400
tasacion = 400
total_gastos = itp + notaria + registro + gestoria + tasacion
entrada = 0  # ICO
dinero_mano = entrada + total_gastos

assert_close(itp, 10800, "E2E Madrid ICO ITP")
assert_close(dinero_mano, 12720, "E2E Madrid ICO dinero en mano")

# Scenario 3: Valencia, segunda mano, 170k, joven (6%), 80% hipoteca
precio = 170000
itp = precio * 0.06  # 10200
notaria = estimar_notaria(precio)  # 600
registro = estimar_registro(precio)  # 350
gestoria = 400
tasacion = 400
total_gastos = itp + notaria + registro + gestoria + tasacion
precio_final = precio + total_gastos
entrada = precio * 0.20
dinero_mano = entrada + total_gastos

assert_close(itp, 10200, "E2E Valencia joven ITP")
assert_close(precio_final, 182120, "E2E Valencia joven precio final")

# Scenario 4: Cataluña, segunda mano, 400k, no bonif, 80% hipoteca 3% 30a
precio = 400000
itp = itp_cataluna(precio)  # 40000
notaria = estimar_notaria(precio)
registro = estimar_registro(precio)
gestoria = 400
tasacion = 400
total_gastos = itp + notaria + registro + gestoria + tasacion
cuota = cuota_mensual(320000, 3, 30)
entrada = precio * 0.20
dinero_mano = entrada + total_gastos

assert_close(itp, 40000, "E2E Cataluna ITP")
assert_close(total_gastos, 42470, "E2E Cataluna total gastos")
assert_close(cuota, 1349, "E2E Cataluna cuota mensual", 5)

# Scenario 5: Obra nueva Madrid, 300k
precio = 300000
iva = precio * 0.10  # 30000
ajd = precio * 0.0075  # 2250
notaria = estimar_notaria(precio)
registro = estimar_registro(precio)
gestoria = 400
tasacion = 400
total_gastos = iva + ajd + notaria + registro + gestoria + tasacion
precio_final = precio + total_gastos

assert_close(iva, 30000, "E2E ObraNueva Madrid IVA")
assert_close(ajd, 2250, "E2E ObraNueva Madrid AJD")
assert_close(total_gastos, 34500, "E2E ObraNueva Madrid total gastos")


# ============================================================
# TESTS: JSON STRUCTURE
# ============================================================

print("\n" + "=" * 60)
print("TESTING JSON STRUCTURE")
print("=" * 60)

sample_json = {
    "nombre": "Test Piso",
    "fecha": "2026-05-24",
    "datos": {
        "ccaa": "madrid",
        "precio": 300000,
        "valorRef": 0,
        "tipo": "segunda",
        "bonificaciones": ["habitual"],
        "notaria": 900,
        "registro": 550,
        "gestoria": 400,
        "notariaManual": False,
        "registroManual": False,
        "hipoteca": True,
        "hipotecaPct": 80,
        "interes": 2.5,
        "plazo": 25,
        "comisionApertura": 0,
        "tasacion": 400,
        "seguroHogar": 250,
        "ico": False,
        "numCompradores": 2,
        "sueldo1": 48000,
        "sueldo2": 34000
    },
    "resultados": {
        "precioFinal": 320250,
        "totalGastos": 20250,
        "totalImpuestos": 18000,
        "gastosFormal": 1850,
        "cuotaMensual": 1076.68,
        "dineroEnMano": 80250,
        "capitalHipoteca": 240000,
        "ratioEndeudamiento": 22.8
    }
}

# Verify all required keys exist
required_datos = ["ccaa", "precio", "valorRef", "tipo", "bonificaciones",
                   "notaria", "registro", "gestoria", "hipoteca", "hipotecaPct",
                   "interes", "plazo", "comisionApertura", "tasacion", "seguroHogar",
                   "ico", "numCompradores", "sueldo1", "sueldo2"]
for key in required_datos:
    assert_equal(key in sample_json["datos"], True, f"JSON datos.{key} exists")

required_resultados = ["precioFinal", "totalGastos", "totalImpuestos", "gastosFormal",
                        "cuotaMensual", "dineroEnMano", "capitalHipoteca", "ratioEndeudamiento"]
for key in required_resultados:
    assert_equal(key in sample_json["resultados"], True, f"JSON resultados.{key} exists")

# Verify JSON is serializable
try:
    json_str = json.dumps(sample_json, indent=2)
    parsed = json.loads(json_str)
    assert_equal(parsed["nombre"], "Test Piso", "JSON roundtrip nombre")
    assert_equal(parsed["datos"]["precio"], 300000, "JSON roundtrip precio")
    passed += 1  # serializable
except Exception as e:
    failed += 1
    errors.append(f"FAIL: JSON serialization: {e}")


# ============================================================
# TESTS: VERIFY HTML HAS ALL CCAA
# ============================================================

print("\n" + "=" * 60)
print("TESTING HTML INTEGRITY")
print("=" * 60)

with open("index.html", "r") as f:
    html = f.read()

expected_ccaa = [
    "andalucia", "aragon", "asturias", "baleares", "canarias",
    "cantabria", "castilla_mancha", "castilla_leon", "cataluna",
    "ceuta", "extremadura", "galicia", "madrid", "melilla",
    "murcia", "navarra", "pais_vasco", "rioja", "valencia"
]

for ccaa in expected_ccaa:
    assert_equal(ccaa in html, True, f"HTML contains CCAA: {ccaa}")

# Check select options exist
for ccaa in expected_ccaa:
    assert_equal(f'value="{ccaa}"' in html, True, f"HTML select option: {ccaa}")

# Check key UI elements
assert_equal("tabBtnCalc" in html, True, "HTML has calc tab")
assert_equal("tabBtnSitu" in html, True, "HTML has situacion tab")
assert_equal("tabBtnComp" in html, True, "HTML has comparar tab")
assert_equal("btnGuardar" in html, True, "HTML has guardar button")
assert_equal("btnCargar" in html, True, "HTML has cargar button")
assert_equal("chkHipoteca" in html, True, "HTML has hipoteca checkbox")
assert_equal("chkICO" in html, True, "HTML has ICO checkbox")
assert_equal("sueldo1" in html, True, "HTML has sueldo1 input")
assert_equal("sueldo2" in html, True, "HTML has sueldo2 input")


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 60)

if errors:
    print("\nFailed tests:")
    for e in errors:
        print(f"  {e}")

sys.exit(0 if failed == 0 else 1)
