const {cors, admin, db, patientsModule, imagesCollectionFolder, imagesCollectionModule, bucketName, auditLogsModule} = require("../app");
const {decrypt} = require("../utils/helpers");

async function getImages(patientId, pov) {
    try {
        // Iterate over each image document
        const imageUrl = `${imagesCollectionFolder}/${patientId}/${pov}.jpg`; // Construct the image URL
        // Generate signed URL
        const options = {
            version: 'v2',
            action: 'read',
            expires: Date.now() + 8 * 60 * 60 * 1000
        };

        // Create a signed URL for the image
        const signedUrl = await admin.storage().bucket(bucketName).file(imageUrl).getSignedUrl(options);
        return signedUrl[0]

    } catch (error) {
        console.error(`Failed to upload image: ${error.message}`);
        throw new Error(`Image upload failed: ${error.message}`);
    }
}

async function deleteImages(patientId) {
    try {
        // Delete images from Google Cloud Storage
        const imagePaths = [
            `${imagesCollectionFolder}/${patientId}/frontTeeth.jpg`, // Adjust file names as necessary
            `${imagesCollectionFolder}/${patientId}/upperJaw.jpg`,
            `${imagesCollectionFolder}/${patientId}/lowerJaw.jpg`,
            `${imagesCollectionFolder}/${patientId}/signature.jpg`
        ];

        const storageDeletePromises = imagePaths.map(imagePath =>
            admin.storage().bucket(bucketName).file(imagePath).delete().catch(error => {
                console.error(`Failed to delete image at ${imagePath}: ${error.message}`);
            })
        );
        await Promise.all(storageDeletePromises); // Delete images from storage

    } catch (error) {
        console.error(`Failed to upload image: ${error.message}`);
        throw new Error(`Image upload failed: ${error.message}`);
    }
}

exports.patientsInfo = async (req, res) => {
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

            // Extract query parameters with default values
            const limit = parseInt(req.query.limit) || 100; // Default to 100 records per page
            const offset = parseInt(req.query.offset) || 0; // Default to 0 records (start from the beginning)

            const {country, raceEthnicity, minAge, maxAge, startDate, endDate} = req.query; // Example parameters for filtering patients
            // Apply filters based on provided parameters
            // Prepare Firestore query for counting patients
            let queryCount = db.collection(patientsModule);

            // Apply filters based on provided parameters for count
            if (country) {
                queryCount = queryCount.where('country', '==', country);
            }
            if (raceEthnicity) {
                queryCount = queryCount.where('raceEthnicity', '==', raceEthnicity);
            }
            if (minAge) {
                queryCount = queryCount.where('age', '>=', parseInt(minAge));
            }
            if (maxAge) {
                queryCount = queryCount.where('age', '<=', parseInt(maxAge));
            }
            if (startDate) {
                queryCount = queryCount.where('createdAt', '>=', admin.firestore.Timestamp.fromDate(new Date(startDate)));
            }
            if (endDate) {
                queryCount = queryCount.where('createdAt', '<=', admin.firestore.Timestamp.fromDate(new Date(endDate)));
            }
            // Filter by status
            queryCount = queryCount.where('status', '==', 'approved'); // Add filter for status

            // Get the total count of patients
            const countSnapshot = await queryCount.get();
            const totalCount = countSnapshot.size; // Get the count of matching documents


            // Prepare Firestore query for fetching patients with limit and offset
            let query = db.collection(patientsModule)
                .where('status', '==', 'approved') // Apply same filters for fetching patients
                .limit(limit)
                .offset(offset * limit);
            if (country) {
                query = query.where('country', '==', country); // Ensure age is a number
            }
            if (raceEthnicity) {
                query = query.where('raceEthnicity', '==', raceEthnicity);
            }
            if (minAge) {
                query = query.where('age', '>=', parseInt(minAge)); // Filter for minimum age
            }
            if (maxAge) {
                query = query.where('age', '<=', parseInt(maxAge)); // Filter for maximum age
            }
            // Date filtering
            if (startDate) {
                query = query.where('createdAt', '>=', admin.firestore.Timestamp.fromDate(new Date(startDate)));
            }
            if (endDate) {
                query = query.where('createdAt', '<=', admin.firestore.Timestamp.fromDate(new Date(endDate)));
            }


            // Execute the query
            const patientsSnapshot = await query.get();
            // Array to hold all patient data with images
            const patientsData = [];

            if (patientsSnapshot.empty) {
                return res.status(404).json({message: 'No patients found.', patientsData});
            }

            // Iterate over each patient document
            for (const doc of patientsSnapshot.docs) {
                const patient = {id: doc.id, ...doc.data()}; // Get patient data

                // Query for related images using the patientId
                const imagesSnapshot = await db.collection(imagesCollectionModule).where('patientId', '==', patient.id).get();

                // Prepare an object to store image data
                const imagesData = {
                    frontTeeth: {
                        imageUrl: '',
                        calculusGrade: 0,
                        gingivitisGrade: 0,
                        discolorationGrade: 0,
                        mouthUlcerGrade: 0,
                        cariesGrade: 0,
                        pov: ''
                    },
                    upperTeeth: {
                        imageUrl: '',
                        calculusGrade: 0,
                        gingivitisGrade: 0,
                        discolorationGrade: 0,
                        mouthUlcerGrade: 0,
                        cariesGrade: 0,
                        pov: ''
                    },
                    lowerTeeth: {
                        imageUrl: '',
                        calculusGrade: 0,
                        gingivitisGrade: 0,
                        discolorationGrade: 0,
                        mouthUlcerGrade: 0,
                        cariesGrade: 0,
                        pov: ''
                    },
                    signatureImageUrl: '',
                };

                // Iterate over each image document related to the patient
                for (const imageDoc of imagesSnapshot.docs) {
                    const imageData = imageDoc.data();
                    const pov = imageData.pov;

                    // Get signed URLs for the images
                    const imageUrl = await getImages(patient.id, pov); // Await the signed URL
                    if (pov === 'frontTeeth') {
                        imagesData.frontTeeth = {...imagesData.frontTeeth, ...imageData, imageUrl};
                    } else if (pov === 'upperJaw') {
                        imagesData.upperTeeth = {...imagesData.upperTeeth, ...imageData, imageUrl};
                    } else if (pov === 'lowerJaw') {
                        imagesData.lowerTeeth = {...imagesData.lowerTeeth, ...imageData, imageUrl};
                    }
                }

                // Get the signed URL for the signature image
                imagesData.signatureImageUrl = await getImages(patient.id, "signature");
                patient.email = decrypt(patient.email)
                // Combine patient data with images
                patientsData.push({patient: patient, ...imagesData});
            }

            // Send response with patient data and count
            res.status(200).json({
                message: 'Success',
                totalCount: totalCount, // Include the total count of patients
                patientsData
            });

        } catch (error) {
            console.error('Error in predictTeeth:', error);
            res.status(500).send('An error occurred while generating content.');
        }
    });
};

