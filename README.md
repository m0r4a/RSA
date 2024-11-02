Esta mini documentación es temporal, ya quiero entregar el proyecto.

## Funciones principales

### rsa_encrypt

#### Descripción

Esta función toma un string y un valor en bits para encriptar el string, te devuelve:

> texto_cifrado, modulo, llave_privada, llave_pública

#### Ejemplo de uso

```python
from functions.rsa_encrypt import rsa_encrypt


texto_cifrado, modulo, llave_privada, llave_publica = rsa_encrypt("Hello, Bison!", 512)
```

> [!NOTE]
> Al parecer que el valor de la llave pública sea "65537" es como un estandar o algo así, entonces dejé que la llave pública sea siempre ese valor.

### rsa_decrypt

#### Descripción

Esta función toma el número correspondiente al mensaje encriptado, el módulo, la llave privada y la llave pública y retorna el string desencriptado. 

#### Ejemplo de uso

```python
from functions.rsa_decrypt import rsa_decrypt


rsa_decrypt(texto_cifrado, modulo, llave_privada, llave_publca)
```

## full_test.py

En este archivo contiene una pequeña prueba pre-escrita para de como se ve encriptar y desencriptar algo

## To-Do

- Mejorar las funciones para que no tengan side-effects
- Mejorar el manejo del output de las llaves
