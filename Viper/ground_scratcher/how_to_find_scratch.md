# How do you find the correct select syntax with bs4 for a website?
1. First go to the website and go into the developer settings (F12)
2. Then open selector and select the element which holds the important data
3. then rightclick and copy css-selector (alternatively copy css-path which is more precise but longer)
4. if you are smart about it you can select a group of important nodes and then parse that or 
5. go into python and use ```soup.select(*here*)``` to copy it in here
6. Afterwards make sure that there are no tbody nodes because they do not exist in the source code and are browser generated
7. You should be done
8. If not slowly cascade down step by step the css selectors and see at what point the ```select()``` goes wrong

## Enjoy !
