from api.ai import Agent

agent = Agent(
     '<subscription-key>',
     'd7b00ed0ee08464c860a9f6e8eb7164e',
     '6fef320b63224ce6a42b443ec8428db1',
)
def chat(inp):
    response = agent.query(inp)
    result = response['result']
    # fulfillment = result['fulfillment']
    # response = fulfillment['speech']
    # intent = result['metadata']['intentName']
    searched_item = result['parameters']['searched_item']
    print(response)
    print("\n\n\n\n\n\n\n{}".format(intent))
    print("\n\n\n\n\n\n\n{}".format(searched_item))

chat("what is java?")












# import speech_recognition as sr
# from gtts import gTTS
# from playsound import playsound
# 
# def speak(message):
    # speech = gTTS(text=message , lang='en')
    # speech.save("speech.mp3")
    # print(message)
    # playsound("speech.mp3")
# 
# # r = sr.Recognizer()
# 
# # while(1):
      # 
# #     # Exception handling to handle
# #     # exceptions at the runtime
# #     try:
          # 
# #         # use the microphone as source for input.
# #         with sr.Microphone() as source2:
              # 
# #             # wait for a second to let the recognizer
# #             # adjust the energy threshold based on
# #             # the surrounding noise level
# #             r.adjust_for_ambient_noise(source2, duration=0.2)
              # 
# #             #listens for the user's input
# #             audio2 = r.listen(source2)
              # 
# #             # Using ggogle to recognize audio
# #             MyText = r.recognize_google(audio2)
# #             MyText = MyText.lower()
  # 
# #             print("Did you say "+MyText)
# #             # print(MyText)
              # 
# #     except sr.RequestError as e:
# #         print("Could not request results; {0}".format(e))
          # 
# #     except sr.UnknownValueError:
# #         print("unknown error occured")
# # speak("hello world")

