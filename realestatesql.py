import tkinter
import tkinter.messagebox
import sqlite3
import random

#known bugs: when you sell a house and simulate a week and you don't close the view player owned property and you again try to sell the house, when you rebuy the property, you immeadietly sell it again, when you simulate a week


money = 0
week = 0
year = 0

conn = sqlite3.connect("database.db")

c = conn.cursor()

c.execute("SELECT transactions FROM player_account")

root = tkinter.Tk()
root.title("Real Estate Game")


#Classes

# auxiliary class to calculate the value of a property
class Property:

    def __init__(self, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood):  # initialize the parameters
        self.plot_base_value = plot_base_value
        self.house_base_value = house_base_value
        self.house_condition = house_condition
        self.security = security
        self.education = education
        self.transportation = transportation
        self.neighborhood = neighborhood

    # calculate the value of a property
    def calculate_combined_value(self):  # calculate the value of a property
        house_true_value = (self.house_condition / 500) * self.house_base_value
        combined_value = (self.plot_base_value + house_true_value) * (
                (self.security + self.education + self.transportation + self.neighborhood) / 2000)
        return combined_value

c.execute("SELECT ROWID, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood FROM house_database")
all_data = c.fetchall()
for listing in range(len(all_data)):
    rowid = all_data[listing][0]
    plot_base_value = all_data[listing][1]
    house_base_value = all_data[listing][2]
    house_condition = all_data[listing][3]
    security = all_data[listing][4]
    education = all_data[listing][5]
    transportation = all_data[listing][6]
    neighborhood = all_data[listing][7]
    rowid = Property(plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood)
    combined_value = rowid.calculate_combined_value()


# functions

# progress one week and execute functions. Also create an annual statement of accounts at the end of the year
def simulate_week():
    global week, year
    if week >= 52:
        week = -1
        year += 1
        create_annual_report()
        # Jahresabschluss, alte transactions tabelle in neuer Tabelle speichern und transactions Tabelle löschen
    week += 1
    week_label.config(text=week)
    year_label.config(text=year)
    listings_leaving_market()
    # house_price_changes()
    new_listings()
    tenant_leaves()
    search_tenant()
    search_buyer()
    random_offer()
    collect_rent()
    calculate_money()
    overdraft_interest()
    calculate_money()
    game_over()
    #country_economy_changes()


