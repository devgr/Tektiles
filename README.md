#Textile Fabric Consultants Inc.
This is the code for the in-development website for Textile Fabric Consultants Inc.

Built with the Django framework, there are several applications that make up the site:

1. Blog
2. Textile Companion app
3. Webstore
4. Main site (home page, about us)

##How to load the project
###Components neeeded

####GitHub

You are reading this documentation, so you've found GitHub. If Git / GitHub / version control in general is unfamiliar to you, [here][id-rw]'s a good guide to help you get started (*readwrite.com*).
[id-rw]: http://readwrite.com/2013/09/30/understanding-github-a-journey-for-beginners-part-1 "Understanding GitHub..."
GitHub can be used via the command line, through the Windows / Mac client, and through the browser. Here are some tips from my experience:

- Always sync with github before editing code or running the website.
- After changing code, commit and push your changes. If you were just running the site, you can discard any binary files that changed. In theory, the .gitignore file should take care of this, but that has not worked consistently with this project. Don't add a file you don't want tracked!
- The database is contained in `userdb.sqlite3`. Since the database is synced with github like all of the other files, it's important that two people aren't modifying the database at the same time, otherwise git will git confused about the versions.

####Python
<https://www.python.org>

This Django project is tested with Python 2.7.6 or 2.7.7. It may be compatible with 2.6 as well (and there is now Django for Python 3) but this code is written in Python 2.7. So, install Python if not already installed and verify that it is working properly.

####Pip
Pip is a package manager for Python. It can be used to install Django and much of what follows.

<https://pip.pypa.io/en/latest/installing.html>

*If you are using Windows, this may be easier:*

<https://sites.google.com/site/pydatalog/python/pip-for-windows>

####Django
<https://docs.djangoproject.com/en/1.6/>

This project uses version 1.6, the current version when the project was started. It may be worth considering moving to version 1.7 because it includes some helpful database migration tools. *See Issue 18*

Instalation instructions:

Install django with `pip install Django`. If on a unix system, you may need to put `sudo` before pip commands.

<https://docs.djangoproject.com/en/1.6/topics/install/#installing-official-release>

As discussed in the docs, you can install everything inside of a python virtualenv. I didn't, but I think that would be a good idea. That would make the project much more portable. Actually, you could build a virtualenv with everything installed, then just have that on git so that everyone has the same environment.

_Recomendation:_ I found it was very helpful to work through the bit Django tutorial (especially parts 1 through 4) that starts here:

<https://docs.djangoproject.com/en/1.6/intro/tutorial01/>

It takes about a full day to do, but it will give you the needed background to dive into this project.

#####Plugins
The usefulness of Django really comes from all of its plugins. Or maybe all of its plugins just provide basic functionality that you need to make a website work. Regardless, there's a bunch to install and this may not be a complete list. When you try to run the server, you'll get a sort-of-meaningful error message if you are missing a plugin. Some of these aren't used currently but might be useful. To install each of these, do `pip install` name of the plugin. Most of these will have their documentation at [readthedocs][id-rtd].

[id-rtd]: https://readthedocs.org/ "Read them."

- django-bootstrap-toolkit
	- Bootstrap is the frontend framework for this site, which works in with Django templates through this plugin.
	
- django-admin-bootstrapped
	- Makes the admin pages look really nice!
	
- django-endless-pagination
	- Really great tool for splitting con tent up over multiple pages or use lazy loading and infinite scrolling. Not sure if anything on the site is using it right now, but it is worth looking into since it makes a typically tricky task very simple.
	
- django-imagekit
	- provides the images resizing and cropping for dynamically adding companion app items and store items.
	- http://django-imagekit.readthedocs.org/en/latest/index.html
	
- django-crispy-forms
	- Used for the forms for login / account info.
	- http://django-crispy-forms.readthedocs.org/en/latest/genindex.html
	
- django-embed-video
	- Not used. The idea was for embeding videos for the companion app, but youtube works best for that.
	
- django-annoying
	- Cleans up some "annoying" things in the django framework. https://github.com/skorokithakis/django-annoying
	
- django-jsonview
	- Basically lets django work with json objects similarly to javascript.
	- https://github.com/jsocol/django-jsonview
	
