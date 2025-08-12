
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm # To import colormaps
import numpy as np
import os

os.system('clear')

data_left = pd.read_csv('/Users/deveshdarji/Desktop/Semester 3/Health Analytics/Final Project/one_hot_encoded_PhysicalEffects.csv')
data_not_oneHot = pd.read_csv('/Users/deveshdarji/Desktop/Semester 3/Health Analytics/Final Project/BinaryData_V1.csv')

data_not_oneHot.columns






def map_response_inplace(df, column_name):
    """
    Remaps values in a specified column of a DataFrame in-place.
    'yes' becomes 1, 'no' becomes -1, 'not mentioned' becomes 0,
    and empty cells become 'N/A'. Handles case-insensitivity for 'yes' and 'no'.

    Args:
        df (pd.DataFrame): The input DataFrame to modify.
        column_name (str): The name of the column to modify.

    Returns:
        None: The DataFrame is modified directly. Returns None if an input error occurs.
    """
    # --- Input Validation ---
    if not isinstance(df, pd.DataFrame):
        print("Error: Input 'df' must be a pandas DataFrame.")
        return None
    if not isinstance(column_name, str):
        print("Error: Input 'column_name' must be a string.")
        return None
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in the DataFrame.")
        print(f"Available columns: {list(df.columns)}")
        return None # Indicate failure clearly

    # --- Processing ---
    try:
        print(f"Processing column: '{column_name}' in-place...")

        # Define the mapping: lowercase keys to target values
        mapping = {'yes': 1, 'no': -1, 'yes then no': -1, 'not mentioned': 0}

        # Apply the mapping
        df[column_name] = (df[column_name]
                           .astype(str)
                           .str.lower()
                           .replace('nan', np.nan, regex=False) # Handle potential 'nan' strings
                           .map(mapping)
                          )

        # Handle empty cells (which might be represented as empty strings or NaN after the map)
        df[column_name] = df[column_name].fillna('N/A')
        df.loc[df[column_name].astype(str).str.strip() == '', column_name] = 'N/A'

        # Attempt to convert to a numeric type where possible (excluding 'N/A')
        numeric_values = pd.to_numeric(df[column_name], errors='coerce')
        if numeric_values.notna().all():
            try:
                df[column_name] = numeric_values.astype('Int64')
                print(f"Column '{column_name}' converted to Int64 (nullable integer).")
            except (ValueError, TypeError):
                print(f"Column '{column_name}' kept as numeric (float).")
        else:
            print(f"Column '{column_name}' contains non-numeric values ('N/A'), keeping as object type.")

        print("Mapping complete (in-place).")

    except Exception as e:
        print(f"An unexpected error occurred during processing column '{column_name}': {e}")
        return None # Return None on unexpected errors


def one_hot_encode_comma_separated(df, column_name):
  """
  Performs one-hot encoding on a DataFrame column containing comma-separated values.

  Args:
    df (pd.DataFrame): The input DataFrame.
    column_name (str): The name of the column containing comma-separated strings
                       that needs to be one-hot encoded.

  Returns:
    pd.DataFrame: A new DataFrame containing the one-hot encoded columns.
                  Column names are derived from the unique values found after
                  splitting and stripping whitespace. Returns an empty DataFrame
                  if the specified column doesn't exist or if there are issues.
  """
  if column_name not in df.columns:
      print(f"Error: Column '{column_name}' not found in the DataFrame.")
      return pd.DataFrame() # Return an empty DataFrame

  try:
    # Ensure the column is treated as string and fill potential NaNs with empty strings
    # This prevents errors if there are missing values
    series_to_encode = df[column_name].astype(str).fillna('')

    # Use str.get_dummies() which splits the string by the separator (',')
    # and creates the one-hot encoded columns directly.
    # It automatically handles finding unique values and creating columns.
    one_hot_encoded_df = series_to_encode.str.get_dummies(sep=',')

    # Clean up column names by stripping potential leading/trailing whitespace
    # that might have been present in the original data next to commas.
    one_hot_encoded_df.columns = one_hot_encoded_df.columns.str.strip()

    # Optional: Remove column corresponding to empty string if it was created
    if '' in one_hot_encoded_df.columns:
        one_hot_encoded_df = one_hot_encoded_df.drop(columns=[''])

    return one_hot_encoded_df

  except Exception as e:
      print(f"An error occurred during one-hot encoding: {e}")
      return pd.DataFrame()

def summarize_one_hot_counts(df_one_hot, sort_descending=True):
  """
  Calculates the number of 1s in each column of a one-hot encoded DataFrame.

  Args:
    df_one_hot (pd.DataFrame): The input DataFrame assumed to contain
                               one-hot encoded columns (0s and 1s).
    sort_descending (bool, optional): If True, sorts the output table by
                                      count in descending order.
                                      Defaults to True.

  Returns:
    pd.DataFrame: A DataFrame with two columns: 'Category' (original column names)
                  and 'Count' (number of 1s in that column). Returns an empty
                  DataFrame if the input is not a valid DataFrame or is empty.
  """
  # Input validation
  if not isinstance(df_one_hot, pd.DataFrame):
      print("Error: Input must be a pandas DataFrame.")
      return pd.DataFrame(columns=['Category', 'Count'])
  if df_one_hot.empty:
      print("Input DataFrame is empty.")
      return pd.DataFrame(columns=['Category', 'Count'])

  try:
      # Sum each column (axis=0). This counts the 1s efficiently.
      # We assume columns are numeric (0s and 1s).
      # If columns could contain non-numeric data, add error handling or conversion.
      category_counts = df_one_hot.sum(axis=0)

      # Convert the resulting Series to a DataFrame
      summary_df = category_counts.reset_index()

      # Rename the columns for clarity
      summary_df.columns = ['Category', 'Count']

      # Ensure the 'Count' column is integer type
      summary_df['Count'] = summary_df['Count'].astype(int)

      # Sort the DataFrame if requested
      if sort_descending:
          summary_df = summary_df.sort_values(by='Count', ascending=False)

      # Reset index after sorting (optional, for cleaner output)
      summary_df = summary_df.reset_index(drop=True)

      return summary_df

  except Exception as e:
      print(f"An error occurred during calculation: {e}")
      return pd.DataFrame(columns=['Category', 'Count'])


