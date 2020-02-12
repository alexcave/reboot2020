import pandas as pd
import argparse
# import sqlalchemy

db_user = 'user'
db_pass = 'password'
db_name = 'lending_solutions_data'
cloud_sql_connection_name = 'lbg-reboot-feb2020-team-11:europe-west2:lending-solutions-db'


# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
# db = sqlalchemy.create_engine(
#     # Equivalent URL:
#     # mysql+pymysql://user:password@/lending_solutions_data?unix_socket=/cloudsql/lbg-reboot-feb2020-team-11:europe-west2:lending-solutions-db
#     sqlalchemy.engine.url.URL(
#         drivername="mysql+pymysql",
#         username=db_user,
#         password=db_pass,
#         database=db_name,
#         query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
#     ),
#     # ... Specify additional properties here.
#     # ...
# )

# query = """

#     SELECT *
#     FROM lending_solutions_data.pca

#     UNION

#     SELECT *
#     FROM lending_solutions_data.loan

#     UNION
    
#     SELECT *
#     FROM lending_solutions_data.credit_card

#     UNION
    
#     SELECT *
#     FROM lending_solutions_data.car_finance

# """

# df = pd.read_sql(sql = query, con = db.engine)



def df_runner(amount, term):

    # df = pd.read_sql()

    df_pca = pd.read_csv("pca_data.csv")
    # df_car_finance = pd.read_csv("C:\\Users\\Andreas Armstrong\\Documents\\Python Projects\\reboot2020\\car_finance.csv")
    df_credit_card = pd.read_csv("credit_card.csv")
    # removed credit card,platinum balance transfer,up to 15min,,0,1,12000,01/01/2019,
    df_loan = pd.read_csv("loan.csv")
    
    # loan,home imporvement loan,,,3.83,1,9999,01/01/2019,
    # loan,home imporvement loan,,,3,10000,25000,01/01/2019,


    # df = pd.concat([df_pca, df_car_finance, df_credit_card, df_loan])

    df = pd.concat([df_pca, df_credit_card, df_loan])

    df["daily_charge"] = df["daily_charge"].fillna(0)

    # check where amount is not greater than max
    df = df[df["max_amount"] >= amount]
    
    # check where amount is greater than min
    df = df[df["min_amount"] <= amount]
    
    # daily_rate
    df["daily_rate"] =  df["intrest_rate"]/ 100 / 365

    # cost
    df["cost"] = (df["daily_rate"]* term * amount) + (df["daily_charge"]* term )

    min_cost = df["cost"].min()

    df = df[df["cost"] == min_cost].sort_values(by = "intrest_rate", ascending=True)

    df = df.drop_duplicates(keep='first')

    # recommended_product_group = df.loc[0, "product_group"]
    # recommended_product_name = df.loc[0, "product_name"]
    # recommended_product_cost = df.loc[0, "cost"]

    # return recommended_product_group, recommended_product_name, recommended_product_cost
    return df
    
    



if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input_amount', type=float, default=5000)
    parser.add_argument('--input_term', type = int, default=1200)

    args = parser.parse_args()

    print(df_runner(args.input_amount, args.input_term))