# open a new window, which shows all the houses which are available with their price
def view_property_market():

    # load all the houses which are available for sale into a listbox
    def load_houses_property_market():
        listbox_house_price_sellings.delete(0, tkinter.END)
        listbox_id_sellings.delete(0, tkinter.END)
        c.execute(
            "SELECT ROWID, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood FROM house_database WHERE player_owned = 0")
        all_data = c.fetchall()
        for listing in range(len(all_data)):
            rowid = all_data[listing][0]
            plot_base_value = all_data[listing][1]
            house_base_value = all_data[listing][2]
            house_condition = all_data[listing][3]
            security = all_data[listing][4]
            education = all_data[listing][5]
            transportation = all_data[listing][6]
            neighborhood = all_data[listing][7]
            rowid = Property(plot_base_value, house_base_value, house_condition, security, education, transportation,
                             neighborhood)
            combined_value = rowid.calculate_combined_value()
            listbox_house_price_sellings.insert(tkinter.END, combined_value)
            listbox_id_sellings.insert(tkinter.END, all_data[listing][0])

    # buy a house for the stated value in the listbox(might change that, that the player can offer a specific amount and negotiate with the seller)
    def buy_house():
        try:
            rowid = listbox_id_sellings.get(listbox_house_price_sellings.curselection()[0])
            purchase_price = listbox_house_price_sellings.get(listbox_house_price_sellings.curselection()[0])
            with conn:
                c.execute(
                    "UPDATE house_database SET player_owned = (:player_owned), on_the_market = (:on_the_market) WHERE ROWID = (:ROWID)",
                    {'player_owned': 1, 'on_the_market': 0, 'ROWID': rowid})
                c.execute("INSERT INTO player_account VALUES (:transactions)", {'transactions': -purchase_price})
            load_houses_property_market()
            calculate_money()
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="You must select a house to buy.")


    property_market_window = tkinter.Toplevel(root)
    property_market_window.title("Property Market")

    frame_stats_name = tkinter.Frame(property_market_window)
    frame_stats_name.pack()
    money_label_label = tkinter.Label(frame_stats_name, text="Money:", width=10)
    money_label_label.pack(side=tkinter.LEFT)
    week_label_label = tkinter.Label(frame_stats_name, text="Week:", width=10)
    week_label_label.pack(side=tkinter.LEFT)
    year_label_label = tkinter.Label(frame_stats_name, text="Year:", width=10)
    year_label_label.pack(side=tkinter.LEFT)

    frame_stats = tkinter.Frame(property_market_window)
    frame_stats.pack()
    money_label = tkinter.Label(frame_stats, text=money, width=10)
    money_label.pack(side=tkinter.LEFT)
    week_label = tkinter.Label(frame_stats, text=week, width=10)
    week_label.pack(side=tkinter.LEFT)
    year_label = tkinter.Label(frame_stats, text=year, width=10)
    year_label.pack(side=tkinter.LEFT)

    frame_tasks = tkinter.Frame(property_market_window)
    frame_tasks.pack()
    listbox_id_sellings = tkinter.Listbox(frame_tasks, height=10, width=10)
    listbox_id_sellings.pack(side=tkinter.LEFT)
    listbox_house_price_sellings = tkinter.Listbox(frame_tasks, height=10, width=40)
    listbox_house_price_sellings.pack(side=tkinter.LEFT)
    scrollbar_house_price_sellings = tkinter.Scrollbar(frame_tasks)
    scrollbar_house_price_sellings.pack(side=tkinter.LEFT, fill=tkinter.Y)
    listbox_house_price_sellings.config(yscrollcommand=scrollbar_house_price_sellings.set)
    scrollbar_house_price_sellings.config(command=listbox_house_price_sellings.yview)

    button_buy_house = tkinter.Button(frame_tasks, text="Buy House", width=48, command=buy_house)
    button_buy_house.pack()

    load_houses_property_market()


