import { useState } from "react";
import Button from "../button";
import Modal from "../modal";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import InputText from "../inputText";
import { getProfile } from "@/lib/helper";

export default function FormLogin({ setScreen, setUser }: { setScreen: any, setUser: any }) {
  const [formData, setFormData] = useState<{ [key: string]: { value: string, error: string } }>({
    email: { value: "", error: "" },
    password: { value: "", error: "" }
  })
  const [isInvalidCredentials, setIsInvalidCredentials] = useState(false)
  const [showError, setShowError] = useState(false)

  const [loading, setLoading] = useState(false)
  const setData = (key: string, value: string) => {
    setFormData((prev) => ({ ...prev, [key]: { value, error: "" } }))
  }
  const setError = (key: string, error: string) => {
    setFormData((prev) => ({ ...prev, [key]: { value: prev[key].value, error } }))
  }

  const onSubmit = (e: any) => {
    e.preventDefault()
    login()
  }
  const login = async () => {
    if (!validate()) return
    setLoading(true)
    const auth = getAuth()
    signInWithEmailAndPassword(auth, formData.email.value, formData.password.value).then(async () => {
      const res = await getProfile()
      if (res?.success) {
        const user = res?.data?.dentistData || {}
        setUser(user)
        if (!user.name || !user.phoneNumber || !user.country) {
          setScreen("updateProfile")
        } else {
          setScreen("home")
        }
      } else {
        setShowError(true)
      }
    }).catch((error) => {
      console.log(error)
      const errorCode = error.code;
      const errorMessage = error.message;
      console.log(errorCode)
      console.log(errorMessage)
      if (errorCode === "auth/invalid-credential") {
        setIsInvalidCredentials(true)
      } else {
        setShowError(true)
      }
    }).finally(() => {
      setLoading(false)
    })
  }

  const validate = () => {
    let isValid = true
    if (!formData.email.value.trim()) {
      setError("email", "Email is required")
      isValid = false
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(formData.email.value)) {
      setError("email", "Invalid email address")
      isValid = false
    }
    if (!formData.password.value.trim()) {
      setError("password", "Password is required")
      isValid = false
    }

    return isValid
  }
  return (
    <>
      <div className={`my-auto mx-auto w-full max-w-[568px] flex flex-col justify-center items-center ${loading && "pointer-events-none"}`}>
        <div className="text-[28px] font-black text-center">Sign in</div>
        <form onSubmit={onSubmit} className="w-full pt-12 flex flex-col bg-[url('/images/form-deco.png')] bg-top bg-no-repeat">
          <InputText label="Email" value={formData.email.value} error={formData.email.error} onChange={(e) => setData("email", e.target.value)}></InputText>
          <InputText className="mt-4" label="Password" type="password" value={formData.password.value} error={formData.password.error} onChange={(e) => setData("password", e.target.value)}></InputText>
          {isInvalidCredentials && (<div className="text-[14px] text-red-100 mt-2">Email or Password is not correct</div>)}
          <Button className="mx-auto mt-12" onClick={login} loading={loading}>Login</Button>
        </form>
        <div className="mx-auto text-center mt-12">
          <div className="text-[14px] text-gray-100 mt-7 underline" onClick={() => setScreen('forgotPassword')}>Forgot password?</div>
        </div>
      </div>
      {showError && (<Modal>
        <div className="p-5 flex flex-col items-center gap-2">
          <img src="/images/icon-error.svg" className="block w-[54px] shrink-0" alt="" />
          <div className="text-[20px] font-bold text-red-100 gap-2">Error!</div>
          <div className="leading-[1.4] text-center">Something went wrong.</div>
          <Button variant="white" onClick={() => setShowError(false)}>OK</Button>
        </div>
      </Modal>)}
    </>
  )
}