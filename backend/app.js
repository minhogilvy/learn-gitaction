// Initialize Firebase Admin SDK
const path = require('path')
const admin = require('firebase-admin')
const serviceAccountPath = process.env.SERVICE_ACCOUNT_PATH
const publisher = process.env.MULTI_MODEL_PUBLISHER
const projectId = process.env.PROJECT_ID
const bucketName = process.env.BUCKET_NAME
const teethFolder = process.env.TEETH_FOLDER
const multiModel = process.env.MULTI_MODEL
const region = process.env.REGION
const apiKey = process.env.API_KEY
const draftCollectionFolder = process.env.TEETH_DRAFT_COLLECTION_FOLDER
const imagesCollectionFolder = process.env.TEETH_COLLECTION_FOLDER
const imagesCollectionModule = process.env.COLLECTION_MODULE
const auditLogsModule = process.env.AUDIT_LOGS_MODULE
const patientsModule = process.env.PATIENTS_MODULE
const dentistsModule = process.env.DENTISTS_MODULE
const cors = require('cors')({ origin: true })

module.exports = {
  cors
}
