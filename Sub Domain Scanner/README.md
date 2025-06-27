## 🔍 Subdomain Scanner

The Subdom Scanner V1 - 06/26/2025 

Is a standard subdomain scanner made in python that can be broken down and understood as such;
- Firstly python modules; request (to make a get-request to validate the domain), pyfiglet (to make a banner) and sys (to read to user input arg from the user) are imported.
- The next step, after the banner, is to have a subdomain enumerator list. This list I have used is a "highly effective" list (Credits to <a href="https://github.com/n0kovo/n0kovo_subdomains"> n0kovo </a>).
(⚠️ Make sure you download the .txt file when trying to run the scanner locally.)
- Now, we store the contents of the file in variable1 (var1) and then run it through ".spiltlines()" to have seperated and store it in variable2 (var2). So an overall uniformity is created.
- Then, creating a for loop where variables from var2 are called and the placed into "hxxps://var.{sys.argv[1]}". Wherein the sys.argv[1] will be the domain name entered by the user. This overall iteration is stored in variable3 (var3).
- Lastly, the loop then tries to connect with an overall subdomain.domain.tld pattern on HTTPS for a successful ping. For any exception connection error, that instance is passed over, but if there are no error the subdomain is deemed VALID.
- And Viola 🎉 !! A subdomain scanner is created.
- This is version 1 of the Subdom Scanner, a new feature will be added to upcoming version !!

---