# open a new window, which shows all the houses which are owned by the player
def view_player_owned_properties():

    # load all the houses which are owned by the player into a listbox
    def load_houses_player_owned():
        listbox_house_price_player_house.delete(0, tkinter.END)
        listbox_id_player_house.delete(0, tkinter.END)
        c.execute(
            "SELECT ROWID, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood FROM house_database WHERE player_owned = 1")
        all_data = c.fetchall()
        for listing in range(len(all_data)):
            rowid = all_data[listing][0]
            plot_base_value = all_data[listing][1]
            house_base_value = all_data[listing][2]
            house_condition = all_data[listing][3]
            security = all_data[listing][4]
            education = all_data[listing][5]
            transportation = all_data[listing][6]
            neighborhood = all_data[listing][7]
            rowid = Property(plot_base_value, house_base_value, house_condition, security, education, transportation,
                             neighborhood)
            combined_value = rowid.calculate_combined_value()
            listbox_house_price_player_house.insert(tkinter.END, combined_value)
            listbox_id_player_house.insert(tkinter.END, all_data[listing][0])


    # selling a house owned by the player
    def sell_house():
        try:
            house_id = listbox_id_player_house.get(listbox_house_price_player_house.curselection()[0])

            # open a new window with an entry in which the player can enter a price at which the player wants to sell
            def confirm_price():
                try:
                    rowid = listbox_id_player_house.get(listbox_house_price_player_house.curselection()[0])
                    asking_price = sell_house_entry.get()
                    asking_price = float(asking_price)
                    asking_price = round(asking_price, 2)
                    with conn:
                        c.execute("UPDATE house_database SET asking_price = (:asking_price) WHERE ROWID = (:ROWID)",
                                  {'asking_price': asking_price, 'ROWID': rowid})
                    sell_house_window.destroy()
                except:
                    tkinter.messagebox.showwarning(title="Warning!", message="You must enter a numeric value.")
                    sell_house_window.destroy()
                    sell_house()

            sell_house_window = tkinter.Toplevel(root)
            sell_house_window.title("Rent")
            sell_house_frame = tkinter.Frame(sell_house_window)
            sell_house_frame.pack()
            sell_house_label = tkinter.Label(sell_house_frame, text="Asking Price:", width=10)
            sell_house_label.pack()
            sell_house_entry = tkinter.Entry(sell_house_frame)
            sell_house_entry.pack()
            sell_house_confirm = tkinter.Button(sell_house_frame, text="Confirm", width=10, command=confirm_price)
            sell_house_confirm.pack()
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="You must select a house to sell.")


    #  renting a house of the player
    def rent_house():
        try:
            house_id = listbox_id_player_house.get(listbox_house_price_player_house.curselection()[0])

            # open a new window with an entry in which the player can enter an amount at which the player wants to rent the property
            def confirm_rent():
                try:
                    rowid = listbox_id_player_house.get(listbox_house_price_player_house.curselection()[0])
                    rent = rent_entry.get()
                    rent = float(rent)
                    rent = round(rent, 2)
                    with conn:
                        c.execute("UPDATE house_database SET asking_rent = (:asking_rent) WHERE ROWID = (:ROWID)",
                                  {'asking_rent': rent, 'ROWID': rowid})
                    rent_window.destroy()
                except:
                    tkinter.messagebox.showwarning(title="Warning!", message="You must enter a numeric value.")
                    rent_window.destroy()
                    rent_house()

            rent_window = tkinter.Toplevel(root)
            rent_window.title("Rent")
            rent_frame = tkinter.Frame(rent_window)
            rent_frame.pack()
            rent_label = tkinter.Label(rent_frame, text="Rent:", width=10)
            rent_label.pack()
            rent_entry = tkinter.Entry(rent_frame)
            rent_entry.pack()
            rent_frame_confirm = tkinter.Button(rent_frame, text="Confirm", width=10, command=confirm_rent)
            rent_frame_confirm.pack()
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="You must select a house to set rent.")


    # evicting a tenant from a house owned by the player
    def evict_tenants():
        try:
            rowid_player_house = listbox_id_player_house.get(listbox_house_price_player_house.curselection()[0])
            c.execute("SELECT ROWID, rent FROM house_database WHERE ROWID = (:ROWID)", {'ROWID': rowid_player_house})
            all_data = c.fetchall()
            try:
                house_rent = all_data[0][1]
                check_for_tenant = 1 / house_rent
                tenant_compensation = 3 * house_rent
                with conn:
                    c.execute(
                        "UPDATE house_database SET rent = (:rent), asking_rent = (:asking_rent) WHERE ROWID = (:ROWID)",
                        {'rent': 0, 'asking_rent': 0, 'ROWID': rowid_player_house})
                    c.execute("INSERT INTO player_account VALUES (:transactions)",
                              {'transactions': -tenant_compensation})
            except:
                tkinter.messagebox.showwarning(title="Warning!", message="There is no Tenant to evict.")
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="You have to select a house.")


    player_owned_properties_window = tkinter.Toplevel(root)
    player_owned_properties_window.title("Property Market")
    frame_stats_name = tkinter.Frame(player_owned_properties_window)
    frame_stats_name.pack()
    money_label_label = tkinter.Label(frame_stats_name, text="Money:", width=10)
    money_label_label.pack(side=tkinter.LEFT)
    week_label_label = tkinter.Label(frame_stats_name, text="Week:", width=10)
    week_label_label.pack(side=tkinter.LEFT)
    year_label_label = tkinter.Label(frame_stats_name, text="Year:", width=10)
    year_label_label.pack(side=tkinter.LEFT)

    frame_stats = tkinter.Frame(player_owned_properties_window)
    frame_stats.pack()
    money_label = tkinter.Label(frame_stats, text=money, width=10)
    money_label.pack(side=tkinter.LEFT)
    week_label = tkinter.Label(frame_stats, text=week, width=10)
    week_label.pack(side=tkinter.LEFT)
    year_label = tkinter.Label(frame_stats, text=year, width=10)
    year_label.pack(side=tkinter.LEFT)

    frame_tasks = tkinter.Frame(player_owned_properties_window)
    frame_tasks.pack()
    listbox_id_player_house = tkinter.Listbox(frame_tasks, height=10, width=10)
    listbox_id_player_house.pack(side=tkinter.LEFT)
    listbox_house_price_player_house = tkinter.Listbox(frame_tasks, height=10, width=40)
    listbox_house_price_player_house.pack(side=tkinter.LEFT)
    scrollbar_house_price_player_house = tkinter.Scrollbar(frame_tasks)
    scrollbar_house_price_player_house.pack(side=tkinter.LEFT, fill=tkinter.Y)
    listbox_house_price_player_house.config(yscrollcommand=scrollbar_house_price_player_house.set)
    scrollbar_house_price_player_house.config(command=listbox_house_price_player_house.yview)

    button_sell_house = tkinter.Button(frame_tasks, text="Sell House", width=48, command=sell_house)
    button_sell_house.pack()
    button_rent_house = tkinter.Button(frame_tasks, text="Rent House", width=48, command=rent_house)
    button_rent_house.pack()
    button_evict_tenants = tkinter.Button(frame_tasks, text="Evict Tenants", width=48, command=evict_tenants)
    button_evict_tenants.pack()

    load_houses_player_owned()


