# python-exercise

Python exercise using Docker, MongoDB and Pandas

## Pasos para probar la solución:

1. Clonar el repositorio usando `git clone https://github.com/andresbuenob/python-exercise.git`
2. Abrir la carpeta python-exercise y correr `docker-compose build`
3. Una vez terminado el proceso anterior, levantar los servicios de la aplicación usando `docker-compose up`
4. En una terminal nueva, ejecutar la terminal del contenedor con el comando `docker exec -it python-exercise_app_1 sh`
5. En la terminal del contenedor correr el main de la aplicación con `python main.py`
6. La aplicación iniciará y realizará los procesos principales solicitados en la prueba, una vez estos estén finalizados, la aplicación quedará pausada esperando un _input_. Se le solicitará al usuario que se redireccione a la página de autenticación de Github usando la url generada de forma automática por la aplicación. **Este debe autenticarse con su usuario y contraseña de Github.**
7. Después de la autenticación, será redireccionado a otra página. **El usuario debe copiar la url completa de la página a la cual fue redireccionado, y pegarla en la terminal**. La aplicación estará esperando el ingreso de la url para continuar. Si la autenticación es exitosa, la información de la tabla y resultados del proceso serán mostrados en la terminal.
