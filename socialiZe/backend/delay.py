import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Names you can change
csv_file = 'frame_log_20240215_192408.csv'
fps = 30


def plot_fps_interval_delay(csv_file, fps):
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate the difference in time between successive frames
    df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
    
    # Calculate cumulative sum to get the real time in seconds from the start
    df['cumulative_time'] = df['time_diff'].cumsum()
    
    # Select every <fps>th frame to calculate interval delay
    interval_index = np.arange(0, len(df), fps)
    selected_timestamps = df.iloc[interval_index]
    
    # Calculate the delay between these intervals
    selected_timestamps['interval_delay'] = selected_timestamps['cumulative_time'].diff().fillna(0)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(selected_timestamps.index, selected_timestamps['interval_delay'], marker='o', linestyle='-')
    plt.title('Delay Between Every {} Frames'.format(fps))
    plt.xlabel('Frame Number')
    plt.ylabel('Interval Delay (seconds)')
    plt.grid(True)
    plt.show()


plot_fps_interval_delay(csv_file, fps)