# creating new random listings
def new_listings():
    pass


# sometimes listings are leaving the market, because they were bought
def listings_leaving_market():
    pass


# looking if there is a buyer for the houses for the offered price which the player wants to sell the property
def search_buyer():
    c.execute(
        "SELECT ROWID, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood, asking_price FROM house_database WHERE player_owned = 1")
    all_data = c.fetchall()
    for listing in range(len(all_data)):
        rowid = all_data[listing][0]
        plot_base_value = all_data[listing][1]
        house_base_value = all_data[listing][2]
        house_condition = all_data[listing][3]
        security = all_data[listing][4]
        education = all_data[listing][5]
        transportation = all_data[listing][6]
        neighborhood = all_data[listing][7]
        asking_price = all_data[listing][8]
        property_class = Property(plot_base_value, house_base_value, house_condition, security, education, transportation,
                         neighborhood)
        combined_value = property_class.calculate_combined_value()
        if asking_price <= combined_value:
            with conn:
                c.execute(
                    "UPDATE house_database SET player_owned = (:player_owned), on_the_market = (:on_the_market), asking_price = (:asking_price) WHERE ROWID = (:ROWID)",
                    {'player_owned': 0, 'on_the_market': 1, 'asking_price': 999999999999, 'ROWID': rowid})
                c.execute("INSERT INTO player_account VALUES (:transactions)", {'transactions': asking_price})


# random offer from a buyer for a player house
def random_offer():
    pass


# # looking if there is a tenant for the houses for the offered rent at which the player wants to rent the property
def search_tenant():
    c.execute("SELECT ROWID, asking_rent, rent FROM house_database WHERE player_owned = 1")
    search_tenant_data = c.fetchall()
    c.execute(
        "SELECT ROWID, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood, asking_rent, rent FROM house_database WHERE player_owned = 1")
    all_data = c.fetchall()
    for listing in range(len(all_data)):
        rowid = all_data[listing][0]
        plot_base_value = all_data[listing][1]
        house_base_value = all_data[listing][2]
        house_condition = all_data[listing][3]
        security = all_data[listing][4]
        education = all_data[listing][5]
        transportation = all_data[listing][6]
        neighborhood = all_data[listing][7]
        asking_rent = all_data[listing][8]
        rent = all_data[listing][9]
        property_class = Property(plot_base_value, house_base_value, house_condition, security, education, transportation,
                         neighborhood)
        combined_value = property_class.calculate_combined_value()
        if rent == 0:
            if asking_rent * 12 * 25 <= combined_value:
                with conn:
                    c.execute("UPDATE house_database SET rent = (:rent) WHERE ROWID = (:ROWID)",
                              {'rent': asking_rent, 'ROWID': rowid})


