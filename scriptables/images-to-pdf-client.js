/**
@license
MIT License
*/

"use strict";

/**
Script name.
*/
Script.name("images-to-pdf");

/**
Input: Array of image file paths (from Shortcuts) as first shortcut parameter.
Second plain text: endpoint URL (e.g. https://<host>/imagesToPdf )
Optional third plain text: image mode (e.g. RGB, L)
*/
const imageFiles = args.shortcutParameter; // Expect array of file paths
const url = args.plainTexts[0];
const imageMode = args.plainTexts.length > 1 ? args.plainTexts[1] : "RGB";

let fm = FileManager.local();
const tempDir = fm.temporaryDirectory();
const outPath = tempDir + "out-images.pdf";

if (!imageFiles || imageFiles.length === 0) {
  Script.setShortcutOutput("No image files provided");
  Script.complete();
}

async function imagesToPdf(files, endpoint, mode) {
  const request = new Request(endpoint);
  request.method = "POST";
  request.addParameterToMultipart("image_mode", mode);
  const paramName = "files";
  for (let i = 0; i < files.length; i++) {
    const f = files[i];
    if (fm.fileExists(f)) {
      request.addFileToMultipart(f, paramName);
    }
  }
  const response = await request.load();
  return response;
}

const result = await imagesToPdf(imageFiles, url, imageMode);
if (result) {
  fm.write(outPath, result);
  Script.setShortcutOutput(outPath);
} else {
  Script.setShortcutOutput("Request failed");
}
Script.complete();
