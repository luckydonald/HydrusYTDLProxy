# HydrusYTDLProxy
A thing to allow to use YouTube-dlp with Hydrus Network


# How to run
## a) Local
#### Local Prerequisites
- Python 3.10+
- ffmpeg

#### Local Install
```shell
pip install -r /install/requirements.txt
```

#### Run
```shell
fastapi run main.py
```

## b) Docker:
```shell
docker build -t hydrus-ytdl-proxy .
docker run -d -p 4458:4458 hydrus-ytdl-proxy
```

## c) Coolify:
1. Add as <kbd>NIXPACK</kbd>
2. Set start command to `fastapi run main.py --port=4458`
3. Set network port to `4458`.


## Hydrus Network Setup
1. Open Hydrus Network
2. Go to <kbd>network</kbd> ➔ <kbd>downloader components</kbd> ➔ <kbd>manage gallery url generators…</kbd> and click on <kbd>Add</kbd> to add a new one with the following settings:
      1. name: `HydrusYTDLProxy url`
      2. url template: `http://<YOUR_SERVER_HOST_OR_IP>:4458/meta?url={url}`
         - Replace `<YOUR_SERVER_HOST_OR_IP>` with your server's host or IP address,  
           or localhost if you are running it on the same machine as Hydrus Network.
         - Use `https` instead of `http` if you have ssl configured (Coolify does that), then you should also drop or adapt the port (`:4458`).
         - Adapt the port `4458` if you run the server on a different port.
      3. replacement phrase: `{url}`
      4. search term separator: _empty_
      5. initial search text (to prompt user): `url to download`
      6. example text search: `https://www.youtube.com/watch?v=dQw4w9WgXcQ` or 
      7. example request url: _automatically generated: `http://<YOUR_SERVER_HOST_OR_IP>:4458/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
      8. matches as a: _automatically generated_
         - Initially _empty_.
         - Later will be `Matched HydrusYTDLProxy (meta as gallery) url class.`.
      9. <kbd>OK</kbd>
2. Go to <kbd>network</kbd> ➔ <kbd>downloader components</kbd> ➔ <kbd>manage parsers…</kbd> and click on <kbd>add</kbd> to add a new one with the following settings:
      1. name or description (optional): `HydrusYTDLProxy (meta)`
      2. example urls ➔ <kbd>add</kbd>: `http://<YOUR_SERVER_HOST_OR_IP>:4458/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
      3. fetch test data from url: _same as above_
      4. click on <kbd>fetch test data from url</kbd>
      5. set up parsers.
   1. <kbd>add</kbd>
      1.  ➔ **name or description(optional)**: `URL (best format)`
      2. **content type**: <kbd>urls</kbd>
      3. **url type**: <kbd>url to download/pursue (file/post url)</kbd>
      4. **url quality precedence (higher is better)**: `75`
      5. <kbd>edit formula</kbd> (type JSON, otherwise click <kbd>change formula type</kbd>)
         1. **name/description**: `URL (best format) from json`
         2. <kbd>add</kbd> the following 3 steps:
            1. dictionary entry by key:
               - match type: <kbd>fixed characters</kbd>
               - fixed text: `formats`
            2. dictionary entry by key:
               - match type: <kbd>fixed characters</kbd>
               - fixed text: `best`
            3. dictionary entry by key:
               - match type: <kbd>fixed characters</kbd>
               - fixed text: `url`
         3. **content to fetch**: <kbd>string</kbd>
         4. _no string processing_.
   2. You can add more parsers if you want, e.g. for title, description, tags, other formats, etc.
      - See http://<YOUR_SERVER_HOST_OR_IP>:4458/docs for available fields for the /meta endpoint.
   3. <kbd>OK</kbd>
