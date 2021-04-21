# foodgram-project
# Run
1. [Install Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/) (if you have Linux).
2. Clone repository https://github.com/ilyukevich/foodgram-project.git
3. Create an ENV file in the root of the project and fill it
4. Open foodgram-project folder and run ```sudo docker-compose up -d```
5. Go inside container ```sudo docker exec -it foodgram-project_web_1 bash```
6. Run commands:
   
   ```python manage.py collectstatic```
   
   ```python manage.py migrate```
   
   ```python manage.py load_ingredients```
   
   ```python manage.py createsuperuser``` - fill credential for new admin user.
   
   ```python manage.py runserver```
4. Go to http://localhost:8080/ or http://localhost:8080/admin/ for an admin panel.

# Functionality
* Full user authentication.
* Create/edit/delete new recipe.
* Filter by breakfast/lunch/dinner.  
* Choose from a bunch of ingredients.
* Add to favourites.
* Favourites page.
* Follow another authors.
* Add to shopping list.
* Download shopping list.

# What I used
* Python
* Django
* Django REST
* Docker
