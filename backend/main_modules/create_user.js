const {cors, db, admin, imagesCollectionModule, patientsModule} = require("../app");
const { v4: uuidv4 } = require('uuid')
const {encrypt} = require("../utils/helpers");


exports.createUser = async (req, res) => {
    cors(req, res, async () => {
        try {
            let decodedToken;

            const accessToken = req.headers.authorization?.split('Bearer ')[1]

            if (!accessToken) {
                return res.status(401).send('Unauthorized: No access token provided.')
            }
            // Verify the accessToken
            try {
                 decodedToken = await admin.auth().verifyIdToken(accessToken);
            } catch (error) {
                return res.status(401).send('Unauthorized: Invalid access token.');
            }
            const itemUUID = uuidv4()
            console.log(itemUUID)
            const uid = decodedToken.uid;
            const  fullName = req.body['fullName']
            const  age = req.body['age']
            const  email = req.body['email']
            const  country = req.body['country']
            const  raceEthnicity = req.body['raceEthnicity']
            if (!fullName || !age || !email || !country || !raceEthnicity) {
                return res.status(400).send({message: 'Missing required fields.'});
            }

            const userData = {
                fullName: fullName,
                age: age,
                email: encrypt(email),
                country: country,
                raceEthnicity: raceEthnicity,
                dentistId: uid,
                createdAt: admin.firestore.FieldValue.serverTimestamp(),
                status:'waiting'
            }

            await db.collection(patientsModule).doc(itemUUID).set(userData)

            const dataResponse = {userId: itemUUID};
            res.status(200).send(dataResponse)
        } catch (error) {
            console.error(error)
            res.status(500).send('An error occurred while generating content.')
        }
    })
}
