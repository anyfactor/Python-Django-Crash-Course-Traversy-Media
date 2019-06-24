# Python Django Crash Course Traversy Media

[Link to the video](https://www.youtube.com/watch?v=D6esTdOLXh4)


### Warning This tutorial is largely deprecated as django 2 introduces a lot of changes


Django is high level framework, Flask is low level web framework.

Django forces you to do things in its own structured way.

MVC(Model View Controller) design pattern, separates parts of the app. Django is influenced by this.

MTV(Model Template View) Model is interaction with data, Template is for presentation and View is the logic layer for displaying appropriate template.

Each project has separate apps (Blog app, Store app)

We will be installing XAMPP for MySQL and phpmyadmin(?)

## Setting up VENV (Virtual Environment)

Install Virtual Environment Wrapper

```pip install virtualenvwrapper-win```

To create a virtual environment in the project directory

```mkvirtualenv py1```

In *py1* our environment files go. We don't work here.

If you have multiple environments and you want to switch to one,

```workon py1```

## Initiating django

After installing, to initiate django

```django-admin startproject *projectname*```

Now, cd into the django project directory(the name is "djangoproject") that has been created.

Inside the the directory we have manage.py and another folder with the same name.

Manage.py is the CLI client.

Remember to remove the encryption key from settings.py under the djangoproject directory. Before deploying also set debuge to false. Any application you create add to the installed_apps list.

Running the webserver

```python manage.py runserver```

The site will be available at localhost:8000

Migrations do things to the database.

## Installing MySQL database

To install mysql client for python

```pip install mysqlclient```

But if that does not "magically" works like in the video. Use the precompiled binary.

Start XAMP control. Start MySQL and APACHE. In the browser, go to ```localhost/phpmyadmin```. Then select databases from the menu. And create a database called djangoroject. Creating tables and everything will be done through migrations.

Now, go to the settings.py comment the old database dictionary out. Input this one -

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoproject',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': ''
    }
}
```

Give a empty password unlike what brad does.

In the CLI now run, ```python manage.py migrate```

Now, restart the server. Go to **localhost:8000/admin**, this our admin/backend interface.

We can create a superuser to login in the admin dashboard.

Stop server. IN CLI ```python manage.py createsuperuser --username=anyfactor --email=anyfactor@anyfactor.xyz```

Then give a password, which is at least 8 characters. Password for this app is anyfactordjango.

Then rerun the server, go to admin and login.

Groups is user groups, and add users. 

We are now creating a post app (blog website)

```python manage.py startapp post``` post is the name of our app. This creates a new directory for our post app. views.py is for controlling, load templates and a lot of things.

 Go to core settings file, installed apps list and put in the name of the app ```'post'```

Go to core urls.py file and in the urlpatterns list add, ```path('post/', include('post.urls'))``` and in the file add to the django.urls import statement add include.

Create a urls.py file in the post directory, and give the following code

```python
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index')
]
```

the url is going to look in the views file for index.

Now go to views.py on the same directory to create our index function.

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello")
```

The httpresponse just shows the text to show everything is working.

main url files see the url, then passes it on to the second url which directs it to the views file.

Now, remove the httpresoponse statement and type ```return render(request,  'post/index.html')``` which renders template. It will automatically look for a folder called templates then refer to the path provided.

Inside the post folder we are going to create directory called templates, and inside that create another folder name post.

Now we are going to layout. That will hold our header and footer for all pages.

In the same templates/post folder create **layout.html**

Brad, uses materialize css framework so, use the cdn link. Now we put in our header - footer html. And for the content we will use "jinja templating". We will put in the code where we want to show our content -

```
{% block content %}
{% endblock %}
```

Now, head back to the index.html file to extend the jinja templating.

```
{% extends 'post/layout.html' %}
```

Now whatever we want to output in the block contents of layout html, we have wrap that with that block content thing, so

```
{% block content %}
<h1> Hey, this is text you will input in the layout, my dude </h1>
{% endblock %}
```

Now, we have the templating system figured out.

We can also include dynamic data is our template.

In views.py in the render method add a parameter of dictionary. similar to this

```{'title': 'latest post'}```

and we get back to index.html and can add the title key to the dictionary anywhere within double square brackets -

```<h2>{{title}}</h2>```

The key will refer to the value in the dictionary.

So, view.py > index.html > layout html >> index.html + layout html.

So, this how we create our blog post. We will create model, from the model the data goes to the views file, and from views the data is showed.

Now in the post folder's models.py we go.

so create a class and classify the information for the blog post.

```python
from django.db import models
from datetime import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(default=datetime.now, blank=True)
```

Charfield contains limited characters compared to textfield.

Now, CLI stop server. Now, we will create a migration based on this model, that hold the information we have provided in the models.py in the database in a table.

In CLI ```python manage.py makemigrations post```

This will created the file but not the database table.

Now, to create the database table in the CLI ```python manage.py migrate```

Check our database at phpmyadmin and there it is.

Now, we are going to add an admin link in the header so, let's modify layout.html with -

```<a href="/admin" class='center-align'>Admin Login</a>```

let's login to the admin panel, and as you can see there is no significant changes there.

So, you will not register your model in post folder's admin.py file. So, add -

```python
from .models import Post

admin.site.register(Post)
```

So, it access the models.py file in the same directory then gets the post class.

So in the admin panel you will see "posts" but everywhere we have "post" that is because takes it on itself to add that "s"

So, if you want to fix that. Go to the models.py (of the post directory, duh) than within the class post add another class. This is the following code.

```python
    class Meta:
        verbose_name_plural = "Posts"
```

Now let's add our first post to the blog from the admin panel.


After saving you can see the post is saved as "post object". You want to have the title name as the post name.

So, you get back to the models.py again under the post class add a function.

```python
    def __str__(self):
        return self.title
```

So, we want to have the homepage go the blog page. Rather than making another app, we can do it by going to the main urls.py (in the djangoproject directory)

and in the urlpatterns list, add

```python
path('', include('post.urls'))
```

Now, lets go to the post folder's view.py where we are going to bring the post from the model.

import the post class from the models. Than in the index function add  

```python
posts = post.objects.all()[:10]

context = {
    'title': "Latest Posts",
    'posts': posts
}

return render(request, 'post/index.html', context)
```

This will show 10 post. In this tutorial he skips pagination. We will also remove the previous dictionary in the return statement.

The views gets the posts from the model. 

Now, to modify the index.html file to show all the posts from the views file. Add this code between the block contents

```
<ul class="collection">
    {% for i in posts %}
        <li class="collection-item">{{i.title}}</li>
    {% endfor %}
</ul>
```
For easy remembering multiline "programming" you have to start and end, for single line variable access double square brackets.

These just provides you with a list of titles. We want something "clickable" to get to the body of the blog posts itself.

```
<li class="collection-item"><a href="post/details/{{i.id}}">{{i.title}}</a></li>
```
Now, go to the post folder's urls.py and on the urlspattern list add

```
path('details/<int:id>/', views.details, name='details')
```

Now go to the views file (in the post directory) create another function

```python
def details(request, id):
    post = Post.objects.get(id=id)

    context = {
        'post' = post
    }

    return render(request, 'post/details.html', context)
```

Now we are going to create the details.html on the templates/post

```
{% extends 'post/layout.html' %}

{% block content %}
<h3> Hey, this is the text you will input in the layout, my dude </h3>
<h5>{{post.title}}</h5>

<div class="card">
    <div class="card-content">
        {{post.body}}
    </div>
    <div class="card-action">
        {{post.created_at}}
    </div>
</div>
<a href="/" class="btn">Go back</a>
{% endblock %}
```

