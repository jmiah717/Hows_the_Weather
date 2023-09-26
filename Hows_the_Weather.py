from tkinter import *
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os
from PIL import ImageTk, Image
import datetime
from state_conversion import state_abbrev
from Exception_Classes import InvalidUserInput, APIError, IndexError


class Weather:
    """
    Weather application for displaying weather information based on user input.

    This application allows users to enter a city and state (and optionally a country) to retrieve current weather information for that location. It uses the OpenWeatherMap API to fetch weather data, including temperature, humidity, sunrise, and sunset times. The application displays weather icons corresponding to the current weather condition.

    Args:
        root (Tk): The root Tkinter window for the application.

    Attributes:
        root (Tk): The root Tkinter window.
        font_1 (tuple): Font settings for smaller text.
        font_2 (tuple): Font settings for larger text.
        font_3 (tuple): Font settings for additional text.
        text (Entry): Input field for entering the location.
        label_1 (Label): Label for displaying the entered location.
        label_2 (Label): Label for displaying current weather information.
        label_3 (Label): Label for displaying additional weather information.
        picture_frame (Frame): Frame for displaying weather icons.
        city (str): The entered city.
        state (str): The entered state.
        country (str): The entered country (optional).
        weather_icons (dict): A dictionary mapping weather conditions to icon paths.
        weather_labels (dict): A dictionary of labels for displaying weather icons.

    Methods:
        getLatLong(city, state, country="") -> tuple:
            Retrieve latitude and longitude coordinates for a given location.

        getWeather(event):
            Fetch weather data from the OpenWeatherMap API and update the display.

        is_night(sunrise, sunset, current_time, tz_offset) -> bool:
            Determine if it is currently night or day in the searched location.

        clear_labels():
            Clear the weather icon labels.

        getOutput(weather, json, sunrise, sunset, current_time, timezone_offset):
            Update the labels with weather information based on current conditions.

    Example:
        root = Tk()
        application = Weather(root)
        root.mainloop()
    """

    def __init__(self, root):
        self.root = root
        self.root.configure(bg="lightskyblue1")
        self.root.geometry("800x500")
        self.root.title("How's the Weather?")

        self.font_1 = "tahoma", 15, "bold"
        self.font_2 = "tahoma", 35, "bold"
        self.font_3 = "tahoma", 13

        self.text = Entry(self.root, font=self.font_1)
        self.text.pack()
        self.text.focus()
        self.text.bind("<Return>", self.getWeather)

        self.label_1 = Label(self.root, font=self.font_2, text="City, State")
        self.label_1.configure(bg="lightskyblue1")
        self.label_1.pack()

        self.label_2 = Label(self.root, font=self.font_1)
        self.label_2.configure(bg="lightskyblue1")
        self.label_2.pack()

        self.label_3 = Label(self.root, font=self.font_3)
        self.label_3.configure(bg="white")
        self.label_3.pack(side=LEFT)

        self.picture_frame = Frame(self.root, width=50, height=50)
        self.picture_frame.configure(bg="lightskyblue1")
        self.picture_frame.pack()
        self.picture_frame.place(anchor="center", relx=0.5, rely=0.55)

        self.city = ""
        self.state = ""
        self.country = ""

        # List of all US state/territory abbreviations
        self.us_states = state_abbrev()

        # Weather Icons
        self.weather_icons = {
            "clear_day": "Weather_App/Weather_Icons/sunny.png",
            "day_cloud": "Weather_App/Weather_Icons/Day_cloud_sun.png",
            "haze": "Weather_App/Weather_Icons/Haze.png",
            "rain_day": "Weather_App/Weather_Icons/umbrella.png",
            "mist": "Weather_App/Weather_Icons/mist.png",
            "night_clear": "Weather_App/Weather_Icons/clear_night.png",
            "night_rain": "Weather_App/Weather_Icons/night_rain.png",
            "night_cloud": "Weather_App/Weather_Icons/night_cloudy.png",
        }

        # Labels for Images
        self.weather_labels = {}
        for weather_type, icon_path in self.weather_icons.items():
            image = ImageTk.PhotoImage(Image.open(icon_path))
            label = Label(self.picture_frame, image=image)
            label.configure(bg="lightskyblue1", image=image)
            self.weather_labels[weather_type] = label
            label.image = image

        load_dotenv()
        self.api_key = os.getenv("API_KEY")

    # Function to take city name and return lat/long for searching
    def getLatLong(self, city: str, state: str, country: str = "") -> tuple:
        """
        getLatLong takes the city, state, and country information and creates a tuple with the longitude and latitude of the location for use with the API

        Args:
            city (string): name of the city the user enters
            state (string): state in the US the user is searching
            country (str, optional): country code outside of the US. Defaults to "".

        Returns:
            tuple: (Latitude, Longitude)
        """
        try:
            if state.lower().strip() in self.us_states:
                country = "us"
            else:
                country = state
                state = ""

            convert_city_api = (
                f"http://api.openweathermap.org/geo/1.0/direct?q="
                f"{city},{state},{country}&limit=5&appid={self.api_key}"
            )
            print(convert_city_api)
            city_json = requests.get(convert_city_api).json()
            lat = city_json[0]["lat"]
            long = city_json[0]["lon"]

            return (lat, long)
        except (InvalidUserInput, APIError, IndexError):
            return messagebox.showerror(
                title="Error!",
                message="Something went wrong, please try again or cancel.",
            )
        except:
            return messagebox.showerror(
                title="Error!",
                message="Please enter a valid city, state or city, country",
            )

    # Function for requesting API and getting weather information
    def getWeather(self, event) -> None:
        """
        getWeather makes a request to the API in order to use the getOutput function to get the weather information for a given location

        Args:
            event (Tkinter Event): Interacts with Tkinter widget to use the information entered to get the data requested from the API
        """

        # Get city, state, country data
        input_text = self.text.get()

        # Split data by comma
        input_pieces = input_text.split(",")

        # Check for the parts needed in search
        if len(input_pieces) >= 2:
            self.city = input_pieces[0].strip()
            self.state = input_pieces[1].strip()

            if len(input_pieces) >= 3:
                self.country = input_pieces[2].strip()
            else:
                self.country = ""
        try:
            lat, long = self.getLatLong(self.city, self.state, self.country)
            lat = str(lat)
            long = str(long)
            api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={self.api_key}"

        except (InvalidUserInput, APIError, IndexError):
            return messagebox.showerror(
                title="Error!",
                message="Something went wrong, please try again or cancel.",
            )
        except:
            return messagebox.showerror(
                title="Error!",
                message="Please enter a valid city, state or city, country",
            )
        json_data = requests.get(api).json()
        weather = json_data["weather"][0]["main"]
        sunrise_unix = json_data["sys"]["sunrise"]
        sunset_unix = json_data["sys"]["sunset"]
        timezone_offset = json_data["timezone"]
        current_time_utc = datetime.datetime.utcnow()
        current_time_in_zone = current_time_utc + datetime.timedelta(
            seconds=timezone_offset
        )
        self.is_night(sunrise_unix, sunset_unix, current_time_in_zone, timezone_offset)

        self.getOutput(
            weather.lower(),
            json_data,
            sunrise_unix,
            sunset_unix,
            current_time_in_zone,
            timezone_offset,
        )

        print(api)  # TODO: Get rid of me

    # Determine if it is night
    def is_night(
        self, sunrise: int, sunset: int, current_time: datetime, tz_offset
    ) -> bool:
        """
        is_night uses the unix sunrise and sunset information along with the current time in UTC format and the time zone information to create a true or false return. It returns true if it is currently either prior to sunrise or after sunset in the given location and false otherwise.

        Args:
            sunrise (int): Unix sunrise time from the JSON
            sunset (int): Unix sunset time from JSON
            current_time (datetime class): Current date/time in UTC format
            tz_offset (int): Integer representing the time zone offset searched location

        Returns:
            bool: True if night and False if daytime in the searched location
        """
        current_time_unix = int(
            (current_time - datetime.datetime(1970, 1, 1)).total_seconds() - (tz_offset)
        )
        if current_time_unix < sunrise or current_time_unix > sunset:
            return True
        else:
            return False

    def clear_labels(self):
        """
        clear_labels _summary_
        """
        for label in self.weather_labels.values():
            label.pack_forget()

    def getOutput(self, weather, json, sunrise, sunset, current_time, timezone_offset):
        """
        getOutput _summary_

        Args:
            weather (_type_): _description_
            json (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            nighttime = self.is_night(sunrise, sunset, current_time, timezone_offset)
            long_temp = 1.8 * int(json["main"]["temp"] - 273.15) + 32
            faren_temp = "{:.2f}".format(long_temp)
            pre_min_temp = 1.8 * int(json["main"]["temp_min"] - 273.15) + 32
            pre_max_temp = 1.8 * int(json["main"]["temp_max"] - 273.15) + 32
            min_temp = "{:.2f}".format(pre_min_temp)
            max_temp = "{:.2f}".format(pre_max_temp)
            humidity = json["main"]["humidity"]
            sunrise_timezone = sunrise + timezone_offset
            sunset_timezone = sunset + timezone_offset
            sunrise_time = datetime.datetime.utcfromtimestamp(sunrise_timezone)
            sunset_time = datetime.datetime.utcfromtimestamp(sunset_timezone)

            # Default setting in case information not found
            final_weather = weather + "\n" + str(faren_temp) + " ℉"

            # Clear Previously Used Labels
            self.clear_labels()

            if nighttime:
                if weather.lower() == "clear":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["night_clear"].pack()
                elif weather.lower() == "clouds":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["night_cloud"].pack()
                elif weather.lower() == "rain":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["night_rain"].pack()
            else:
                if weather.lower() == "clear" or weather.lower() == "sunny":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["clear_day"].pack()
                elif weather.lower() == "clouds" or weather.lower() == "partly cloudy":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["day_cloud"].pack()
                elif weather.lower() == "rain":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["rain_day"].pack()
                elif weather.lower() == "haze" or weather.lower() == "hazy":
                    final_weather = weather + "\n" + str(faren_temp) + " ℉"
                    self.weather_labels["haze"].pack()

            max_min_humidity = (
                "Low:\t"
                + str(min_temp)
                + " ℉"
                + "\n"
                + "High:\t"
                + str(max_temp)
                + " ℉"
                + "\n"
                + "Humidity:\t"
                + str(humidity)
                + " %"
                + "\n"
                + "Sunrise:\t"
                + str(sunrise_time.strftime("%I:%M"))
                + " AM"
                + "\n"
                + "Sunset:\t"
                + str(sunset_time.strftime("%I:%M"))
                + " PM"
            )

            return (
                self.label_1.config(text=final_weather),
                self.label_3.config(text=max_min_humidity, justify=LEFT),
            )

        except (InvalidUserInput, APIError, IndexError):
            return messagebox.showerror(
                title="Error!",
                message="Something went wrong, please try again or cancel.",
            )
        except:
            return messagebox.showerror(
                title="Error!",
                message="Please enter a valid city, state or city, country",
            )


if __name__ == "__main__":
    root = Tk()
    application = Weather(root)
    root.mainloop()


# TODO: Consider breaking up the files into modules imported into the class
# TODO: typing in "aldlskfj" gives a result for Ḩeşār-e Sefīd, IR -- need to perhaps fix that and other nonsense entries

# TODO: Display city, state/country with the info
