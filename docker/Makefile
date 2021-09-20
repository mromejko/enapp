COMPOSE_PROJECT_NAME:="$(shell cat name.conf)"
export COMPOSE_PROJECT_NAME

start:
	rm -rf ./api/requirements.txt
	cp ./../requirements.txt ./api/requirements.txt
	docker-compose --file docker-compose.yml --env-file ./../.env up -d

stop:
	docker-compose -f docker-compose.yml stop
	rm -rf ./api/requirements.txt

destroy:
	make stop
	docker-compose -f docker-compose.yml rm -f

logs:
	docker-compose logs -f

seed:
	make clean
	docker exec -it enapp_api bash -c 'flask db migrate && flask db upgrade && flask seeder'

clean:
	rm -rf ./../migrations/versions/*