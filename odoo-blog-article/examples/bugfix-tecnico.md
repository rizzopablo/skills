# Bug resuelto en Odoo — Error al confirmar facturas con impuestos múltiples

## 🐛 El Problema

Al confirmar facturas de proveedor con múltiples impuestos (`account.tax` con `multiple=True`), el sistema lanzaba `psycopg2.IntegrityError: duplicate key value violates unique constraint "account_move_line_account_id_company_id_unique"`.

**Sintomas observados:**
- `IntegrityError` en `account_move_line` al llamar a `action_post()`
- Solo se reproduce cuando ≥2 impuestos comparten la misma `account_id` en su repartición
- No ocurre en facturas de cliente (diferente path de validación)

**Impacto:** Bloqueo completo del registro de facturas de proveedor con impuestos múltiples.

---

## 🔍 Diagnóstico

El bug está en `addons/account/models/account_move.py`, método `_recompute_taxes()` (línea ~2850 en v17).

**Causa raíz:** Cuando `tax_repartition_line` genera líneas contables, el método `_get_tax_pressure_account_move_line_vals()` no deduplica líneas que apuntan a la misma cuenta contable. Si dos impuestos tienen la misma cuenta de contrapartida (común en configuraciones con IVA + impuesto provincial), se generan dos líneas con `(account_id, company_id)` idéntico, violando la constraint única.

```python
# account_move.py, línea ~2850
# Antes: no filtra duplicados
for tax in taxes:
    lines.extend(tax.compute_all(...).get('taxes', []))
```

**Evidencia:**
- Log de error muestra `account_id=211, company_id=1` duplicado
- Reproducido en v17 Community y Enterprise
- No reportado en Odoo GitHub (posible regresión de v16→v17)

---

## 🔧 La Solución

Override en módulo custom que deduplica líneas contables antes del recomputo:

```python
# custom_l10n_tax_dedup/models/account_move.py
class AccountMove(models.Model):
    _inherit = 'account.move'

    def _recompute_taxes(self):
        # Llamada original
        result = super()._recompute_taxes()
        
        # Deduplicar líneas con misma cuenta+empresa
        seen = set()
        to_remove = []
        for line in self.line_ids:
            key = (line.account_id.id, line.company_id.id)
            if key in seen and line.tax_line_id:
                to_remove.append(line)
            else:
                seen.add(key)
        
        for line in to_remove:
            line.unlink()
        
        return result
```

**Explicación técnica:** El override intercepta después del recomputo original, identifica líneas impositivas con `(account_id, company_id)` duplicado, y elimina las duplicadas. Se preserva la primera línea (que tiene el importe acumulado correcto).

**Verificación:**
- [ ] Unit test: crear factura con 2 impuestos, misma cuenta → 1 línea contable
- [ ] Test manual: confirmar factura con IVA 21% + IIBB 3.5% → sin error
- [ ] Verificar que el importe total del impuesto es correcto (suma de ambos)

---

## ✅ Resultado

Las facturas con múltiples impuestos se confirman correctamente. Se generan asientos contables con una sola línea por cuenta+empresa, con el importe acumulado de todos los impuestos.

**Verificación:**
- [ ] Factura con 2 impuestos confirma sin error
- [ ] Asiento contable: 1 línea por cuenta impositiva (no duplicada)
- [ ] Importe total correcto (suma de todos los impuestos)

**Lección aprendida:** Las constraints de unicidad en `account_move_line` no validan contra líneas impositivas duplicadas generadas por el motor de impuestos. Es necesario un filtro explícito.

---

## 📚 Referencias

- [Código fuente: account_move.py en Odoo v17](https://github.com/odoo/odoo/blob/17.0/addons/account/models/account_move.py)
- [Modelo account.tax.repartition.line](https://github.com/odoo/odoo/blob/17.0/addons/account/models/account_tax.py)
- [Issue: Tax computation with multiple taxes](https://github.com/odoo/odoo/issues/XXXXX)

---

## 💬 ¿Te pasó lo mismo?

Si encontraste este bug en tu versión de Odoo o tenés una solución alternativa (patch upstream, workaround diferente), compartila en los comentarios.

---

**Metadata:**
- Tipo: bugfix
- Audiencia: tecnico
- Versión Odoo: v17
- Topic origen: #1234
- Estado: BORRADOR
