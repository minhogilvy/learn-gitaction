const {cors} = require("../app");

exports.learnAction = async (req, res) => {
    cors(req, res, async () => {
        try {
            res.status(200).send({"message": "Hello, i am here"})
        } catch (error) {
            console.error(error)
            res.status(500).send('An error occurred while generating content.')
        }
    })
}
