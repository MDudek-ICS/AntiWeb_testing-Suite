# AntiWeb: Testing Suite

## Introducción 
Una vulnerabilidad ha sido encontrada en aplicaciones web usadas en ics/ot que corren sobre servidores Anti-Web (hasta 3.8.7).
La vulnerabilidades que se han identificado  afectan a varios fabricantes de renombre en la industria de la automatización de procesos industriales y telecomunicaciones. Estos devices ya cuentan con dos viejos CVEs (CVE-2010-4730 & CVE-2010-473) a lo que luego de reportar consiguió un tercero CVE (2017-9097) e inmediatamente el vendor lanzó un parche. En inmediatamente siguieron otros. 


Para tener una referencia aproximada del grado de exposición con la que cuentan esto dispositivos nos valemos de los host que se encuentran indexados en Shodan, siendo estos un poco mayor de 800 devices potencialmente vulnerables. 

Con respecto al LFI que nuestra tool procura de explotar, hoy los distintos vendors afectados ya cuentan con sus respectivos parche oficiales que contrarresta la vulnerabilidad. Por lo que de alguna forma el intentar explotar el fallos viene a corroborar el compromiso de los operadores y responsables de estas tecnologías, respondiendo a una pregunta fundamental: "Se habrán instalado los parches correspondientes?" 

# Las tools son 3:
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


# Tool: "Anti-web" 
### Usage:

 	usr@pwn:~$ python anti-web-v1.py --help
	usage: anti-web.py [-h] [-v] --host HOST [--port PORT] [--file LFI]

	[+] CVE: CVE-2017-9097

	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --version  show program's version number and exit
	  --host HOST    host
	  --port PORT    set port (default = 80)
	  --file LFI     Test LFI

	[+] Demo: anti-web.py --host 192.168.1.100 --port 80



# Tool: "Seek And Destroy"
### Usage:

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




# Tool "Remote Command Execution": 
### Usage:

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

 
