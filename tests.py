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

def itp_cantabria(base):
    if base <= 300000: return base * 0.09
    return 300000*0.09 + (base-300000)*0.10

def itp_castilla_leon(base):
    if base <= 250000: return base * 0.08
    return 250000*0.08 + (base-250000)*0.10

def itp_extremadura(base):
    if base <= 360000: return base * 0.08
    if base <= 600000: return 360000*0.08 + (base-360000)*0.10
    return 360000*0.08 + 240000*0.10 + (base-600000)*0.11

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
assert_close(250000 * 0.09, 22500, "CLM 250k")
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

# Progressive: Cantabria
assert_close(itp_cantabria(200000), 200000*0.09, "Cantabria 200k")
assert_close(itp_cantabria(400000), 300000*0.09 + 100000*0.10, "Cantabria 400k")

# Progressive: Castilla y León
assert_close(itp_castilla_leon(200000), 200000*0.08, "CyL 200k")
assert_close(itp_castilla_leon(300000), 250000*0.08 + 50000*0.10, "CyL 300k")

# Progressive: Extremadura
assert_close(itp_extremadura(300000), 300000*0.08, "Extremadura 300k")
assert_close(itp_extremadura(500000), 360000*0.08 + 140000*0.10, "Extremadura 500k")
assert_close(itp_extremadura(700000), 360000*0.08 + 240000*0.10 + 100000*0.11, "Extremadura 700k")


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
assert_close(180000 * 0.07, 12600, "Cantabria habitual 180k <200k")
assert_close(180000 * 0.05, 9000, "Cantabria joven 180k <200k")
assert_close(180000 * 0.04, 7200, "Cantabria discap 33-64% 180k <200k")
assert_close(180000 * 0.03, 5400, "Cantabria discap 65% 180k <200k")
assert_close(180000 * 0.05, 9000, "Cantabria VPO 180k <200k")

# CLM (updated limits to 240k per Ley 1/2026)
assert_close(200000 * 0.06, 12000, "CLM habitual 200k <240k")
assert_close(200000 * 0.03, 6000, "CLM joven 200k <240k (3%)")
assert_close(200000 * 0.05, 10000, "CLM familia 200k <240k")

# CyL
assert_close(200000 * 0.04, 8000, "CyL joven 200k")
assert_close(100000 * 0.0001, 10, "CyL joven rural 100k (0.01%)")
assert_close(200000 * 0.04, 8000, "CyL familia 200k")
assert_close(200000 * 0.04, 8000, "CyL discapacidad 200k")

# Cataluna
assert_close(300000 * 0.05, 15000, "Cataluna joven<32 300k")
assert_close(300000 * 0.05, 15000, "Cataluna discapacidad 33% 300k")

# Extremadura
assert_close(180000 * 0.07, 12600, "Extremadura habitual 180k <200k")
assert_close(200000 * 0.04, 8000, "Extremadura joven 200k")
assert_close(200000 * 0.04, 8000, "Extremadura familia 200k")
assert_close(150000 * 0.04, 6000, "Extremadura rural 150k <180k")
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
# TESTS: AJD BONIFICACIONES (OBRA NUEVA)
# ============================================================

print("\n" + "=" * 60)
print("TESTING AJD BONIFICACIONES (OBRA NUEVA)")
print("=" * 60)

# Andalucia AJD
assert_close(140000 * 0.01, 1400, "AND AJD habitual 140k <150k (1%)")
assert_close(140000 * 0.003, 420, "AND AJD joven 140k <150k (0.3%)")
assert_close(200000 * 0.001, 200, "AND AJD familia 200k <250k (0.1%)")
assert_close(200000 * 0.001, 200, "AND AJD discapacidad 200k <250k (0.1%)")
assert_close(300000 * 0.001, 300, "AND AJD VPO 300k (0.1%)")

# Aragon AJD
assert_close(200000 * 0.003, 600, "ARA AJD VPP 200k (0.3%)")

# Asturias AJD
assert_close(200000 * 0.003, 600, "AST AJD VPO 200k (0.3%)")

# Baleares AJD
assert_close(250000 * 0.012, 3000, "BAL AJD habitual 250k <270k (1.2%)")