# looking if a tenant wants to leave a rented house be cause it got to expansive for the offered value of the property
def tenant_leaves():
    c.execute(
        "SELECT ROWID, plot_base_value, house_base_value, house_condition, security, education, transportation, neighborhood, rent FROM house_database WHERE player_owned = 1")
    all_data = c.fetchall()
    for listing in range(len(all_data)):
        rowid = all_data[listing][0]
        plot_base_value = all_data[listing][1]
        house_base_value = all_data[listing][2]
        house_condition = all_data[listing][3]
        security = all_data[listing][4]
        education = all_data[listing][5]
        transportation = all_data[listing][6]
        neighborhood = all_data[listing][7]
        rent = all_data[listing][8]
        property_class = Property(plot_base_value, house_base_value, house_condition, security, education, transportation,
                         neighborhood)
        combined_value = property_class.calculate_combined_value()
        if rent >= combined_value / (12 * 28):
            c.execute("UPDATE house_database SET rent = (:rent) WHERE ROWID = (:ROWID)",
                      {'rent': 0, 'ROWID': rowid})


# calculating the available money of the player by adding all transactions from the player_account table
def calculate_money():
    global money
    money = 0
    c.execute("SELECT transactions FROM player_account")
    transactions = c.fetchall()
    for transaction in transactions:
        money += transaction[0]
    money = round(money, 2)
    money_label.config(text=money)


# calculating the interest if the player has overdrawn his account
def overdraft_interest():
    global money
    interest_rate = 0.089 / 12
    if money < 0:
        interest = interest_rate * money
        with conn:
            c.execute("INSERT INTO player_account VALUES (:transactions)", {'transactions': interest})


# adding the rent of the rented houses of the player to the player_account table
def collect_rent():
    c.execute("SELECT ROWID, rent FROM house_database WHERE player_owned = 1")
    all_data = c.fetchall()
    for house_item in range(len(all_data)):
        house_id = all_data[house_item][0]
        house_rent = all_data[house_item][1]
        if house_rent != 0:
            with conn:
                c.execute("INSERT INTO player_account VALUES (:transactions)", {'transactions': house_rent})


# creating an annual finacial report
def create_annual_report():
    c.execute("SELECT transactions FROM player_account")
    all_transactions = c.fetchall()
    revenue = 0
    for transaction in range(len(all_transactions)):
        revenue = revenue + all_transactions[transaction]
    c.execute("INSERT INTO player_annual_reports VALUES(:revenue)", {'revenue': revenue})
    #löschen der transactions in der tabelle player_account


# further refinement needed
def house_price_changes():
    c.execute("SELECT ROWID, base_value FROM player_houses")
    all_data = c.fetchall()
    for house_item in all_data:
        house_id = house_item[0]
        house_price = house_item[1]
        house_price = round(house_price * 1.02, 2)
        with conn:
            c.execute("UPDATE player_houses SET base_value = (:base_value) WHERE ROWID = (:ROWID)",
                      {'base_value': house_price, 'ROWID': house_id})

    c.execute("SELECT ROWID, base_value FROM house_market")
    all_data = c.fetchall()
    for house_item in all_data:
        house_id = house_item[0]
        house_price = house_item[1]
        house_price = round(house_price * 1.02, 2)
        with conn:
            c.execute("UPDATE house_market SET base_value = (:base_value) WHERE ROWID = (:ROWID)",
                      {'base_value': house_price, 'ROWID': house_id})


# changing the values of the economy to change the prices of the houses
def country_economy_changes():
    c.execute("SELECT ROWID, country_economy_multiplier FROM country")
    all_data = c.fetchall()
    world_economy_crash_generator = random.randint(1, 7)
    for country in range(len(all_data)):
        rowid = all_data[country][0]
        country_economy_multiplier = all_data[country][1]
        if world_economy_crash_generator == 7:
            crash_intensity = round(random.uniform(0.7, 0.85), 2)
            country_economy_multiplier = country_economy_multiplier * crash_intensity
        else:
            growth_intensity = round(random.uniform(0.02, 0.1), 2)
            country_economy_multiplier = country_economy_multiplier * (1 + growth_intensity)
        with conn:
            c.execute(
                "UPDATE country SET country_economy_multiplier = (:country_economy_multiplier) WHERE ROWID = (:ROWID)",
                {'country_economy_multiplier': country_economy_multiplier, 'ROWID': rowid})


