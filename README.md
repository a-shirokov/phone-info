# Phone number info

## Basic Commands

### Running app

```bash
docker-compose -f local.yml -f local.override.yml up -d django celery-worker celery-beat
```

### Refresh phone numbering data

```bash
docker-compose -f local.yml -f local.override.yml run django python manage.py refreshphonenumbering
```

## API

### Schemes
```
GET /api/phones/:phone_number 
```

### Tests

```bash
http -v GET http://localhost:8000/api/phones/79173453223
```
or
```bash
curl -v http://localhost:8000/api/phones/79173453223
```
