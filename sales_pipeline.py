import pandas as pd
import copy

#PHASE 0: SETUP & LOAD

pd.set_option('display.max_columns', None)  # Show ALL columns
pd.set_option('display.width', 1000)        # Wider display


df_raw_data = pd.read_csv('E:\python Scripts\Projects\Data\company_sales_messy.csv')
df_working = df_raw_data.copy(deep=True) #Pandas way

#Display the data
print(f'The Orignal Data: {df_raw_data.to_string()}')
print(f'The Working Data: {df_working.to_string()}')
print()

#PHASE 1: DATA DIAGNOSIS

#1 Checking shape (rows, columns)
#   counting rows and columns
print(df_working.shape) # 50 Rows , 12 Columns
print()
#   checking the data types
print(df_working.dtypes)
print()
                    #data_types [
                            #ID                  int64
                            #Customer_Name      object
                            #Sale_Date          object
                            #Amount_$           object
                            #Product            object
                            #Region             object
                            #Notes              object
                            #Discount_%        float64
                            #Return_Flag        object
                            #Employee_ID        object
                            #Customer_Since     object
                            #Order_Type         object
                    #]

#   cheching missing data
missing_data = df_working.isnull().sum() # .isnull = Creates a DataFrame of True/False       # .sum() = In Python: True = 1, False = 0
print(missing_data[missing_data > 0])    #           True = missing value, False = has value # .sum() counts True values (1's) column-wise

#missing_data = [
#Sale_Date       1
#Product         3
#Notes          13
#Employee_ID     1     
#]

print()

print(df_working.head())
print()

#2 List all column names

print(df_working.columns.tolist())
print()


#PHASE 2: COLUMN CLEANING

#1 Amount_$: Remove $ and commas → convert to float

print(df_working['Amount_$'])
print()
df_working['Amount_$'] = df_working['Amount_$'].str.replace(',', '')
df_working['Amount_$'] = df_working['Amount_$'].str.replace('$', '')
print(df_working['Amount_$'])
print()
df_working['Amount_$'] = df_working['Amount_$'].astype(float)
print(df_working['Amount_$'])
print()

#2 Sale_Date: Handle 7 date formats → proper datetime   #  skipped 

# Displaying the bad data
#print(df_working['Sale_Date'])
#print()
#uniqe_dates = df_working['Sale_Date'].unique()
#print(uniqe_dates)
#print()

#df_working['Sale_Date'] = pd.to_datetime(df_working['Sale_Date'], errors='coerce')
#print(df_working['Sale_Date'])


#3 Region: Standardize (NY→New York, CA→California, etc.)

#displaying the bad data
print(df_working['Region'].unique())
print()

#cleaning
region_map = {
    'NY' : 'New York',
    'NYC': 'New York', 
    'CA' : 'California',
    'DC' : 'Washington DC',
    'TX' : 'Texas',
    'FL' : 'Florida',
    'LA' : 'Los Angeles',
    'MA' : 'Massachusetts'
}

df_working['region_map'] = df_working['Region'].replace(region_map)
print(df_working['region_map'])
print()

del df_working['Region']
print(df_working.to_string())
print()

#rename region_map to just Region
df_working = df_working.rename(columns={'region_map': 'Region'})
print(f"Renamed: region_map → Region")
print()

print("Current columns after rename:", df_working.columns.tolist())
print()

#4 Product: Fill empty → "Unknown", standardize names

#displaying the bad data
print(df_working['Product'])
print()
print(df_working['Product'].unique())
print()

#cleaning
df_working['Product'] = df_working['Product'].replace('', 'Unknown')
df_working['Product'] = df_working['Product'].fillna('Unknown')   
df_working['Product'] = df_working['Product'].replace('Monitor Ultra','Ultra Monitor').replace('Mouse Wireless','Wireless Mouse')
print(df_working['Product'])
print()
print(df_working['Product'].unique())
print()


#5 Discount_%: Handle missing values

#Displaying the bad data
print(df_working['Discount_%']) #dtype: float64
print()

# Find negative discounts (impossible!)
negative = df_working[df_working['Discount_%'] < 0]
print(f"Negative discounts: {len(negative)} rows")
if len(negative) > 0:
    print(negative[['Discount_%']].head())

print()

# Find discounts > 100% (also impossible!)
over_100 = df_working[df_working['Discount_%'] > 100]
print(f"Discounts > 100%: {len(over_100)} rows")
if len(over_100) > 0:
    print(over_100[['Discount_%']].head())

print()

#6 Return_Flag: Ensure only "Y"/"N"

print(df_working['Return_Flag'].unique())
print()
print(df_working['Return_Flag'].value_counts(dropna=False))
print()

#7 Employee_ID: Fill or mark missing

#Displaying the bad data
print(df_working['Employee_ID'].unique())
print()


df_working['Employee_ID'] = df_working['Employee_ID'].fillna('Unknown')
print(df_working['Employee_ID'])
print()
print(df_working['Employee_ID'].value_counts(dropna=False))
print()

