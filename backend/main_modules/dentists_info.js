const {cors, admin, db,
    dentistsModule
} = require("../app");
const {encrypt, decrypt} = require("../utils/helpers");

// Helper function to verify access token
async function verifyAccessToken(req) {
    const accessToken = req.headers.authorization?.split('Bearer ')[1];
    if (!accessToken) {
        throw new Error('Unauthorized: No access token provided.');
    }

    try {
        return await admin.auth().verifyIdToken(accessToken);
    } catch (error) {
        throw new Error('Unauthorized: Invalid access token.');
    }
}

// Function to retrieve dentist information from Firestore by UID
exports.getDentistInfo = async (req, res) => {
    cors(req, res, async () => {
        try {
            const decodedToken = await verifyAccessToken(req);
            const uid = decodedToken.uid;

            // Fetch dentist information from Firestore
            const dentistDoc = await db.collection(dentistsModule).doc(uid).get();
            if (!dentistDoc.exists) {
                return res.status(200).json({ message: 'Dentist not found.', dentistData: {}});
            }

            const dentistData = dentistDoc.data();
            // Decrypt sensitive data
            dentistData.email = decrypt(dentistData.email);
            dentistData.phoneNumber = decrypt(dentistData.phoneNumber);

            res.status(200).json({
                message: 'Success',
                dentistData
            });

        } catch (error) {
            console.error('Error in getDentistInfo:', error);
            res.status(500).json({ message: error.message || 'An error occurred while retrieving dentist data.' });
        }
    });
};

// Function to create a new dentist entry in Firestore
exports.createDentistInfo = async (req, res) => {
    cors(req, res, async () => {
        try {
            const decodedToken = await verifyAccessToken(req);
            const uid = decodedToken.uid;
            const email = decodedToken.email;  // Retrieve email from the token

            // Get dentist data from request body
            const { name, country, phoneNumber } = req.body;

            if (!name || !country || !phoneNumber) {
                return res.status(400).json({ message: 'Missing required fields.' });
            }

            const dentistData = {
                name,
                email: encrypt(email),
                country,
                phoneNumber: encrypt(phoneNumber),
                createdAt: admin.firestore.FieldValue.serverTimestamp(),
            };

            // Create new dentist document in Firestore
            await db.collection(dentistsModule).doc(uid).set(dentistData);

            res.status(201).json({
                message: 'Dentist created successfully',
                dentistData
            });

        } catch (error) {
            console.error('Error in createDentistInfo:', error);
            res.status(500).json({ message: error.message || 'An error occurred while creating dentist data.' });
        }
    });
};