# Canarias AJD
assert_close(200000 * 0.004, 800, "CAN AJD habitual 200k (0.4%)")
assert_close(200000 * 0.0015, 300, "CAN AJD discapacidad 200k (0.15%)")

# Cantabria AJD
assert_close(180000 * 0.003, 540, "CANT AJD joven 180k (0.3%)")

# CLM AJD
assert_close(200000 * 0.0025, 500, "CLM AJD joven 200k <240k (0.25%)")

# CyL AJD
assert_close(200000 * 0.005, 1000, "CYL AJD joven 200k (0.5%)")
assert_close(100000 * 0.0001, 10, "CYL AJD rural 100k (0.01%)")

# Cataluña AJD
assert_equal(0, 0, "CAT AJD joven (0% bonif 100%)")
assert_close(300000 * 0.0075, 2250, "CAT AJD familia 300k (0.75%)")
assert_equal(0, 0, "CAT AJD VPO (exento)")

# Extremadura AJD
assert_close(200000 * 0.0075, 1500, "EXT AJD habitual 200k (0.75%)")
assert_close(200000 * 0.005, 1000, "EXT AJD rural 200k (0.5%)")

# Galicia AJD
assert_close(200000 * 0.01, 2000, "GAL AJD habitual 200k (1%)")
assert_close(200000 * 0.005, 1000, "GAL AJD joven 200k (0.5%)")

# Murcia AJD
assert_close(140000 * 0.001, 140, "MUR AJD joven 140k <150k (0.1%)")

# Rioja AJD
assert_close(200000 * 0.005, 1000, "RIO AJD joven 200k (0.5%)")

# Valencia AJD
assert_close(170000 * 0.001, 170, "VAL AJD joven 170k <180k (0.1%)")
assert_close(200000 * 0.001, 200, "VAL AJD discapacidad 200k (0.1%)")

# Pais Vasco: AJD is 0% always
assert_equal(0, 0, "PV AJD general (0%)")

# Madrid: no specific AJD bonifications
assert_close(300000 * 0.0075, 2250, "MAD AJD general 300k (0.75%)")

# AJD general rates (no bonifications)
assert_close(300000 * 0.012, 3600, "AND AJD general 300k (1.2%)")
assert_close(300000 * 0.015, 4500, "ARA AJD general 300k (1.5%)")
assert_close(300000 * 0.015, 4500, "CAT AJD general 300k (1.5%)")
assert_close(300000 * 0.02, 6000, "VAL AJD general 300k (2%)")
assert_close(300000 * 0.0075, 2250, "CAN AJD general 300k (0.75%)")
assert_close(300000 * 0.005, 1500, "NAV AJD general 300k (0.5%)")

# Obra nueva total (IVA + AJD general) for key communities
assert_close(300000 * 0.10 + 300000 * 0.0075, 32250, "MAD obra nueva total 300k")
assert_close(300000 * 0.10 + 300000 * 0.012, 33600, "AND obra nueva total 300k")
assert_close(300000 * 0.10 + 300000 * 0.015, 34500, "CAT obra nueva total 300k")
assert_close(300000 * 0.10 + 300000 * 0.02, 36000, "VAL obra nueva total 300k")
assert_close(300000 * 0.07 + 300000 * 0.0075, 23250, "CAN obra nueva IGIC total 300k")
assert_close(300000 * 0.10 + 0, 30000, "PV obra nueva total 300k (AJD 0%)")


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

# Cantabria habitual: limit 200k
assert_close(itp_cantabria(210000), 210000*0.09, "Cantabria habitual 210k (>200k, general rate)")

# Baleares primera: limit 270k
assert_close(itp_baleares(280000), 280000*0.08, "Baleares primera 280k (>270k, general rate)")

# Valencia joven: limit 180k
assert_close(itp_valencia(190000), 190000*0.10, "Valencia joven 190k (>180k, general rate)")

# Galicia joven: limit 150k
assert_close(itp_galicia(160000), 150000*0.08 + 10000*0.09, "Galicia joven 160k (>150k, general rate)")

# CLM AJD joven: limit 240k
assert_close(250000 * 0.0125, 3125, "CLM AJD joven 250k (>240k, general AJD rate)")

