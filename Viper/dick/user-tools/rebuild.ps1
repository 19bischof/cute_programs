mkdir lookup -ErrorAction Ignore

# Read JSON content
$jsonPath = "manifest.json"
$jsonContent = Get-Content $jsonPath -Raw | ConvertFrom-Json

# Parse version and bump minor
$versionParts = $jsonContent.version -split '\.'
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1] + 1
$jsonContent.version = "$major.$minor"

# Convert back to JSON with indentation and write to file
$jsonContent | ConvertTo-Json -Depth 10 | Set-Content $jsonPath

Compress-Archive -Path manifest.json,userscript.js -DestinationPath lookup/extension.xpi -Update

