const fs = require('fs')
const path = require('path')
const axios = require('axios')
const crypto = require('crypto')
const { PassThrough } = require('stream')
const CryptoJS = require('crypto-js')
const tf = require('@tensorflow/tfjs-node');

const labels = [
  "none",
  "upper jaw",
  "lower jaw",
  "front teeth",
  "Mouth only",
  "teeth left right",
  "upper jaw dark",
  "front teeth dark",
  "lower jaw dark",
  "blur"
]

const category = [
  "none",
  "upperJaw",
  "lowerJaw",
  "frontTeeth",
  "mouthOnly",
  "teethLeftRight",
  "upperJawDark",
  "frontTeethDark",
  "lowerJawDark",
  "blur"
]

const secretKey = CryptoJS.enc.Utf8.parse('bQJGDFWiYLreQpewFoiUNPJuFw7Zgj3L') // 32 bytes key for AES-256
const iv = CryptoJS.enc.Utf8.parse('9427036115899683') // 16 bytes IV
let model;

async function convertImageToBase64 (imagePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(imagePath, { encoding: 'base64' }, (err, data) => {
      if (err) {
        return reject(err)
      }
      resolve(data)
    })
  })
}

function encodeSHA256 (input) {
  return crypto.createHash('sha256').update(input).digest('hex')
}

async function convertImageUrlToBase64 (imageUrl) {
  try {
    const response = await axios.get(imageUrl, { responseType: 'arraybuffer' })
    const base64 = Buffer.from(response.data, 'binary').toString('base64')
    return base64
  } catch (error) {
    console.error('Error fetching the image:', error)
    throw error
  }
}

async function convertRetrieveMediaURLToBase64 (imageUrl, url, apiToken) {
  try {
    const resImage = await getRetrieveMediaURL(imageUrl, url, apiToken)
    const response = await axios.get(resImage.data.url, {
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: 'Bearer ' + apiToken
      },
      responseType: 'arraybuffer'
    })
    return Buffer.from(response.data, 'binary').toString('base64')
  } catch (error) {
    console.error('Error fetching the image:', error)
    throw error
  }
}

async function getRetrieveMediaURL (imageUrl, url, apiToken) {
  const response = await axios.get(url + imageUrl, {
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      Authorization: 'Bearer ' + apiToken
    }
  })
  if (response.status === 200) {
    return response
  }
}

async function initModel() {
  try {
    console.log("Initializing model...");

    // Construct the model path correctly
    const modelPath = path.join(__dirname, '../model/model.json'); // Adjust if your structure is different


    const modelURL = `file://${modelPath}`;

    console.log(`Loading model from ${modelURL}...`);

    model = await tf.loadLayersModel(modelURL);
    console.log("Model loaded successfully.");

  } catch (error) {
    console.error("Error initializing model:", error);
  }
}
//todo
//*
// https://js.tensorflow.org/api/latest/#loadLayersModel
//*
async function predict(base64Image) {
  // Ensure the model is initialized
  if (!model) {
    await initModel();
  }

  if (!base64Image) {
    throw new Error("Base64 image is required for prediction.");
  }

  const buffer = Buffer.from(base64Image, 'base64');

  // Decode the image to a tensor
  let tensor = tf.node.decodeImage(buffer, 3); // The second argument specifies the number of channels

  // Resize the image to the expected shape [224, 224, 3]
  tensor = tf.image.resizeBilinear(tensor, [224, 224]).toFloat();

  // Normalize the image to have values between 0 and 1 if required by the model
  const normalizedTensor = tensor.div(tf.scalar(255));

  // Add a batch dimension: [1, 224, 224, 3]
  const inputTensor = tf.expandDims(normalizedTensor, 0);

  // Make the prediction
  const prediction = await model.predict(inputTensor).dataSync(); // Use .data() for a promise that resolves with the data
  // Assume 'labels' and 'category' are defined elsewhere in your code
  return Array.from(prediction).map((probability, index) => ({
    className: labels[index], // Make sure 'labels' is correctly defined
    category: category[index], // Make sure 'category' is correctly defined
    probability
  }));
}


// Function to encrypt data
function encrypt(data) {
  return CryptoJS.AES.encrypt(data, secretKey, { iv: iv }).toString();
}

// Function to decrypt data
function decrypt(encryptedData) {
  const bytes = CryptoJS.AES.decrypt(encryptedData, secretKey, { iv: iv });
  return bytes.toString(CryptoJS.enc.Utf8); // Return the decrypted data as string
}



module.exports = {
  convertImageUrlToBase64,
  convertRetrieveMediaURLToBase64,
  encrypt,
  decrypt,
  predict,
  encodeSHA256
}
