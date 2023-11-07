import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

state_codes = {}
with open('state_codes-1.txt', 'r') as f:
    for line in f:
        code, state = line.strip().split(',')
        state_codes[state.title()] = code

counties_by_state = {}
with open('counties.txt', 'r') as f:
    current_state = None
    for line in f:
        if line.strip() and not line.startswith('\t'):
            current_state = state_codes[line.strip().title()]
            counties_by_state[current_state] = []
        elif line.startswith('\t'):
            counties_by_state[current_state].append(line.strip())


print("Loading data...\n")
epa_data = pd.read_csv('daily_44201_2021.csv', parse_dates=['Date Local'], low_memory=False)

while True:
    state_code = input("\nEnter 2-letter state code (Q to quit): ").upper()
    
    if state_code == 'Q':
        break

    if state_code not in state_codes.values():
        print("Invalid state code. Try again.")
        continue

    state_name = [k for k, v in state_codes.items() if v == state_code][0]

    for idx, county in enumerate(counties_by_state[state_code], start=1):
        print(f"{idx}: {county}\n")

    while True:
        county_num = input("Enter number for county: ")
        if not county_num.isdigit() or int(county_num) not in range(1, len(counties_by_state[state_code]) + 1):
            print("Invalid selection. Please try again.")
            continue

        county = counties_by_state[state_code][int(county_num) - 1]

        filtered_data = epa_data[(epa_data['State Name'] == state_name) & (epa_data['County Name'] == county)]
        filtered_data = filtered_data.sort_values(by='Date Local')

        average_aqi = filtered_data['AQI'].mean()

        plot_color = 'green' if average_aqi <= 50 else 'red'

        plt.figure(figsize=(10, 5))
        plt.plot(filtered_data['Date Local'], filtered_data['AQI'], color=plot_color)
        plt.title(f"{county} County, {state_name} (avg. AQI: {round(average_aqi)})")
        plt.ylabel('AQI')

        plt.tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False) 

        choice = input("\nChoose destination for plot:\n\n\t1. Screen\n\n\t2. File\n")
        if choice == '1':
            plt.show()
        elif choice == '2':
            filename = input("\nEnter file with extension of jpg|png|pdf: ")
            plt.savefig(filename)
        else:
            print("Invalid choice. Try again.")
            continue

        another_county = input(f"\nAnother {state_name} county? (y/n): ")

        if another_county.lower() == 'y':
            print()
            for idx, county in enumerate(counties_by_state[state_code], start=1):
                print(f"{idx}: {county}\n")
            plt.clf()
            plt.close()
            continue
        else:
            break

print("Goodbye!")