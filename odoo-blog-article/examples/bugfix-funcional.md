# Bug resuelto en Odoo — Error al confirmar facturas con impuestos múltiples

## 🐛 El Problema

Al intentar confirmar una factura de proveedor con más de un impuesto aplicado (IVA 21% + IIBB provincial), Odoo arrojaba un error de validación impidiendo el registro contable.

**Sintomas observados:**
- Error "Cannot reconcile tax lines" al confirmar factura
- Solo ocurría cuando había ≥2 impuestos en la misma línea
- Funcionaba correctamente en facturas de cliente, solo fallaba en proveedor

**Impacto:** Los contadores no podían registrar facturas de proveedores con impuestos múltiples, bloqueando el cierre contable mensual.

---

## 🔍 Diagnóstico

La causa raíz estaba en la validación de líneas impositivas en el modelo `account.tax.repartition.line`. Cuando se aplicaban múltiples impuestos a una misma línea de factura, el sistema intentaba generar asientos contables con cuentas de contrapartida duplicadas, violando la restricción de unicidad.

**Desde la UI:**
1. Crear factura de proveedor
2. Agregar línea con producto que tiene 2 impuestos configurados (ej: IVA 21% + IIBB 3.5%)
3. Click en "Confirmar" → Error

**Causa raíz:** El método `_compute_tax_totals` no filtraba correctamente las líneas de repartición cuando un producto tenía múltiples impuestos con la misma cuenta de contrapartida.

---

## 🔧 La Solución

Se aplicó un override en el módulo de localización para filtrar líneas de repartición duplicadas antes de generar los asientos contables.

**Cómo verificar que se corrigió:**
1. Ir a Contabilidad → Proveedores → Facturas
2. Crear nueva factura con producto que tenga 2+ impuestos
3. Confirmar → Debería registrar el asiento sin error

---

## ✅ Resultado

Las facturas con múltiples impuestos se confirman correctamente, generando los asientos contables correspondientes.

**Verificación:**
- [ ] Factura con 2 impuestos confirma sin error
- [ ] Asiento contable generado con todas las líneas impositivas
- [ ] Balance de comprobación muestra los importes correctos

**Lección aprendida:** Cuando se configuran múltiples impuestos por defecto en productos, es importante verificar que las cuentas de contrapartida no se superpongan entre sí.

---

## 📚 Referencias

- [Documentación de impuestos en Odoo](https://www.odoo.com/documentation/17.0/esp_accounting/taxes.html)
- [Issue relacionado en GitHub Odoo](https://github.com/odoo/odoo/issues/XXXXX)

---

## 💬 ¿Te pasó lo mismo?

Si encontraste este problema en tu implementación o tenés una solución alternativa, compartila en los comentarios. Cada configuración de impuestos es diferente y otras soluciones pueden ayudar a la comunidad.

---

**Metadata:**
- Tipo: bugfix
- Audiencia: funcional
- Versión Odoo: v17
- Topic origen: #1234
- Estado: BORRADOR
