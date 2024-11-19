import { useState } from "react";
import Button from "../button";
import Modal from "../modal";
import InputText from "../inputText";
import InputSelect from "../inputSelect";
import { updateProfile } from "@/lib/helper";

export default function FormUpdateProfile({ setScreen, setUser }: { setScreen: any, setUser: any }) {
  const [formData, setFormData] = useState<{ [key: string]: { value: string, error: string } }>({
    fullName: { value: "", error: "" },
    phone: { value: "", error: "" },
    country: { value: "South Africa", error: "" },

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
    if (!formData.fullName.value.trim()) {
      setError("fullName", "Full name is required")
      isValid = false
    }
    if (!formData.phone.value.trim()) {
      setError("phone", "Phone number is required")
      isValid = false
    }
    if (!formData.country.value.trim()) {
      setError("country", "Country is required")
      isValid = false
    }
    return isValid
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setLoading(true)
    const res = await updateProfile({
      name: formData.fullName.value,
      phoneNumber: formData.phone.value,
      country: formData.country.value
    })
    if (res?.success) {
      setUser(res?.data?.dentistData)
      setScreen('home')
    } else {
      setShowError(true)
    }
  }
  return (
    <>
      <div className={`my-auto mx-auto w-full max-w-[568px] flex flex-col justify-center items-center ${loading && "pointer-events-none"}`}>
        <div className="text-[28px] font-black text-center">Complete Your Profile</div>
        <form onSubmit={onSubmit} className="w-full mt-5 pt-2 flex flex-col bg-[url('/images/form-deco.png')] bg-top bg-no-repeat">
          <div className="text-center">Please complete your profile to get started</div>
          <InputText className="mt-12" label="Full name" placeholder="Enter your full name" value={formData.fullName.value} error={formData.fullName.error} onChange={(e) => setData("fullName", e.target.value)}></InputText>
          <InputText className="mt-5" label="Phone number" placeholder="Enter your phone number" type="tel" value={formData.phone.value} error={formData.phone.error} onChange={(e) => setData("phone", e.target.value)}></InputText>
          <InputSelect className="mt-5" key="selectCountry" label="Country" value={formData.country.value} error={formData.country.error} options={["South Africa", "Tanzania", "Nigeria", "Kenya"]} onChange={(e) => setData("country", e.target.value)}></InputSelect>
          <Button className="mx-auto mt-14" loading={loading}>Update Profile</Button>
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