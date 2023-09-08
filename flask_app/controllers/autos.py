from flask import render_template, flash, redirect, session, request
from flask_app import app
from flask_app.models.autos import Auto


@app.route('/')
def inicio():

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")


    return render_template(
        'inicio.html', autos=Auto.get_all()
    )

@app.route('/new')
def agregar():

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")


    return render_template(
        'formulario_agregar_auto.html',
    )

@app.route('/compras')
def compras():

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")


    return render_template(
        'compras.html', autos=Auto.get_all(session['usuario']['id'])
    )

@app.route('/procesar_auto', methods=["POST"])
def procesar_auto():
    print(request.form)

    # validacion
    errores = Auto.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/new")
    
    # guardar en base
    id = Auto.save(request.form)

    flash("Auto registrado correctamente", "success")
    return redirect("/")

@app.route('/procesar_auto_editar/<id>', methods=["POST"])
def procesar_auto_editar(id):
    print(request.form)

    # validacion
    errores = Auto.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/auto/editar/"+id)
    
    # actualizar en base
    instancia_auto = Auto.get(id)
    instancia_auto.modelo = request.form['modelo']
    instancia_auto.precio = request.form['precio']
    instancia_auto.marca = request.form['marca']
    instancia_auto.anio = request.form['anio']
    instancia_auto.descripcion = request.form['descripcion']
    instancia_auto.update()

    flash("Auto actualizado correctamente", "success")
    return redirect("/")

@app.route('/auto/eliminar/<id>')
def eliminar(id):

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")
    
    Auto.eliminar(id)

    flash("Auto eliminado correctamente", "success")
    return redirect("/")

@app.route('/auto/editar/<id>')
def editar(id):

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")
    
    return render_template(
        'formulario_editar_auto.html', auto=Auto.get(id)
    )

@app.route('/auto/mostrar/<id>')
def mostrar(id):

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")
    
    return render_template(
        'mostrar_auto.html', auto=Auto.get(id)
    )

@app.route('/auto/vender/<id>')
def vender(id):

    if 'usuario' not in session:
        flash("no estás logeado!!!!", "error")
        return redirect("/login")
    
    instancia_auto = Auto.get(id)
    instancia_auto.vender()

    flash("Auto vendido!!!!", "success")
    return redirect("/")