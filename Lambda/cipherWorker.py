from Lambda.cipherWorkerModules import congifReader, cipherSolver, receive_message_with_attributes, read_all_items


url = congifReader()[0]

tableName = receive_message_with_attributes(url)[0][2]

# I know it's spelled encrypted not encypted
encryptedWord = read_all_items(tableName)[0].get('encypted-text')

answer, key = cipherSolver(encryptedWord)

print("the word is "+answer+", which was shifted "+str(key)+" places")