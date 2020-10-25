# LeetcodeCompetitionBot
A Discord Bot that Analyzes Leetcode Image Submissions for a challenge event by the McMaster CS Society. Uses Azure's Computer Vision API to analyze the images.

### Discord API
The Bot watches for the command -leetCodeSubmission followed by a question number that is attempted. Based on the result of the script, the bot will reply to the user whether their submission has been accepted or not. If not, the bot will elaborate what went wrong.

### Azure Computer Vision API
The Bot sends a POST to Azure's Computer Vision API which has Optical Character Recognition capabilities. This API analyzes the image to check whether certain tags are present in the image. It  replies to the bot with a JSon with all the words present in it.

### Google Sheets API
The Mac CS Society was keeping score of the participants with the help of a google sheet. Using the Google Sheet API, the bot is able to automatically update the sheet by processing the response given by the Azure resource.
