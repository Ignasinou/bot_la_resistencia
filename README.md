# La Resistencia bot - empty slot

The following script bypasses a Google captcha and then checks if there are slots availables in [La Resistencia](https://elterrat.com/contacto/publico-la-resistencia/) TV show.

### Bypass Google Recaptcha:

In order to check the availables slots from la Resistencia form we should first bypass a Google recaptcha. From this captcha we will focus on the audio task (audio to text).

To achieve the bypassing we first need to download the audio and loaded it again into a ~~[speech-to-text website](https://speech-to-text-demo.ng.bluemix.net/)~~ python [speech_recognition](https://pypi.org/project/SpeechRecognition/) library. Then the result is fed into the captcha answer field.

### Selenium automation

The proposed solution is executed by using Selenium (headless). 

### ~~Heroku~~ Pythonanywhere.com and gridSend

Once the script detects that there is a free slot an email is send to the user by using gridSend. Everything is stored in a www.pythonanywhere.com server ~~and it runs every 10 min by using Heroku Schedulers~~.

#### Disclaimer: 

Sometimes if there are a lot of petitions to the site, the captcha will detect it and it will block the requests. In order to approach this changing the proxy might be a solution.
