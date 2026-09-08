# Costos de los servicios de inteligencia artificial

Exportaciones de los paneles de facturación de los dos proveedores, descargadas
el 8 de septiembre de 2026. Respaldan las cifras de costo del capítulo 5
(análisis del riesgo de sobrecostos).

## Archivos

| Prefijo | Proveedor | Granularidad |
|---|---|---|
| `openai_*` | OpenAI | un renglón por día, monto en `amount_value` |
| `anthropic_*` | Anthropic | varios renglones por día (modelo × tipo de token), monto en `cost_usd` |

Los rangos de OpenAI no se superponen. Los de Anthropic sí comparten días entre
archivos, por lo que la agregación deduplica por renglón.

## Reproducir las cifras

```
python3 agregar_costos.py
```

Sin dependencias externas. Los totales por pedido y por ítem usan los volúmenes
de la misma ventana informados en el capítulo 4 (3871 pedidos, 29457 ítems).

## Cobertura

La serie va del 1 de junio al 8 de septiembre de 2026, sin días faltantes. La
ventana de análisis de la memoria es del 4 de junio (primer pedido) al 17 de
agosto de 2026.

## Nota sobre datos sensibles

Los archivos conservan las columnas originales de los paneles, que incluyen el
identificador de la organización y el identificador de la clave de API. Son
identificadores, no credenciales, pero conviene revisarlos antes de publicar el
repositorio.
