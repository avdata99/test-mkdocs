# Bienvenido a la prueba de MkDocs

Una version de este documento esta disponible en formato PDF [here]({{ pdf_url }}).  

## Prueba de variables de entorno

 - test_var: **{{ test_var }}**
 - test_var2: **{{ test_complex_obj.test_var2 }}**
 - test_var3: **{{ test_complex_obj.test_var3 }}**

## Prueba de codigo fuente

Algo de código Python


``` py title="Un poco de Python" linenums="1"
test = True
if test:
    print('Test ok')
```

Algo de JS

``` js title="codigo-app.js"
test = true;
if (test == true):
    console.log('Test ok');
```

## Prueba de imagen

<img class="cordoba-river-imag"
    src="{{ assets_folder }}/img/cordoba-rio.jpg" alt="Cordoba river"
    title="Cordoba river"
    style="float: left; width: 150px; padding: 14px; margin: 14px; border: 2px solid red"/> 

Esta imagen tiene estilos diferentes para las versiones HTML y PDF.  