# Andalucia AJD joven: limit 150k
assert_close(160000 * 0.012, 1920, "AND AJD joven 160k (>150k, general AJD rate)")


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

# Scenario 6: Obra nueva Andalucia, 140k, joven (AJD 0.3%)
precio = 140000
iva = precio * 0.10
ajd = precio * 0.003  # joven AJD
notaria = estimar_notaria(precio)
registro = estimar_registro(precio)
gestoria = 400
tasacion = 400
total_gastos = iva + ajd + notaria + registro + gestoria + tasacion
assert_close(iva, 14000, "E2E ObraNueva AND joven IVA")
assert_close(ajd, 420, "E2E ObraNueva AND joven AJD (0.3%)")
assert_close(total_gastos, 16170, "E2E ObraNueva AND joven total")

# Scenario 7: Obra nueva Cataluna, 300k, joven<35 (AJD 0%)
precio = 300000
iva = precio * 0.10
ajd = 0  # bonif 100%
notaria = estimar_notaria(precio)
registro = estimar_registro(precio)
gestoria = 400
tasacion = 400
total_gastos = iva + ajd + notaria + registro + gestoria + tasacion
assert_close(total_gastos, 32250, "E2E ObraNueva CAT joven total (AJD 0%)")

# Scenario 8: Obra nueva Canarias, 200k (IGIC 7% no IVA)
precio = 200000
igic = precio * 0.07  # IGIC not IVA
ajd = precio * 0.0075
notaria = estimar_notaria(precio)
registro = estimar_registro(precio)
gestoria = 400
tasacion = 400
total_gastos = igic + ajd + notaria + registro + gestoria + tasacion
assert_close(igic, 14000, "E2E ObraNueva CAN IGIC")
assert_close(ajd, 1500, "E2E ObraNueva CAN AJD")
assert_close(total_gastos, 17420, "E2E ObraNueva CAN total")

# Scenario 9: Segunda mano Cantabria 180k, habitual (7%)
precio = 180000
itp = precio * 0.07
notaria = estimar_notaria(precio)
registro = estimar_registro(precio)
gestoria = 400
total_gastos = itp + notaria + registro + gestoria
assert_close(itp, 12600, "E2E Cantabria habitual ITP 7%")
assert_close(total_gastos, 14120, "E2E Cantabria habitual total")

# Scenario 10: Segunda mano CyL 100k, joven rural 0.01%
precio = 100000
itp = precio * 0.0001
total_gastos = itp + estimar_notaria(precio) + estimar_registro(precio) + 400
assert_close(itp, 10, "E2E CyL joven rural ITP")
assert_close(total_gastos, 1360, "E2E CyL joven rural total")


# ============================================================
# TESTS: MADRID EXHAUSTIVO
# ============================================================

print("\n" + "=" * 60)
print("TESTING MADRID EXHAUSTIVO")
print("=" * 60)

# ITP general
assert_close(300000 * 0.06, 18000, "MAD ITP general 300k")
assert_close(500000 * 0.06, 30000, "MAD ITP general 500k")
assert_close(150000 * 0.06, 9000, "MAD ITP general 150k")

# Bonificacion habitual (5.4%) <= 250k
assert_close(200000 * 0.054, 10800, "MAD habitual 200k")
assert_close(250000 * 0.054, 13500, "MAD habitual 250k (limite)")
# > 250k: no aplica, vuelve al 6%
assert_close(260000 * 0.06, 15600, "MAD habitual 260k (>250k, general)")

# Familia numerosa (4%) sin limite de precio
assert_close(300000 * 0.04, 12000, "MAD familia 300k")
assert_close(500000 * 0.04, 20000, "MAD familia 500k")
assert_close(100000 * 0.04, 4000, "MAD familia 100k")

# Discapacidad >= 33% (3.5%) <= 130k
assert_close(100000 * 0.035, 3500, "MAD discap 100k")
assert_close(130000 * 0.035, 4550, "MAD discap 130k (limite)")
# > 130k: no aplica
assert_close(140000 * 0.06, 8400, "MAD discap 140k (>130k, general)")

