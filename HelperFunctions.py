
#def get_df_name(df):
#    """
#    returns the name of the pandas dataframe
#    """
#    name =[x for x in globals() if globals()[x] is df][0]
#    return name


def print_null_Count(df):
    """
    df : input data frame 
    function prints the count of null values in each column
    """
    #name = get_df_name(df)
    print("Null values  :","\n",df.isnull().sum().sum())
    
def replace_null(df,col):
    """
    df:input data fram
    col : column name, that needs to be replaced
    function returns data frame after replacing null values in col with 0
    
    """
    df[col] = df[col].fillna(0)
    #df.describe()
    return df

def rename_colum(df,col,newcol):
    """
    df:input data fram
    col : column name, that needs to be renamed
    newcol : new column name
    function returns data frame after renaming the column
    
    """
    df = df.rename(columns={col: newcol})
    print(df.head(1))
    return df