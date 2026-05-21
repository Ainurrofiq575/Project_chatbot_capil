try:

    from app.chatbot.chatbot_ai import chatbot_response

    print("Chatbot berhasil dimuat!")

    while True:

        tanya = input("Anda: ")

        jawab = chatbot_response(tanya)

        print("Bot:", jawab)

except Exception as e:

    print("ERROR:")
    print(e)