3. Go to <kbd>network</kbd> ➔ <kbd>downloader components</kbd> ➔ <kbd>manage parsers…</kbd> and click on <kbd>add</kbd> to add a new one with the following settings:
   1. name or description (optional): `HydrusYTDLProxy (redirect)`
   2. example urls ➔ <kbd>add</kbd>: `https://www.pornhub.com/view_video.php?viewkey=ph63348bf2f3330`
   3. fetch test data from url: _same as above_
   4. click on <kbd>fetch test data from url</kbd>
   5. set up parsers: <kbd>add</kbd>
      1. **name or description(optional)**: `URL: Redirect to API (click edit formula twice to edit domain)`
      2. **content type**: <kbd>urls</kbd>
      3. **url type**: <kbd>url to download/pursue (file/post url)</kbd>
      4. **url quality precedence (higher is better)**: `50`
      5. <kbd>edit formula</kbd> (type ZIPPER, otherwise click <kbd>change formula type</kbd>)
         1. **name/description**: `Zipper rule to build the new url to redirect to the API.`
         2. <kbd>add</kbd> the following 3 zipped parts:
            - Zipper (start of url)
                1. <kbd>change formula type</kbd> ➔ <kbd>change to a new ZIPPER formula…</kbd>
                2. <kbd>edit formula</kbd>
                   1. **name/description**: `EDIT HOST HERE IN "substitution phrase"`
                   2. <kbd>add</kbd>
                      1. <kbd>change formula type</kbd> ➔ <kbd>change to a new CONTEXT VARIABLE formula…</kbd>
                      2. <kbd>edit formula<kbd>
                         1. **name/description**: `url`
                         2. **variable name**: `url`
                         3. _no string processing_.
                         4. <kbd>apply</kbd>
                      3. <kbd>apply</kbd>
                   3. **substitution phrase**: `http://<YOUR_SERVER_HOST_OR_IP>:4458`
                   4. <kbd>apply</kbd>
                3. <kbd>apply</kbd>
            - Zipper (middle part of url)
                1. <kbd>change formula type</kbd> ➔ <kbd>change to a new ZIPPER formula…</kbd>
                2. <kbd>edit formula</kbd>
                   1. **name/description**: `middle part of url`
                   2. <kbd>add</kbd>
                      1. <kbd>change formula type</kbd> ➔ <kbd>change to a new CONTEXT VARIABLE formula…</kbd>
                      2. <kbd>edit formula</kbd>
                         1. **name/description**: `url`
                         2. **variable name**: `url`
                         3. _no string processing_.
                         4. <kbd>apply</kbd>
                      3. <kbd>apply</kbd>
                   3. **substitution phrase**: `/meta?url=`
                   4. <kbd>apply</kbd>
                3. <kbd>apply</kbd>
            - Context variable (middle part of url)
                1. <kbd>change formula type<kbd> ➔ <kbd>change to a new CONTEXT VARIABLE formula…</kbd>
                2. <kbd>edit formula<kbd>
                   1. **name/description**: `encoded url`
                   2. **variable name**: `url`
                   3. Click <kbd>no string processing</kbd>.
                      1. Click <kbd>add</kbd> 
                         1. Select <kbd>String Converter</kbd>
                         2. **example string**: `https://www.pornhub.com/view_video.php?viewkey=ph63348bf2f3330`
                         3. Click <kbd>add</kbd>
                            1. **conversion type**: <kbd>encode</kbd>
                            2. **encoding type**: <kbd>url percent encoding</kbd>
                            3. **example string**: `https://www.pornhub.com/view_video.php?viewkey=ph63348bf2f3330`
                            4. **converted string**: _automatically generated: `https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`_
                            5. <kbd>apply</kbd>
                         4. <kbd>apply</kbd>
                      2. <kbd>apply</kbd>
                   4. <kbd>apply</kbd>
                3. <kbd>apply</kbd>
               - fixed text: `formats`
            2. dictionary entry by key:
               - match type: <kbd>fixed characters</kbd>
               - fixed text: `best`
            3. dictionary entry by key:
               - match type: <kbd>fixed characters</kbd>
               - fixed text: `url`
         3. **substitution phrase**: `\1\2\3`
         4. _no string processing_.
         5. <kbd>apply</kbd>
      3. <kbd>apply</kbd>
   6. set up parsers: <kbd>add</kbd>
      1. **name or description(optional)**: `URL: just the given url for association`
      2. **content type**: <kbd>urls</kbd>
      3. **url type**: <kbd>POST parsers only: url to associate (source url)</kbd>
      4. **url quality precedence (higher is better)**: `100`
      5. <kbd>edit formula<kbd> (type CONTEXT VARIABLE, otherwise click <kbd>change formula type</kbd> before)
            1. **name/description**: `Original URL for association`
            2. **variable name**: `url` 
            3. <kbd>apply</kbd>
         6. <kbd>apply</kbd>
      6. <kbd>apply</kbd>
   7. <kbd>apply</kbd>
