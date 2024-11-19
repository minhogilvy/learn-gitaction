import Button from "@/components/button"
import Modal from "@/components/modal"
import AddPatient from "@/components/screens/addPatient"
import Capture from "@/components/screens/capture"
import ForgotPassword from "@/components/screens/forgotPassword"
import Home from "@/components/screens/home"
import Login from "@/components/screens/login"
import Rate from "@/components/screens/rate"
import ResetEmailSent from "@/components/screens/resetEmailSent"
import Signature from "@/components/screens/signature"
import Thankyou from "@/components/screens/thankyou"
import UpdateProfile from "@/components/screens/updateProfile"
import { getProfile, submitSignature } from "@/lib/helper"
import { useEffect, useRef, useState } from "react"

export type Teeth = {
  image?: string | null
  calculusGrade: number,
  cariesGrade: number,
  discolorationGrade: number,
  gingivitisGrade: number,
  mouthUlcerGrade: number
}
export type Pov = "frontTeeth" | "upperJaw" | "lowerJaw"
export type ImageError = "incorrect_angle" | "unable_to_detect" | "image_is_too_dark" | "image_is_blurry" | ""

export default function Index() {
  const [screen, setScreen] = useState<"login" | "home" | "addPatient" | "capture" | "rate" | "confirm" | "thankyou" | "forgotPassword" | "resetEmailSent" | "resetPassword" | "resetSuccess" | "updateProfile">("login")
  const [user, setUser] = useState<{ name: string, country: string, phoneNumber: string }>({
    "name": "",
    "country": "",
    "phoneNumber": ""
  })
  const patientId = useRef('')
  const [pov, setPov] = useState<Pov>("frontTeeth");
  const defaultData = {
    userId: "",
    imageSignature: "",
    frontTeeth: {
      image: "",
      calculusGrade: 0,
      cariesGrade: 0,
      discolorationGrade: 0,
      gingivitisGrade: 0,
      mouthUlcerGrade: 0
    },
    upperJaw: {
      image: "",
      calculusGrade: 0,
      cariesGrade: 0,
      discolorationGrade: 0,
      gingivitisGrade: 0,
      mouthUlcerGrade: 0
    },
    lowerJaw: {
      image: "",
      calculusGrade: 0,
      cariesGrade: 0,
      discolorationGrade: 0,
      gingivitisGrade: 0,
      mouthUlcerGrade: 0
    }
  }
  const [data, setData] = useState<{ userId?: string, imageSignature: string, frontTeeth: Teeth, upperJaw: Teeth, lowerJaw: Teeth }>(() => defaultData)
  const [signature, setSignature] = useState<string>("")
  const [loading, setLoading] = useState(false)
  const [showError, setShowError] = useState(false)

  const setTeethImage = (image: string) => {
    setData((prev) => ({ ...prev, [pov]: { ...prev[pov], image } }))
  }

  const updateRate = async (rate: Teeth) => {
    setData((prev) => ({ ...prev, [pov]: { ...prev[pov], ...rate } }))
    if (pov === "upperJaw") {
        setShowError(false)
        setLoading(true)
        const res = await submitSignature({
          userId: patientId.current,
          imageSignature: signature!,
          frontTeeth: data?.frontTeeth,
          upperJaw: data?.upperJaw,
          lowerJaw: data?.lowerJaw
        })
        if (res?.success) {
          setScreen('thankyou')
        } else {
          setShowError(true)
        }
        setLoading(false)
    } else {
      setPov(prev => prev === "frontTeeth" ? "lowerJaw" : "upperJaw")
      setScreen("capture")
    }
  }

  const setPatientId = (id: string) => {
    patientId.current = id
  }

  const back = () => {
    if (pov === "frontTeeth") {
      reset()
      setScreen("addPatient")
    } else if (pov === "lowerJaw") {
      setPov("frontTeeth")
      setScreen("rate")
    } else {
      setPov("lowerJaw")
      setScreen("rate")
    }
  }

  const reset = () => {
    setPatientId("")
    setPov("frontTeeth")
    setData(() => defaultData)
  }
  const backToHome = () => {
    reset()
    setScreen("home")
  }
  const newRecord = () => {
    reset()
    setScreen("confirm")
  }

  useEffect(() => {
    getProfile().then((res) => {
      if (res?.success) {
        const user = res?.data.dentistData
        if (!user.name || !user.phoneNumber || !user.country) {
          setScreen("updateProfile")
        } else {
          setUser(user)
          setScreen("home")
        }
      }
    })
  }, [])

  return (
    <>
      {screen === 'login' && (
        <Login setScreen={setScreen} setUser={setUser}></Login>
      )}
      {screen === 'forgotPassword' && (
        <ForgotPassword setScreen={setScreen}></ForgotPassword>
      )}
      {screen === 'resetEmailSent' && (
        <ResetEmailSent backToHome={backToHome} setScreen={setScreen}></ResetEmailSent>
      )}
      {screen === 'updateProfile' && (
        <UpdateProfile setScreen={setScreen} setUser={setUser}></UpdateProfile>
      )}
      {screen === 'home' && (
        <Home setScreen={setScreen} user={user}></Home>
      )}
      {screen === 'addPatient' && (
        <AddPatient backToHome={backToHome} setScreen={setScreen} setPatientId={setPatientId}></AddPatient>
      )}
      {screen === "capture" && (
        <Capture
          setScreen={setScreen}
          back={back}
          pov={pov}
          setTeethImage={setTeethImage}
          patientId={patientId.current}
        ></Capture>
      )}
      {screen === "rate" && (
        <Rate backToHome={backToHome} imageData={data[pov].image!} updateRate={updateRate} pov={pov} loading={loading}></Rate>
      )}
      {screen === 'confirm' && (
        <Signature backToHome={backToHome} setScreen={setScreen} setSignature={setSignature}></Signature>
      )}
      {screen === 'thankyou' && (
        <Thankyou backToHome={backToHome} newRecord={newRecord}></Thankyou>
      )}
      {showError && (<Modal>
        <div className="p-5 flex flex-col items-center gap-2">
          <img src="/images/icon-error.svg" className="block w-[54px] shrink-0" alt="" />
          <div className="text-[20px] font-bold text-red-100 gap-2">Submission Failed</div>
          <div className="leading-[1.4] text-center">There was a problem submitting the data. Please check your internet connection and try again.</div>
          <Button variant="white" onClick={() => setShowError(false)}>Retry</Button>
        </div>
      </Modal>)}
    </>
  )
}