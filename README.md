# Inventario
Proyecto integrado para Talent Tech 2024
Aplicación de Gestión de Inventario


Descripción


Esta aplicación permite gestionar un inventario de productos utilizando una base de datos SQLite. Puedes agregar, actualizar, eliminar y buscar productos. Además, se genera un reporte de productos con stock bajo y se pueden eliminar productos con campos vacíos o nulos.



Funcionalidades Implementadas

Agregar Producto: Permite agregar un nuevo producto al inventario con los siguientes campos:


	Nombre: El nombre del producto. Este campo no puede estar vacío y no se puede repetir.
	
Descripción: Una descripción opcional del producto.

	Cantidad: La cantidad del producto en inventario. Debe ser un número entero positivo.

	Precio: El precio del producto. Debe ser un número decimal positivo.
	Categoría: La categoría del producto. Solo se aceptan letras (sin números o caracteres especiales).

Actualizar Producto: Permite actualizar la cantidad de un producto existente. Se solicita el ID del producto y la nueva cantidad.


Eliminar Producto: Permite eliminar un producto del inventario proporcionando su ID.

Ver Productos: Muestra todos los productos del inventario, incluyendo el ID, nombre, descripción, cantidad, precio y categoría.


Buscar Producto: Permite buscar productos en el inventario por:


	ID
	
Nombre

	Categoría

Generar Reporte de Stock Bajo: Permite generar un reporte de productos cuyo stock sea inferior o igual a un valor umbral especificado por el usuario.


Limpiar Productos Vacíos: Elimina productos con campos vacíos o nulos en el nombre, descripción o categoría.



Requisitos

Python 3.x: La aplicación está escrita en Python y requiere una instalación de Python 3.x o superior.

SQLite3: La base de datos se gestiona con SQLite3, que está incluido en las versiones estándar de Python.


Cómo Ejecutar la Aplicación

Abrir carpeta: Abrir la carpeta de Trabajo Final, contiene Inventario.py y inventario.db.


Ejecutar la aplicación:


	Abre una terminal o línea de comandos.

	Navega a la carpeta donde se encuentra el archivo Inventario.py.

	Ejecuta el archivo con el siguiente comando:
Inventario.py

Interacción con la aplicación: Una vez que la aplicación se ejecute, se mostrará un menú con las siguientes opciones:


	
1. Agregar producto
	
2. Actualizar cantidad de producto

	3. Eliminar producto

	4. Ver productos

	5. Buscar producto

	6. Generar reporte de stock bajo

	7. Salir

El usuario podrá elegir la opción deseada ingresando el número correspondiente.



Notas

Los productos no pueden tener el mismo nombre. 
Si intentas agregar un producto con un nombre ya existente, la aplicación mostrará un mensaje de error.

El campo "Categoría" solo acepta texto (sin números ni caracteres especiales).
