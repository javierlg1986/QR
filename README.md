# QR
E007 WebApp QR

2.1 Estudio de alternativas:

Se estudiarán detalladamente los distintos flujos de trabajo. Al menos, se tendrán en cuenta las siguientes actividades:
•	Creación de etiquetas
•	Asignación de etiquetas a elementos físicos.
•	Captura de etiqueta para visualizar datos vinculados.
Para la creación de etiquetas, se buscarán los flujos óptimos para:
•	Creación de etiquetas en batch, en oficina, minimizando el tiempo total del proceso.
•	Creación de etiquetas individualmente en campo, evitando desplazamientos a oficina para realizar un pequeño número de etiquetas.
Para todos los puntos se considerarán las etiquetas NFC de plástico y los códigos QR impresos.
Se ponderará la idoneidad de un flujo de trabajo atendiendo a las siguientes condiciones:
•	Baja intervención humana y elevada automatización.
•	Baja probabilidad de errores.
•	Baja coste económico.
•	Que no requiera equipos específicos.

Se entregará un documento de estudio de alternativas que incluirá los siguientes apartados:
•	Estudio flujo de trabajo para creación de etiquetas
•	Estudio flujo de trabajo para asignación de etiquetas a elementos físicos
•	Estudio flujo de trabajo para captura de etiquetas y visualización de datos
•	Conclusiones

2.2	Desarrollo aplicación web

Se desarrollará un módulo para creación, asignación y captura de etiquetas. En esta fase inicial de avance del proyecto «Ames Digital Water», se propone que el módulo funcione como una aplicación web independiente. 
Sin embargo, debe preverse su integración como una parte de la futura aplicación de Operación, Mantenimiento y Conservación (OM&C) según se recoge en el proyecto.
La creación de etiquetas debe prever la impresión masiva en hojas de pegatinas. Para ello, la aplicación permitirá configurar los tamaños de impresión para las medidas de los distintos formatos existentes en el mercado.
Para la asignación de etiquetas, se prevé al menos:
•	Localización geográfica del elemento físico en mapa.
•	Vinculación de una fotografía.
•	Datos básicos, descripción, comentarios, etc.
•	Vinculación de documento PDF.
•	Filtrado y búsqueda de elementos en mapa.

Respecto a la arquitectura y componentes, se tendrán en cuenta las siguientes consideraciones:
•	Se utilizarán lenguajes considerados estándares de la industria.
•	Se utilizará software libre, evitando cargar al Concello con el pago de licencias.
•	Se minimizará en la medida de lo posible las librerías de terceros garantizando en todo caso la disponibilidad en el largo plazo.
•	Se realizarán scripts de instalación y población de la base de datos de modo que el despliegue requiera la mínima intervención.
•	Se entregará el código fuente con licencia MIT.

La aplicación implementará las conclusiones del estudio de alternativas. Como mínimo, tendrá las siguientes páginas:
•	Inicio o menú para escoger las alternativas.
•	Creación de etiquetas, individuales y por lotes.
•	Asignación de etiqueta utilizando un visor GIS.
•	Visualización de datos básicos.
•	Actualización de datos básicos, subir fotos y documentos PDF.

Tras la validación de la versión definitiva, se realizará la entrega de:
•	Código fuente con los comentarios utilizados durante el desarrollo.
•	Documentación. Se entregará un único documento con los siguientes apartados o anexos:
o	Guía de desarrollo
o	Guía de instalación
o	Guía de pruebas de funcionamiento
o	Guía de pruebas de seguridad

2.3	Pruebas de implantación

Como fase inicial de implantación del sistema de identificación, se crearán varias etiquetas QR y NFC para realizar las pruebas pertinentes y demostrar el buen funcionamiento del sistema.
Se designarán tres (3) jornadas de acompañamiento al personal designado por el Concello de Ames para la asignación de elementos a las tarjetas generadas: equipos de ETAP, equipos de EDAR y elementos de red.

Se pondrá a disposición del Concello de Ames un dispositivo de lectura/escritura de tarjetas NFC, así como las etiquetas QR y NFC utilizados para las pruebas.
Se generarán actas de las jornadas de acompañamiento, incluyendo fecha, hora, personal implicado, etiquetas generadas, etiquetas asignadas, datos actualizados, incidencias detectadas, etc. 

2.4	Formación
Se preparará la documentación de uso de la aplicación y explicación de los procesos de creación, asignación y captura de etiquetas al personal designado por el Concello de Ames.
Una vez realizada la actividad formativa, se acompañará al personal designado por el Concello a campo, para comprobar que la implementación sea la prevista.

La documentación presentada en la jornada de divulgación quedará subida en la aplicación web.