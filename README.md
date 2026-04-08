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





## 1.0.0

2014.03.12: First production deploy of website linked at http://ludovicopratesi.it.

Customer asks some reviews of code that will be deployed in a next tag.
