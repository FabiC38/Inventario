import sqlite3

def obtener_conexion():
    """Establece y devuelve la conexión a la base de datos."""
    return sqlite3.connect("inventario.db")

def crear_database():
    """Crea la base de datos y la tabla de productos si no existen."""
    connection = obtener_conexion()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        categoria TEXT
                    )''')
    connection.commit()
    connection.close()

def agregar_product():
    """Agrega un nuevo producto al inventario."""
    print("Agregar Producto")
    # Diccionario con las entradas que pedirá al usuario
    inputs = {"nombre": "Ingrese el nombre del producto: ",
              "descripcion": "Ingrese una descripción del producto: ",
              "cantidad": "Ingrese la cantidad del producto: ",
              "precio": "Ingrese el precio del producto: ",
              "categoria": "Ingrese la categoría del producto (solo texto): "}

    # Diccionario donde se almacenarán los valores ingresados por el usuario
    values = {}
    
    # Se recorren las claves del diccionario para pedir los datos al usuario
    for key, prompt in inputs.items():
        if key == "cantidad":
            while True:
                try:
                    # Pedir la cantidad como un número entero
                    values[key] = int(input(prompt))
                    # Validar que la cantidad no sea negativa
                    if values[key] < 0:
                        print("La cantidad no puede ser negativa.")
                        continue
                    break
                except ValueError:
                    # Si el valor no es un número, se muestra un mensaje de error
                    print("Por favor, ingrese un número válido para la cantidad.")
        elif key == "precio":
            while True:
                try:
                    # Pedir el precio como un número flotante
                    values[key] = float(input(prompt))
                    # Validar que el precio no sea negativo
                    if values[key] < 0:
                        print("El precio no puede ser negativo.")
                        continue
                    break
                except ValueError:
                    # Si el valor no es un número válido, se muestra un mensaje de error
                    print("Por favor, ingrese un número válido para el precio.")
        elif key == "categoria":
            while True:
                # Pedir la categoría
                values[key] = input(prompt)
                # Validar que la categoría no sea numérica
                if values[key].isalpha():  # Comprobar si la categoría es solo texto
                    break
                else:
                    print("La categoría debe contener solo texto. Por favor, intente nuevamente.")
        else:
            # Para nombre y descripción, solo se pide que no estén vacíos
            values[key] = input(prompt)
            if not values[key]:  # Validar que no se deje vacío
                print(f"El campo {key} no puede estar vacío.")
                return

    # Verificar que todos los campos sean válidos antes de insertar
    if not values["nombre"] or not values["descripcion"] or not values["categoria"]:
        print("El nombre, la descripción y la categoría son campos obligatorios.")
        return

    # Verificar si el nombre del producto ya existe en la base de datos
    try:
        with obtener_conexion() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM productos WHERE nombre = ?", (values["nombre"],))
            existing_product = cursor.fetchone()
            
            if existing_product:
                # Si ya existe un producto con el mismo nombre, se muestra un mensaje
                print(f"El producto con el nombre '{values['nombre']}' ya existe en el inventario.")
                return

        print(f"Ingresando producto con los siguientes valores: {values}")  # Depuración

        # Si el producto no existe, proceder a agregarlo
        try:
            with obtener_conexion() as connection:
                cursor = connection.cursor()
                # Insertar el nuevo producto en la base de datos
                cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                               (values["nombre"], values["descripcion"], values["cantidad"], values["precio"], values["categoria"]))
                connection.commit()
            print("Producto agregado con éxito.")
        except sqlite3.Error as e:
            # Si ocurre algún error al intentar insertar el producto, se muestra un mensaje
            print(f"Error al agregar el producto: {e}")

    except sqlite3.Error as e:
        # Si ocurre un error al verificar si el producto ya existe, se muestra un mensaje
        print(f"Error al verificar el producto: {e}")

def actualizar_product():
    """Actualiza la cantidad de un producto en el inventario."""
    try:
        product_id = int(input("Ingrese el ID del producto que desea actualizar: "))
        cantidad = int(input("Ingrese la nueva cantidad del producto: "))
    except ValueError:
        print("Por favor, ingrese un número válido para el ID o la cantidad.")
        return

    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?",
                       (cantidad, product_id))
        connection.commit()
        connection.close()
        print("Cantidad del producto actualizada con éxito.")
    except sqlite3.Error as e:
        print(f"Error al actualizar el producto: {e}")

def eliminar_product():
    """Elimina un producto del inventario."""
    try:
        product_id = int(input("Ingrese el ID del producto que desea eliminar: "))
    except ValueError:
        print("Por favor, ingrese un número válido para el ID.")
        return

    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
        connection.commit()
        connection.close()
        print("Producto eliminado con éxito.")
    except sqlite3.Error as e:
        print(f"Error al eliminar el producto: {e}")

def ver_products():
    """Muestra todos los productos en el inventario."""
    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM productos")
        products = cursor.fetchall()
        connection.close()

        print("\nLista de productos en el inventario:")
        print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
        print("-" * 60)
        for product in products:
            print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]} | {product[4]} | {product[5]}")
    except sqlite3.Error as e:
        print(f"Error al obtener los productos: {e}")

def buscar_product():
    """Busca productos por ID, nombre o categoría."""
    search_option = input("Buscar por: 1. ID, 2. Nombre, 3. Categoría. Seleccione una opción: ")
    
    try:
        connection = obtener_conexion()
        cursor = connection.cursor()

        if search_option == "1":
            product_id = int(input("Ingrese el ID del producto: "))
            cursor.execute("SELECT * FROM productos WHERE id = ?", (product_id,))
        elif search_option == "2":
            nombre = input("Ingrese el nombre del producto: ")
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
        elif search_option == "3":
            categoria = input("Ingrese la categoría del producto: ")
            cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
        else:
            print("Opción no válida.")
            return

        products = cursor.fetchall()
        connection.close()

        if products:
            print("\nResultados de la búsqueda:")
            print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
            print("-" * 60)
            for product in products:
                print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]} | {product[4]} | {product[5]}")
        else:
            print("No se encontraron productos que coincidan con los criterios de búsqueda.")
    except sqlite3.Error as e:
        print(f"Error al buscar productos: {e}")

def generar_low_stock_report():
    """Genera un reporte de productos con stock bajo."""
    try:
        threshold = int(input("Ingrese el umbral de stock bajo: "))
    except ValueError:
        print("Por favor, ingrese un número válido para el umbral de stock.")
        return

    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (threshold,))
        low_stock_products = cursor.fetchall()
        connection.close()

        print("\nReporte de productos con stock bajo:")
        print("ID | Nombre | Descripción | Cantidad | Precio | Categoría")
        print("-" * 60)
        for product in low_stock_products:
            print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]} | {product[4]} | {product[5]}")
    except sqlite3.Error as e:
        print(f"Error al generar el reporte de stock bajo: {e}")

def limpiar_productos_vacios():
    """Elimina productos vacíos o con campos nulos."""
    try:
        connection = obtener_conexion()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre IS NULL OR descripcion IS NULL OR categoria IS NULL OR nombre = '' OR descripcion = '' OR categoria = ''")
        productos_vacios = cursor.fetchall()

        if productos_vacios:
            print(f"Se eliminarán los siguientes productos vacíos:")
            for producto in productos_vacios:
                print(producto)
        
        cursor.execute("DELETE FROM productos WHERE nombre IS NULL OR descripcion IS NULL OR categoria IS NULL OR nombre = '' OR descripcion = '' OR categoria = ''")
        connection.commit()
        connection.close()

        print("Registros vacíos eliminados con éxito.")
    except sqlite3.Error as e:
        print(f"Error al eliminar registros vacíos: {e}")

def main():
    """Función principal para interactuar con el sistema de gestión de inventario."""
    crear_database()

    # Limpiar productos vacíos o incorrectos al iniciar el programa
    limpiar_productos_vacios()

    while True:
        print("\nGestión de Inventario")
        print("1. Agregar producto")
        print("2. Actualizar cantidad de producto")
        print("3. Eliminar producto")
        print("4. Ver productos")
        print("5. Buscar producto")
        print("6. Generar reporte de stock bajo")
        print("7. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            agregar_product()
        elif choice == "2":
            actualizar_product()
        elif choice == "3":
            eliminar_product()
        elif choice == "4":
            ver_products()
        elif choice == "5":
            buscar_product()
        elif choice == "6":
            generar_low_stock_report()
        elif choice == "7":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main()