exports.deletePatientsInfo = async (req, res) => {
    cors(req, res, async () => {
        if (req.method === 'DELETE') {
            try {
                // Extract patient ID from the URL
                const parts = req.url.split('/'); // Split the URL by '/'
                const patientId = parts[1]; // Assuming the structure is /delete-patients/{id}

                // Check if the patientId is valid
                if (!patientId) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    return res.end(JSON.stringify({ message: 'Patient ID is required.' }));
                }

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

                // Check if the patient exists
                const patientDoc = await db.collection(patientsModule).doc(patientId).get();
                if (!patientDoc.exists) {
                    return res.status(404).json({message: 'Patient not found.'});
                }
                // Prepare the audit log entry
                const logs = {
                    systemDelete: admin.firestore.FieldValue.serverTimestamp(),
                    dentistId: patientDoc.data().dentistId,
                    patientId: patientId
                };

                // Delete the patient document
                await db.collection(patientsModule).doc(patientId).delete();

                // Dynamically add the image's pov and imageId to the logs object
                let logEntry = {
                    ...logs
                };
                // Delete associated images from Firestore
                const imagesSnapshot = await db.collection(imagesCollectionModule).where('patientId', '==', patientId).get();
                // Log deletion event into the audit logs and add image data to logs
                imagesSnapshot.forEach((imageDoc) => {
                    const imageData = imageDoc.data();
                    const pov = imageData.pov; // Get pov
                    const imageId = imageDoc.id; // Get image ID

                    logEntry = {...logEntry,
                        [pov]: imageId  // Dynamically add the pov and its corresponding imageId
                    }
                    console.log(`Audit Log: Added pov: ${pov}, imageId: ${imageId}`);
                });
                // Create a log entry for each image document
                await db.collection(auditLogsModule).doc().set(logEntry);

                // Delete associated images in Firestore
                const deletePromises = imagesSnapshot.docs.map(imageDoc => imageDoc.ref.delete());
                await Promise.all(deletePromises); // Delete all associated images in Firestore

                // Assuming you have a function to delete images from storage
                await deleteImages(patientId);


                // Send success response
                res.status(200).json({message: 'Patient and associated images deleted successfully.'});


            } catch (error) {
                console.error('Error deleting patient:', error);
                res.status(500).send('An error occurred while deleting the patient.');
            }
        } else {
            // Handle other routes or methods
            res.writeHead(405, {'Content-Type': 'application/json'});
            res.end(JSON.stringify({message: 'Method not allowed.'}));
        }
    });
};
