# SETUP BUILD MODE 
# PROD
# File: database.py
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:admin@postgres/alem'
# index.html
#  const base_url = "http://165.22.13.172:8000"



# DEV
# File: database.py
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:admin@localhost/alem'
# index.html
#  const base_url = "https://02qyk.localtonet.com"










# Prod: don't forget pull db from server
# # Bug: double call

# update_yandex_token_in_prod(generate_new_token())
# generate_new_token()
# generate_new_token()


# Make ngrok public api: ngrok http 5005

# digital ocean pass apA91ata!a
# Install Docker in do
# curl -fsSL https://get.docker.com -o get-docker.sh


#  git commit -m "add order status listener"
#  git config --global user.semail "miko_982@mail.ru"
#  git config --global user.name "Meirlen"
#  git rm -r --cached .
# git push origin master

# git remote add origin https://github.com/Meirlen/WBOT_API.git
# git remote set-url origin https://github.com/Meirlen/WBOT_API.git

# git branch -M main

# git push origin master


# cmd
# rm -rf directory_name
# docker container ls
# docker rm 5c7a2a2632b8
# docker stop 5c7a2a2632b8
# docker-compose up

# Delete all local images
# docker rmi -f $(docker images -aq) 

# Для запуска докер образа docker-compose up
# Для обновления:
# docker-compose up --force-recreate --build -d
# docker image prune -f
# See logs specify service
# docker-compose logs api

# Stop all containers
# docker kill $(docker ps -q)

# Delete all containers
# docker rm -f $(docker ps -aq)

# Clear db cash
# docker-compose down --volumes

# Db cred:
# db name = alem
# db user = postgres
# db pass = admin
# 

# git rm -r --cached .
# git add .

docker ps
docker container inspect b66fd9b06429

cd WBOT_API
git fetch
git pull
docker-compose up --force-recreate --build -d

git add .
git commit -m "setup mobile api"
git push origin master
# Добрый день, так как продукт новый были перебои на стороне сервера, сейчас бот работает в сатбильном режиме.Приносим извинения за доставленные неудобства.