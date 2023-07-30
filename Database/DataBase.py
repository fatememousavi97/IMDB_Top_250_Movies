#!/usr/bin/env python
# coding: utf-8

# Now that we Crawled and collected data as csv files we
# wanna create a database with "MySQL" and "MySQL connector"

# # Import libraries

# In[23]:


import streamlit as st
from pathlib import Path
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt 
import numpy as np
import altair as alt
import csv
import pandas as pd


# first we should Create a user and grant all previliges to it in MySQL

# Now that we Created user we should connect python to MySQL with MySQL connector

# create a mysql connection using `mysql.connector.connect` function and pass initial configs!

# In[5]:


cnx = mysql.connector.connect(
    user="fateme_mousavi",
    host="127.0.0.1", 
    password="FMousavi11121375",
)
cursor = cnx.cursor()


# # DataBase Creation

# In[6]:


def create_database(cursor, DB_NAME): 
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        cursor.reset()
        print(f"Successfully created database: {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")


# In[7]:


DB_NAME = 'IMDB'
create_database(cursor, DB_NAME)


# Check database name in our localhost 

# In[8]:


cursor.execute("SHOW DATABASES;")
DBs = tuple()
for x in cursor:
    DBs += x


# In[9]:


for i, x in enumerate(DBs):
    print(f"{i}\t{x}")


# # Tables Creation

# First table: movie

# In[10]:


TABLES = {}
TABLES['movie'] = (
    "CREATE TABLE IF NOT EXISTS `movie` ("
    "  `id` varchar(8) NOT NULL,"
    "  `title` varchar(128),"
    "  `year` int(11) ,"
    "  `runtime` int(11) ,"
    "  `parental_guide` varchar(8) NOT NULL,"
    "  `gross_us_canada` int(11),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


# Second Table: Person

# In[11]:


TABLES['person'] = (
    "CREATE TABLE IF NOT EXISTS `person` ("
    "  `id` varchar(8) NOT NULL,"
    "  `name` varchar(32),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


# Third table: Cast

# In[13]:


TABLES['cast'] = (
    "CREATE TABLE IF NOT EXISTS `cast` ("
    "`id` INT NOT NULL AUTO_INCREMENT,"
    " `movie_id` varchar(8) NOT NULL,"
    " `person_id` varchar(8) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `cast_ibfk_1` FOREIGN KEY (`person_id`) "
    "     REFERENCES `person` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `cast_ibfk_2` FOREIGN KEY (`movie_id`) "
    "     REFERENCES `movie` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


# fourth table: Crew

# In[14]:


TABLES['crew'] = (
    "CREATE TABLE IF NOT EXISTS `crew` ("
    "`id` INT NOT NULL AUTO_INCREMENT,"
    " `movie_id` varchar(8) NOT NULL,"
    " `person_id` varchar(8) NOT NULL,"
    " `role` varchar(8) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `crew_ibfk_1` FOREIGN KEY (`person_id`) "
    "     REFERENCES `person` (`id`) ON DELETE CASCADE,"
    "  CONSTRAINT `crew_ibfk_2` FOREIGN KEY (`movie_id`) "
    "     REFERENCES `movie` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


# Last table: Genre

# In[16]:


TABLES['genre'] = (
    "CREATE TABLE IF NOT EXISTS `genre` ("
    "`id` INT NOT NULL AUTO_INCREMENT,"
    " `movie_id` varchar(8) NOT NULL,"
    " `genre` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `genre_ibfk_2` FOREIGN KEY (`movie_id`) "
    "     REFERENCES `movie` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


# In[17]:


cursor.execute(f"USE {DB_NAME}")


# In[18]:


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


# Show tables that we created

# In[19]:


cursor = cnx.cursor()
cursor.execute(f"USE {DB_NAME};")
cursor.execute("SHOW TABLES;")
for x in cursor:
    print(x)


# # Data Insertion

# Insert Movie table Data from CSV file

# In[24]:


with open('movie.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row['id'], row['title'], row['year'],row['runtime'],row['parental_guide'],row['gross_us_canada'])
        # insert

        sql_statement =('INSERT INTO movie'
                       '(id,title, year, runtime, parental_guide, gross_us_canada)'
                        'VALUES(%(id)s, %(title)s, %(year)s, %(runtime)s, %(parental_guide)s, %(gross_us_canada)s)')
        
        cursor.execute(sql_statement,row)
cnx.commit()


# Query to show Movie table

# In[25]:


cursor.execute('select * from movie order by runtime;')


# In[26]:


records = []
for item in cursor.fetchall() :
    print(item)
    records.append(item)


# In[27]:


len(records)


# # Insert Person table data from CSV

# In[28]:


with open('person.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row['person_id'], row['name'])
        # insert

        sql_statement =('INSERT INTO `person`'
                       '(`id`, `name`)'
                        'VALUES(%(person_id)s, %(name)s)')
        
        cursor.execute(sql_statement,row)
cnx.commit()


# In[29]:


cursor.execute('select * from person;')
records = []
for item in cursor.fetchall() :
    print(item)
    records.append(item)


# In[30]:


len(records)


# Insert Cast table data

# In[32]:


with open('cast.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row['movie_id'], row['person_id'])
        # insert

        sql_statement =('INSERT INTO `cast`'
                       '(`movie_id`,`person_id`)'
                        'VALUES(%(movie_id)s, %(person_id)s)')
        
        cursor.execute(sql_statement,row)
cnx.commit()


# In[33]:


cursor.execute('select * from cast;')
records = []
for item in cursor.fetchall() :
    print(item)
    records.append(item)


# In[34]:


len(records)


# Insert Crew table Data

# In[35]:


with open('crew.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row['movie_id'], row['person_id'],row['role'])
        # insert

        sql_statement =('INSERT INTO `crew`'
                       '(`movie_id`,`person_id`,`role`)'
                        'VALUES(%(movie_id)s, %(person_id)s, %(role)s)')
        
        cursor.execute(sql_statement,row)
cnx.commit()


# In[36]:


cursor.execute('select * from crew;')
records = []
for item in cursor.fetchall() :
    print(item)
    records.append(item)


# In[37]:


len(records)


# In[38]:


with open('genre.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        print(row['movie_id'], row['genre'])
        # insert

        sql_statement =('INSERT INTO `genre`'
                       '(`movie_id`,`genre`)'
                        'VALUES(%(movie_id)s, %(genre)s)')
        
        cursor.execute(sql_statement,row)
cnx.commit()


# In[39]:


cursor.execute('select * from genre;')
records = []
for item in cursor.fetchall() :
    print(item)
    records.append(item)


# In[40]:


len(records)


# # Close the Cursor

# In[41]:


cursor.close() 

