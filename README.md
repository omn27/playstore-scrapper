# Buscando correos expirados

_El proyecto esta inspirado en una serie de [articulos](https://www.elladodelmal.com/2020/03/el-club-de-los-poetas-muertos-parte-1.html) de Chema Alonso en el cual muestra el riesgo que hay actualmente al instalar apps en android, ya que en muchos casos, las aplicaciones que tenemos instaladas solicitan mas permisos que los necesarios para un funcionamento normal._

# Objetivo
El objetivo es encontrar correos que esten dados de baja por inactividad en hotmail, outlook, protonmail o el que sea, pero que tengan cuenta activa en android developer. Asi, se podria registrar en outlook, hotmail o el que sea, el correo que se dio de baja y poder solicitar un restablecimiento de la contraseña en android developer.

# ¿Como el proyecto logra el objetivo?
El programa consiste en buscar en bing links de apps de playstore que tengan asociadas un correo outlook, protonmail, o el que sea, en el apartado de "contacto del programador". A medida que va obteniendo los links, el programa se encarga de obtener el correo asociado y comprobar si el mismo se encuentra expirado. Si se expirado tambien verifica si ese correo esta registrado en android developer, ya que hay casos en que el correo esta expirado pero no tiene cuenta en android developer.

# ¿Como funciona internamente el programa?
Por defecto el programa se ejecuta con al menos 5 hilos(1 hilo para el main, 2 hilos para dado un link obtener el email asociado, 1 hilo que escribe los registros en la db, y 1 hilo que se encarga de ir creando hilos por cada vez que se necesita obtener el estado de un email, activo o inactivo). El hilo del main se dedica a buscar en bing dependiendo del dork que se utilice, una vez que obtiene los links de la busqueda se fija que no exista en la db la app de playstore a la que hace referencia el link. Si la app no existe todavia en la db, el main deja ese registro en la cola llamemosla "Cola A". Hay 2 hilos esperando porque se deje un mensaje en esa "Cola A", a medida que el main deja links en esa "cola A", esos hilos se encargan de sacar los elementos de la "Cola A" y buscar en la playstore, el correo asociado a ese link. A medida que obtienen los emails asociados a cada link, los emails son depositados en otra cola, llamemosla "Cola B". Esta "Cola B" es monitoreada por otro hilo que se encarga de obtener los emails que se van depositando en la cola, y por cada email inicializa un nuevo hilo que verifica si el email esta activo o no. Dentro de este ultimo hilo, si cuando verifica el estado de email se encuentra con que esta en estado inactivo, el hilo va a llamar a otra funcion encargada de verificar si email existe en android developer. En ambos casos, exista o no en android developer, el hilo deja un objeto compuesto por nombre de la app, email, estado del email y estado del email en android developer, en otra ultima cola denominada "Cola C". Por ultimo, esta "cola C" es consumida por otro hilo encargado de insertar el registro en la base de datos

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

* Python 3.x instalado
* Python 3 PIP instalado
* Tor como servicio

### Instalación 🔧

```
% git clone https://github.com/omn27/playstore-scrapper.git
% cd playstore-scrapper
% python -m pip install -r requirements.txt
% python main.py
```

### Ejecutar

```
% python scrapper.py
```
