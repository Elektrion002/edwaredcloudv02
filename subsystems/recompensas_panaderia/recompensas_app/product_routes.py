from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from recompensas_app import db
from recompensas_app.models.product import Product
from recompensas_app.product_forms import ProductForm
import os

bp = Blueprint('product', __name__, url_prefix='/admin/catalog')

@bp.route('/')
@login_required
def list():
    if not hasattr(current_user, 'username'): # Solo Staff
        return redirect(url_for('main.index'))
    products = Product.query.order_by(Product.sku).all()
    return render_template('product/list.html', title='Gestión de Catálogo', products=products)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if not hasattr(current_user, 'username'):
        return redirect(url_for('main.index'))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            sku=form.sku.data,
            descripcion=form.descripcion.data,
            tipo_producto=form.tipo_producto.data,
            precio_venta=form.precio_venta.data,
            precio_costo=form.precio_costo.data,
            precio_puntos=form.precio_puntos.data,
            es_canjeable=form.es_canjeable.data,
            puntos_generados=form.puntos_generados.data,
            activo=form.activo.data
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Producto {product.sku} agregado exitosamente.', 'success')
        return redirect(url_for('product.list'))
    
    return render_template('product/product_form.html', title='Agregar Producto', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not hasattr(current_user, 'username'):
        return redirect(url_for('main.index'))
    
    product = Product.query.get_or_404(id)
    form = ProductForm(original_sku=product.sku)
    
    if form.validate_on_submit():
        product.sku = form.sku.data
        product.descripcion = form.descripcion.data
        product.tipo_producto = form.tipo_producto.data
        product.precio_venta = form.precio_venta.data
        product.precio_costo = form.precio_costo.data
        product.precio_puntos = form.precio_puntos.data
        product.es_canjeable = form.es_canjeable.data
        product.puntos_generados = form.puntos_generados.data
        product.activo = form.activo.data
        
        db.session.commit()
        flash(f'Producto {product.sku} actualizado.', 'success')
        return redirect(url_for('product.list'))
    elif request.method == 'GET':
        form.sku.data = product.sku
        form.descripcion.data = product.descripcion
        form.tipo_producto.data = product.tipo_producto
        form.precio_venta.data = product.precio_venta
        form.precio_costo.data = product.precio_costo
        form.precio_puntos.data = product.precio_puntos
        form.es_canjeable.data = product.es_canjeable
        form.puntos_generados.data = product.puntos_generados
        form.activo.data = product.activo
        
    return render_template('product/product_form.html', title='Editar Producto', form=form)

@bp.route('/toggle/<int:id>')
@login_required
def toggle(id):
    if not hasattr(current_user, 'username'):
        return redirect(url_for('main.index'))
    
    product = Product.query.get_or_404(id)
    product.activo = not product.activo
    db.session.commit()
    status = "activado" if product.activo else "desactivado"
    flash(f'Producto {product.sku} {status}.', 'info')
    return redirect(url_for('product.list'))