- Pillow
	- A derivation of PIL, the python imaging library. There's a whole bunch of versions out there, but this one should work.
	- http://pillow.readthedocs.org/en/latest/installation.html
	
- haystack
	- special installation:
	<pre><code>pip install -e git+https://github.com/toastdriven/django-haystack.git@master#egg=django-haystack</pre></code>
	- Find a needle in a haystack. Provides search for Elasticsearch
	
- pyelasticsearch
	- install the plugin, but there are other steps involved. See the next section.

- pytz
	- Time zones. Date and times are magically localized.
	
- requests
	- Fixes the problems with Python's built in HTTP
	
		<http://docs.python-requests.org/en/latest/>

####Elastic Search
<http://www.elasticsearch.org>

This provides the search functionality on different parts of the site. It's really powerful, and could be used for more (blog searching, description searching on the companion app). Gerenally for search, you would just make database queries (I actually think that would be simpler for the webstore). Elasticsearch however makes it possible to search large amounts of text.
In addition to the django plugin, you also need to have a standalone program installed on your computer, or the server when it is deployed. This program powers the search, so if you are running the site and want to use the search features, you will also need to run the elasticsearch program. Also, in order for image upload from the admin pages to work, elasticsearch *must* be running.
Download the client for your system at:

<http://www.elasticsearch.org/overview/elkdownloads/>

Or use one of the following methods:

- OS X:
	`brew install elasticsearch` *see http://brew.sh*

- Ubuntu & other Debian variants:
	`apt-get install elasticsearch`
	also, see: <http://www.elasticsearch.org/guide/en/elasticsearch/reference/1.x/setup-repositories.html>

- Windows:
	`.\bin\elasticsearch`

###### Next, run:
<pre><code>elasticsearch -D es.config="path to YAML config"</code></pre>

###### Example:
elasticsearch -D es.config=/usr/local/Cellar/elasticsearch/0.90.0/config/elasticsearch.yml

##### Testing on localhost
You will need to make a simple addition to the elasticsearch.yml file to test on localhost. Navigate to the elasticsearch.yml file (i.e. /usr/local/etc.../elasticsearch.yml) and add the following to the bottom of the file.

    discovery.zen.ping.multicast.enabled: false
    discovery.zen.ping.unicast.hosts: ["127.0.0.1"]
    cluster:
        name: #name it whatever you would like
    network:
        host: 127.0.0.1
    path:
        logs: /usr/local/var/log
        data: /usr/local/var/data
        
Credit: http://django-haystack.readthedocs.org/en/latest/installing_search_engines.html

####PHP / Apache
This is a Django application, so what's this about PHP??
In order to calculate shipping for the webstore, you have to get the prices from the shipping companies' api, which is PHP for UPS. FedEx and USPS also have PHP APIs, but there are some other options as well. This piece of the project is not fully implemented, but see the UPS_Calculator section for more information.
- Install an Apache server and set up PHP. Lots of different ways to do this!
- MAMP is simple for Mac, WampServer is simple for Windows

####Bootstrap
Bootstrap is the magical front-end framework that makes the site look pretty, format correctly on all browsers, and respond to different browser sizes so the site works great on mobile, tablet, and desktop. No additional setup is needed; it's all in the project already.
Learn *everything* here:
http://getbootstrap.com/

####Stripe
Payments are (or would be) handled by Stripe https://stripe.com/
It's not very tightly integrated at this point, but we made this choice mainly for security and ease of use reasons.

####Javascript, Jquery, and AJAX
The client side dynamic parts of the site are implemented with Javascript (along with some cool CSS3). Most of that comes from bootstrap.js, such as the modals (panels that popup with content). Some of it is custom javascript though, and it is not very organized. Basically, when we realized we needed to do something client side, it got thrown into javascript in with the html templates. For example, the client side code that handles the [incomplete] shopping cart is mixed in with the webstore template. I think it would be helpful to make that into own javascript file.

In order to give the site a more fluid feeling, each app only has a couple pages and very few refreshes happen. Most of the data is loaded dynamically with AJAX. For example, clicking on the details about a store item does an AJAX Get call to load the additional information - that way the information is loaded into the same page rather than needing to go to a new page just to see details about an item. Another example is updating your account information. When you press save, that does an AJAX Post to save the new information to the database.

