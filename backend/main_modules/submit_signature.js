const {cors, admin, db, bucketName, draftCollectionFolder, imagesCollectionFolder, imagesCollectionModule,
    patientsModule
} = require("../app");

/**
 * Uploads an image to Google Cloud Storage.
 * @param {string} userId - The user ID.
 * @param {string} imageSignature - The base64 image data.
 */
async function uploadImageSignature(userId, imageSignature) {
    try {
        // Fetch the existing user document
        const doc = await db.collection(patientsModule).doc(userId).get();
        const docData = doc.data();

        // Check if user data exists
        if (!docData) {
            throw new Error('User data not found.');
        }

        // Convert base64 image to buffer
        const buffer = Buffer.from(imageSignature, 'base64');

        // Create a unique filename for the image
        const fileName = `${imagesCollectionFolder}/${userId}/signature.jpg`; // Customize the filename as needed

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

        await copyAndDeleteUserDraftImages(bucket, userId)

        // Update user data in Firestore
        await db.collection(patientsModule).doc(userId).update({status: 'approved'});

        console.log(`Image uploaded successfully to ${fileName}`);
    } catch (error) {
        console.error(`Failed to upload image: ${error.message}`);
        throw new Error(`Image upload failed: ${error.message}`);
    }
}


/**
 * Copies all files from the draftCollection folder to the imagesCollection folder
 * and then deletes the original draft images for a specific user.
 * @param {object} bucket - The Google Cloud Storage bucket object.
 * @param {string} userId - The user ID whose draft images are to be copied and deleted.
 */
async function copyAndDeleteUserDraftImages(bucket, userId) {
    try {
        const draftFolderPath = `${draftCollectionFolder}/${userId}/`; // Source path
        const imagesFolderPath = `${imagesCollectionFolder}/${userId}/`; // Destination path

        // List all files in the draft folder
        const [files] = await bucket.getFiles({ prefix: draftFolderPath });

        if (files.length === 0) {
            console.log(`No files found in ${draftFolderPath} for user ID: ${userId}`);
            return;
        }

        // Copy each file to the new location
        const copyPromises = files.map(async (file) => {
            const destFileName = file.name.replace(draftFolderPath, imagesFolderPath); // New destination path
            const destFile = bucket.file(destFileName);

            await file.copy(destFile);
            console.log(`Copied ${file.name} to ${destFileName}`);
        });

        // Wait for all copy operations to complete
        await Promise.all(copyPromises);
        console.log(`All files copied from ${draftFolderPath} to ${imagesFolderPath} for user ID: ${userId}`);

        // Now delete the original draft images
        const deletePromises = files.map(file => {
            console.log(`Deleting ${file.name}...`); // Log the name of the file being deleted
            return file.delete();
        });

        await Promise.all(deletePromises); // Execute all deletions in parallel
        console.log(`Successfully deleted draft images for user ID: ${userId}`);
    } catch (error) {
        console.error(`Error during copy and delete operation: ${error.message}`);
        throw new Error(`Failed to copy and delete files: ${error.message}`);
    }
}


exports.submitSignature = async (req, res) => {
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
            let { userId, imageSignature, frontTeeth, upperJaw, lowerJaw } = req.body;

            // Validate input data
            if (!userId || !imageSignature || !frontTeeth || !upperJaw || !lowerJaw) {
                return res.status(400).send({ message: 'Missing required fields.' });
            }

            // Check if userId exists in Firestore
            const userDoc = await db.collection(patientsModule).doc(userId).get();
            if (!userDoc.exists) {
                return res.status(404).send({ message: 'User not found.' });
            }
            // Clean baseTeethImage if it contains a data URL
            const regex = /^data:image\/(png|jpg|jpeg);base64,/;
            if (regex.test(imageSignature)) {
                imageSignature = imageSignature.replace(regex, '');
            }

            const createdAt = admin.firestore.FieldValue.serverTimestamp();

            // Prepare and set user data in Firestore
            const userTeethData = {
                frontTeeth: { ...frontTeeth, patientId: userId, pov: "frontTeeth", createdAt: createdAt},
                upperJaw: { ...upperJaw, patientId: userId, pov: "upperJaw", createdAt: createdAt},
                lowerJaw: { ...lowerJaw, patientId: userId, pov: "lowerJaw", createdAt: createdAt}
            };

            // Save each part of the teeth data to Firestore
            for (const [key, data] of Object.entries(userTeethData)) {
                await db.collection(imagesCollectionModule).doc().set(data);
            }

            // Upload image signature
            await uploadImageSignature(userId, imageSignature);

            // Send success response
            res.status(200).send({ message: 'Success' });

        } catch (error) {
            console.error(error);
            res.status(500).send('An error occurred while generating content.');
        }
    });
};
