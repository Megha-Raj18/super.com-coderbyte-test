import pandas as pd
import re

def main():

    data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'
    rows = data.split('\n') # getting each individual row for the table
    columns = rows[0].split(';') # im getting the column information from the first row of the stringified table here

    column_vals = []
    for r in range(1, len(rows)): # getting all the comlumn values separately and printing them out just to see what were working with
        col = []
        for c in range(len(rows[r].split(';'))):
            column_value = rows[r].split(';')[c]
            col.append(column_value) # appending each individual column value to a list
            
        column_vals.append(col) #appending each column to a list column_vals which has all column values for the table
    column_vals.pop() # removing the last entry since its empty anyways

    # creating the dataframe. its still dirty though :(
    df = pd.DataFrame((column_vals), columns = columns)
    df['FlightCodes'] = pd.to_numeric(df['FlightCodes'], errors = 'coerce')

    #creating a function to clean up Airline codes using regex expressions
    def clean_up(line):
        return re.sub(r'[^a-zA-Z\s]', '', line).strip()

    df['Airline Code'] = df['Airline Code'].apply(clean_up)

    #function to fill in the missing flight code values
    def fill_missing_codes(df, col):
        for i in range(1, len(df)):
            if pd.isna(df[col].iloc[i]) : #if value in any cell is empty
                df[col].iloc[i] = df[col].iloc[i - 1] + 10 # fill in empty spots with the previous cell value incremented by 10 as requested
        return df

    df = fill_missing_codes(df, 'FlightCodes')

    df['FlightCodes'] = df['FlightCodes'].astype(int)

    df['To_From'] = df['To_From'].apply(str.upper) # make the city names capital for readability

    # separate to_from column

    df[['To','From']] = df["To_From"].str.split('_', expand = True)
    df.drop(columns = ["To_From"], inplace = True)
    print (df)

if __name__ == "__main__":
    main()