# quick test if the change is not to high or to low during growth and crisis times
country_economy_multiplier = 1
tet_year = 0
def country_economy_test():
    global country_economy_multiplier, tet_year
    world_economy_crash_generator = random.randint(1, 7)
    country_economy_multiplier
    tet_year += 1
    if world_economy_crash_generator == 7:
        crash_intensity = round(random.uniform(0.7, 0.85), 2)
        country_economy_multiplier = country_economy_multiplier * crash_intensity
    else:
        growth_intensity = round(random.uniform(0.02, 0.1), 2)
        country_economy_multiplier = country_economy_multiplier * (1 + growth_intensity)
    print(country_economy_multiplier)
    print(tet_year)


# changing the values of the regional economy to change the prices of the houses
def region_economy_changes():
    c.execute("SELECT region_economy_multiplier, region_density_multiplier, primary_sector, secondary_sector, tertiary_sector, quaternary_sector FROM region")
    all_data = c.fetchall()
    for region in range(len(all_data)):
        region_economy_multiplier = all_data[region][1]
        region_density_multiplier = all_data[region][2]
        primary_sector = all_data[region][3]
        secondary_sector = all_data[region][4]
        tertiary_sector = all_data[region][5]
        quaternary_sector = all_data[region][6]
    pass


# changing the local factors to change the value of the houses
def local_factors_changes():
    c.execute("SELECT local_density_multiplier, security, education, transportation, neighborhood FROM local")
    all_data = c.fetchall()
    for local_area in range(len(all_data)):
        local_density_multiplier = all_data[region][1]
        security = all_data[region][2]
        education = all_data[region][3]
        transportation = all_data[region][4]
        neighborhood = all_data[region][5]

    pass


# if the player has overdrawn his account for 12 consecutive weeks, the game ends
def game_over():
    global game_over_counter
    if money <= 0:
        game_over_counter += 1
    if game_over_counter >= 12:
        tkinter.messagebox.showwarning(title="Game over!", message="You have overdrawn you account for too long. The bank has seized all your properties.")
    pass


# GUI
frame_stats_name = tkinter.Frame(root)
frame_stats_name.pack()

money_label_label = tkinter.Label(frame_stats_name, text="Money:", width=10)
money_label_label.pack(side=tkinter.LEFT)

week_label_label = tkinter.Label(frame_stats_name, text="Week:", width=10)
week_label_label.pack(side=tkinter.LEFT)

year_label_label = tkinter.Label(frame_stats_name, text="Year:", width=10)
year_label_label.pack(side=tkinter.LEFT)

frame_stats = tkinter.Frame(root)
frame_stats.pack()

money_label = tkinter.Label(frame_stats, text=money, width=10)
money_label.pack(side=tkinter.LEFT)

week_label = tkinter.Label(frame_stats, text=week, width=10)
week_label.pack(side=tkinter.LEFT)

year_label = tkinter.Label(frame_stats, text=year, width=10)
year_label.pack(side=tkinter.LEFT)

frame_tasks = tkinter.Frame(root)
frame_tasks.pack()

button_view_property_market = tkinter.Button(root, text="View Property Market", width=48, command=view_property_market)
button_view_property_market.pack()

button_view_player_owned_properties = tkinter.Button(root, text="View Your Properties", width=48, command=view_player_owned_properties)
button_view_player_owned_properties.pack()

button_simulate_week = tkinter.Button(root, text="Simulate week", width=48, command=simulate_week)
button_simulate_week.pack()

button_simulate_crash = tkinter.Button(root, text="Simulate crash", width=48, command=country_economy_test)
button_simulate_crash.pack()

calculate_money()

root.mainloop()

conn.close()
