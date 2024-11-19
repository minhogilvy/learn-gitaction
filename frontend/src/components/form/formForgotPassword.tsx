import { useState } from "react";
import Button from "../button";
import Modal from "../modal";
import { getAuth, sendPasswordResetEmail } from "firebase/auth";
import InputText from "../inputText";

export default function FormForgotPassword({ setScreen }: { setScreen: any }) {
  const [formData, setFormData] = useState<{ [key: string]: { value: string, error: string } }>({
    email: { value: "", error: "" },
  })
  const [showError, setShowError] = useState(false)

  const [loading, setLoading] = useState(false)
  const setData = (key: string, value: string) => {
    setFormData((prev) => ({ ...prev, [key]: { value, error: "" } }))
  }
  const setError = (key: string, error: string) => {
    setFormData((prev) => ({ ...prev, [key]: { value: prev[key].value, error } }))
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
    return isValid
  }

  const resetPassword = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setLoading(true)
    const auth = getAuth();
    sendPasswordResetEmail(auth, formData.email.value)
      .then(() => {
        setScreen('resetEmailSent')
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorCode)
        console.log(errorMessage)
      }).finally(() => {
        setLoading(false)
      })
  }
  return (
    <>
      <div className={`my-auto mx-auto w-full max-w-[568px] flex flex-col justify-center items-center ${loading && "pointer-events-none"}`}>
        <div className="text-[28px] font-black text-center">Forgot password</div>
        <form onSubmit={resetPassword} className="w-full mt-5 pt-2 flex flex-col bg-[url('/images/form-deco.png')] bg-top bg-no-repeat">
          <div className="text-center">A password reset link will be sent to the provided email address.</div>
          <InputText className="mt-12" label="Email" placeholder="Enter your registered email address" value={formData.email.value} error={formData.email.error} onChange={(e) => setData("email", e.target.value)}></InputText>
          <Button className="mx-auto mt-14" loading={loading}>Reset Password</Button>
        </form>
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