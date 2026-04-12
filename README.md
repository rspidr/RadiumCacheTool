# RadiumCacheTool
A Python tool to parse and export Radium's library cache file - you can also delete your library cache. (This is an edit of [@Jegarde](https://github.com/Jegarde)'s [RecRoom-Library-Cache-Tool](https://github.com/Jegarde/RecRoom-Library-Cache-Tool))

<img width="1006" height="193" alt="image" src="https://github.com/user-attachments/assets/257d428f-1873-40c3-9f7d-e023372c1934" />

# Features
- Parse library cache
- Delete library cache

# Parsing
The script parses the library cache file into a readable txt file just like Jegarde's tool but it now look for img.epicquest.live urls instead of img.rec.net. It categorizes the URLs by their file extensions and it also sorts the URLs in each category in order of date from most recent to least recent.
Once it is done parsing, it exports the parsed library in a RadiumCacheOutput.txt file.

<img width="755" height="709" alt="image" src="https://github.com/user-attachments/assets/7aa155c2-efdc-4d65-9d63-8c8055b48588" />

# Location of the Library file
Radium uses the same Library cache file normal RecRoom uses currently (`%userprofile%\AppData\LocalLow\Against Gravity\Rec Room\Library`)
