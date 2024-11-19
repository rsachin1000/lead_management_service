import pandas as pd


if __name__ == '__main__':
    path = 'scripts/leads_data.csv'

    df = pd.read_csv(path)
    


    print(df.head())

