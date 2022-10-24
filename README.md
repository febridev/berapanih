# Scrap Shell Oil Price Indonesia ![](https://img.shields.io/badge/stats-experimental-orange)
### Source
[https://www.shell.co.id/in_id/pengendara-bermotor/bahan-bakar-shell/how-shell-price-fuel.html](https://www.shell.co.id/in_id/pengendara-bermotor/bahan-bakar-shell/how-shell-price-fuel.html)

## Installation
### Setup Docker Image
```bash
## docker image build -t image:version .
## example
docker image build -t webscrap:1.0 .
```
### Setup Bash Environment
For a little bit security, we will export all credential for PostgreSQL database on bash environment 
```bash
export user="username_database"
export passdb="password_database"
export host="ip_for_database"
export port="port_for_database"
export dbname="database_name"
export tblname="table_name"
```

### Run Docker Image
Running with detach mode 
```bash
docker run --name container_name -d image:version \
--user=$user \
--passdb=$passdb \
--host=$host \
--port=$port \
--dbname=$dbname \
--tblname=$tblname
```
