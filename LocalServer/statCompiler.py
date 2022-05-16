"""
Created on 7/6/2021

"""
from datetime import *
import plotly.graph_objects as go
from plotly import offline
import calendar

def parse_data(logfile):
    """
    Pull and parse data from logfile into master list.
    """
    f = open(logfile)
    stat_lst = []
    for aline in f:
        if aline[0] == 'B':
            aline = aline.split(',')
            block_list = aline[15]
            if block_list == 'pfB_VCM_v4':
                stat_lst.append(aline)
    ret = stat_giver(stat_lst)
    return ret

def stat_giver(stat_lst):
    """
    Returns these statistics: geolocation, domain names, IP addresses from the last day, last five days, and last month, top five IP addresses from the last day, last five days, and last month."
    """
    now = datetime.now()
    day_num = 0
    day_lst = []
    five_days_num = 0
    five_days_lst = []
    month_num = 0
    month_lst = []
    all_list = []
    domain_dict = {}
    country_dict = {}
    dates_dict = {}
    timestamp_dict = {}
    num_of_attacks = {}

    for i in range(5):
        day = now - timedelta(days=4 - i)
        day = str(calendar.month_name[day.month]) + ' ' + str(day.day)
        dates_dict[day] = 0
    #Loop over stat_lst, each lst is a line from unified.log seperated by commas.
    for lst in stat_lst:
        mal_IP = lst[10]

        # IP address as key, number of attacks as value
        if mal_IP not in num_of_attacks:
            num_of_attacks[mal_IP] = 0
        num_of_attacks[mal_IP] += 1
        

        #Create dictionary with ip as key, timestamp as value.
        timestamp = lst[1]
        timestamp_dict[mal_IP] = timestamp
        #Create dictionary with IP addresses as key, country name as value, by calling geolocate.find_country.
        country_code = lst[14]
        country_dict[mal_IP] = find_country(country_code) 

        #Create list of domain names (if applicable).
        mal_domain = lst[18]
        domain_dict[mal_IP] = mal_domain
            
        #Put date in correct format, i.e. "yyyy-mm-dd".
        date_to_convert = lst[1]
        date_to_convert = date_to_convert.split(' ')
        month_name = date_to_convert[0]
        datetime_object = datetime.strptime(month_name, "%b")
        month_number = datetime_object.month
        year = date.today().year
        day = date_to_convert[1]
        if len(str(month_number)) == 1:
            month_number = f"0{str(month_number)}"
        if len(str(day)) == 1:
            day = f"0{str(day)}"
        converted_date = f"{year}-{month_number}-{day}"

        #Call function "datetime_object_maker" to turn formatted string date into datetime object.
        then = datetime_object_maker(converted_date)
        all_list.append(mal_IP)
        
        #Compare the two datetime objects ("now" and "then", and append the IP to appropiate list (day_lst, five_days_lst, or month_lst.))
        if (now-then).days < 1:
            day_num += 1
            day_lst.append(mal_IP)
        if (now-then).days < 5:
            five_days_num += 1
            five_days_lst.append(mal_IP)
        if (now-then).days < 31:
            month_num += 1
            month_lst.append(mal_IP)

        then = str(calendar.month_name[then.month]) + ' ' + str(then.day)
        if then in dates_dict:
             dates_dict[then] += 1
    
    #last100 list reversed for most recent at top of table
    last100 = []
    all_list = all_list[-100:]
    for ip in reversed(all_list):
        if ip not in last100:
            last100.append(ip)

    #Call function "top_five_tuples" to store the top five IP values in each category, in tuple format.)
    top_day_tuples = top_five_tuples(day_lst)
    top_fivedays_tuples = top_five_tuples(five_days_lst)
    top_month_tuples = top_five_tuples(month_lst)
    all_tuples = top_five_tuples(all_list)

    #Call function "num_formatter" to turn number of hits into string.
    day_num = num_formatter(day_num)
    five_days_num = num_formatter(five_days_num)
    month_num = num_formatter(month_num)

   
    #Create country_num_dict, key=country and value=number of IP addresses from country. Maxlength=10.
    country_num_dict = country_num_dict_maker(country_dict)
    sorted_country_num_keys = sorted(country_num_dict.keys(), reverse=True, key=lambda x: country_num_dict[x])
    if len(sorted_country_num_keys) > 10:
        sorted_country_num_keys = sorted_country_num_keys[:10]
        sorted_country_num_keys = sorted(sorted_country_num_keys, key=lambda x: x[0])
    else:
        sorted_country_num_keys = sorted(sorted_country_num_keys, key=lambda x: x[0])
    sorted_country_num_values = [country_num_dict[country] for country in sorted_country_num_keys]

    #Create country graph using plotly, turn into html.
    dex = len(sorted_country_num_keys)
    colors = ['#C84E00', '#E89923', '#FFD960', '#C84E00', '#E89923', '#FFD960', '#C84E00', '#E89923', '#FFD960', '#C84E00'][:dex]
    fig = go.Figure(data=[go.Bar(x=sorted_country_num_keys, y=sorted_country_num_values, text=sorted_country_num_values, textposition='auto')])
    fig.update_traces(marker_color=colors, marker_line_color='rgb(122,0,0)', marker_line_width=1.5, opacity=0.7)
    fig.update_layout(title_text='Top Countries by IP Blocks', title=dict(font_size=30, font_color='#012169'), title_x=0.5, yaxis=dict(title='Hits', color='#012169', titlefont_size=25), xaxis=dict(title="Countries", color='#012169', titlefont_size=25))
    country_html = offline.plot(fig, include_plotlyjs=False, output_type='div')

    #Create blocksperday graph using plotly, turn into html.
    graph_dates_lst = [item for item in dates_dict.keys()]
    graph_hits_lst = [item for item in dates_dict.values()]
    fig = go.Figure(data=[go.Scatter(x=graph_dates_lst, y=graph_hits_lst)])
    fig.update_layout(title=dict(text="Blocks Over Past Five Days", font_size=30, font_color='#012169'), title_x=0.5, xaxis=dict(title='Date', titlefont_size=25, color='#012169'), yaxis=dict(title='Blocks', titlefont_size=25, color='#012169'))
    day_hits_html = offline.plot(fig, include_plotlyjs=False, output_type='div')

    #Return a list of variables to be passed to the function "statistics" in app.py. From there, each variable is rendered using Jinja template to be displayed in html.
    return [day_num, day_lst, five_days_num, five_days_lst, month_num, month_lst, top_day_tuples, top_fivedays_tuples, top_month_tuples, domain_dict, country_dict, country_html, day_hits_html, all_tuples, timestamp_dict, num_of_attacks, last100]

