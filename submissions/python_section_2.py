from datetime import time

import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    # Extract unique IDs to create the distance matrix
    unique_ids = pd.concat([df['from_id'], df['to_id']]).unique()
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)

    # Populate the distance matrix with known distances
    for _, row in df.iterrows():
        from_id = row['from_id']
        to_id = row['to_id']
        distance = row['distance']

        # Set the distance for both directions
        distance_matrix.at[from_id, to_id] = distance
        distance_matrix.at[to_id, from_id] = distance  # Symmetric entry

    # Compute cumulative distances (Floyd-Warshall algorithm for all pairs shortest path)
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, j] > distance_matrix.at[i, k] + distance_matrix.at[k, j]:
                    distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix

    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_data = []

    # Iterate over rows and columns (id_start and id_end) in the matrix
    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end:  # Exclude cases where id_start equals id_end
                distance = df.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Convert the unrolled data into a DataFrame
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df




def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type
    for vehicle, rate in rates.items():
        df[vehicle] = df['distance'] * rate
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Initialize columns for start and end days/times
    df['start_day'] = pd.Series(days_of_week * (len(df) // 7) + days_of_week[:len(df) % 7])
    df['end_day'] = df['start_day']  # For simplicity, use the same day for start and end in this example
    df['start_time'] = time(0, 0)  # Start of the day
    df['end_time'] = time(23, 59)  # End of the day

    # Apply discount factors based on time intervals
    def calculate_discount(row):
        day = row['start_day']
        if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:  # Weekdays
            if row['start_time'] >= time(0, 0) and row['start_time'] < time(10, 0):
                discount_factor = 0.8
            elif row['start_time'] >= time(10, 0) and row['start_time'] < time(18, 0):
                discount_factor = 1.2
            else:  # 18:00 to 23:59
                discount_factor = 0.8
        else:  # Weekends
            discount_factor = 0.7

        # Adjust vehicle rates based on the discount factor
        for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
            row[vehicle] *= discount_factor

        return row

    # Apply the discount calculation to each row
    df = df.apply(calculate_discount, axis=1)

    return df