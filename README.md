# Tag history

Per eseguire il dump del database aggiungere nella root del progetto il file `.pgpass_dump` contenente:

```bash
127.0.0.1:5432:ludovicopratesi_db:ludovicopratesi_usr:LA_PASSWORD
```

Poi dare al file i seguenti permessi

```bash
chmod 600 /srv/apps/ludovicopratesi/.pgpass_dump
```

Se si vuole lanciare in cron il comando eseguire:

```bash
DB_SYSTEM_USER='' DB_PASSFILE='/srv/apps/ludovicopratesi/.pgpass_dump' sh runner.sh
```

## Production env

Le credenziali di produzione non devono stare nel repository. Copiare
`etc/env/ludovicopratesi.env.example` in `/srv/apps/ludovicopratesi/.env.production`,
compilare i valori reali e dare permessi stretti:

```bash
cp etc/env/ludovicopratesi.env.example /srv/apps/ludovicopratesi/.env.production
chmod 600 /srv/apps/ludovicopratesi/.env.production
```

Per eseguire i comandi Django in produzione:

```bash
set -a
. /srv/apps/ludovicopratesi/.env.production
set +a
/srv/venvs/ludovicopratesi/bin/python manage.py migrate --settings=www.settings.prod --noinput
/srv/venvs/ludovicopratesi/bin/python manage.py collectstatic --settings=www.settings.prod --noinput
```

Deploy rapido in produzione:

```bash
chmod +x /srv/apps/ludovicopratesi/bin/deploy_prod.sh
/srv/apps/ludovicopratesi/bin/deploy_prod.sh
```

Lo script esegue `git pull --ff-only`, carica `.env.production`, lancia
`collectstatic` con `www.settings.prod` e infine fa `supervisorctl reload`.
Se `deploy` non ha accesso diretto al socket di Supervisor, lo script riprova
automaticamente con `sudo supervisorctl`.
Se vuoi ricaricare solo il programma applicativo invece di tutto supervisord:

```bash
SUPERVISOR_ACTION=restart /srv/apps/ludovicopratesi/bin/deploy_prod.sh
```





## 1.0.0

2014.03.12: First production deploy of website linked at http://ludovicopratesi.it.

Customer asks some reviews of code that will be deployed in a next tag.
