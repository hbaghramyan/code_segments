## Especificación de la aplicación para compartir código

### Resumen
Crea un servicio de API utilizando prácticas JSON y RESTful, destinado a la creación, difusión y gestión de segmentos de código. Esta API debe cumplir con la siguiente lista de directrices:

### Características clave de un segmento de código
**2.1** La porción de código debe incluir el texto del código y su lenguaje de programación asociado, con las opciones de Java, PHP, Python, JavaScript o texto plano. También existe la oportunidad de proporcionar un título y el nombre del autor, pero estos no son obligatorios.

### Marcado de tiempo
**2.2** Se debe implementar un registro automático de tiempo para rastrear el inicio de cada segmento de código.

### Puntos finales de la API
**2.3** La API debe mantener un único punto final que permita las siguientes capacidades:

- **2.3.1** Mostrar todos los segmentos de código. Los usuarios de la API pueden implementar filtros basados en la fecha de creación o el lenguaje y también pueden ejecutar búsquedas de palabras clave dentro del título o el contenido. Es esencial paginar los resultados, con cada página predeterminada a 20 entradas y el límite superior limitado a 100.
- **2.3.2** Introducción de nuevos segmentos con los datos mencionados anteriormente. La respuesta debe incluir el nuevo segmento de código en formato JSON en el cuerpo y la URL única en los encabezados. También es necesario incluir un secreto confidencial en la respuesta para futuras eliminaciones del segmento.
- **2.3.3** Recuperar un segmento de código específico utilizando su ID única.
- **2.3.4** Eliminar un segmento de código específico utilizando su ID única y el secreto correspondiente.
- **2.3.5** Cualquier actualización de un segmento de código debe resultar en un nuevo segmento con una nueva ID y secreto, en lugar de alterar el segmento existente.

### Accesibilidad
**2.4** La API debe proporcionar acceso abierto, permitiendo que todas las acciones sean realizadas por cualquiera.

### Privacidad
**2.5** La API también debe proporcionar una provisión para segmentos de código privados. Dichos segmentos deben omitirse de cualquier resultado basado en listas, haciéndolos solo accesibles a través de su URL o ID única.
