const {predict} = require('../utils/helpers');
const {cors, admin, db, bucketName, draftCollectionFolder, patientsModule} = require("../app");

async function convertAndPredict(baseTeethImage, pov) {
    try {
        // Make prediction using the base64 image
        const results = await predict(baseTeethImage);

        // Sort the predictions by probability in descending order
        const sortedResults = results.sort((a, b) => b.probability - a.probability);

        // Define the messages based on the sorted results
        const messages = {
            "blur": "image_is_blurry",
            "none": "incorrect_angle",
            "mouthOnly": "unable_to_detect",
            "upperJawDark": "image_is_too_dark",
            "frontTeethDark": "image_is_too_dark",
            "lowerJawDark": "image_is_too_dark",
        };
        console.log("sortedResults: " + JSON.stringify(sortedResults))
        // Get the prediction with the highest probability
        const highestProbabilityPrediction = sortedResults[0];

        // Check if pov matches the highest probability className
        if (highestProbabilityPrediction && highestProbabilityPrediction.category === pov &&
            highestProbabilityPrediction.probability >= 0.6) {
            return {status: 200, message: "Success"};
        } else {
            // Return the corresponding message if it exists
            const responseMessage = highestProbabilityPrediction && messages[highestProbabilityPrediction.category]
                ? messages[highestProbabilityPrediction.category]
                : messages['none'];
            return {status: 202, message: responseMessage};
        }
    } catch (error) {
        // Handle any errors that occur during the process
        console.log(`Error: ${error.message}`);
        throw error; // Optionally rethrow the error if you want to handle it upstream
    }
}

/**
 * Uploads an image to Google Cloud Storage.
 * @param {string} userId - The user ID.
 * @param {string} pov - The point of view.
 * @param {string} baseTeethImage - The base64 image data.
 */
async function uploadImageDraw(userId, pov, baseTeethImage) {
    try {
        // Convert base64 image to buffer
        const buffer = Buffer.from(baseTeethImage, 'base64');

        // Create a unique filename for the image
        const fileName = `${draftCollectionFolder}/${userId}/${pov}.jpg`; // Customize the filename as needed

        // Upload the image to the specified bucket
        const bucket = admin.storage().bucket(bucketName); // Ensure this is the correct bucket name

        // Create a file object
        const file = bucket.file(fileName);

        // Upload the image to the specified bucket
        await file.save(buffer, {
            metadata: {
                contentType: 'image/jpeg', // Use 'image/jpeg' for JPG images
            },
        });

        console.log(`Image uploaded to ${fileName}`);
    } catch (error) {
        console.error(`Failed to upload image: ${error.message}`);
        throw new Error(`Image upload failed: ${error.message}`);
    }
}


exports.uploadImage = async (req, res) => {
    cors(req, res, async () => {
        try {
            // Extract and verify access token
            const accessToken = req.headers.authorization?.split('Bearer ')[1];
            if (!accessToken) {
                return res.status(401).send('Unauthorized: No access token provided.');
            }

            let decodedToken;
            try {
                decodedToken = await admin.auth().verifyIdToken(accessToken);
            } catch (error) {
                return res.status(401).send('Unauthorized: Invalid access token.');
            }

            // Extract data from request body
            let baseTeethImage = req.body['image'];
            const pov = req.body['pov'];
            const userId = req.body['userId'];

            // Validate required fields
            if (!baseTeethImage || !pov || !userId) {
                return res.status(400).send({ message: 'Missing required fields.' });
            }

            // Check if userId exists in Firestore
            const userDoc = await db.collection(patientsModule).doc(userId).get();
            if (!userDoc.exists) {
                return res.status(404).send({ message: 'User not found.' });
            }

            // Clean baseTeethImage if it contains a data URL
            const regex = /^data:image\/(png|jpg|jpeg);base64,/;
            if (regex.test(baseTeethImage)) {
                baseTeethImage = baseTeethImage.replace(regex, '');
            }

            // Predict teeth
            const result = await convertAndPredict(baseTeethImage, pov);
            if (result.status === 200) {
                await uploadImageDraw(userId, pov, baseTeethImage);
            }

            // Send the response based on the result from convertAndPredict
            res.status(result.status).send({
                message: 'Success',
                code: result.status === 202 ? result.message : null
            });
        } catch (error) {
            console.error('Error in predictTeeth:', error);
            res.status(500).send('An error occurred while generating content.');
        }
    });
};