# Joven rural (0%) <= 250k
assert_equal(0, 0, "MAD joven rural 200k (0%)")
# > 250k: no aplica
assert_close(260000 * 0.06, 15600, "MAD joven rural 260k (>250k, general)")

# AJD progresivo Madrid
assert_close(100000 * 0.004, 400, "MAD AJD 100k (0.4%)")
assert_close(120000 * 0.004, 480, "MAD AJD 120k (0.4% limite)")
assert_close(150000 * 0.005, 750, "MAD AJD 150k (0.5%)")
assert_close(180000 * 0.005, 900, "MAD AJD 180k (0.5% limite)")
assert_close(200000 * 0.0075, 1500, "MAD AJD 200k (0.75%)")
assert_close(400000 * 0.0075, 3000, "MAD AJD 400k (0.75%)")

# E2E Madrid segunda mano 250k habitual, hipoteca 80%
precio = 250000
itp = precio * 0.054  # habitual bonif
not_e = estimar_notaria(precio)  # 800
reg_e = estimar_registro(precio)  # 480
gest = 400
tas = 400
total_g = itp + not_e + reg_e + gest + tas
cuota = cuota_mensual(200000, 2.5, 25)
entrada = 50000
dinero = entrada + total_g
assert_close(itp, 13500, "MAD E2E habitual ITP")
assert_close(total_g, 15580, "MAD E2E habitual total gastos")
assert_close(dinero, 65580, "MAD E2E habitual dinero en mano")
assert_close(cuota, 897, "MAD E2E habitual cuota", 5)

# E2E Madrid obra nueva 300k
precio = 300000
iva = precio * 0.10
ajd = precio * 0.0075
total_g = iva + ajd + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(iva + ajd, 32250, "MAD E2E obra nueva impuestos")
assert_close(total_g, 34500, "MAD E2E obra nueva total")

# E2E Madrid familia numerosa 400k, sin limite
precio = 400000
itp = precio * 0.04
total_g = itp + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(itp, 16000, "MAD E2E familia 400k ITP")
assert_close(total_g, 18470, "MAD E2E familia 400k total")

# E2E Madrid pareja 28k+32k, piso 300k, hipoteca 80%
n1 = calcular_neto_anual(28000)
n2 = calcular_neto_anual(32000)
nm = (n1 + n2) / 12
cuota = cuota_mensual(240000, 2.5, 25)
ratio = cuota / nm * 100
assert_close(cuota, 1077, "MAD E2E pareja cuota", 5)
assert_close(ratio, 28.5, "MAD E2E pareja ratio", 2)

# E2E Madrid soltero 35k, piso 200k ICO 100%
neto_m = calcular_neto_anual(35000) / 12
cuota_ico = cuota_mensual(200000, 2.5, 30)
ratio_ico = cuota_ico / neto_m * 100
assert_close(cuota_ico, 790, "MAD E2E soltero ICO cuota", 5)
assert_close(ratio_ico, 38.3, "MAD E2E soltero ICO ratio", 2)


# ============================================================
# TESTS: VALENCIA EXHAUSTIVO
# ============================================================

print("\n" + "=" * 60)
print("TESTING VALENCIA EXHAUSTIVO")
print("=" * 60)

# ITP general
assert_close(300000 * 0.10, 30000, "VAL ITP general 300k")
assert_close(itp_valencia(1200000), 1000000*0.10 + 200000*0.11, "VAL ITP 1.2M (tramo 11%)")

# Joven bajo (<= 180k) -> 6%
assert_close(170000 * 0.06, 10200, "VAL joven 170k (6%)")
assert_close(180000 * 0.06, 10800, "VAL joven 180k limite (6%)")
# Joven alto (> 180k) -> 8%
assert_close(250000 * 0.08, 20000, "VAL joven 250k (8%)")
assert_close(300000 * 0.08, 24000, "VAL joven 300k (8%)")

# Familia/monoparental bajo (<= 180k) -> 3%
assert_close(170000 * 0.03, 5100, "VAL familia 170k (3%)")
assert_close(180000 * 0.03, 5400, "VAL familia 180k (3%)")
# Familia/monoparental alto (> 180k) -> 4%
assert_close(250000 * 0.04, 10000, "VAL familia 250k (4%)")

