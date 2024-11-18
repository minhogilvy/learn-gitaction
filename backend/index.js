const { v4: uuidv4 } = require('uuid')
const fs = require('fs')

const { createUser } = require("./main_modules/create_user.js");
const { uploadImage } = require("./main_modules/upload_image.js");
const {patientsInfo, deletePatientsInfo} = require("./main_modules/patients_info");
const {getDentistInfo, createDentistInfo} = require("./main_modules/dentists_info");
const {submitSignature} = require("./main_modules/submit_signature");


exports.patientsInfo = patientsInfo
exports.getDentistInfo = getDentistInfo
exports.createDentistInfo = createDentistInfo
exports.deletePatientsInfo = deletePatientsInfo
exports.createUser = createUser
exports.uploadImage = uploadImage
exports.submitSignature = submitSignature
