import asyncio  #for asynchronous programming , to sennd multiple api requests concurrently
import speech_recognition as sr
import pyttsx3 # for text to sppech conversion
import pywhatkit # automating tasks like send messages,utube searches
import datetime
import wikipedia
import pyjokes
import time
import webbrowser
import os
import requests
import aiohttp  #for asyn http requests
import python_weather
from selenium import webdriver # control a web browser programmatically to automate web browser actions, such as opening websites, clicking elements, filling out forms,
from webdriver_manager.chrome import ChromeDriverManager # Auto-downloads ChromeDriver
from selenium.webdriver.chrome.service import Service    # Manages WebDriver as a service
from selenium.webdriver.common.by import By              # Locates elements on web pages
from selenium.webdriver.chrome.options import Options     # Configures Chrome browser options

newsapi_key = "ab9b7b9d6da84903b9de4fc98283bbab"

# initialise speech recognisation
listener = sr.Recognizer()
engine = pyttsx3.init()

# voice selection and adjustments

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0-male,1-female
engine.setProperty('rate', 140)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
    
def take_command(trigger_word_active=True):
    command=""
    start_time=time.time()
    try:
        with sr.Microphone() as source:
            print("Listening............")
            listener.adjust_for_ambient_noise(source,duration=1)
            while True:
                if time.time() - start_time > 180: #if exceed 3 mins stop listening
                    print("Stopped listening due to timeout.")
                    break
                try:
                    voice = listener.listen(source,timeout=10,phrase_time_limit=10)
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    if trigger_word_active and 'thara' in command:
                        command = command.replace('thara','').strip()
                        print(f"Command recieved: {command}")
                        break
                    elif not trigger_word_active:
                        print(f"Command recieved: {command}")
                        break
                # except sr.WaitTimeoutError:
                #     continue
                except sr.RequestError as e:
                    print(f"Couldn't process results: {e}")
                    break
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"An Error occured: {e}")
                    break
    except Exception as e:
        print(f"An error occured: {e}")
    return command


def search_google(query):
    options = Options() #setup selenuim webdriver
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get("https://www.google.com")
    # search in google
    search_box = driver.find_element(By.NAME,"q")
    search_box.send_keys(query) 
    search_box.submit()
       
    # extract search results
    time.sleep()# wait for search results to load
    results = driver.find_elements(By.CSS_SELECTOR, 'h3')
    links = [result.find_element(By.XPATH,'..').get_attribute('href') for result in results[:5]]
    driver.quit()
    return links

