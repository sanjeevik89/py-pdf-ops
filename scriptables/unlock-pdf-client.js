/**

@license

Copyright (c) 2022 Sanjeevi Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all

copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.
*/

"use strict";

/**

Name the script.
@see {@link https://docs.scriptable.app/script/#name}
*/
Script.name("unlock-pdfs");
/**

Pdf file supplied by a share sheet or a shortcut action.
@see {@link https://docs.scriptable.app/args/}
*/
const inPDF = args.shortcutParameter

/**

Plain texts supplied by a share sheet or a shortcut action.
@see {@link https://docs.scriptable.app/args/}
*/
const password = args.plainTexts[0];
const url = args.plainTexts[1];
/**

The link you want to share.
@type {string}
*/// // //
let fm = FileManager.local();
const temp_dir = fm.temporaryDirectory();

if( fm.fileExists(inPDF) ) {
let temp_file_path = temp_dir + "/temp-in.pdf" ;
fm.remove(temp_file_path);
fm.copy(inPDF, temp_file_path);
let outPDF = await unlockPdf(temp_file_path, password, url);
temp_file_path = temp_dir + "/temp-out.pdf" ;
fm.write(temp_file_path, outPDF);

/**

Pass output to the iOS shortcuts.
@see {@link https://docs.scriptable.app/pasteboard/#script}
*/////
Script.setShortcutOutput(temp_file_path);
/**

Exit the script.
@see {@link https://docs.scriptable.app/script/#complete}
*/
Script.complete();
}

async function unlockPdf(filePath,pass, url) {

const file_param_name = 'file';    
let request = new Request(url);
request.method = "POST";
request.addParameterToMultipart("password", pass);
request.addFileToMultipart(filePath, file_param_name);
let response= await request.load();

if (!response) {
      return undefined;
} else {
    return response
}
}