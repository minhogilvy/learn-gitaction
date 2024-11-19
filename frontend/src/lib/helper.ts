import { Teeth } from "@/pages";
import { getUSer } from "./firebase/auth";

const baseUrl = process.env.NEXT_PUBLIC_API_HOST

const requestAPI = async (url: string, data: object | null, method?: "POST" | "GET") => {
  const user = getUSer()
  const token = await user?.getIdToken()
  if (!token) return
  try {
    const body = data ? JSON.stringify(data) : null;
    const response = await fetch(url, {
      method: method || "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body,
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    return {
      status: response.status,
      success: true,
      data: json,
    } as { status: number, success: boolean, data: any, error?: string | string[] }
  } catch (error) {
    console.error(error);
  }
}

export const addPatient = async (data: {
  fullName: string,
  age: number,
  email: string,
  country: string,
  raceEthnicity: string
}) => {
  const url = `${baseUrl}/create-user`;
  return await requestAPI(url, data)
}

export const predictTeeth = async (data: {
  image: string,
  pov: string,
  userId: string
}) => {
  const url = `${baseUrl}/upload-image`;
  return await requestAPI(url, data)
}

export const updateProfile = async (data: {
  name: string,
  country: string,
  phoneNumber: string
}) => {
  const url = `${baseUrl}/update-profile`;
  return await requestAPI(url, data)
}
export const getProfile = async () => {
  const url = `${baseUrl}/get-profile`;
  return await requestAPI(url, null, "GET")
}

export const submitSignature = async (data: {
  userId: string,
  imageSignature: string,
  frontTeeth: Teeth,
  upperJaw: Teeth,
  lowerJaw: Teeth
}) => {
  const url = `${baseUrl}/submit-signature`;
  return await requestAPI(url, {
    userId: data.userId,
    imageSignature: data.imageSignature,
    frontTeeth: { ...data.frontTeeth, image: null },
    upperJaw: { ...data.upperJaw, image: null },
    lowerJaw: { ...data.lowerJaw, image: null },
  })
}

export const claim = (value: number, min: number, max: number) => {
  return Math.min(Math.max(value, min), max)
}

export const radToDeg = (rad: number) => {
  return rad * 180 / Math.PI
}