import os
import re
import pandas as pd

def divisions_column(file, division_name):
    """
    Adds the actual division name of the teams in the file since
    the files don't provide them.
    """

    headers = [*pd.read_csv(file,encoding = 'ISO-8859-1', nrows=1)]

    df = pd.read_csv(file, encoding="ISO-8859-1", sep=',', usecols=[c for c in headers if c != 'Referee'])

    df['division'] = str(division_name)
    df.to_csv(file, index = False)

    print('Completed process for:' + str(file))

def add_division_names(path):
    """
    This function will loop through a given directory with all of the scraped
    files. From there it will use if/else statements (not great)
    to add specific division names
    to the specific CSV's
    :param path: directory path
    :return: CSV's with divisional data
    """

    for subdir, dirs, files in os.walk(path):
        print('Working on Directory: ' + str(subdir.split('\\')[-1:][0].title()))
        for file in files:
            if 'E0' in str(file):
                divisions_column(os.path.join(subdir, file), 'Premier League')
            elif 'E1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Championship')
            elif 'SC0' in str(file):
                divisions_column(os.path.join(subdir, file), 'Scottish Premiership')
            elif 'SC1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Scottish Championship')
            elif 'D1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Bundesliga 1')
            elif 'D2' in str(file):
                divisions_column(os.path.join(subdir, file), 'Bundesliga 2')
            elif 'I1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Serie A')
            elif 'I2' in str(file):
                divisions_column(os.path.join(subdir, file), 'Serie B')
            elif 'SP1' in str(file):
                divisions_column(os.path.join(subdir, file), 'La Liga')
            elif 'SP2' in str(file):
                divisions_column(os.path.join(subdir, file), 'Segunda Division')
            elif 'F1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Ligue 1')
            elif 'F2' in str(file):
                divisions_column(os.path.join(subdir, file), 'Ligue 2')
            elif 'N1' in str(file):
                divisions_column(os.path.join(subdir, file),'Eredivisie')
            elif 'B1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Belgium First Division A')
            elif 'P1' in str(file):
                divisions_column(os.path.join(subdir, file), 'Primeira Liga')


def create_seasons(path):
    """
    The files that we've scraped for aren't necessarily in the best shape (datetime wise).
    So what i'm going to do in this function is to create a season column.
    I.E (2018/2019) season.
    :param path: Where the files live on your PC
    :return: cleaned CSV's
    """

    for subdir, dirs, files in os.walk(path):
        print('Working on Directory: ' + str(subdir.split('\\')[-1:][0].title()))
        for file in files:
            print(os.path.join(subdir, file))
            try:
                headers = [*pd.read_csv(os.path.join(subdir, file),encoding = 'ISO-8859-1', nrows=1)]
                df = pd.read_csv(os.path.join(subdir, file), encoding="ISO-8859-1", sep=',',
                                 usecols=[c for c in headers if c != ['Referee']])
                df = df.rename(columns = {'AS': 'AAS'})
                df = df[~df['Date'].isnull()]
                real_dates = []
                m = '\d+'

                for index, row in df.iterrows():
                    x = re.findall(m, row['Date'])
                    x = int(x[1])
                    if x >= 8:
                        year1 = int(row['Date'][-2:]) + 2000
                        year2 = year1 + 1
                        real_dates.append(str(year1) + "/" + str(year2))
                    elif x <= 5:
                        year1 = int(row['Date'][-2:]) + 2000
                        year2 = year1 - 1
                        real_dates.append(str(year2) + "/" + str(year1))
                    else:
                        real_dates.append(0)

                df['season'] = real_dates
                df.to_csv(os.path.join(subdir, file), index=False)

            except Exception as e:
                print('Looks like something broke! ' + str(e))

def choose_columns(path):
    """
    We only want a certain set of columns for our warehouse so here we subset the data
    """
    for subdir, dirs, files in os.walk(path):
        print('Working on Directory: ' + str(subdir.split('\\')[-1:][0].title()))
        for file in files:
            print(os.path.join(subdir, file))
            df = pd.read_csv(os.path.join(subdir, file), encoding="ISO-8859-1", sep=',')
            df = df.loc[:, df.columns.isin(['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG','HTR',
                                'HS', 'AAS', 'HST', 'AST','HF', 'AF', 'HFKC', 'AFKC', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR',
                                            'season', 'division'])]
            df.columns = map(str.lower, df.columns)
            df.to_csv(os.path.join(subdir, file), index=False)


def rename_file(path):
    """
    I found that there was an issue with some of the file names when actually uploading them into
    the Redshift cluster. So this renames the file if they are only (B1) (D1) (E1) etc.
    """
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if len(file.split(' ')) == 1:
                print(file)
                newfile = file[:2] + ' ' + str(file)
                os.rename(os.path.join(subdir, file), os.path.join(subdir, newfile))
            else:
                pass