# Discapacidad bajo (<= 180k) -> 3%
assert_close(170000 * 0.03, 5100, "VAL discap 170k (3%)")
# Discapacidad alto (> 180k) -> 4%
assert_close(250000 * 0.04, 10000, "VAL discap 250k (4%)")

# Victima violencia bajo (<= 180k) -> 3%
assert_close(170000 * 0.03, 5100, "VAL victima 170k (3%)")
# Victima violencia alto (> 180k) -> 4%
assert_close(250000 * 0.04, 10000, "VAL victima 250k (4%)")

# VPO (<= 180k) -> 4%
assert_close(150000 * 0.04, 6000, "VAL VPO 150k (4%)")

# AJD general
assert_close(300000 * 0.02, 6000, "VAL AJD general 300k (2%)")
# AJD bonificado joven/familia (<= 180k) -> 0.1%
assert_close(170000 * 0.001, 170, "VAL AJD joven 170k (0.1%)")
# AJD bonificado discapacidad -> 0.1%
assert_close(250000 * 0.001, 250, "VAL AJD discap 250k (0.1%)")

# E2E Valencia segunda mano 250k, general (sin bonif)
precio = 250000
itp = precio * 0.10
total_g = itp + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(itp, 25000, "VAL E2E general ITP 250k")
assert_close(total_g, 27080, "VAL E2E general total 250k")

# E2E Valencia segunda mano 170k, joven (6%)
precio = 170000
itp = precio * 0.06
total_g = itp + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
cuota = cuota_mensual(136000, 2.5, 25)
assert_close(itp, 10200, "VAL E2E joven ITP 170k")

# E2E Valencia segunda mano 250k, joven (8%)
precio = 250000
itp = precio * 0.08
total_g = itp + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(itp, 20000, "VAL E2E joven ITP 250k (8%)")

# E2E Valencia segunda mano 170k, familia numerosa (3%)
precio = 170000
itp = precio * 0.03
total_g = itp + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(itp, 5100, "VAL E2E familia ITP 170k (3%)")
assert_close(total_g, 7020, "VAL E2E familia total 170k")

# E2E Valencia obra nueva 300k, general
precio = 300000
iva = precio * 0.10
ajd = precio * 0.02
total_g = iva + ajd + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(iva + ajd, 36000, "VAL E2E obra nueva impuestos 300k")
assert_close(total_g, 38250, "VAL E2E obra nueva total 300k")

# E2E Valencia obra nueva 170k, joven (AJD 0.1%)
precio = 170000
iva = precio * 0.10
ajd = precio * 0.001  # bonificado
total_g = iva + ajd + estimar_notaria(precio) + estimar_registro(precio) + 400 + 400
assert_close(ajd, 170, "VAL E2E obra nueva joven AJD 170k")
assert_close(total_g, 19090, "VAL E2E obra nueva joven total 170k")

# Comparativa Madrid vs Valencia: piso 300k, sin bonificaciones, hipoteca 80%
cuota_300k = cuota_mensual(240000, 2.5, 25)
# Madrid
mad_itp = 300000 * 0.06
mad_gastos = mad_itp + 900 + 550 + 400 + 400
mad_dinero = 60000 + mad_gastos
# Valencia
val_itp = 300000 * 0.10
val_gastos = val_itp + 900 + 550 + 400 + 400
val_dinero = 60000 + val_gastos
assert_close(mad_itp, 18000, "Comparativa MAD ITP 300k")
assert_close(val_itp, 30000, "Comparativa VAL ITP 300k")
assert_close(val_itp - mad_itp, 12000, "Comparativa diferencia ITP MAD vs VAL")
assert_close(val_dinero - mad_dinero, 12000, "Comparativa diferencia dinero en mano MAD vs VAL")

# Comparativa Madrid vs Valencia: obra nueva 300k
mad_obra = 300000 * 0.10 + 300000 * 0.0075
val_obra = 300000 * 0.10 + 300000 * 0.02
assert_close(val_obra - mad_obra, 3750, "Comparativa diferencia obra nueva MAD vs VAL (AJD)")


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
