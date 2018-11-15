# Project 1, Part 3

* Assigned: 10/18
* Due:  11/27 10AM EST
* (worth 50% of overall Project 1 grade)


In this part of the project, you will complete the web application by building the front end
on top of the `Flask` Python webserver.


* [Project overview](http://github.com/w4111/project1)
* If your teammate has dropped the class, [see the contingency plan](http://github.com/w4111/project1/part1.md#contingency)
* For any questions about collaboration, [see the Syllabus](http://github.com/w4111/syllabus#cheating)
* If there are questions of general interest, please post to Piazza.


# Requirements

Implement the application you described in Part 1 in Python using Flask.

* Your application must execute SQL query strings on the provided staff database. (*Note*: This means you cannot use an ORM. Part of the goal of this project is to practice writing and debugging SQL queries. Tools that attempt to make this "easier" are not permitted.)
* Your application must provide a way to view or interact with all the entities and relationships in your final ER diagram.
* It does not need to be beautiful or sophisticated. Plain text pages are acceptable! However, if you want to make it fancy, you can do that (there will be a few "bonus" prizes for sophisticted applications).
* In general, you can probably use whatever third-party libraries you want, except for ORMs or other libraries that simplify database access. If you are unsure if a library is permitted, ask a staff member or on Piazza.
* Your application should prevent forms of SQL injection described in lecture.

*Note*: if you anticipate doing a huge number of queries (say hundreds of queries per second), 
or will have a huge database (more than 10k rows),
please let the staff know so we can allocate resources appropriately.


# References


The following documentation may be helpful for both learning Python and Flask:

* [Java to Python Cheatsheet](https://github.com/w4111/syllabus/blob/master/java2python.md)
* [Python tutorial](https://docs.python.org/2/tutorial/)
* [Learn Python The Hard Way](http://learnpythonthehardway.org/book/)
* [Flask documentation](http://flask.pocoo.org)
* [Flask Tutorial](http://flask.pocoo.org/docs/latest/tutorial/)
* [Jinja Template documentation](http://jinja.pocoo.org/)
* [Jinja Tutorial](https://realpython.com/blog/python/primer-on-jinja-templating/)

If your application has users, and you'd like to implement login/logout pages with password authentication, check:
* [Flask Quickstart: Sessions](http://flask.pocoo.org/docs/1.0/quickstart/#sessions)
* [Creating a login page](https://pythonspot.com/login-authentication-with-flask/)
    * Note: do not follow the "Connecting to your database" section of this tutorial, as it uses ORM. Remember that you are **not** allowed to use ORM, and your code must issue SQL queries instead.



# Getting Started

Your job is to implement your proposed web application.  To help you out,
we have provided a bare-bones Flask web application in [./webserver/](./webserver/).
It provides code that connects to a database url, and a default index page.
Take a look at the comments in `server.py` to see how to use modify the server.
You will need to connect to the class database (used for part 2).

Please read all these directions, and get the example server we provide running. Once you get it
running you should edit it to talk to your own database and start working on your custom logic.


### A Short Introduction to SQLAlchemy

We use a python package called `SQLAlchemy` to simplify our work for connecting to the database.
For example, `server.py` contains the following code to load useful functions from
the package:

        # import useful functions from the package
        from sqlalchemy import *

`SQLAlchemy` is able to connect to many different types of DBMSes such as 
SQLite, PostgreSQL, MySQL, Oracle and other databases.  Each such DBMS
is called an "engine".  The `create_engine()` function sets up the configuration
to specify which type of DBMS we want to connect to, and what their parameters are.

        engine = create_engine(DATABASEURI)


Given an engine, we can then connect to it (this is similar to how `psql` connects
to the staff database).

        conn = engine.connect()

At this point, the `conn` connection object can be used to
execute queries to the database.  This is basically what `psql`
is doing under the covers!  

        cursor = conn.execute("select 1")

The `execute` function takes a SQL query string as input, and
returns a `cursor` object.  You can think of this as an iterator 
over the result relation.  This means you can run `select *` 
on a million row table, and not run out of memory. Instead of
sending the entire result at once. Instead, this
object lets you treat the result as an iterator and call `.next()`
on it, or loop through it.  [See the documentation for a detailed description](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy).

        # this fetches the first row if called right after
        # the execute function above.  It also moves the
        # iterator to the next result row.
        record = cursor.fetchone()

        # this will fetch the next record, or None if
        # there are no more results.
        second_record = cursor.fetchone()

        # this loops through the results of the cursor one by one
        for row in cursor:
          print list(row)


The above description is a way to directly write and run SQL
queries as strings, and directly manipulate the result relations.
SQLAlchemy is also an [Object Relational Mapper](https://en.m.wikipedia.org/wiki/Object-relational_mapping)
that provides an interface that hides SQL query strings and 
result sets from you.  Instead you access and manipulate
tables in the database as if they were normal Python objects.

**In this project, you will directly write and run SQL queries, 
and will not use any ORM functionality.**


### Working with GitHub

* Fork this repository so you have your own copy that you can edit.
  You will submit a link to the repository. (click the Fork button on the top right corner of this page)
* Clone it to your VM (or your local machine, if you have Python installed and want to run locally): `git clone git@github.com:[YOUR_GITHUB_USERNAME]/project1.git`
* Edit your files
* Use the following commands to add and checkpoint (commit) your changes locally

        git add --help
        git add <new files to store in git>
        git commit -m "a sentence describing your changes"

* When everything has been committed you can `push` all the committed changes so GitHub.com has a copy

        git push

* If you cloned the repository on another machine (say the VM), then you can download and apply those
  changes from GitHub.com

        git pull

Some notes

* Your life will be easier by setting up [SSH keys](https://help.github.com/articles/generating-ssh-keys/)
  and cloning the `git://....` versions of repositories.  That way GitHub won't keep asking for your password
  when running `git` commands. However, if don't know what this means, stick to the original HTTP version.
* Most errors you will encounter can be solved by consulting a [search](http://www.google.com) [engine](http://www.bing.com).


### Running on the virtual machine

You will deploy your application to your Google App Engine virtual machine.

* [Steps to create an instance from Part2](./gcp_instructions.pdf).

Also, you'll need to open the firewall so you can access your web application. This is a one-time setup.

* [Steps to open firewall for Flask](./firewall_instructions.pdf).


1. Write down the external IP of your virtual machine, but remember that it changes every time you restart it.
2. Perform some default installations and scaffolding for the web-app. [Setup Instructions](./setup_instructions/setup.md).
2. Copy your code to the Google App Engine virtual machine as per instructions above or on GitHub's help pages.
3. Click on the SSH button on the Google App Engine dashboard to access your virtual machine and enter the "test" virtualenv.
4. Run the python server with the defaults, which will listen for requests on port 8111.  Run with `--help` if you need help

        cd project1/webserver
        python server.py --debug


5. Go to `http://<IP ADDRESS>:8111/` in your browser to check that it worked.  
   You will need this URL when presenting the project to your mentor.


### (Optional) Running locally

**Note**: This is just a *suggestion*. Since it is impossible to support setting up Python on everyone's
personal computers, we can't really help debug issues that aren't happening on an Google App Engine VM. Your best
bet is google, office hours, or asking your fellow students on piazza.

It is much more convenient to be able to test your application on your laptop or local computer, and
run it on the Google App Engine VM when you are happy with the code. You can do this by following the virtualenv
setup commands from HW0 on your own computer. Once you have the correct virtualenv set up, you can
run the the web server with:

To run the webserver, go into the `webserver/` directory and run (make sure you have enabled the `virtualenv` environment)

        python server.py --debug

It should print something like:

        running on 0.0.0.0:8111
        * Running on http://0.0.0.0:8111/

The `0.0.0.0` listens to any IPv4 address on the machine.  The `8111` after the `:` is the port number.
So if this is running on your laptop, you can open you web browser to `http://localhost:8111`.

You can specify a custom port by passing a host and port as arguments:

        python server.py --debug 0.0.0.0 8888

To see its command line options, use the `--help` flag

        python server.py --help

If you run the server with the `--debug` flag, it will automatically pick up changes when you reload the page, which is more convenient than restarting the server each time. It additionally will display detailed errors in the web browser, instead of only on the console.


### (optional) Longer Term Running

The following are optional instructions on how to keep servers running. You'll need it after your project is complete, so staff can access your application to run additional tests if needed.

There are several ways to keep the server running after you have logged out of the VM.
Note that these are all poor man's techniques.

1. **nohup**.  the HUP signal is how the terminal warns a process of user logout.  the nohup
   command ensures that the process ignores this signal, allowing it to continue running.
   the "&" character at the end of the command tells the terminal to detach this process
   from the terminal.  

        nohup python server.py 0.0.0.0 8008 &
   
   
   You can kill the process explicitly by getting the process ID and using the `kill` command:

        ps -A | grep python
        kill <the ID of the python process>

2. **[tmux](https://en.m.wikipedia.org/wiki/Tmux)** is a remote terminal manager.  You can think of the terminal as two parts --  
   the client that you interact with by typing characters and pressing ENTER, and a
   server that actually reads those commands and runs processes in response.  
   Usually when you login to a VM, the client and server are tied together in a single process,
   so that when you logout the client and server both die.  TMUX on the other hand
   explicitly starts two processes -- the server process that continues to run after you log out,
   and a client process that connects to the server process. This way, even if you disconnect,
   only the client dies.  When you re-connect, you can re-attach to the server process and
   resume your terminal session!  This is what I do.  

        # install tmux
        sudo apt-get install tmux

        # run tmux
        tmux

        # it will open a terminal
        python server.py 0.0.0.0 8008

        # don't press ctrl-c, just close your window.

  Tmux is quite powerful -- come ask me directly or post to piazza if you are curious about its other functionalities.  GNU Screen
  is an alternative to tmux.
  
  
  
### (optional) Copy Remote Database to Local

[These](./Copy_db_to_local.md) are optional instructions on how to copy the remote database to local for testing.


# Grading

* How well your application matches the Part 1 submission, and how well you incorporated the mentor's feedback?
* Does it let a user access all the entities and relationships on the ER diagram?
* Your grade will not be based on how _sophisticated_ the user interface is (though it may mildly help)
* Your grade will suffer if it doesn't work, requires the user typing SQL, crashes or
  locks up on bad inputs, is vulnerable to the SQL injection described in lecture, and otherwise does
  not work as you described in part 1.


# Submission

Please leave your virtual machine running so the IP address does not change (see "Longer Term Running" above), then submit a PDF file to Gradescope containing:
* both members' name and UNI;
* the URL to access your application;
    * if your application has some authentication flow (i.e. some sign-in page), include such credentials as well;
* link to the GitHub repo containing your codebase;
    * if you make any changes to your repo after you submitted your PDF file, we'll consider it as submission date instead;
* any changes made to your schema since Part 2 (and why);



Students will present to their project mentor between `11/27` and `11/29`.

Mentors will email you to schedule a 15 minute meeting by `11/23`.

Contact your mentor immediately if you have not been contacted by `11/26`.

You will show off your project using the mentor's web browser:

1. Give your mentor the app's URL so they can run it in Chrome or Firefox -- make sure you tested in those browsers!
    * your grade will suffer _considerably_ if this step doesn't work

2. Your mentor will interact with your application and test the functionality described in Part 1
    *  Have a number of example interactions prepared ahead of time to show your mentor.  
       The more you impress your mentor, the better your grade is likely to be.

3. Your mentor may ask to look at your code, so have it available.  

4. The web interface doesn't need to be fancy, however users **should not need to type anything resembling SQL**.


