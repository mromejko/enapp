# EnApp

### Docker

Jak uruchomić:

- na samym początku w głownym katalogu projektu wykonujemy:

```
cp .env.local .env
```
- w katalogu docker wykonujemy:

```
make start
```
Zbuduje obrazy i uruchomi kontenery.

- musimy chwilę poczekać aż postgres będzie up and running. Jeżeli zrobimy to wcześniej niż postgres się podniensie zobaczymy brzydki error. Następnie wykonujemy:

```
make seed
```

Uzupełni bazę danych przykładowymi danymi.

Jak wyświetlić logi ze wszystkich kontenerów:

```
make logs
```

---

### Aplikacja

Aplikacja będzie dostępna pod adresem:
```
http://0.0.0.0:8080/v1
```
Swagger (opis API) obecny jest tutaj:
```
http://0.0.0.0:8080/v1/docs
```

### Baza danych

W bazie danych znajduje się jeden klient (ID = 1). Posiada 3 stacje energetyczne. Każda stacja ma "logi" z informacją ile energi zostało pobrane danego dnia. W bazie jest kilka wpisów dla każdej stacji.

### Informacja o zleceniu wykonania raportu (RabbitMQ)

Do rabbit'a idzie wiadomość:

```
{"request": "client.report", "client_id": <CLIENT_ID>, "report_id": <REPORT_ID>}
```

W bazie danych zostaje dodana informacja o raporcie. Raport ma status "In progress". Kolumna przechowująca dane raportu jest pusta.
