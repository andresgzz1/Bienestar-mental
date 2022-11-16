# Bienestar-mental



 1) Crear entorno virtual con conda
 
    - descargar e instalar miniconda python 3.7    ->   https://docs.conda.io/en/latest/miniconda.html

    - Crear entorno virtual desde cmd con comando: "conda create -n nombre_entorno python==3.7"
  
    - Activar entorno virtual con comando: conda activate nombre_entorno

 2) Configurar SQL Server
 
    - Para configurar SQL server en Django necesitamos del siguiente Driver: 'ODBC Driver 13 for SQL Server' instalado en la computadora
    -> https://www.microsoft.com/es-es/download/details.aspx?id=50420
 
    - Además de instalar el motor de SQL Server en la computadora.
    -> https://www.microsoft.com/es-es/sql-server/sql-server-downloads
    
    - Se recomienda manipular bd SQL Server con programa SQL Server studio 18
    

#######
ES IMPORTANTE REALIZAR EL PIP INSTALL -R REQUIREMENTES.TXT
#######  
Va a detectar cambios remotos en las ramas de github (no significa que obtenga los cambios)
git fetch

Me va a mover a la rama main 
git checkout main

Va actualizar la rama local con lo ultimo de la main
git pull

Nos devolvemos a la rama en la que estamos trabajando
git checkout nombre_rama

Va hacer la fusion de ramas 
git merge origin main


git push