def calcular_presupuesto_final(precios_materiales, necesita_flete):

    total = 0
    
    for material in precios_materiales:
        total = total + material
        
    if necesita_flete:
        costo_flete = 5000
        total += costo_flete

    return total