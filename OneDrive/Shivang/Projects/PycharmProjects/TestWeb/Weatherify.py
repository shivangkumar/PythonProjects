# Weatherify
# Code to pull the probability of rain and send a daily email to the user
# Created by Shivang Kumar

import forecastio
import json
import smtplib


def getLoginCredentials():
    with open(pathToConfig, 'r') as file:
        try:
            credentials = json.load(file)
        except ValueError:
            credentials = {}
        finally:
            return credentials


def main():
    user = getLoginCredentials()
    api_key = user['apiKey']
    latitude = user['latitude']
    longitude = user['longitude']
    rainThreshold = user['rainThreshold']
    forecast = forecastio.load_forecast(api_key, latitude, longitude)
    byHour = forecast.hourly().data
    count = 0
    hourlyPrediction = []
    rainyHours = []
    for i in range(2, 16):  # Monitor between 7:00 AM and 8:00 PM
        hour = byHour[i]
        print hour.icon + str(hour.time)
        count += 1
        temp = {'Time': hour.time, 'RainPrediction': hour.precipProbability}
        if hour.precipProbability >= rainThreshold:
            temp['RainFlag'] = True
            # rainyHours.append(temp['Time'])
        else:
            temp['RainFlag'] = False
        hourlyPrediction.append(temp)
    print count
    rainyHours = [x['Time'] for x in hourlyPrediction if x['RainFlag']]
    print '----------Rain expected at:\n'
    for time in rainyHours:
        print time
    print '----------Done'

    # Email results to user:
    emailContents = 'Rain expected at:\n'
    for time in rainyHours:
        emailContents += str(time) + '\n'
    smtpObject = smtplib.SMTP('smtp-mail.outlook.com', 587)
    print(smtpObject.ehlo())
    smtpObject.starttls()
    smtpObject.login(user['fromUsername'], user['password'])
    smtpObject.sendmail(user['fromUsername'], user['toUsername'], 'Subject: Weatherify Prediction \n'
                        + emailContents)
    print('Mail sent!')
    smtpObject.quit()


pathToConfig = 'C:\Users\Shivang Zenbook\OneDrive\Shivang\Projects\PycharmProjects\TestWeb\WeatherifyConfig.txt'
if __name__ == '__main__':
    main()
