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


rsa_decrypt(cipher, n, d, e)
```

## Buenas prácticas

Aunque el código funciona y ha pasado por diferentes etapas de refactorización creo que aún se puede mejorar mucho, trataré de que las funciones no tengan _side effects_, simplemente devuelvan los valores y el print de tablas que sea aparte, fuera de eso, creo que está bien el código.
