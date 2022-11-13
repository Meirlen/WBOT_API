

uvicorn main:app
python run_token_updater.py
python run_order_status_listener.py



# SETUP BUILD MODE 
# Prod: don't forget pull db from server
# # Bug: double call
change_build_mode(is_release = False)

# update_yandex_token_in_prod(generate_new_token())
# generate_new_token()
# generate_new_token()


# Make ngrok public api: ngrok http 5005

# digital ocean pass apA91ata!a
# Install Docker in do
# curl -fsSL https://get.docker.com -o get-docker.sh


#  git commit -m "big changes"
#  git config --global user.email "miko_982@mail.ru"
#  git config --global user.name "Meirlen"
#  git rm -r --cached .


# git remote add origin https://github.com/Meirlen/WBOT_API.git
# git remote set-url origin https://github.com/Meirlen/WBOT_API.git

# git branch -M main
# git push -u origin main

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

#Delete all containers
# docker rm -f $(docker ps -aq)

# git rm -r --cached .
# git add .


# Rasa 
# rasa run --enable-api
# rasa run actions
# rasa shell --debug
