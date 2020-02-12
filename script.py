import pandas as pd
import argparse
import sqlalchemy

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


def cost_of_loan(amount, term_in_days, apr):

    daily_rate = apr/ 100 / 365 

    daily_cost = amount * term_in_days * daily_rate

    return daily_cost


def calculate(amount, term):

    if amount <= 1200:
        recommendation = 'pca'

    elif amount > 1200 and term <= 30:
        recommendation = 'credit_card'
    
    else :
        recommendation = 'loan'

    return recommendation


def main_runner(input_amount, input_term):


    recommended_product = calculate(input_amount, input_term)

    # if recommended_product in ['loan', 'credit_card']:
        
    cost = cost_of_loan(input_amount, input_term, apr = 5 )

    print("Recommended Product: ", recommended_product)
    print("Cost of loan: ", cost)


if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--input_amount', type=float, default=500)
    parser.add_argument('--input_term', type = int, default=30)

    args = parser.parse_args()

    main_runner(args.input_amount, args.input_term)
