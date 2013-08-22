# -*- coding: utf-8 -*-
import email, re, sqlite3 as db
import os,sys, datetime
import glob
#import numpy as np
#import matplotlib.pyplot as plt
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis


path_to_emails = "/Users/anna.somova/smth/python_parse/emails/"
email_tpl = "*.txt" 
path_to_db = "/Users/anna.somova/smth/python_parse/test2.db"
counts=[]
try:
    connection = db.connect(path_to_db)
    with connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS cnt")
        cursor.execute("CREATE TABLE cnt(id INT, date DATE, new INT, up INT, rep INT)")
       
        
        
        i=0
        for infile in glob.glob(os.path.join(path_to_emails,email_tpl)):
            print str(i)+infile
            i+=1
            file = open(infile,"r")
            msg = email.message_from_file(file)
            content = msg.get_payload()
            #print content
            text = re.findall('тем: (\d*), обновлено тем: (\d*), поднято авторами (\d*).',content) #' (\d*)[,.]'
            print text
            counts.append([i,datetime.date.today(),text[0][0],text[0][1],text[0][2]])
            #result = cursor.fetch()
            #print result
        cursor.executemany("INSERT INTO cnt VALUES(?,?,?,?,?)",counts)

except db.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit()

finally:
    if connection:
        cursor.execute("SELECT * FROM cnt")
        tests = cursor.fetchall()
        for test in tests:
            print test
        
        connection.close()

        # Set the vertical range from 0 to 100
        max_y = 100

        # Chart size of 200x125 pixels and specifying the range for the Y axis
        chart = SimpleLineChart(200, 125, y_range=[0, max_y])

        # Add the chart data
        data=[]
        data.append(tests[0][2])
        data.append(tests[1][2])
        chart.add_data(data)

        # Set the line colour to blue
        chart.set_colours(['0000FF'])

        # Set the vertical stripes
        chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)

        # Set the horizontal dotted lines
        chart.set_grid(0, 25, 5, 5)

        # The Y axis labels contains 0 to 100 skipping every 25, but remove the
        # first number because it's obvious and gets in the way of the first X
        # label.
        left_axis = range(0, max_y + 1, 25)
        left_axis[0] = ''
        chart.set_axis_labels(Axis.LEFT, left_axis)

        # X axis labels
        chart.set_axis_labels(Axis.BOTTOM, \
                              [1,2])

        chart.download('line-stripes.png')