Jquery (the javascript library) is used for making the AJAX calls and is also used in some other places since it makes many common javascript tasks simple and easy. Jquery is being loaded from the Google CDN; that tends to be helpful for page load times. Learn more at http://jquery.com/

##Running the project

Assuming everything is all set up as discussed above, there is a good chance that you will be able to start up the site using the development webserver that django provides. For deployment, you'll run Django off of an apache webserver most likely as discussed here https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/

####Steps to load the site:

0. Pull from GitHub to be sure you have the latest version.
1. Start up your php server if working with the shipping calculator.
2. Start the elastic search process if wanting to search or are adding things to the database through the admin pages.
3. Navigate to the main directory for the project with the command line and run `python manage.py runserver`
4. In the browser, access the site at `127.0.0.1:8000/'
5. Access the admin pages at `127.0.0.1:8000/admin` - you can log in with "admin" and "password". *I recommend changing these before deployment.*

##Database
###Background
Python has built in support for sqlite, and that is the default dbms for django. Because of the abstractions that django's data access layer provides, it really makes little difference what database system you want to use since you won't be writing SQL directly. Django provides wrappers for MySQL among many others. Sqlite is intersting in that you don't need to run a seperate database server like you would for MySQL, thus the database file is right in with the rest of the project. That's simple, but we have had many issues with keeping the database file in-sync through github. Once setup, it might be simpler to have a MySQL database that is on a server that the application connects to - that way you don't have to worry about people having different versions.
###Schema
The schema for the db is defined in each of the models. Although the site is made up of several apps, their tables are in the same databse ("userdb").
###Migrations
If you make a change to one of the fields in a model, that effectively changes the database schema. (You can change the functions in the models without issue, just referring to the database fields here). You'll need to "migrate" the database to the new schema. As mentioned earlier, there are some tools that can do this such as the South plugin or newer versions of Django. However, after some change had been made to the database structure a while back, we found that we needed to do migrations manually. You need to "dump" the database to a JSON file, clear the whole db, then rebuild the db from the dump file. This will give you the opportunity to define default values or otherwise handle changes that you wanted to make to the database schema. You can do this with the dumpdata and loaddata commands. Check those out here:
https://docs.djangoproject.com/en/1.6/ref/django-admin/

##Layout of source code
###.idea
###UPS_Calculator
This is the php project for calculating shipping costs using the UPS api. There's the php code and an html page to test it out with. The next step is to integrate the calling code into the webstore checkout and handle those ajax requests in php.
###avatars
The images that are uploaded and processed for the webstore and companion app are stored here.
###blog
Django application of the blog.
###companion
Django application for the companion app. Note how this app works in with the user model, requiring authentication to access.
###frontend
Handles some of the home page / about us pages.
###login
The user model is defined here. Note that UserProfile has a one to one relationship with the User auth model provided by Django. That provides secure passwords and the basics for managing users.
###mysite
`settings.py` lives here, along with `urls.py` that make up the main configuration for the full site.
###src
ignore
###static
I'm not really sure what this is for. I think this was for protyping and is unused.
###store_images
###templates
###webstore



###### Plugins No Longer Used
- south
	- Database migration tool. Not used anymore after we did some structural changes to the db and had to manually rebuild it.



##Current development
View the **Issues** section on the GitHub page for all of the inprogress or planned development.

-----
Current Development version of the Tektiles App for Textile Fabric Inc


1. Inorder for the package to work you must have python and django installed.

2. unpack the archive to your home directory
	$tar xf filename 

3. in your home directory issue:

	$python manage.py runserver
	
   3.1 
	This will start a local webserver at the loopback address on port 8000
	**alternative: you can specify the address and port by appending it to the end of the cmd 
	e.g. 
		$python manage.py runserver 10.0.1.25:8080

		note: The port you choose may be protected by the os and you may have to run as super user.

   3.2
	Once the server is running, test by opening your web browser and enter 127.0.0.1:8000/ this will 		show the boot page for the django app