col_to_encode = 'What was the stated reason for starting antidepressants? Has the user mentioned it?_desc'


one_hot_df = one_hot_encode_comma_separated(data_not_oneHot, col_to_encode)


one_hot_df.columns

summary_table = summarize_one_hot_counts(one_hot_df)

summary_table
summary_table.to_csv('/Users/deveshdarji/Desktop/Semester 3/Health Analytics/Final Project/Medication_Start_summary_table.csv', index=False)


#combined_df = pd.concat([data_left, one_hot_df], axis=1)
# combined_df = combined_df.drop(columns=[col_to_encode])
# combined_df.to_csv('/Users/deveshdarji/Desktop/Semester 3/Health Analytics/Final Project/one_hot_encoded_PhysicalEffects.csv', index=False)


def plot_pie_chart_from_column(
    df,
    column_name,
    label_map=None,
    title=None,
    colors=None,
    explode_slice=None, # Index of the slice to explode (e.g., 0 for the first/largest)
    figsize=(10, 7)
):
    """
    Generates and displays a visually appealing pie chart for the distribution
    of values in a specified DataFrame column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column whose distribution to plot.
        label_map (dict, optional): A dictionary mapping values in the column
                                     to display labels (e.g., {1: 'Yes', 0: 'No'}).
                                     Defaults to None (uses original values as labels).
        title (str, optional): The title for the pie chart. Defaults to a generated
                               title based on the column name.
        colors (list or str, optional): A list of color codes or a matplotlib
                                        colormap name (e.g., 'viridis').
                                        Defaults to None (uses a default colormap).
        explode_slice (int, optional): The index of the slice to 'explode' slightly
                                       (0 is the largest slice based on value_counts).
                                       Defaults to None (no slice exploded).
        figsize (tuple, optional): The size of the figure (width, height).
                                   Defaults to (10, 7).
    """
    # --- Input Validation ---
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in the DataFrame.")
        return

    # --- Calculate Value Counts ---
    value_counts = df[column_name].value_counts()

    if value_counts.empty:
        print(f"No data found in column '{column_name}' to plot.")
        return

    # --- Prepare Data for Plotting ---
    sizes = value_counts.values

    # Prepare Labels
    if label_map:
        # Use the map, handling potential missing keys gracefully
        labels = [label_map.get(x, f'Other ({x})') for x in value_counts.index]
    else:
        # Use the original values as labels if no map provided
        labels = value_counts.index.astype(str).tolist()

    # Prepare Colors
    num_slices = len(labels)
    if isinstance(colors, list) and len(colors) >= num_slices:
        plot_colors = colors[:num_slices] # Use provided list
    elif isinstance(colors, str):
        try:
            colormap = cm.get_cmap(colors) # Use specified colormap name
            plot_colors = colormap(np.linspace(0.2, 0.9, num_slices))
        except ValueError:
            print(f"Warning: Colormap '{colors}' not recognized. Using default.")
            plot_colors = cm.viridis(np.linspace(0.3, 0.9, num_slices)) # Default fallback
    else:
        # Default colors using a colormap
        plot_colors = cm.viridis(np.linspace(0.3, 0.9, num_slices))

    # Prepare Explode
    explode = [0] * num_slices
    if explode_slice is not None and 0 <= explode_slice < num_slices:
        explode[explode_slice] = 0.1 # Explode the specified slice

    # Prepare Title
    if title is None:
        # Generate a default title
        clean_col_name = column_name.replace("_flag","").replace("_", " ")
        title = f'Distribution of:\n{clean_col_name}'

    # --- Create and Customize the Pie Chart ---
    fig, ax = plt.subplots(figsize=figsize)

    ax.pie(sizes,
           explode=explode,
           labels=labels,
           colors=plot_colors,
           autopct='%1.1f%%',
           shadow=True,
           startangle=140,
           pctdistance=0.85,
           labeldistance=1.1
           )

    ax.set_title(title, fontsize=14, pad=20)
    ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()
    plt.show()







#     print("\n--- Plot 2: Customized Usage ---")
custom_labels = {
    1: 'Yes',
    0: 'Not mentioned',
    -1: 'No',
}

#fdb462 (Soft Orange)
#b3e2cd (Minty Green)
#cbd5e8 (Lavender Blue)
custom_colors = ['#fc8d62','#e5c494','#ffd92f'] # Light red, blue, green

plot_pie_chart_from_column(
    df=data_not_oneHot,
    column_name='After stopping antidepressants, did the user experience withdrawal symptoms?_flag',
    label_map=custom_labels,
    title='Withdrawal Symptoms Reported by Speakers',
    colors=custom_colors, # Can also use a colormap name like 'plasma'
    explode_slice=0 # Explode the largest slice (index 0)
)



