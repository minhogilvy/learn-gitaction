import { useState } from "react";
import Button from "../button";
import Modal from "../modal";
import { confirmPasswordReset, getAuth, verifyPasswordResetCode } from "firebase/auth";
import InputText from "../inputText";
import { useRouter } from "next/router";
import firebase_app from "@/lib/firebase/config";

export default function FormResetPassword({ setScreen }: { setScreen: any }) {
  const router = useRouter()
  const [formData, setFormData] = useState<{ [key: string]: { value: string, error: string } }>({
    password: { value: "", error: "" },
    passwordConfirm: { value: "", error: "" }
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
    if (!formData.password.value.trim()) {
      setError("password", "Password is required")
      isValid = false
    }
    if (!formData.passwordConfirm.value.trim()) {
      setError("password", "Confirm Password is required")
      isValid = false
    } else if (formData.password.value !== formData.passwordConfirm.value) {
      setError("passwordConfirm", "The passwords you entered do not match. Please try again.")
      isValid = false
    }

    return isValid
  }

  const onSubmit = (e: any) => {
    e.preventDefault()
    if (!validate()) return
    setLoading(true)
    const actionCode = router.query.oobCode as string
    if (!actionCode) return
    const auth = getAuth(firebase_app)
    verifyPasswordResetCode(auth, actionCode).then(() => {
      confirmPasswordReset(auth, actionCode, formData.password.value).then(() => {
        setScreen('resetSuccess')
      }).catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorCode)
        console.log(errorMessage)
        setShowError(true)
      }).finally(() => {
        setLoading(false)
      })
    }).catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.log(errorCode)
      console.log(errorMessage)
      setShowError(true)
    }).finally(() => {
      setLoading(false)
    })
  }
  return (
    <>
      <div className={`my-auto mx-auto w-full max-w-[568px] flex flex-col justify-center items-center ${loading && "pointer-events-none"}`}>
        <div className="text-[28px] font-black text-center">Reset Your Password</div>
        <form onSubmit={onSubmit} className="w-full pt-12 flex flex-col bg-[url('/images/form-deco.png')] bg-top bg-no-repeat">
          <InputText label="New Password" type="password" value={formData.password.value} error={formData.password.error} onChange={(e) => setData("password", e.target.value)}></InputText>
          <InputText className="mt-5" label="Confirm New Password" type="password" value={formData.passwordConfirm.value} error={formData.passwordConfirm.error} onChange={(e) => setData("passwordConfirm", e.target.value)}></InputText>
          <Button className="mx-auto mt-12" loading={loading}>Save Password</Button>
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