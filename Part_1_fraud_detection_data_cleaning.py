# Import librairies needed
import pandas as pd
import datetime
import math

# Loading dataset 
dataset = pd.read_csv(
                    filepath_or_buffer = 'fraudTest.csv', 
                    index_col=0
                    )

# To display max col in the .head()
pd.set_option(
    'display.max_columns', 
    None
    )

###########################################################################
#                                                                         #
#               1.Deleting first useless columns                          #    
#                                                                         #
# #########################################################################

# Creating a variable containing useless columns for analysis
useless_col = ['merchant',
                'street',
                'city',
                'zip',
                'lat',
                'long',
                'job',
                'trans_num',
                'unix_time', 
                'merch_lat',
                'merch_long',
                ]

# Creating a new dataset with only interesting columns
df = dataset.loc[:, [col for col in dataset.columns if col not in useless_col]]

############################################################################
#                                                                          #
#        2.Creating the 'age' column with the 'dob' column                 #  
#                                                                          #
# ##########################################################################

# Modifing the 'dob' column type to datetime type to extract the 'age' of people
df['birth_date'] = pd.to_datetime(df.dob)

# Fonction to calculate the 'age' from the 'dob' data
def from_dob_to_age(born):
    today = datetime.date.today()
    return (today.year 
    - born.year 
    - ((today.month, today.day) < (born.month, born.day))
    )

# Creating the 'age' column
df['age'] = df['birth_date'].apply(lambda x: from_dob_to_age(x))

# Dropping useless used columns
df = df.drop(
    ['dob', 'birth_date'],
    axis=1
    )

############################################################################
#                                                                          #
#        3.Extracting the 'year', 'month', 'day', 'dayofweek', 'hour'      #  
#                  with the 'trans_date_trans_time' column                 #
#                                                                          #
# ##########################################################################

# Column 'time_trans' tranformation to datetime type to manipulate datetime type
df['time_trans'] = pd.to_datetime(
    df.trans_date_trans_time
    )

# Extraction of the year, month, day, dayofweek, hour from the 'time_trans' columns
df['trans_year'] = df['time_trans'].dt.year
df['trans_month'] = df['time_trans'].dt.month
df['trans_day'] = df['time_trans'].dt.day
df['trans_day_week'] = df['time_trans'].dt.dayofweek
df['trans_hour'] = df['time_trans'].dt.hour

# Deleting now the 'trans_date_trans_time' and 'time_trans' columns
df = df.drop(
    ['trans_date_trans_time', 'time_trans'],
    axis=1
    )

############################################################################
#                                                                          #
#    4.Concatenating 'first' and 'last' to create the full_namne column    #  
#                                                                          #
# ##########################################################################

## Concatenation de first et last into full name
df['full_name'] = df['first'] + ' ' + df['last']

# Dropping useless used columns
df = df.drop(
    ['first', 'last'],
    axis=1
    )
############################################################################
#                                                                          #
#                   5.Extracting the MMI number card                       #  
#                                                                          #
# ##########################################################################

# Adding 'card issuer' column from 'cc_num' column
# Source : https://www.forbes.com/advisor/credit-cards/what-does-your-credit-card-number-mean/
df['card_issuer_MMI'] = [f'mmi{str(x)[0:1]}' for x in df['cc_num']]

# Deleting useless column already used to create news feature for analysis
del df['cc_num']

############################################################################
#                                                                          #
#                   6.Left columns visualization                           #  
#                                                                          #
# ##########################################################################

# Create a variable containing the list of columns to create a loop function to get the number of unique values by columns
df_cols = df.columns.to_list()

# Using the loop function to get the unique number of each columns in the list 'df_cols'
for col in df_cols:
    print('------------------')
    print(col)
    print(len(df[col].unique()))

# Dropping the 'trans_year' column which have only one value : 2020
df = df.drop(
    ['trans_year'],
    axis=1
    )


############################################################################
#                                                                          #
#                   7.Scaling the 'amt' column                             #  
#                                                                          #
# ##########################################################################

# Amount transformation to integer type
df['amt']=df['amt'].apply(lambda x: int(x))

# Scaling the 'amt' column
df['amt_scaled'] = df['amt'].apply(lambda x : '0-100' if x > 0 and x <= 100
                                        else '101-1000' if (x > 100) and (x <= 1000)
                                        else '1001-2000' if (x > 1000) and (x <= 2000)
                                        else '2001-3000' if (x > 2000) and (x <= 3000)
                                        else '3001-4000' if (x > 3000) and (x <= 4000)
                                        else '4001-5000' if (x > 4000) and (x <= 5000)
                                        else '5001-10000' if (x > 5000) and (x <= 10000)
                                        else '10001-20000' if (x > 10000) and (x <= 20000)
                                        else 'More than 20001')

del df['amt']

############################################################################
#                                                                          #
#                   8.Scaling the 'city_pop' column                        #  
#                                                                          #
# ##########################################################################

# jusqu'à 1.999, une agglomération est un village
# entre 2.000 et 5.000 habitants, on parle d'un bourg ; 
# entre 5.000 et 20.000 d'une petite ville ; 
# entre 20.000 et 50.000 d'une ville moyenne ; 
# entre 50.000 et 200.000 d'une grande ville. 
# Au-delà, les géographes parlent de métropole.

# Source : https://www.lejdd.fr/Societe/quelle-est-la-difference-entre-une-ville-et-un-village-4038323#:
# ~:text=Allons%20encore%20plus%20loin%20%3A%20entre,les%20g%C3%A9ographes%20parlent%20de%20m%C3%A9tropole.

df['city_pop_scaled'] = df['city_pop'].apply(lambda x : 'Village' if x >= 0 and x < 2000
                                                else 'Town' if (x >= 2000) and (x < 5000)
                                                else 'Small city' if (x >= 5000) and (x < 20000)
                                                else 'Medium city' if (x >= 2000) and (x < 50000)
                                                else 'Large city' if (x >= 50000) and (x < 200000)
                                                else 'Metropolis')

# Dropping the 'year' column with only 1 value ('2020')
df = df.drop(
    ['city_pop'],
    axis=1)

############################################################################
#                                                                          #
#                 9.Reindexation of the df to prepare it for               #
#               the next step ('is_fraud' at the end of the df)            #  
#                                                                          #
# ##########################################################################


df = df[['category',
        'card_issuer_MMI',
        'trans_month',
        'trans_day',
        'trans_day_week',
        'trans_hour',
        'amt_scaled',
        'full_name',
        'gender',
        'age',
        'state',
        'city_pop_scaled',
        'is_fraud']]       

############################################################################
#                                                                          #
#               10.Rename and save the df into the name                    #
#                 'fraud_detection_data_cleaning                           #
# #                                                                        #
# ##########################################################################

# Rename the dataset
dataset_fraud_detection = df

# Saving the clean dataset for the next step
dataset_fraud_detection.to_csv(r'src/dataset_fraud_detection', index=False)