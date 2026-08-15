import time
import pandas as pd


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Ask the user to specify a city, month, and day to analyze.

    Returns:
        city: Enter Name of the city to analyze.
        month: Enter Month to filter by, or "all" for no month filter.
        day: Enter Day of the week to filter by, or "all" for no day filter.
    """
    print("Hello! Let's explore some US bikeshare data!")

    valid_cities = [
        'chicago',
        'new york city',
        'washington'
    ]

    while True:
        city = input(
            "\nEnter a city: Chicago, New York City, or Washington.\n"
        ).strip().lower()

        if city in valid_cities:
            break

        print(
            "Invalid city. Please enter Chicago, "
            "New York City, or Washington."
        )

    valid_months = [
        'all',
        'january',
        'february',
        'march',
        'april',
        'may',
        'june'
    ]

    while True:
        month = input(
            "\nEnter a month: January, February, March, "
            "April, May, June, or All.\n"
        ).strip().lower()

        if month in valid_months:
            break

        print(
            "Invalid month. Please enter a month "
            "from January to June, or All."
        )

    valid_days = [
        'all',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
    ]

    while True:
        day = input(
            "\nEnter a day of the week, or enter All.\n"
        ).strip().lower()

        if day in valid_days:
            break

        print(
            "Invalid day. Please enter Monday through Sunday, "
            "or All."
        )

    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Load data for the selected city and apply month and day filters.

    Args:
        city: Name of the city to analyze.
        month: Month to filter by, or "all".
        day: Day of the week to filter by, or "all".

    Returns:
        A pandas DataFrame containing the filtered city data.
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = [
            'january',
            'february',
            'march',
            'april',
            'may',
            'june'
        ]

        month_number = months.index(month) + 1
        df = df[df['month'] == month_number]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Display statistics on the most frequent travel times."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if df.empty:
        print("No travel data is available for the selected filters.")
    else:
        month_names = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ]

        most_common_month_number = int(
            df['month'].mode().iloc[0]
        )

        most_common_month = month_names[
            most_common_month_number - 1
        ]

        print("Most common month:", most_common_month)

        most_common_day = df['day_of_week'].mode().iloc[0]
        print("Most common day of week:", most_common_day)

        most_common_hour = int(df['hour'].mode().iloc[0])
        print("Most common start hour:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if df.empty:
        print("No station data is available for the selected filters.")
    else:
        most_common_start_station = (
            df['Start Station'].mode().iloc[0]
        )

        print(
            "Most commonly used start station:",
            most_common_start_station
        )

        most_common_end_station = (
            df['End Station'].mode().iloc[0]
        )

        print(
            "Most commonly used end station:",
            most_common_end_station
        )

        most_common_trip = (
            df.groupby(['Start Station', 'End Station'])
            .size()
            .idxmax()
        )

        print(
            "Most frequent start and end station combination:",
            most_common_trip[0],
            "to",
            most_common_trip[1]
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Display statistics on total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if df.empty:
        print(
            "No trip duration data is available "
            "for the selected filters."
        )
    else:
        total_travel_time = df['Trip Duration'].sum()
        print("Total travel time:", total_travel_time, "seconds")

        mean_travel_time = df['Trip Duration'].mean()
        print("Mean travel time:", mean_travel_time, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Display statistics about bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if df.empty:
        print("No user data is available for the selected filters.")
    else:
        if 'User Type' in df.columns:
            print("Counts of user types:")
            print(df['User Type'].value_counts())
        else:
            print("User Type data is not available.")

        if 'Gender' in df.columns:
            print("\nCounts of gender:")
            print(df['Gender'].value_counts())
        else:
            print("\nGender data is not available for this city.")

        if 'Birth Year' in df.columns:
            birth_years = df['Birth Year'].dropna()

            if not birth_years.empty:
                earliest_birth_year = int(birth_years.min())
                most_recent_birth_year = int(birth_years.max())
                most_common_birth_year = int(
                    birth_years.mode().iloc[0]
                )

                print(
                    "\nEarliest year of birth:",
                    earliest_birth_year
                )

                print(
                    "Most recent year of birth:",
                    most_recent_birth_year
                )

                print(
                    "Most common year of birth:",
                    most_common_birth_year
                )
            else:
                print("\nBirth Year data is empty.")
        else:
            print("\nBirth Year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """
    Display five rows of raw data at a time when requested.

    The user can continue requesting the next five rows until the
    user enters "no" or no additional rows remain.
    """
    print('\nRaw Data Display\n')

    if df.empty:
        print("No raw data is available for the selected filters.")
        print('-' * 40)
        return

    start_index = 0
    rows_per_display = 5

    while start_index < len(df):
        while True:
            response = input(
                "Would you like to see 5 lines of raw data? "
                "Enter yes or no.\n"
            ).strip().lower()

            if response in ['yes', 'no']:
                break

            print("Invalid input. Please enter yes or no.")

        if response == 'no':
            print("Raw data display stopped.")
            break

        end_index = start_index + rows_per_display

        print(
            "\nDisplaying raw data rows {} to {}:\n".format(
                start_index + 1,
                min(end_index, len(df))
            )
        )

        print(df.iloc[start_index:end_index])

        start_index = end_index

        if start_index >= len(df):
            print("\nThere is no more raw data to display.")
            break

    print('-' * 40)


def get_restart_choice():
    """Ask whether the user wants to restart the program."""

    while True:
        restart = input(
            "\nWould you like to restart? Enter yes or no.\n"
        ).strip().lower()

        if restart in ['yes', 'no']:
            return restart

        print("Invalid input. Please enter yes or no.")


def main():
    """Run the US Bikeshare data analysis program."""

    while True:
        city, month, day = get_filters()

        try:
            df = load_data(city, month, day)
        except FileNotFoundError:
            print(
                "\nThe required CSV file was not found. "
                "Make sure the CSV files are in the same folder "
                "as this Python file."
            )
            break
        except KeyError as error:
            print(
                "\nA required column is missing from the data file:",
                error
            )
            break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = get_restart_choice()

        if restart == 'no':
            print("\nThank you for using the US Bikeshare program!")
            break


if __name__ == "__main__":
    main()