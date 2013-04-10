#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import MySQLdb
dbname = "duelifydb"
conn = MySQLdb.connect('localhost', 'django_user', 'houmie123', dbname, charset='utf8')
cur = conn.cursor()

cur.execute("INSERT INTO duelify_app_category (category) VALUES ('Entertainment'), ('Sports'), ('Politics'), ('Music'), ('Business'), ('Health');")

#for line in f:
#    cur.execute("INSERT INTO chasebot_app_country (country_code, country_name) VALUES (%s, %s)", (line[:2] , line[3:-1]))                
#        
#f.close()

# Make the changes to the database persistent
conn.commit()


cur.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
cur.execute(sql)

results = cur.fetchall()
for row in results:
    sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
    cur.execute(sql)

# Close communication with the database
cur.close()
conn.close()