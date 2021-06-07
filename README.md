# OrbSpider
OrbSpider is a Spider (web scraper), built using scrapy and scrapy-selenium.
--------------------------------------------------------------------------   
   This project covers almost every frequently used action and process of Web scraping (using scrapy & selenium).
   So if needed, you can use it for reference.

   I hope my work helps some people, at least to some degree.

   Fork & Star the repository if you like it! TIA..... Hope you have a great day.
--------------------------------------------------------------------------


I've used MAL as the target website in this project.

For those of you who don't know what MAL is -
   " MyAnimeList (MAL) is the world's most active online anime and manga community and database. "


<----------> Why use scrapy and selenium both? Why not use only one?:

You can definitely use only Selenium or Scrapy but they both have their pros and cons.

First of all you can't scrape websites that use javascript with scrapy only. you would have to use splash or selenium to do that.

Selenium is not meant to be used for scraping. Mainly it was developed for automation. But because of its user friendliness, vast functions & ability of scraping, we use it with scrapy through a library called scrapy-selenium.

So, the next question arises... why not use selenium solely for web scraping? The answer is, it's too slow for large projects and doesn't have an already built structure to process scraped data like scrapy has.

So, there you go...


<----------> What will it (the OrbSpider) do?:

01. It will go to the homepage of MAL, find and get to the login-form page.
02. Will enter the login credentials, login, redirect to the main page and accept cookies from the popup window.
03. Will navigate to the desired page (in this case to the list of all the anime that i've already completed)
04. Will extract the Field data (see items.py section to find more information about the fields used) and store them in a SQlite Database (see pipelines.py section to find more information about the storing process).


<------> /spiders/MALCompleted.py:
The main code for logging in, navigating and data parsing is written here. You may edit the code based on the website that you want to scrape and the fields that you want to scrape the data for.


<------> /items.py:
The fields that are used in this project are -

01. anime_title : the title of an anime
02. personal_rating : the score (my personal rating) of a particular anime
03. Images : the cover images/ thumbnails from the Completed Animes list


<------> /middlewares.py:

In order to avoid IP Blocking and other difficulties, I've created a custom middleware to select a random user-agent from a given user-agents list, so that the spider uses a different user-agent each time a request is sent to the MAL server.


<------> /pipelines.py:
I've used two pipelines in this project.

01. Images Pipeline: Customized the scrapy default images pipeline to store images using the Anime title as image name instead of the default hashed image urls.

You can customize the Files pipeline similarly. Use 'file_urls' in place of 'image_urls' to customize the files pipeline.

You can customize the pipelines further to suit your needs easily. For more info please visit https://doc.scrapy.org/en/latest/topics/media-pipeline.html to read the documentation.

02. Sqlite Pipeline: A sqlite pipeline to store the scraped data in a sqlite database.
You can change the Database name, Table name and Column names in the code to match your needs.
I've only saved the path of the images in the database as the images are already downloaded and stored in my HDD.

Use the data type "BLOB" if you want to store the image directly to the database.
Use DB Browser for Sqlite to view the database.


<------> /settings.py:
To avoid getting banned i've set AUTOTHROTTLE_ENABLED and HTTPCACHE_ENABLED to True.

To avoid complexity I've set ROBOTSTXT_OBEY to False. But, I encourage you to follow the robots.txt rules if possible.

You can change the image store path in the settings.py file. In case we need to download an image of larger size, i've set the download timeout to 30 min. According to your need you can change that too.