def get_wikipedia_summary(topic):
    try:
        return wikipedia.summary(topic,sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple entries for this topic. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any info...."
    except Exception:
        return "Sorry, I couldn't retrive info."
    
    
def get_nutrition_tips():
    return "Try to include variety of fruits and vegetables in your diet, and drink plenty of water."
def get_recipe_ideas():
    return "Try searching for recipes with ingredients you have at home. A popular option is pasta or stir-fry."

async def get_weather(city_name : str):
    api_key = 'e11452321f1e40b6dc863a919c1a7fc5'  # Replace with your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status==200:
                    data = await response.json()
                    
                    tempc=data['current']['temp_c']
                    loc = data['location']['name']
                    
                    print(f"The temperature in {location} is {temperature_c} degrees Celsius.")
                    talk(f"The temperature in {location} is {temperature_c} degrees Celsius.")
                else:
                    print(f"Failed to retrieve weather data: {response.status}")
                    talk("Sorry, I couldn't fetch the weather information. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")
            talk("Sorry, I couldn't fetch the weather information. Please try again.")
            
            
def run_tara(trigger_word_active=True):
    command = take_command(trigger_word_active)
    print(f"Processing command: {command}")
    opened_app_or_site=False  # Flag to check if an application or website was opened
    
    if command:
        command_handled=False   # Flag to check if the command was handled
        
        # Open websites
        sites = [
            ["Google", "https://google.com"], ["Facebook", "https://facebook.com"],
            ["Twitter", "https://twitter.com"], ["LinkedIn", "https://linkedin.com"],
            ["YouTube", "https://youtube.com"], ["Instagram", "https://instagram.com"],
            ["Reddit", "https://reddit.com"], ["Amazon", "https://amazon.com"],
            ["Wikipedia", "https://wikipedia.org"], ["Gmail", "https://gmail.com"],
            ["Outlook", "https://outlook.com"], ["Yahoo Mail", "https://yahoo.com"],
            ["Hacker News", "https://news.ycombinator.com"], ["GitHub", "https://github.com"],
            ["Stack Overflow", "https://stackoverflow.com"], ["Google Docs", "https://docs.google.com"],
            ["Google Drive", "https://drive.google.com"], ["Zoom", "https://zoom.us"],
            ["Microsoft", "https://microsoft.com"], ["Apple", "https://apple.com"],
            ["PayPal", "https://paypal.com"], ["Spotify", "https://spotify.com"],
            ["Netflix", "https://netflix.com"], ["CNN", "https://cnn.com"],
            ["BBC", "https://bbc.com"], ["Forbes", "https://forbes.com"],
            ["Weather.com", "https://weather.com"], ["Medium", "https://medium.com"],
            ["Quora", "https://quora.com"], ["Twitch", "https://twitch.tv"],
            ["Coursera", "https://coursera.org"], ["edX", "https://edx.org"],
            ["Khan Academy", "https://khanacademy.org"], ["Duolingo", "https://duolingo.com"],
            ["IMDb", "https://imdb.com"], ["Etsy", "https://etsy.com"],
            ["Target", "https://target.com"], ["TripAdvisor", "https://tripadvisor.com"]
        ]
        
        # Open applications
        applications = [
            ["Brave", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk"],
            ["Excel", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"],
            ["Google Chrome", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"],
            ["Microsoft Edge", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk"],
            ["OneDrive", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OneDrive.lnk"],
            ["OneNote", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OneNote.lnk"],
            ["Outlook", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Outlook.lnk"],
            ["PowerPoint", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"],
            ["Publisher", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Publisher.lnk"],
            ["Word", r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"],
            ["vs code", r"C:\Users\ayush\Desktop\Visual Studio Code.lnk"],
            ["Spotify", r"C:\Users\ayush\Desktop\Spotify.lnk"],
            ["Postman", r"C:\Users\ayush\Desktop\Postman.lnk"],
            ["Brave (Desktop)", r"C:\Users\Public\Desktop\Brave.lnk"],
            ["Microsoft Edge (Desktop)", r"C:\Users\Public\Desktop\Microsoft Edge.lnk"],
            ["Google Chrome (Desktop)", r"C:\Users\Public\Desktop\Google Chrome.lnk"]
        ]
        
        # check for sites
        for site in sites:
            if f"open {site[0]}".lower() in command.lower():
                talk(f"Opening {site[0]}")
                webbrowser.open(site[1])
                opened_app_or_site=True
                command_handled=True
                print(f"Opening website: {site[0]}")
                break
        
        # check for applications
        for app in applications:
            if f"open {app[0]}".lower() in command.lower():
                talk(f"Opening {app[0]}")
                os.system(f'start "" "{app[1]}"')
                opened_app_or_site = True
                command_handled = True
                break
        
        # Additional commands
        if not command_handled:
            if 'play' in command:
                song = command.replace('play','').strip()
                talk(f'Playing {song}')
                pywhatkit.playonyt(song)
                command_handled=True
                
            if 'temperature in' in command:
                city = command.replace('weather in','').strip()
                talk(f"Getting weather for {city}")
                command_handled=True
                asyncio.run(get_weather(city))
            elif "news" in command:
                try:
                    print("Fetching news....")
                    talk("Here are some of today's top news headlines:")
                    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}")
                    if r.status_code==200:
                        data=r.json()
                        articles=data.get('articles',[])
                        if articles:
                            for article in articles[:5]:
                                print(article['title'])
                                talk(article['title'])
                        else:
                            talk("No news articles found.")
                    else:
                        talk("error fetching news.😕")
                except requests.RequestException as e:
                    talk(f"Error fetching news: {e}")

                finally:
                    command_handled = True
                
            elif 'the time' in command:
                time_now = datetime.datetime.now().strftime('%I:%M %p')
                print(f'Current time is: {time_now}')
                talk(f'Current time is {time_now}')
                command_handled = True
            elif 'the date' in command:
                date_today = datetime.datetime.now().strftime('%d %B, %Y')
                print(f'Today is: {date_today}')
                talk(f'Today is {date_today}')
                command_handled = True
            elif 'the day' in command:
                day_today = datetime.datetime.now().strftime('%A')
                print(f'Today is: {day_today}')
                talk(f'Today is {day_today}')
                command_handled = True
            elif 'tell me something about' in command:
                person = command.replace('tell me something about', '').strip()
                print(f"Searching Wikipedia for: {person}")
                summary = get_wikipedia_summary(person)
                print(summary)
                talk(f"According to Wikipedia, {summary}")
                command_handled = True
            elif 'search' in command:
                query = command.replace('search', '').strip()
                talk("Please wait for a minutes I am Searching on Google.")
                print(f"Searching Google for: {query}")
                links = search_google(query)
                talk(f"Here are some links I found:")
                for link in links:
                    print(link)
                    # talk(link)
                command_handled = True
            elif 'exit' in command or 'bye' in command:
                print("Program interrupted. Exiting...")
                talk("I am Signing off! Goodbye! Have a nice day!")
                return False
            elif 'hello' in command:
                talk('Hello! How can I assist you today?')
                command_handled = True
            elif 'how are you' in command:
                talk('I am doing well, thank you for asking. How can I assist you?')
                command_handled = True
            elif 'thank you' in command:
                talk('You are welcome! Is there anything else I can help you with?')
                command_handled = True
            elif 'what is your name' in command:
                talk('My name is Thara.')
                command_handled = True
            elif 'who are you' in command:
                talk('I am Thara, your personal assistant. How can I help you today?')
                command_handled = True
            elif 'what can you do' in command or 'what you can do' in command:
                talk('I can play music, tell you the time, date, and much more. What would you like to do?')
                command_handled = True
            elif 'date' in command:
                talk('Sorry, I have a headache.')
                talk('but i can we plane for  next week, I will go anywhere you take me')
                command_handled = True
            elif 'you be my girlfriend' in command:
                talk('This is one of those things we both have to agree on.  I did prefer to keep our relationship friendly')
                talk(' Romance make me incredibly awkward')
                command_handled = True
            elif 'you be my boyfriend' in command:
                talk('This is one of those things we both have to agree on.  I did prefer to keep our relationship friendly')
                talk(' Romance make me incredibly awkward')
                command_handled = True
            elif 'are you single' in command:
                talk('I am in a relationship with Wi-Fi.')
                command_handled = True
            elif 'joke' in command:
                talk(pyjokes.get_joke())
                command_handled = True
            elif 'what is your favourite colour' in command:
                talk('My favorite color is blue.')
                command_handled = True
            elif 'what is your favourite food' in command:
                talk('I like Internet.')
                command_handled = True
            elif 'open google using chrome' in command.lower():
                talk("Opening Google using Chrome.")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver.get("https://www.google.com")
                time.sleep(2)  # Allow some time to view the result
                driver.quit()
                command_handled = True
            elif 'what is your favourite movie' in command:
                talk('Some of my favorite movies are "3 Idiots" from Bollywood, "The Matrix" from Hollywood, and "Baahubali" from South Indian cinema.')

                command_handled = True
            elif 'what is your favourite book' in command:
                talk('I like the book The Alchemist by Paulo Coelho.')
                command_handled = True
            elif 'what is your favourite sport' in command:
                talk('I like cricket.')
                command_handled = True
            elif 'who is Tarani Rashmitha' in command:
                talk('Tarani Rashmitha is a student who is pursuing BTech in Computer Science and Engineering.')
                talk('who has designed and developed me as a AI assistant. If you have any other questions, feel free to ask!')
                command_handled = True
            elif 'who created you' in command:
                talk("I was created by Tarani Rashmitha, who designed and developed me as a personal assistant. If you have any other questions, feel free to ask!")
                command_handled = True
            elif 'weather in' in command:
                city = command.split('weather in')[1].strip()
                asyncio.run(get_weather(city))
                command_handled = True
            elif 'nutrition' in command:
                nutrition_tips = get_nutrition_tips()
                talk(nutrition_tips)
                command_handled = True
            elif 'recipe' in command:
                recipe_ideas = get_recipe_ideas()
                talk(recipe_ideas)
                command_handled = True
            elif 'how to make pasta' in command or 'pasta recipe' in command:
                talk("Here's a simple recipe for making pasta:")
                talk("1. Boil water in a large pot. Add a pinch of salt to the water.")
                talk("2. Once the water is boiling, add the pasta. Stir occasionally to prevent sticking.")
                talk("3. Cook the pasta according to the package instructions, usually 8-12 minutes.")
                talk("4. While the pasta is cooking, you can prepare the sauce. Heat some olive oil in a pan and add garlic, onions, or your preferred vegetables.")
                talk("5. Add your favorite sauce or ingredients like tomatoes, herbs, or cream to the pan and let it simmer.")
                talk("6. Drain the pasta once it's cooked and add it to the sauce. Mix well.")
                talk("7. Serve hot with grated cheese or fresh basil if desired.")
                talk("Enjoy your homemade pasta!")
                command_handled = True


        if not command_handled:
            talk('Sorry, I did not understand that. Please say the command again.')

    if opened_app_or_site:
        # Prompt for activation only after opening a website or application
        run_tara()

    return True


# Initial startup message
print("Hello, I am Thara, your virtual assistant. How can I assist you.")
talk("Hello, I am chitti 3 point O, your virtual assistant. How can I assist you.")


# Choose the mode: Set `trigger_word_active` to True for trigger word activation or False for continuous listening
trigger_word_active = True

while True:
    try:
        if not run_tara(trigger_word_active):
            break
    except KeyboardInterrupt:
        print("The program has been interrupted. Exiting now...")
        talk("I am signing off. Goodbye, and have a great day!")

        break
    time.sleep(1)  # Small delay to prevent continuous looping       

    