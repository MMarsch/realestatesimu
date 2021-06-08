import sqlite3
import random

conn = sqlite3.connect("database.db")

c = conn.cursor()

#Database operations

#c.execute("""DROP TABLE tasks""")

#neighboorhood, education, transportation, security, condition

#c.execute("""CREATE TABLE house_market (
 #           base_value FLOAT(12, 2),
  #          house_condition INT(4),
   #         security INT(4),
    #        education INT(4),
     #       transportation INT(4),
      #      neighborhood INT(4),
       #     true_value FLOAT(12)
        #    )""")

#c.execute("""CREATE TABLE player_houses (
 #           base_value FLOAT(12, 2),
  #          house_condition INT(4),
   #         security INT(4),
    #        education INT(4),
     #       transportation INT(4),
      #      neighborhood INT(4),
       #     true_value FLOAT(12),
        #    asking_rent  FLOAT(6, 2),
         #   rent  FLOAT(6, 2),
          #  asking_price FLOAT(12, 2)
           # )""")

#c.execute("""CREATE TABLE house_database (
 #           country_id INT(3),
  #          region_id INT(2),
   #         local_id INT(3),
    #        plot_id INT(4),
     #       plot_base_value FLOAT(12, 2),
      #      house_base_value FLOAT(12, 2),
       #     house_condition INT(4),
        #    security INT(4),
         #   education INT(4),
          #  transportation INT(4),
           # neighborhood INT(4),
            #player_owned INT(1),
      #      on_the_market INT(1),
       #     asking_rent  FLOAT(6, 2),
        #    rent  FLOAT(6, 2),
         #   asking_price FLOAT(12, 2)
          #  )""")

#c.execute("""CREATE TABLE country (
 #           country_id INT(3),
 #           country_name VARCHAR(40),
  #          country_economy_multiplier FLOAT(5, 2)
        #    )""")

#c.execute("""CREATE TABLE region (
 #           region_id INT(2),
 #           region_name VARCHAR(40),
  #          region_economy_multiplier FLOAT(3, 2),
  #          region_density_multiplier FLOAT(4, 2),
   #         primary_sector FLOAT(3, 2),
    #        secondary_sector FLOAT(3, 2),
     #       tertiary_sector FLOAT(3, 2),
      #      quarternary_sector FLOAT(3, 2)
        #    )""")

#c.execute("""CREATE TABLE local (
 #           local_id INT(3),
 #           local_name VARCHAR(40)
#            local_density_multiplier FLOAT(5, 2),
#            security INT(4),
#            education INT(4),
#            transportation INT(4),
#            neighborhood INT(4)
        #    )""")

#c.execute("INSERT INTO house_database VALUES (:country_id, :region_id, :local_id, :plot_id, :plot_base_value, :house_base_value, :house_condition, :security, :education, :transportation, :neighborhood, :player_owned, :on_the_market, :asking_rent, :rent, :asking_price)", {'country_id': 1, 'region_id': 1, 'local_id': 1, 'plot_id': 1, 'plot_base_value': 45000, 'house_base_value': 200000, 'house_condition': 500, 'security': 500, 'education': 500, 'transportation': 500, 'neighborhood': 500, 'player_owned': 0, 'on_the_market': 1, 'asking_rent': 999999, 'rent': 0, 'asking_price': 999999999999})
#c.execute("INSERT INTO house_database VALUES (:country_id, :region_id, :local_id, :plot_id, :plot_base_value, :house_base_value, :house_condition, :security, :education, :transportation, :neighborhood, :player_owned, :on_the_market, :asking_rent, :rent, :asking_price)", {'country_id': 1, 'region_id': 1, 'local_id': 1, 'plot_id': 2, 'plot_base_value': 60000, 'house_base_value': 320000, 'house_condition': 500, 'security': 500, 'education': 500, 'transportation': 500, 'neighborhood': 500, 'player_owned': 0, 'on_the_market': 1, 'asking_rent': 999999, 'rent': 0, 'asking_price': 999999999999})
#c.execute("INSERT INTO house_database VALUES (:country_id, :region_id, :local_id, :plot_id, :plot_base_value, :house_base_value, :house_condition, :security, :education, :transportation, :neighborhood, :player_owned, :on_the_market, :asking_rent, :rent, :asking_price)", {'country_id': 1, 'region_id': 1, 'local_id': 1, 'plot_id': 3, 'plot_base_value': 75000, 'house_base_value': 450000, 'house_condition': 500, 'security': 500, 'education': 500, 'transportation': 500, 'neighborhood': 500, 'player_owned': 0, 'on_the_market': 1, 'asking_rent': 999999, 'rent': 0, 'asking_price': 999999999999})

#c.execute("""DELETE FROM house_database WHERE player_owned = 1""")

#     plot_true_value FLOAT(12), #needs to be calculated and not saved
#     house_true_value FLOAT(12),#needs to be calculated and not saved in database
#     combined_value


#c.execute("""CREATE TABLE player_account (
 #           transactions FLOAT(12, 2)
  #          )""")

#c.execute("""CREATE TABLE player_annual_reports (
 #           revenue FLOAT(15, 2)
  #          )""")

#c.execute("INSERT INTO house_market VALUES (:base_value, :house_condition, :security, :education, :transportation, :neighborhood, :true_value)", {'base_value': 245000, 'house_condition': 500, 'security': 500, 'education': 500, 'transportation': 500, 'neighborhood': 500, 'true_value': 245000})
#c.execute("INSERT INTO house_market VALUES (:base_value, :house_condition, :security, :education, :transportation, :neighborhood, :true_value)", {'base_value': 367000, 'house_condition': 500, 'security': 500, 'education': 500, 'transportation': 500, 'neighborhood': 500, 'true_value': 367000})
#c.execute("INSERT INTO house_market VALUES (:base_value, :house_condition, :security, :education, :transportation, :neighborhood, :true_value)", {'base_value': 433000, 'house_condition': 500, 'security': 500, 'education': 500, 'transportation': 500, 'neighborhood': 500, 'true_value': 433000})

#c.execute("INSERT INTO player_houses VALUES (:base_value)", {'base_value': 433000})

#c.execute("INSERT INTO player_account VALUES (:transactions)", {'transactions': 300000})

#c.execute("SELECT * FROM house_database")
#all_data = c.fetchall()
#print(all_data)

#c.execute("""DROP TABLE house_database""")

#c.execute("SELECT price FROM house_market")

#houses = c.fetchall()
#for i in houses:
#    print(i)

#c.execute("SELECT transactions FROM player_account")

#transactions = c.fetchall()
#for i in transactions:
#    print(i)

#c.execute("""DELETE FROM player_account WHERE ROWID >= 2""")

#c.execute("""DROP TABLE house_market""")

#c.execute("""DROP TABLE player_houses""")
crash_intensity = round(random.uniform(0.5 , 0.85), 2)
print(crash_intensity)

conn.commit()


conn.close()