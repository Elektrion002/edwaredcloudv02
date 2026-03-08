from recompensas_app import create_app, db
from recompensas_app.models.product import Product

app = create_app()

with app.app_context():
    try:
        print("Buscando productos activos...")
        products = Product.query.filter_by(activo=True).all()
        print(f"Productos encontrados: {len(products)}")
        for p in products:
            print(f"- {p.sku}: {p.descripcion} (Venta: {p.precio_venta}, Canje: {p.es_canjeable})")
        
        print("\nIntentando renderizar portal/catalog.html...")
        from flask import render_template
        with app.test_request_context():
            rendered = render_template('portal/catalog.html', title='Test', products=products)
            print("¡Renderizado exitoso!")
            # print(rendered[:500])
    except Exception as e:
        print(f"\n¡ERROR DETECTADO!")
        import traceback
        traceback.print_exc()
