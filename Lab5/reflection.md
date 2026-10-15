\# Reflection



\## 1. What did you learn from using static analysis tools?



I learned that static analysis can find problems in a program even when the program runs correctly. Pylint helped me identify code quality issues such as naming, missing docstrings and unnecessary code. Bandit helped identify security-related problems, while Flake8 mainly helped with formatting and coding style.



\## 2. Which tool was most useful and why?



I found Bandit the most useful because it identified security issues that would not be obvious just by running the program. For example, it detected the use of `random` for application IDs, hardcoded credentials, FTP usage and unsafe deserialization.



\## 3. How did the fixes improve the code?



The fixes made the code cleaner, more consistent and safer. Function names and formatting were improved, unnecessary code was removed, and security-sensitive parts were changed. After the fixes, the final Pylint score was 9.89/10, and Bandit and Flake8 reported no issues.



\## 4. Did static analysis find problems that normal testing did not?



Yes. Normal testing mainly showed whether the program was running and producing the expected output. Static analysis found issues such as insecure coding practices, naming problems, missing documentation and formatting problems that were not visible from the program output.



\## 5. What challenges did you face while fixing the issues?



The main challenge was making the changes without affecting the existing program functionality. Renaming functions required updating their uses in other parts of the program. I also had to rerun the program and the analysis tools after making changes to make sure that the fixes did not introduce new problems.



\## 6. How will you use static analysis in future projects?



I would run static analysis tools during development instead of waiting until the end of a project. This can help find code quality, formatting and security problems earlier and make the code easier to maintain.