4. Go to <kbd>network</kbd> ➔ <kbd>downloader components</kbd> ➔ <kbd>manage url classes</kbd>
   1. and click on <kbd>add</kbd> to add a new one with the following settings:
      1. **name**: `HydrusYTDLProxy (meta)`
      2. **url type**: <kbd>post url</kbd>
      3. tab <kbd>march rules</kbd>
         4. **preferred scheme**: <kbd>http</kbd> (or <kbd>https</kbd> if you have ssl configured)
         5. **network location**: `<YOUR_SERVER_HOST_OR_IP>:4458`
         6. **path components**: _none_
         7. **parameters** ➔ <kbd>add</kbd>
            2. **name**: `url`
            3. **name, %-encoded**: `url`
            4. **match type**: <kbd>regex</kbd>
            5. **regex**: `https?(:|%3A)(/|%2F)(/|%2F).+`
            6. **minimum allowed number of characters**: ☑️ no limit
            7. **maximum allowed number of characters**: ☑️ no limit
            8. **example string**: `https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
            9. **default value**:  ☑️ none
            9. **default value, %-encoded**:  ☑️ none
            10. **default string processor**: _no string processing_.
            11. <kbd>apply</kbd>
      4. tab <kbd>options</kbd>
         1. if matching by subdomain, keep it when normalising: _Disabled. ~~No ◻️~~_
         2. alphabetise GET parameters when normalising: Yes ☑️
         3. disallow match on any extra path components: No ◻️
         4. disallow match on any extra parameters: No ◻️
         5. keep extra parameters for server: Yes ☑️
         6. keep fragment when normalising: No ◻️
         7. post page can produce multiple files: No ◻️
         8. associate a 'known url' with resulting files: Yes ☑️
         9. **optional api/redirect url conversion**: _no string conversion_.
         10. **api/redirect url**: _none set_.
         11. **send referral url**: <kbd>send referral url if available</kbd>
      5. **example url**: `http://<YOUR_SERVER_HOST_OR_IP>:4458/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
      6. <kbd>apply</kbd>
   2. and click on <kbd>add</kbd> to add a new one with the following settings:
      1. **name**: `HydrusYTDLProxy (meta as gallery)`
      2. **url type**: <kbd>gallery url</kbd>
      3. tab <kbd>march rules</kbd>
         4. **preferred scheme**: <kbd>http</kbd> (or <kbd>https</kbd> if you have ssl configured)
         5. **network location**: `<YOUR_SERVER_HOST_OR_IP>:4458`
         6. **path components**: _none_
         7. **parameters** ➔ <kbd>add</kbd>
            2. **name**: `url`
            3. **name, %-encoded**: `url`
            4. **match type**: <kbd>regex</kbd>
            5. **regex**: `https?(:|%3A)(/|%2F)(/|%2F).+`
            6. **minimum allowed number of characters**: ☑️ no limit
            7. **maximum allowed number of characters**: ☑️ no limit
            8. **example string**: `https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
            9. **default value**:  ☑️ none
            9. **default value, %-encoded**:  ☑️ none
            10. **default string processor**: _no string processing_.
            11. <kbd>apply</kbd>
      4. tab <kbd>options</kbd>
         1. if matching by subdomain, keep it when normalising: _Disabled. ~~No ◻️~~_
         2. alphabetise GET parameters when normalising: Yes ☑️
         3. disallow match on any extra path components: No ◻️
         4. disallow match on any extra parameters: No ◻️
         5. keep extra parameters for server: Yes ☑️
         6. keep fragment when normalising: No ◻️
         7. post page can produce multiple files: _Disabled. ~~No ◻️~~_
         8. associate a 'known url' with resulting files: Yes ☑️
         9. **optional api/redirect url conversion**: _no string conversion_.
         10. **api/redirect url**: _none set_.
         11. **send referral url**: <kbd>send referral url if available</kbd>
      5. **example url**: `http://<YOUR_SERVER_HOST_OR_IP>:4458/meta?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
      6. <kbd>apply</kbd>
   3. and click on <kbd>add</kbd> to add a new one with the following settings:
      1. **name**: `HydrusYTDLProxy (dl)`
      2. **url type**: <kbd>file url</kbd>
      3. tab <kbd>march rules</kbd>
         1. **preferred scheme**: <kbd>http</kbd> (or <kbd>https</kbd> if you have ssl configured)
         2. **network location**: `<YOUR_SERVER_HOST_OR_IP>:4458`
         3. **path components** ➔ <kbd>add</kbd>
            1. **match type**: <kbd>fixed characters</kbd>
            2. **fixed text**: `dl`
            3. <kbd>apply</kbd>
         4. **parameters** ➔ <kbd>add</kbd>
            2. **name**: `format`
            3. **name, %-encoded**: `format`
            4. **match type**: <kbd>character set</kbd>
            4. **match type**: <kbd>alphanumeric characters (a-zA-Z0-9)</kbd>
            5. **regex**: `https?(:|%3A)(/|%2F)(/|%2F).+`
            6. **minimum allowed number of characters**: ☑️ no limit
            7. **maximum allowed number of characters**: ☑️ no limit
            8. **example string**: `value`
            9. **default value**:  ☑️ none
            9. **default value, %-encoded**:  ☑️ none
            10. **default string processor**: _no string processing_.
            11. <kbd>apply</kbd>
         5. **parameters** ➔ <kbd>add</kbd>
            2. **name**: `url`
            3. **name, %-encoded**: `url`
            4. **match type**: <kbd>regex</kbd>
            5. **regex**: `https?(:|%3A)(/|%2F)(/|%2F).+`
            6. **minimum allowed number of characters**: ☑️ no limit
            7. **maximum allowed number of characters**: ☑️ no limit
            8. **example string**: `https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330`
            9. **default value**:  ☑️ none
            9. **default value, %-encoded**:  ☑️ none
            10. **default string processor**: _no string processing_.
            11. <kbd>apply</kbd>
      4. tab <kbd>options</kbd>
         1. if matching by subdomain, keep it when normalising: _Disabled. ~~No ◻️~~_
         2. alphabetise GET parameters when normalising: Yes ☑️
         3. disallow match on any extra path components: No ◻️
         4. disallow match on any extra parameters: No ◻️
         5. keep extra parameters for server: Yes ☑️
         6. keep fragment when normalising: No ◻️
         7. post page can produce multiple files: _Disabled. ~~No ◻️~~_
         8. associate a 'known url' with resulting files: Yes ☑️
         9. **optional api/redirect url conversion**: _no string conversion_.
         10. **api/redirect url**: _none set_.
         11. **send referral url**: <kbd>send referral url if available</kbd>
      5. **example url**: `http://<YOUR_SERVER_HOST_OR_IP>:4458/dl?url=https%3A%2F%2Fwww.pornhub.com%2Fview_video.php%3Fviewkey%3Dph63348bf2f3330&format=best`
      6. <kbd>apply</kbd>
5. Now you can use the new url generator in Hydrus Network:
   1. Open a <kbd>new page</kbd> ➔ <kbd>downloader</kbd> ➔ <kbd>gallery</kbd>
   2. Select <kbd>`HydrusYTDLProxy url</kbd> from the dropdown menu.
   3. Paste any YT-DLP / Youtube-dl supported URL into the search box.