#8 Customer_Since: Convert to datetime

#Displaing the bad data
print(df_working['Customer_Since'])
print()

df_working['Customer_Since'] = pd.to_datetime(df_working['Customer_Since'], errors='coerce')
print(df_working['Customer_Since'])
print()
print(df_working['Customer_Since'].dtype)
print()

#9 Order_Type: Check categories

print(df_working['Order_Type'].unique())
print()
print(df_working['Order_Type'].value_counts(dropna=False))
print()


#PHASE 3: DATA VALIDATION

#1 Remove rows with critical missing data

# Before removal
initial_count = len(df_working)
print(f"Initial rows: {initial_count}")

# Remove rows with Amount <= 0
df_working = df_working[df_working['Amount_$'] > 0]

# After removal  
final_count = len(df_working)
removed = initial_count - final_count

print(f"Final rows: {final_count}")
print(f"Removed {removed} invalid sales (Amount <= $0)")

#2 Check/fix duplicates

#Done

#3 Validate value ranges (Amount > 0, etc.)

#None

#4 Cross-check relationships

#Done


#Displaing all data
print(df_working.to_string())
print()

#PHASE 4: ANALYSIS QUESTIONS

#1 Total sales by region

print(df_working['Amount_$'].sum(numeric_only=True))
print()

total_sal_region = df_working.groupby('Region')['Amount_$'].sum()
print(total_sal_region)
print()


#2 Monthly sales trend

#skipped till i finish Sale_Date handle


#3 Return rate analysis

#Percentage of orders that were returned

#count return orders
return_orders = (df_working['Return_Flag'] == 'Y').sum()
print(f'Total return order:{return_orders}')
print()

#count total orders
total_orders = len(df_working)
print(f'Total orders')
print()

per_orders_returned = return_orders / total_orders * 100
print(f'Percentage of orders that were returned : {per_orders_returned}%')
print()

#Which region has highest return rate

count_regions = df_working.groupby('Region').size() # count each city
returned = df_working[df_working['Return_Flag'] == 'Y'] #count order that returned
ret_by_reg = returned.groupby('Region').size() # count each return by city

per_ret_by_reg = ret_by_reg / count_regions * 100
print(f'Percentage of return by cities:{per_ret_by_reg}')
print()

#Which product gets returned most

#count products
all_products = df_working.groupby('Product').size()
print(all_products)
print()

returned_df = df_working[df_working['Return_Flag'] == 'Y']
returned_by_product = returned_df.groupby('Product').size()

per_products = returned_by_product / all_products  * 100
print(per_products)
print()

#4 Top 5 customers by spending

customer_spending = df_working.groupby('Customer_Name')['Amount_$'].sum()
top_5_customers = customer_spending.sort_values(ascending=False)
print(f'Top 5 cutomers : {top_5_customers.head(5)}')
print()

#5 Discount impact on sales

with_discount = df_working[df_working['Discount_%'] > 0]
no_discount = df_working[df_working['Discount_%'] == 0]

# Average sale WITH discount
avg_with_discount = with_discount['Amount_$'].mean()

# Average sale WITHOUT discount  
avg_no_discount = no_discount['Amount_$'].mean()

print(f'Average sale WITH discount: ${avg_with_discount}')
print(f'Average sale WITHOUT discount: ${avg_no_discount}')
print()

#6 Employee performance ranking

emp_id_sal = df_working.groupby('Employee_ID')['Amount_$'].sum()
top_5_emp = emp_id_sal.sort_values(ascending=False)
print(f'Top 5 Employees:{top_5_emp.head(5)}')

#7 Order type distribution

order_type_shii = df_working.groupby('Order_Type').size()
print(order_type_shii)
print()

#Percentage for each type shii

per_type_shii = order_type_shii / total_orders * 100
print(f'Order type DISTRIBUTION Percentage : {per_type_shii}')

#PHASE 5: OUTPUT

#1 Save cleaned data to new CSV

df_working.to_csv('sales_cleaned_final.csv', index=False)

#2 Generate summary report

print("="*60)
print("SALES DATA ANALYSIS REPORT")
print("="*60)
print(f"Date: {pd.Timestamp.today().date()}")
print(f"Records analyzed: {len(df_working)}")
print()

print("KEY FINDINGS:")
print(f"1. Overall return rate: {per_orders_returned:.1f}%")
print(f"2. Worst return region: {per_ret_by_reg.idxmax()} ({per_ret_by_reg.max():.1f}%)")
print(f"3. Top customer: {top_5_customers.index[0]} (${top_5_customers.iloc[0]:,.2f})")
print(f"4. Top employee: {top_5_emp.index[0]} (${top_5_emp.iloc[0]:,.2f})")
print(f"5. Most common order type: {order_type_shii.idxmax()} ({per_type_shii.max():.1f}%)")
