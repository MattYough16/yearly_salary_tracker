import pandas as pd 
from datetime import date

class salary_calculator:

    def enter_amount(self, amount, bincome, bmakeup, best, bbar):
        amount = float(amount)
        salary_df = pd.read_excel('salary_data.xlsx')

        try:
            salary_df.drop(columns={'Unnamed: 0'}, inplace=True)
        except:
            pass

        if not bincome:
            amount = amount*-1

        salary_dict = {'makeup': [0], 'bartending': [0], 'esthetician': [0], 'year': [0]}
        if bmakeup:
            salary_dict['makeup'] = [amount]
        elif bbar:
            salary_dict['bartending'] = [amount]
        elif best:
            salary_dict['esthetician'] = [amount]

        salary_dict['year'] = date.today().year

        new_df = pd.DataFrame(salary_dict)
        salary_df = pd.concat([salary_df, new_df])
        salary_df.reset_index(drop=True, inplace=True)
        salary_df.to_excel('salary_data.xlsx')

        return "Entry Added"
    
    def calc_salary(self, bnet, bgross, year):
        
        year = int(year)
        salary_df = pd.read_excel('salary_data.xlsx')

        try:
            salary_df.drop(columns={'Unnamed: 0'}, inplace=True)
        except:
            pass

        if bnet:
            salary_df = salary_df[salary_df['year'] == year]
            salary = salary_df['makeup'].sum() + salary_df['bartending'].sum() + salary_df['esthetician'].sum()
        elif bgross:
            salary_df = salary_df[salary_df['year'] == year]
            salary_df = salary_df[salary_df['makeup'] >= 0]
            salary_df = salary_df[salary_df['bartending'] >= 0]
            salary_df = salary_df[salary_df['esthetician'] >= 0]

            salary = salary_df['makeup'].sum() + salary_df['bartending'].sum() + salary_df['esthetician'].sum()

        return str(salary)

