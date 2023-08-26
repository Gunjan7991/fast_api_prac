#!/bin/bash
docker-compose -f docker-compose-production.yml down
docker ps -aq | xargs docker stop | xargs docker rm 
docker rmi postgres:15.4-alpine3.18
docker rmi fast_api_prac_fastapi