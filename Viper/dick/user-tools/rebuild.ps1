mkdir lookup -ErrorAction Ignore
Compress-Archive -Path manifest.json,userscript.js -DestinationPath lookup/extension.xpi -Update
