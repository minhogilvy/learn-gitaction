import firebase_app from "./config";
import { getAuth, signInAnonymously } from "firebase/auth";

const auth = getAuth(firebase_app);
export const signInAnonymouslyAsync = async () => {
  try {
    const response = await signInAnonymously(auth);
    return response
  } catch (error) {
    console.log(error);
  }
}

export const getUSer = () => {
  return auth.currentUser
}