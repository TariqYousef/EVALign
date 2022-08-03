### EVALign: Visual Evaluation of Translation Alignment Models

**EVALign** is a framework for quantitative and qualitative evaluation of automatic translation alignment models. It offers several visualization views enabling developers to visualize their models' predictions and compare the performance of their models with other baseline and state-of-the-art models. 
Via different search and filter functions, developers can also inspect the frequent alignment errors and their positions. 

**EVALign** hosts nine gold standard datasets and the predictions of multiple alignment models. The tool is extendable, and adding additional datasets and models is straightforward. 




## Installation 
### As Django app:
- Install dependencies.     
`pip3 install -r requirements.txt`
- Create a postgres database and import from the downloaded database [file](). 
<pre>psql --username=****</pre>
<pre><code>CREATE DATABASE <b>evaling</b>;
psql -h hostname -d <b>evaling</b> -U username -f dbexport.sql</code></pre>

- Create a `.env` file to save DB settings. 
<pre><code>DEBUG=True
SECRET_KEY=**********
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql_psycopg2
SQL_DATABASE=*****
SQL_USER=****
SQL_PASSWORD=****
SQL_HOST=****
SQL_PORT=5432
DATABASE=postgres</code></pre>
- Run the server:   
<code>python manage.py runserver</code>
- Frontend URL: http://127.0.0.1:8000/

### Adding new datasets and models:
_Installation instructions and documentation will be available soon._