def datetime_object_maker(converted_date):
    """
    Turn string date into datetime object.
    """
    then = datetime.strptime(converted_date, '%Y-%m-%d')
    return then

def find_country(country_code):
    if country_code == 'Unk':
        return 'Unknown'
    f = open('countryCodes.txt')
    for line in f :
        line = line.strip()
        if country_code == line.split(',')[0] : # if the country code matches the country code in countryCodes.txt
            return ','.join(line.split(',')[1:]) # return the country name
    return 'Unknown' # if country code is not in countryCodes.txt, return Unknown

def top_five_tuples(lstname):
    """
    Takes lstname, returns sorted list of tuples of length <= 5 for the top five
    in each category where tuple[0]=IP address and tuple[1]=number of attacks.
    """
    dict = {}
    for ip in lstname:
        if ip not in dict:
            dict[ip] = 0
        dict[ip] += 1
    sorted_tuples = sorted(dict.items(), reverse=True, key=lambda x: x[1])
    if len(sorted_tuples) < 5:
        top_five_tuples = sorted_tuples
    else:
        top_five_tuples = sorted_tuples[:5]
    return top_five_tuples

def num_formatter(num):
    """
    These statements are for formatting the string values for the total list of IP addresses.
    """
    ret = f"{num}"
    return ret

def country_num_dict_maker(dict):
    ret = {}
    for country in dict.values():
        if country not in ret:
            ret[country] = 0
        ret[country] += 1
    return ret

if __name__ == '__main__':
    parse_data("unified.log")
