#!/usr/bin/env python3
"""Agrega las exportaciones de facturacion de ambos proveedores de IA y
reproduce las cifras de costo informadas en el capitulo 5."""
import csv
import datetime
import glob
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
VENTANA = ("2026-06-04", "2026-08-17")  # primer pedido -> cierre del analisis
PEDIDOS, ITEMS = 3871, 29457            # capitulo 4, misma ventana


def serie_openai():
    """Un renglon por dia; los archivos no se superponen."""
    diario = {}
    for f in sorted(glob.glob(os.path.join(BASE, "openai_*.csv"))):
        for r in csv.DictReader(open(f)):
            diario[r["start_time_iso"][:10]] = float(r["amount_value"])
    return diario


def serie_anthropic():
    """Varios renglones por dia (modelo x tipo de token) y rangos con
    dias superpuestos entre archivos: se deduplica por renglon."""
    diario, vistos = defaultdict(float), set()
    for f in sorted(glob.glob(os.path.join(BASE, "anthropic_*.csv"))):
        for r in csv.DictReader(open(f)):
            clave = (r["usage_date_utc"], r["model"], r["api_key_id"],
                     r["token_type"], r["usage_type"], r["context_window"],
                     r["cost_usd"])
            if clave in vistos:
                continue
            vistos.add(clave)
            diario[r["usage_date_utc"]] += float(r["cost_usd"])
    return diario


def total(serie, desde, hasta):
    d, h = (datetime.date.fromisoformat(x) for x in (desde, hasta))
    dias = (h - d).days + 1
    suma = sum(serie.get((d + datetime.timedelta(days=i)).isoformat(), 0.0)
               for i in range(dias))
    return suma, dias


if __name__ == "__main__":
    oa, an = serie_openai(), serie_anthropic()
    o, dias = total(oa, *VENTANA)
    a, _ = total(an, *VENTANA)
    print(f"Ventana {VENTANA[0]} a {VENTANA[1]} ({dias} dias)")
    print(f"  OpenAI      US$ {o:7.2f}   ({o / (o + a) * 100:.1f} %)")
    print(f"  Anthropic   US$ {a:7.2f}   ({a / (o + a) * 100:.1f} %)")
    print(f"  Total       US$ {o + a:7.2f}   promedio {(o + a) / dias:.2f}/dia")
    print(f"  Por pedido  US$ {(o + a) / PEDIDOS:.4f}    por item US$ {(o + a) / ITEMS:.5f}")

    print("\nTramos mensuales (ambos proveedores)")
    for etiqueta, desde, hasta in [("04/06 a 30/06", "2026-06-04", "2026-06-30"),
                                   ("julio        ", "2026-07-01", "2026-07-31"),
                                   ("01/08 a 17/08", "2026-08-01", "2026-08-17")]:
        print(f"  {etiqueta}  US$ {total(oa, desde, hasta)[0] + total(an, desde, hasta)[0]:7.2f}")

    print("\nEfecto del cambio en los flujos de n8n (promedio diario)")
    for etiqueta, desde, hasta in [("antes  04/06 a 31/07", "2026-06-04", "2026-07-31"),
                                   ("despues 01/08 a 17/08", "2026-08-01", "2026-08-17")]:
        so, n = total(oa, desde, hasta)
        sa, _ = total(an, desde, hasta)
        print(f"  {etiqueta}:  OpenAI {so / n:.2f}/dia   Anthropic {sa / n:.3f}/dia")
